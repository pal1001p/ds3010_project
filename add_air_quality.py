import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

base_path = '/Users/val/Desktop/DS3000/project/'

# Load existing combined data
print("Loading combined data...")
combined = pd.read_csv(base_path + 'combined_real_estate_data.csv')
print(f'Combined shape: {combined.shape}')

# Load air quality data
print("\nProcessing Air Quality Data...")
air_quality = pd.read_csv(base_path + 'air_quality_ct.csv', header=None)
air_quality.columns = ['town_number']
print(f'Air quality raw shape: {air_quality.shape}')
print(f'Sample raw data: {air_quality["town_number"].head().tolist()}')

# Extract town name (remove numbers at end) and air quality value
air_quality['Town'] = air_quality['town_number'].str.replace(
    r'\d+$', '', regex=True).str.lower().str.strip()
air_quality['air_quality'] = air_quality['town_number'].str.extract(
    r'(\d+)$')[0].astype(int)

# Keep only the columns we need
air_quality = air_quality[['Town', 'air_quality']]
print(f'Air quality processed: {air_quality.shape}')
print(f'Sample air quality data:\n{air_quality.head(10)}')

# Merge with combined data on Town
combined = combined.merge(air_quality, on='Town', how='left')
print(f'\nFinal combined shape: {combined.shape}')
print(f'Rows with air quality data: {combined["air_quality"].notna().sum()}')

# Save
output_path = base_path + 'combined_real_estate_data.csv'
combined.to_csv(output_path, index=False)
print(f'\nSaved to: {output_path}')
print(f'\nColumn list: {combined.columns.tolist()}')
