"""
Train a linear regression model to predict house sale amount directly,
then print the most influential features by coefficient magnitude.
Includes brute force search for best 7-feature combination using MAE.
"""

from pathlib import Path
import time
import itertools
from collections import Counter
from tqdm import tqdm  # Optional: pip install tqdm for progress bar
from scipy import stats
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.pipeline import Pipeline, make_pipeline
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


def brute_force_search_best_features(
    df: pd.DataFrame, 
    feature_cols: list[str],
    n_samples: int = 1000, 
    n_features_to_select: int = 7,
    use_cv: bool = False
) -> pd.DataFrame:
    """
    Brute force search over all combinations of n_features_to_select using MAE.
    
    Args:
        df: Full dataframe
        feature_cols: List of feature column names to search over
        n_samples: Number of random samples to use
        n_features_to_select: Number of features per combination (default 7)
        use_cv: Use 5-fold cross-validation (slower but more robust)
    
    Returns:
        DataFrame with all combinations and their MAE scores
    """
    # Random sample for faster computation
    sampled_df = df.sample(n=min(n_samples, len(df)), random_state=42)
    y = sampled_df["Sale Amount"]
    
    # Generate all combinations
    all_combinations = list(itertools.combinations(feature_cols, n_features_to_select))
    total_combos = len(all_combinations)
    
    print(f"\n{'='*60}")
    print(f"BRUTE FORCE FEATURE SEARCH (using MAE)")
    print(f"{'='*60}")
    print(f"Total features available: {len(feature_cols)}")
    print(f"Selecting: {n_features_to_select} features")
    print(f"Total combinations to test: {total_combos:,}")
    print(f"Sample size: {len(sampled_df):,} rows")
    print(f"Using CV: {use_cv}")
    
    results = []
    start_time = time.time()
    
    # Test each combination
    iterator = tqdm(all_combinations, desc="Testing combinations") if 'tqdm' in globals() else all_combinations
    
    for combo in iterator:
        X = sampled_df[list(combo)].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        if use_cv:
            # Use cross-validation for robust evaluation
            kfold = KFold(n_splits=5, shuffle=True, random_state=42)
            mae_scores = []
            
            for train_idx, val_idx in kfold.split(X):
                X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                
                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_val_scaled = scaler.transform(X_val)
                
                # Train model
                model = Ridge(alpha=1.0)
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_val_scaled)
                
                # Calculate MAE
                mae_scores.append(mean_absolute_error(y_val, y_pred))
            
            avg_mae = np.mean(mae_scores)
            std_mae = np.std(mae_scores)
            
        else:
            # Simple train/test split (faster)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = Ridge(alpha=1.0)
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            
            # Calculate MAE
            avg_mae = mean_absolute_error(y_test, y_pred)
            std_mae = 0
        
        results.append({
            'features': combo,
            'mae': avg_mae,
            'mae_std': std_mae,
            'n_features': len(combo)
        })
    
    elapsed = time.time() - start_time
    
    # Convert to DataFrame and sort by MAE (lower is better)
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('mae', ascending=True).reset_index(drop=True)
    
    print(f"\nSearch completed in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    
    return results_df


def evaluate_feature_combination(df: pd.DataFrame, feature_list: list, n_samples: int = 1000):
    """
    Evaluate a specific feature combination in detail with multiple metrics.
    """
    sampled_df = df.sample(n=min(n_samples, len(df)), random_state=42)
    
    X = sampled_df[feature_list].copy()
    y = sampled_df["Sale Amount"]
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
 
    print(f"\n{'='*60}")
    print(f"DETAILED EVALUATION OF BEST FEATURE COMBINATION")
    print(f"{'='*60}")
    print(f"MAE: ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"\nFeature Coefficients (standardized):")
    
    coef_df = pd.DataFrame({
        'feature': feature_list,
        'coefficient': model.coef_,
        'abs_coef': np.abs(model.coef_)
    }).sort_values('abs_coef', ascending=False)
    
    for _, row in coef_df.iterrows():
        direction = "positive" if row['coefficient'] > 0 else "negative"
        print(f"  {row['feature']}: {direction} ({abs(row['coefficient']):.4f})")
    
    return mae, rmse, r2, model, scaler


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
    
    # Print ALL available numeric features for transparency
    print(f"\n{'='*60}")
    print(f"AVAILABLE NUMERIC FEATURES ({len(numeric_features)} total)")
    print(f"{'='*60}")
    for i, feature in enumerate(numeric_features, 1):
        print(f"{i:>2}. {feature}")
    
    print(f"\n{'='*60}")
    print(f"AVAILABLE CATEGORICAL FEATURES ({len(categorical_features)} total)")
    print(f"{'='*60}")
    for i, feature in enumerate(categorical_features, 1):
        print(f"{i:>2}. {feature}")

    # Print strong numeric correlations to flag potentially redundant features.
    print_high_correlations(X[numeric_features], threshold=0.8, top_n=20)

    # ========================================================================
    # BRUTE FORCE SEARCH FOR BEST 7-FEATURE COMBINATION (using MAE)
    # ========================================================================
    print("\n" + "="*60)
    print("FEATURE COMBINATION OPTIMIZATION (using MAE)")
    print("="*60)
    
    # Check if we have at least 7 numeric features
    if len(numeric_features) < 7:
        print(f"\n⚠️ WARNING: Only {len(numeric_features)} numeric features available.")
        print(f"   Cannot select 7 features. Will select {len(numeric_features)} features instead.")
        n_to_select = min(7, len(numeric_features))
    else:
        n_to_select = 7
    
    print(f"\nUsing {len(numeric_features)} numeric features for search")
    print(f"Target: Select {n_to_select} features that minimize MAE")
    
    # Run brute force search with MAE
    search_results = brute_force_search_best_features(
        df, 
        feature_cols=numeric_features,
        n_samples=1000,
        n_features_to_select=n_to_select,
        use_cv=False  # Set to True for more robust but slower results
    )
    
    # Display top 10 combinations
    print(f"\n{'='*60}")
    print(f"TOP 10 BEST {n_to_select}-FEATURE COMBINATIONS (lowest MAE)")
    print(f"{'='*60}")
    
    for i in range(min(10, len(search_results))):
        row = search_results.iloc[i]
        print(f"\n{i+1}. MAE = ${row['mae']:,.2f} (±${row['mae_std']:.2f})")
        print(f"   Features ({len(row['features'])} features):")
        for j, feature in enumerate(row['features'], 1):
            print(f"      {j}. {feature}")
    
    # Analyze feature frequency in top 100 combinations
    print(f"\n{'='*60}")
    print(f"FEATURE FREQUENCY IN TOP 100 COMBINATIONS")
    print(f"{'='*60}")
    
    feature_counter = Counter()
    for _, row in search_results.head(100).iterrows():
        feature_counter.update(row['features'])
    
    for feature, count in feature_counter.most_common(len(feature_counter)):
        percentage = (count / 100) * 100
        print(f"  {feature}: {percentage:.0f}% of top 100 combinations")
    
    # Get the best combination
    best_features = list(search_results.iloc[0]['features'])
    best_mae = search_results.iloc[0]['mae']
    
    print(f"\n{'='*60}")
    print(f"BEST FEATURE COMBINATION SELECTED")
    print(f"{'='*60}")
    print(f"Best MAE: ${best_mae:,.2f}")
    print(f"Selected {len(best_features)} features:")
    for i, feature in enumerate(best_features, 1):
        print(f"  {i}. {feature}")
    
    # Evaluate the best combination in detail
    evaluate_feature_combination(df, best_features, n_samples=1000)
    

    # ========================================================================
    # TRAIN FINAL MODEL WITH BEST FEATURES
    # ========================================================================
    print("\n" + "="*60)
    print(f"TRAINING FINAL MODEL WITH BEST {len(best_features)} FEATURES")
    print("="*60)
    
    # Use only the best numeric features for final model
    X_best = df[best_features].copy()
    y_best = df["Sale Amount"]
    
    # Handle any missing values
    X_best = X_best.fillna(X_best.median())
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_best, y_best, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train final model
    final_model = Ridge(alpha=1.0)
    final_model.fit(X_train_scaled, y_train)
    y_pred = final_model.predict(X_test_scaled)
    
    # ========================================================================
    # CALCULATE CONFIDENCE INTERVALS
    # ========================================================================
    print("\n" + "="*60)
    print("CALCULATING PREDICTION CONFIDENCE INTERVALS")
    print("="*60)

    # Calculate residuals on test set
    residuals = y_test - y_pred

    # Calculate prediction intervals (95% confidence)
    # For individual predictions, use: prediction ± t*SE
    # Standard error of residuals
    residual_std = np.std(residuals)

    # t-value for 95% confidence with n-2 degrees of freedom
    t_value = stats.t.ppf(0.975, df=len(y_test)-2)

    # Margin of error for 95% confidence interval
    margin_of_error = t_value * residual_std

    print(f"\nResidual standard deviation: ${residual_std:,.2f}")
    print(f"95% Confidence Interval: ±${margin_of_error:,.2f}")
    print(f"This means: Predicted price ± ${margin_of_error:,.2f}")

    # Calculate confidence interval for a specific prediction
    def get_prediction_interval(predicted_price, confidence=0.95):
        """
        Calculate confidence interval for a prediction.
        """
        z_score = stats.t.ppf((1 + confidence) / 2, df=len(y_test)-2)
        interval = z_score * residual_std
        return (predicted_price - interval, predicted_price + interval)

    # Save the margin of error for use in prediction file
    with open("prediction_interval.txt", "w") as f:
        f.write(f"margin_of_error = {margin_of_error}\n")
        f.write(f"residual_std = {residual_std}\n")
        f.write(f"confidence_level = 0.95\n")

    # Final metrics
    final_mae = mean_absolute_error(y_test, y_pred)
    final_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    final_r2 = r2_score(y_test, y_pred)
    
    print(f"\n{'='*60}")
    print(f"FINAL MODEL PERFORMANCE (Best {len(best_features)} Features)")
    print(f"{'='*60}")
    print(f"MAE: ${final_mae:,.2f}")
    print(f"RMSE: ${final_rmse:,.2f}")
    print(f"R²: {final_r2:.4f}")
    
    # Feature coefficients for final model
    print(f"\nFeature Coefficients (standardized) for Final Model:")
    coef_df_final = pd.DataFrame({
        'feature': best_features,
        'coefficient': final_model.coef_,
        'abs_coef': np.abs(final_model.coef_)
    }).sort_values('abs_coef', ascending=False)
    
    for _, row in coef_df_final.iterrows():
        direction = "positive" if row['coefficient'] > 0 else "negative"
        print(f"  {row['feature']}: {direction} ({abs(row['coefficient']):.4f})")
    
    # ========================================================================
    # EXTRACT AND SAVE MEANS, STDS, INTERCEPT, AND COEFFICIENTS
    # ========================================================================
    print("\n" + "="*60)
    print("EXTRACTING MODEL PARAMETERS FOR PREDICTION")
    print("="*60)
    
    # Get intercept
    intercept = final_model.intercept_
    print(f"\nModel Intercept: ${intercept:,.2f}")
    
    # Create dataframe with all parameters
    prediction_params = []
    
    for i, feature in enumerate(best_features):
        mean_val = scaler.mean_[i]
        std_val = scaler.scale_[i]
        coef_val = final_model.coef_[i]
        
        prediction_params.append({
            'feature': feature,
            'coefficient': coef_val,
            'mean': mean_val,
            'std': std_val,
            'intercept': intercept  # Same for all rows
        })
        
        print(f"\n{feature}:")
        print(f"  Mean: {mean_val:,.2f}")
        print(f"  Std Dev: {std_val:,.2f}")
        print(f"  Coefficient: {coef_val:,.4f}")
    
    # Save to CSV
    params_df = pd.DataFrame(prediction_params)
    params_df.to_csv("model_parameters.csv", index=False)
  
    
    # Also save as a simple text file for easy copying
    with open("prediction_params.txt", "w") as f:
        f.write(f"INTERCEPT = {intercept}\n\n")
        f.write("FEATURE_PARAMS = {\n")
        for feature in best_features:
            i = best_features.index(feature)
            f.write(f"    '{feature}': {{\n")
            f.write(f"        'coefficient': {final_model.coef_[i]},\n")
            f.write(f"        'mean': {scaler.mean_[i]},\n")
            f.write(f"        'std': {scaler.scale_[i]},\n")
            f.write(f"    }},\n")
        f.write("}\n")
    
    
    # Save final model coefficients
    coef_df_final.to_csv("final_model_coefficients.csv", index=False)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total numeric features available: {len(numeric_features)}")
    print(f"Best combination uses: {len(best_features)} features")
    print(f"Best MAE achieved: ${best_mae:,.2f}")
    print(f"Final model MAE on holdout: ${final_mae:,.2f}")
    print(f"\nModel parameters saved to:")
    print(f"  - model_parameters.csv")
    print(f"  - prediction_params.txt")
    print(f"  - final_model_coefficients.csv")


if __name__ == "__main__":
    main()