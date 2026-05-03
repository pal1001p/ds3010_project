import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { YEARLY_TREND } from '../data/mockData';

function fmtMoney(v: number) {
  return '$' + (v / 1000).toFixed(0) + 'k';
}

export default function MarketChart() {
  return (
    <div className="content-area">
      <div className="chart-card">
        <h2>Connecticut Market Trends</h2>
        <p className="subtitle">Average assessed value vs. sale amount by year (statewide)</p>

        <ResponsiveContainer width="100%" height={360}>
          <AreaChart data={YEARLY_TREND} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
            <defs>
              <linearGradient id="gradSale" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#ac2b37" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#ac2b37" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="gradAssessed" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#000000" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#000000" stopOpacity={0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#ede9e1" />
            <XAxis dataKey="year" tick={{ fontSize: 12, fill: '#718096' }} />
            <YAxis tickFormatter={fmtMoney} tick={{ fontSize: 12, fill: '#718096' }} />
            <Tooltip
              formatter={(v) => {
                const value = Number(v ?? 0);
                return value.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
              }}
              contentStyle={{
                fontFamily: 'DM Sans, sans-serif',
                fontSize: 13,
                borderRadius: 8,
                border: '1px solid #ede9e1',
                boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: 13, paddingTop: 16 }}
            />

            <Area
              type="monotone"
              dataKey="avgSale"
              name="Avg Sale Price"
              stroke="#ac2b37"
              strokeWidth={2.5}
              fill="url(#gradSale)"
              dot={{ r: 4, fill: '#ac2b37' }}
              activeDot={{ r: 6 }}
            />
            <Area
              type="monotone"
              dataKey="avgAssessed"
              name="Avg Assessed Value"
              stroke="#000000"
              strokeWidth={2.5}
              fill="url(#gradAssessed)"
              dot={{ r: 4, fill: '#000000' }}
              activeDot={{ r: 6 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Gap analysis card */}
      <div className="chart-card" style={{ marginTop: 0 }}>
        <h2>Price Gap Analysis</h2>
        <p className="subtitle">How much above assessed value do properties typically sell for?</p>

        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
          {YEARLY_TREND.map(y => {
            const gap = Math.round((y.avgSale / y.avgAssessed - 1) * 100);
            return (
              <div key={y.year} style={{
                flex: '1 1 100px',
                background: 'var(--cream)',
                borderRadius: 'var(--radius)',
                padding: '16px 20px',
                textAlign: 'center',
                border: '1px solid var(--cream-dark)',
              }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--slate-light)', fontWeight: 600, marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.08em' }}>{y.year}</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, fontFamily: 'var(--font-display)', color: gap > 50 ? 'var(--green-soft)' : 'var(--amber)' }}>+{gap}%</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--slate-light)', marginTop: 2 }}>above assessed</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
