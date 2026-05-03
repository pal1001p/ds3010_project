"""
House Price Prediction Tool with Confidence Intervals
"""

import pandas as pd
import numpy as np
from pathlib import Path


class HousePricePredictor:
    """
    Predict house prices with confidence intervals.
    """
    
    def __init__(self, params_file="model_parameters.csv", interval_file="prediction_interval.txt"):
        """
        Initialize the predictor by loading model parameters.
        """
        # Load parameters (existing code)
        if not Path(params_file).exists():
            raise FileNotFoundError(f"Could not find {params_file}")
        
        self.params_df = pd.read_csv(params_file)
        self.intercept = self.params_df['intercept'].iloc[0]
        self.features = self.params_df['feature'].tolist()
        self.coefficients = dict(zip(self.params_df['feature'], self.params_df['coefficient']))
        self.means = dict(zip(self.params_df['feature'], self.params_df['mean']))
        self.stds = dict(zip(self.params_df['feature'], self.params_df['std']))
        
        # Debug: Print loaded features
        print(f"\n✓ Loaded {len(self.features)} features from model:")
        for i, feature in enumerate(self.features, 1):
            print(f"  {i}. '{feature}'")
        
        # Load confidence interval data
        try:
            with open(interval_file, 'r') as f:
                for line in f:
                    if 'margin_of_error' in line:
                        self.margin_of_error = float(line.split('=')[1].strip())
                    elif 'residual_std' in line:
                        self.residual_std = float(line.split('=')[1].strip())
            self.has_interval = True
            print(f"\n✓ Loaded confidence intervals: ±${self.margin_of_error:,.2f}")
        except:
            self.has_interval = False
            print("\n⚠️ No confidence interval file found")
    
    def verify_features(self, **kwargs):
        """
        Verify that input features match model expectations.
        
        Returns:
            Tuple of (is_valid, corrected_kwargs, missing_features, extra_features)
        """
        print("\n" + "="*60)
        print("FEATURE VERIFICATION")
        print("="*60)
        
        # Explicit mapping for all possible input names to model feature names
        feature_mapping = {
            # Assessed Value variations
            'assessed_value': 'Assessed Value',
    
            
            # List Year variations
            'list_year': 'List Year',
     
            
            # High Schools variations
            'num_high_schools': '# High Schools',
     
            
            # Middle Schools variations
            'num_middle_schools': '# Middle Schools',
           
            
            # Rank score variations
            'school_ranking': 'Rank score (2025)',
         
            
            # Air quality variations
            'air_quality': 'air_quality',
      
            
            # Crime rate variations
            'crime_rate_per_1000': 'Crime Rate per 1000',
        
        }
        
        corrected_kwargs = {}
        missing_features = []
        
        # Apply mapping to each input
        for arg_name, arg_value in kwargs.items():
            if arg_name in self.features:
                # Direct match
                corrected_kwargs[arg_name] = arg_value
                print(f"✓ '{arg_name}' = {arg_value} → Direct match")
            elif arg_name in feature_mapping:
                # Mapped match
                mapped_name = feature_mapping[arg_name]
                corrected_kwargs[mapped_name] = arg_value
                print(f"✓ '{arg_name}' = {arg_value} → Mapped to '{mapped_name}'")
            else:
                # Check if it's already in the correct format (case-insensitive)
                found = False
                for feature in self.features:
                    if arg_name.lower() == feature.lower().replace(' ', '_').replace('#', ''):
                        corrected_kwargs[feature] = arg_value
                        print(f"✓ '{arg_name}' = {arg_value} → Mapped to '{feature}'")
                        found = True
                        break
                if not found:
                    print(f"⚠️ '{arg_name}' = {arg_value} → Unknown feature (will be ignored)")
        
        # Check for missing features
        for feature in self.features:
            if feature not in corrected_kwargs:
                missing_features.append(feature)
        
        # Report results
        print("-"*60)
        if missing_features:
            print(f"❌ MISSING FEATURES ({len(missing_features)}):")
            for feature in missing_features:
                print(f"   • '{feature}'")
        else:
            print("✓ All required features provided")
        
        print("="*60)
        
        is_valid = len(missing_features) == 0
        return is_valid, corrected_kwargs, missing_features
    
    def predict(self, **kwargs):
        """
        Predict house price with confidence interval.
        
        Returns:
            Dictionary with price, lower_bound, upper_bound
        """
        predicted_price = self.intercept
        
        for feature in self.features:
            input_value = kwargs.get(feature, 0)
            mean = self.means[feature]
            std = self.stds[feature] if self.stds[feature] != 0 else 1
            standardized = (input_value - mean) / std
            predicted_price += self.coefficients[feature] * standardized
        
        predicted_price = max(0, predicted_price)
        
        # Calculate confidence interval
        if self.has_interval:
            lower_bound = max(0, predicted_price - self.margin_of_error)
            upper_bound = predicted_price + self.margin_of_error
        else:
            lower_bound = None
            upper_bound = None
        
        return {
            'price': predicted_price,
            'price_rounded': round(predicted_price, 2),
            'lower_bound': round(lower_bound, 2) if lower_bound else None,
            'upper_bound': round(upper_bound, 2) if upper_bound else None,
            'margin_of_error': self.margin_of_error if self.has_interval else None
        }
    
    def predict_with_details(self, **kwargs):
        """
        Predict with detailed breakdown and confidence intervals.
        """
        # First verify features
        is_valid, corrected_kwargs, missing_features = self.verify_features(**kwargs)
        
        if not is_valid:
            print("\n❌ ERROR: Missing required features!")
            print("Please provide values for all required features.")
            print("\nExample prediction:")
            example_args = {feature: 0 for feature in self.features}
            print(f"  predictor.predict({example_args})")
            return None
        
        # Use corrected kwargs for prediction
        result = self.predict(**corrected_kwargs)
        
        # Add contributions
        contributions = {}
        standardized_values = {}
        
        for feature in self.features:
            input_value = corrected_kwargs.get(feature, 0)
            mean = self.means[feature]
            std = self.stds[feature] if self.stds[feature] != 0 else 1
            standardized = (input_value - mean) / std
            standardized_values[feature] = standardized
            contributions[feature] = self.coefficients[feature] * standardized
        
        result['contributions'] = contributions
        result['standardized_values'] = standardized_values
        result['inputs'] = corrected_kwargs
        
        return result


