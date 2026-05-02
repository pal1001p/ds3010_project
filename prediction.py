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
        
        # Load confidence interval data
        try:
            with open(interval_file, 'r') as f:
                for line in f:
                    if 'margin_of_error' in line:
                        self.margin_of_error = float(line.split('=')[1].strip())
                    elif 'residual_std' in line:
                        self.residual_std = float(line.split('=')[1].strip())
            self.has_interval = True
        except:
            self.has_interval = False
            print("⚠️ No confidence interval file found")
        
    
    def predict(self, **kwargs):
        """
        Predict house price with confidence interval.
        
        Returns:
            Dictionary with price, lower_bound, upper_bound
        """
        predicted_price = self.intercept
        
        for feature in self.features:
            input_value = kwargs.get(feature, kwargs.get(feature.replace(' ', '_'), 0))
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
        result = self.predict(**kwargs)
        
        # Add contributions
        contributions = {}
        standardized_values = {}
        
        for feature in self.features:
            input_value = kwargs.get(feature, kwargs.get(feature.replace(' ', '_'), 0))
            mean = self.means[feature]
            std = self.stds[feature] if self.stds[feature] != 0 else 1
            standardized = (input_value - mean) / std
            standardized_values[feature] = standardized
            contributions[feature] = self.coefficients[feature] * standardized
        
        result['contributions'] = contributions
        result['standardized_values'] = standardized_values
        result['inputs'] = kwargs
        
        return result



if __name__ == "__main__":
    predictor = HousePricePredictor()
    
    # Test prediction
    result = predictor.predict_with_details(
        Assessed_Value=325000,
        List_Year=2023,
        num_High_Schools=3,
        num_Middle_Schools=2,
        town_population=25000,
        air_quality=45,
        num_Private_Schools=1
    )
    
    print("\n" + "="*60)
    print("PREDICTION WITH CONFIDENCE INTERVAL")
    print("="*60)
    print(f"Predicted price: ${result['price_rounded']:,.2f}")
    if result['lower_bound']:
        print(f"95% Confidence Interval: ${result['lower_bound']:,.2f} - ${result['upper_bound']:,.2f}")
        print(f"Margin of error: ±${result['margin_of_error']:,.2f}")
    print("="*60)
 