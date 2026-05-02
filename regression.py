"""
Train a linear regression model to predict house sale amount directly,
then print the most influential features by coefficient magnitude.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def resolve_dataset_path() -> Path:
    """
    Find the input CSV. Prefer the user-requested filename and fall back to
    the available final dataset file if needed.
    """
    data = Path("combined_real_estate_data_final.csv")

    if data.exists():
        return data

    raise FileNotFoundError("Could not find 'combined_real_estate_data_final.csv'.")


def normalize_feature_name(
    model_feature_name: str, categorical_source_columns: list[str]
) -> str:
    """
    Convert transformed names like 'num__Population' and
    'cat__zip_x_06010.0' into a base source column name.
    """
    if model_feature_name.startswith("num__"):
        return model_feature_name.replace("num__", "", 1)

    if model_feature_name.startswith("cat__"):
        raw = model_feature_name.replace("cat__", "", 1)
        # One-hot names look like "<original_column>_<category_value>".
        # Match against known source categorical columns to recover the
        # original column name even when that name itself contains underscores.
        for col in sorted(categorical_source_columns, key=len, reverse=True):
            if raw == col or raw.startswith(f"{col}_"):
                return col

    return model_feature_name


def print_high_correlations(
    data: pd.DataFrame, threshold: float = 0.8, top_n: int = 20
) -> None:
    """
    Print highly correlated numeric feature pairs to help identify
    multicollinearity before model fitting.
    """
    numeric_df = data.select_dtypes(include=[np.number]).copy()
    if numeric_df.shape[1] < 2:
        print("\nNot enough numeric features to compute correlations.")
        return

    corr_matrix = numeric_df.corr()
    upper_triangle_mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    corr_pairs = (
        corr_matrix.where(upper_triangle_mask)
        .stack()
        .reset_index()
        .rename(columns={"level_0": "feature_1", "level_1": "feature_2", 0: "corr"})
    )
    corr_pairs["abs_corr"] = corr_pairs["corr"].abs()

    strong_pairs = corr_pairs[corr_pairs["abs_corr"] >= threshold].sort_values(
        "abs_corr", ascending=False
    )

    print(
        f"\nHighly correlated numeric feature pairs "
        f"(|corr| >= {threshold}, top {top_n} shown):"
    )
    if strong_pairs.empty:
        print("- None above threshold.")
        return

    for _, row in strong_pairs.head(top_n).iterrows():
        print(
            f"- {row['feature_1']} vs {row['feature_2']}: "
            f"corr={row['corr']:.4f}"
        )


def main() -> None:
    # Load real estate data.
    data_path = resolve_dataset_path()
    df = pd.read_csv(data_path, low_memory=False)

    # Convert currency-like columns from strings (e.g., "$248,400.00") to numbers.
    for col in ["Sale Amount", "Assessed Value"]:
        if col in df.columns:
            cleaned = (
                df[col]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
            )
            df[col] = pd.to_numeric(cleaned, errors="coerce")

    # 99 percent of houses sold for under $3,000,000
    df = df[df['Sale Amount'] < 3000000]

    # Do not include raw target leakage columns in features.
    # "Sales Ratio" is derived from sale amount and assessed value, so we exclude it.
    # Drop leakage/ID-like columns that can dominate coefficients without being broadly useful.
    drop_columns = {
        "Sale Amount",
        "Sales Ratio",
        "Serial Number",
        "Address",
        "Date Recorded",
        "Location",
        "zip_x",
        "zip_y",
        "# Elementary Schools",
        "Population",
        "zip_population",
        "aian_total_pop",
        "Total NIBRS Crimes"
    }
    X = df.drop(columns=[c for c in drop_columns if c in df.columns])

    y = df["Sale Amount"]

    # Split feature columns by type for preprocessing.
    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

    # Print strong numeric correlations to flag potentially redundant features.
    print_high_correlations(X[numeric_features], threshold=0.8, top_n=20)

    # Build separate preprocessing pipelines for numeric and categorical columns.
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Full pipeline: preprocessing + ridge regression.
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            # Ridge regularization shrinks unstable coefficients in collinear data.
            ("regressor", Ridge(alpha=1.0)),
        ]
    )

    # Standard train/test split for continuous target prediction.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train and evaluate.
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"Loaded dataset: {data_path}")
    print(f"MAE: {mae:,.2f}")
    print(f"RMSE: {rmse:,.2f}")
    print(f"R^2: {r2:.4f}")


    # Get regression coefficients and map them back to transformed feature names.
    # Since numeric features are standardized, larger absolute coefficients imply
    # stronger influence on predicted sale amount in the transformed feature space.
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    coefs = model.named_steps["regressor"].coef_

    coef_df = pd.DataFrame({"feature": feature_names, "coefficient": coefs})
    coef_df["abs_coefficient"] = np.abs(coef_df["coefficient"])

    # Build a column-level ranking by aggregating transformed coefficients
    # back to each original source column.
    coef_df["base_feature"] = coef_df["feature"].map(
        lambda name: normalize_feature_name(name, categorical_features)
    )
    column_ranking = (
        coef_df.groupby("base_feature", as_index=False)
        .agg(
            aggregated_abs_coef=("abs_coefficient", "sum"),
            aggregated_signed_coef=("coefficient", "sum"),
        )
        .sort_values("aggregated_abs_coef", ascending=False)
        .reset_index(drop=True)
    )

    print("\nCoefficient ranking for all source columns:")
    for idx, row in column_ranking.iterrows():
        direction = (
            "positive" if row["aggregated_signed_coef"] >= 0 else "negative"
        )
        print(
            f"{idx + 1:>2}. {row['base_feature']}: "
            f"aggregated_abs_coef={row['aggregated_abs_coef']:.4f}, "
            f"net_direction={direction}"
        )

    # Save full rankings so you can inspect every column without terminal truncation.
    column_ranking.to_csv("coefficient_ranking_all_columns.csv", index=False)
    coef_df.sort_values("abs_coefficient", ascending=False).to_csv(
        "coefficient_ranking_transformed_features.csv", index=False
    )
    print("\nSaved full rankings to:")
    print("- coefficient_ranking_all_columns.csv")
    print("- coefficient_ranking_transformed_features.csv")

    # Also report influence specifically for contextual neighborhood columns.
    context_columns = [
        "Rank (of 177)",
        "# Elementary Schools",
        "# Middle Schools",
        "# High Schools",
        "# Private Schools*",
        "Rank score (2025)",
        "town_population",
        "zip_population",
        "zip_density",
        "aian_total_pop",
        "air_quality",
        "Population",
        "Crime Rate per 1000",
        "Total NIBRS Crimes",
    ]
    context_set = set(context_columns)

    # Aggregate absolute influence across transformed features that come from
    # the same original source column (important for one-hot encoded ZIPs).
    context_df = coef_df[coef_df["base_feature"].isin(context_set)].copy()
    context_summary = (
        context_df.groupby("base_feature", as_index=False)["abs_coefficient"]
        .sum()
        .sort_values("abs_coefficient", ascending=False)
    )

    print("\nTop contextual features among selected columns:")
    for _, row in context_summary.head(10).iterrows():
        print(f"- {row['base_feature']}: aggregated_abs_coef={row['abs_coefficient']:.4f}")


if __name__ == "__main__":
    main()

