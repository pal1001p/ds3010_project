import { useState } from 'react';
import { Zap } from 'lucide-react';
import type { PredictionInput, PredictionResult } from '../types';
import { predictPrice } from '../services/api';

function fmt(n: number) {
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
}

export default function ListingForm() {
  const [form, setForm] = useState<PredictionInput>({
    assessedValue: 500000,
    schoolRank: 0.5,
    airQuality: 30,
    middleSchools: 3,
    highSchools: 6,
    listYear: 2024,
    crimeRate: 5,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const set = (k: keyof PredictionInput, v: string | number) =>
    setForm(prev => ({ ...prev, [k]: v }));

  function clamp(k: keyof PredictionInput, value: number) {
    const ranges: Record<keyof PredictionInput, [number, number]> = {
      assessedValue: [10000, 20000000],
      schoolRank: [0, 1],
      airQuality: [10, 50],
      middleSchools: [0, 7],
      highSchools: [0, 20],
      listYear: [2001, 2024],
      crimeRate: [1, 10],
    };
    const [min, max] = ranges[k];
    return Math.min(max, Math.max(min, value));
  }

  function setNumeric(k: keyof PredictionInput, raw: string) {
    const parsed = Number(raw);
    if (!Number.isFinite(parsed)) return;
    set(k, clamp(k, parsed));
  }

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);
      const data = await predictPrice(form);
      setResult(data);
    } catch {
      setError('Could not reach the backend prediction API. Start the Python server and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="content-area">
      <div className="predict-panel">
        <div className="card">
          <h2>Price Predictor</h2>
          <p className="subtitle">
            Enter property details below. Our regression model will estimate the sale price.
          </p>

          <div className="form-grid">
            <div className="form-field">
              <label className="field-label">
                <span>Assessed Value ($)</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Estimated town-assessed property value in USD. Allowed range: $10,000 to $20,000,000."
                  aria-label="Assessed value: estimated town-assessed property value in USD. Allowed range $10,000 to $20,000,000."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.assessedValue}
                min={10000}
                max={20000000}
                step={5000}
                onChange={e => setNumeric('assessedValue', e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="field-label">
                <span>School Rank</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Score from 0 to 1: 0 is the worst ranking, 1 is the highest ranking."
                  aria-label="School rank: score from 0 (worst) to 1 (best)."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.schoolRank}
                min={0}
                max={1}
                step={0.01}
                onChange={e => setNumeric('schoolRank', e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="field-label">
                <span>Air Quality</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Category used by the model: Good (50), Medium (30), or Bad (10)."
                  aria-label="Air quality: Good 50, Medium 30, or Bad 10."
                >
                  i
                </button>
              </label>
              <select
                value={form.airQuality}
                onChange={e => set('airQuality', Number(e.target.value))}
              >
                <option value={50}>Good (50)</option>
                <option value={30}>Medium (30)</option>
                <option value={10}>Bad (10)</option>
              </select>
            </div>
            <div className="form-field">
              <label className="field-label">
                <span># Middle Schools</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Count of middle schools near the property. Allowed range: 0 to 7."
                  aria-label="Middle schools: count from 0 to 7."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.middleSchools}
                min={0}
                max={7}
                onChange={e => setNumeric('middleSchools', e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="field-label">
                <span># High Schools</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Count of high schools near the property. Allowed range: 0 to 20."
                  aria-label="High schools: count from 0 to 20."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.highSchools}
                min={0}
                max={20}
                onChange={e => setNumeric('highSchools', e.target.value)}
              />
            </div>
            <div className="form-field">
              <label className="field-label">
                <span>Crime Safety Score</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Scale 1–10: 1 is very safe, 10 is not very safe. The model converts this into a crime rate up to 110."
                  aria-label="Crime safety: 1 very safe through 10 not very safe; mapped for the model."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.crimeRate}
                step={1}
                min={1}
                max={10}
                onChange={e => setNumeric('crimeRate', e.target.value)}
              />
            </div>

            <div className="form-field">
              <label className="field-label">
                <span>List Year</span>
                <button
                  type="button"
                  className="field-hint"
                  data-tip="Year the listing applies to. Allowed range: 2001 to 2024."
                  aria-label="List year: 2001 through 2024."
                >
                  i
                </button>
              </label>
              <input
                type="number"
                value={form.listYear}
                min={2001}
                max={2024}
                step={1}
                onChange={e => setNumeric('listYear', e.target.value)}
              />
            </div>

          </div>

          <button
            className="btn-primary"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
                <span className="spinner" /> Predicting…
              </span>
            ) : (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
                <Zap size={16} /> Predict Sale Price
              </span>
            )}
          </button>
          {error && (
            <div className="api-error">
              {error}
            </div>
          )}

          {result && (
            <div className="prediction-result">
              <div className="result-label">Estimated Sale Price</div>
              <div className="result-price">{fmt(result.predictedSaleAmount)}</div>

              <div style={{ fontSize: '0.82rem', color: 'rgba(255,255,255,0.6)' }}>
                Confidence interval: {fmt(result.priceRange.low)} – {fmt(result.priceRange.high)}
              </div>

            </div>
          )}
        </div>

      </div>
    </div>
  );
}
