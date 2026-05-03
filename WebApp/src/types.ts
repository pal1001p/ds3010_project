export interface Property {
  id: number;
  serialNumber: string;
  address: string;
  town: string;
  dateRecorded?: string;
  listYear: number;
  assessedValue: number;
  saleAmount: number;
  salesRatio: number;
  propertyType: string;
  residentialType: string;
  lat: number;
  lng: number;
  schoolRank?: string;
  rankScore2025?: number;
  elementarySchools?: number;
  middleSchools?: number;
  highSchools?: number;
  privateSchools?: number;
  airQuality?: number;
  townPopulation?: number;
  zipCode?: number;
  zipPopulation?: number;
  crimeRate?: number;
  totalCrimes?: number;
}

export interface TownStats {
  town: string;
  avgAssessedValue: number;
  avgSaleAmount: number;
  totalListings: number;
  avgSalesRatio: number;
  lat: number;
  lng: number;
}

export interface PredictionInput {
  assessedValue: number;
  schoolRank: number;
  airQuality: number;
  middleSchools: number;
  highSchools: number;
  listYear: number;
  crimeRate: number;
}

export interface PredictionResult {
  predictedSaleAmount: number;
  confidence: number;
  priceRange: { low: number; high: number };
}

export interface FeatureImportance {
  base_feature: string;
  aggregated_abs_coef: number;
  aggregated_signed_coef: number;
}

export type ActiveView = 'map' | 'predict';