if __name__ == "__main__":
    # Initialize predictor
    predictor = HousePricePredictor()
    
    # Test prediction with ALL required features using snake_case names
    result = predictor.predict_with_details(
        assessed_value=325000,
        list_year=2023,
        num_high_schools=3,
        num_middle_schools=2,
        school_ranking=0.4,
        air_quality=45,
        crime_rate_per_1000=1
    )
    
    # Display results if prediction was successful
    if result:
        print("\n" + "="*60)
        print("PREDICTION WITH CONFIDENCE INTERVAL")
        print("="*60)
        print(f"Predicted price: ${result['price_rounded']:,.2f}")
        if result['lower_bound']:
            print(f"95% Confidence Interval: ${result['lower_bound']:,.2f} - ${result['upper_bound']:,.2f}")
            print(f"Margin of error: ±${result['margin_of_error']:,.2f}")
        
        print("\n" + "="*60)
        print("FEATURE CONTRIBUTIONS")
        print("="*60)
        # Sort contributions by absolute value to show most impactful first
        sorted_contributions = sorted(
            result['contributions'].items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )
        for feature, contribution in sorted_contributions:
            direction = "↑" if contribution > 0 else "↓"
            print(f"{direction} {feature:25} ${contribution:15,.2f} (input: {result['inputs'][feature]})")
        
        print("="*60)
        print(f"Intercept (baseline):      ${predictor.intercept:15,.2f}")
        print(f"Final price:               ${result['price_rounded']:15,.2f}")
        print("="*60)