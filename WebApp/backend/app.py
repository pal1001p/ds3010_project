import os
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field


BACKEND_DIR = Path(__file__).resolve().parent


def _resolve_data_dir() -> Path:
    env_dir = os.getenv("DS3010_DATA_DIR")
    if env_dir:
        return Path(env_dir)

    local_data = BACKEND_DIR / "data"
    if (local_data / "model_parameters.csv").exists():
        return local_data

    # Fallback for current local layout:
    # .../DS 3010/ds_web_app_fixed/backend -> .../DS 3010/ds3010_project
    sibling_project = BACKEND_DIR.parent.parent / "ds3010_project"
    return sibling_project


PROJECT_DATA_DIR = _resolve_data_dir().resolve()
MODEL_PARAMETERS_FILE = PROJECT_DATA_DIR / "model_parameters.csv"
PREDICTION_INTERVAL_FILE = PROJECT_DATA_DIR / "prediction_interval.txt"
FEATURE_IMPORTANCE_FILE = PROJECT_DATA_DIR / "coefficient_ranking_all_columns.csv"


class PredictionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    assessed_value: float = Field(alias="assessedValue")
    school_ranking: float = Field(alias="schoolRank")
    air_quality: float = Field(alias="airQuality")
    num_middle_schools: float = Field(alias="middleSchools")
    num_high_schools: float = Field(alias="highSchools")
    list_year: int = Field(alias="listYear")
    crime_safety_score: float = Field(alias="crimeRate")


class HousePricePredictor:
    def __init__(self, params_file: Path, interval_file: Path) -> None:
        if not params_file.exists():
            raise FileNotFoundError(f"Could not find {params_file}")

        self.params_df = pd.read_csv(params_file)
        self.intercept = float(self.params_df["intercept"].iloc[0])
        self.features = self.params_df["feature"].tolist()
        self.coefficients = dict(
            zip(self.params_df["feature"], self.params_df["coefficient"])
        )
        self.means = dict(zip(self.params_df["feature"], self.params_df["mean"]))
        self.stds = dict(zip(self.params_df["feature"], self.params_df["std"]))

        self.margin_of_error: float | None = None
        if interval_file.exists():
            with interval_file.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if "margin_of_error" in line:
                        self.margin_of_error = float(line.split("=")[1].strip())

    def _normalize_inputs(self, **kwargs: float | int) -> dict[str, float | int]:
        feature_mapping = {
            "assessed_value": "Assessed Value",
            "list_year": "List Year",
            "num_high_schools": "# High Schools",
            "num_middle_schools": "# Middle Schools",
            "school_ranking": "Rank score (2025)",
            "air_quality": "air_quality",
            "crime_rate_per_1000": "Crime Rate per 1000",
            # Accept legacy camelCase keys too.
            "assessedValue": "Assessed Value",
            "listYear": "List Year",
            "highSchools": "# High Schools",
            "middleSchools": "# Middle Schools",
            "schoolRank": "Rank score (2025)",
            "airQuality": "air_quality",
            "crimeRate": "Crime Rate per 1000",
        }
        normalized: dict[str, float | int] = {}
        for key, value in kwargs.items():
            if key in self.features:
                normalized[key] = value
                continue
            mapped = feature_mapping.get(key)
            if mapped:
                normalized[mapped] = value
        return normalized

    def predict(self, payload: PredictionRequest) -> dict:
        # Convert user-facing 1-10 safety score to model crime-rate scale (11-110).
        crime_rate_per_1000 = max(1.0, min(10.0, payload.crime_safety_score)) * 11.0
        raw_inputs = self._normalize_inputs(
            assessed_value=payload.assessed_value,
            list_year=payload.list_year,
            num_middle_schools=payload.num_middle_schools,
            num_high_schools=payload.num_high_schools,
            school_ranking=payload.school_ranking,
            air_quality=payload.air_quality,
            crime_rate_per_1000=crime_rate_per_1000,
        )

        predicted_price = self.intercept
        for feature in self.features:
            input_value = float(raw_inputs.get(feature, self.means.get(feature, 0)))
            mean = float(self.means[feature])
            std = float(self.stds[feature]) if float(self.stds[feature]) != 0 else 1.0
            standardized = (input_value - mean) / std
            predicted_price += float(self.coefficients[feature]) * standardized

        predicted_price = max(0.0, predicted_price)
        lower_bound = (
            max(0.0, predicted_price - self.margin_of_error)
            if self.margin_of_error is not None
            else None
        )
        upper_bound = (
            predicted_price + self.margin_of_error
            if self.margin_of_error is not None
            else None
        )

        return {
            "price": predicted_price,
            "price_rounded": round(predicted_price, 2),
            "lower_bound": round(lower_bound, 2) if lower_bound is not None else None,
            "upper_bound": round(upper_bound, 2) if upper_bound is not None else None,
            "margin_of_error": self.margin_of_error,
        }


app = FastAPI(title="DS3010 Property API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor: HousePricePredictor | None = None
predictor_init_error: str | None = None
try:
    predictor = HousePricePredictor(MODEL_PARAMETERS_FILE, PREDICTION_INTERVAL_FILE)
except Exception as exc:
    predictor_init_error = str(exc)

print(f"[ds3010] model data dir: {PROJECT_DATA_DIR}")
print(f"[ds3010] model_parameters.csv exists: {MODEL_PARAMETERS_FILE.exists()}")
if predictor is None:
    print(f"[ds3010] predictor failed to load: {predictor_init_error}")
else:
    print("[ds3010] predictor loaded OK")


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "predictor_ready": predictor is not None,
        "data_dir": str(PROJECT_DATA_DIR),
        "model_parameters_csv": str(MODEL_PARAMETERS_FILE),
        "model_parameters_exists": MODEL_PARAMETERS_FILE.exists(),
        "predictor_error": predictor_init_error,
    }


@app.post("/api/predict")
def predict(payload: PredictionRequest) -> dict:
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail=f"Predictor unavailable: {predictor_init_error}",
        )
    try:
        return predictor.predict(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/feature-importance")
def feature_importance() -> list[dict]:
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail=f"Predictor unavailable: {predictor_init_error}",
        )
    if not FEATURE_IMPORTANCE_FILE.exists():
        raise HTTPException(status_code=404, detail="Feature-importance CSV not found")

    frame = pd.read_csv(FEATURE_IMPORTANCE_FILE).fillna(0)
    records = frame.to_dict(orient="records")
    return records
