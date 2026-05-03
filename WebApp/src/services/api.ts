import type { FeatureImportance, PredictionInput, PredictionResult } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

type PredictResponse = {
  price_rounded: number;
  lower_bound: number | null;
  upper_bound: number | null;
  margin_of_error: number | null;
};

export async function predictPrice(input: PredictionInput): Promise<PredictionResult> {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });

  if (!response.ok) {
    throw new Error(`Prediction request failed (${response.status})`);
  }

  const data = (await response.json()) as PredictResponse;
  const low = data.lower_bound ?? data.price_rounded;
  const high = data.upper_bound ?? data.price_rounded;
  const confidence = data.margin_of_error ? 0.95 : 0.8;

  return {
    predictedSaleAmount: data.price_rounded,
    confidence,
    priceRange: { low, high },
  };
}

export async function getFeatureImportance(): Promise<FeatureImportance[]> {
  const response = await fetch(`${API_BASE_URL}/api/feature-importance`);
  if (!response.ok) {
    throw new Error(`Feature importance request failed (${response.status})`);
  }

  const data = (await response.json()) as FeatureImportance[];
  return data;
}
