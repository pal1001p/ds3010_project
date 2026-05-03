import { TrendingUp, Home, BarChart2 } from 'lucide-react';
import { TOWN_STATS } from '../data/mockData';

function fmt(n: number) {
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
}

function pct(n: number) {
  return (n * 100).toFixed(1) + '%';
}

export default function NeighborhoodStats() {
  return (
    <div className="content-area">
      {/* Summary strip */}
      <div style={{ display: 'flex', gap: 16 }}>
        {[
          { icon: <Home size={18} />, label: 'Towns Tracked', value: TOWN_STATS.length },
          { icon: <BarChart2 size={18} />, label: 'Total Listings', value: TOWN_STATS.reduce((s, t) => s + t.totalListings, 0).toLocaleString() },
          { icon: <TrendingUp size={18} />, label: 'Avg Sale Price (CT)', value: fmt(Math.round(TOWN_STATS.reduce((s, t) => s + t.avgSaleAmount, 0) / TOWN_STATS.length)) },
        ].map(item => (
          <div key={item.label} style={{
            flex: 1,
            background: 'var(--white)',
            borderRadius: 'var(--radius)',
            padding: '18px 20px',
            boxShadow: 'var(--shadow)',
            border: '1px solid var(--cream-dark)',
            display: 'flex',
            alignItems: 'center',
            gap: 14,
          }}>
            <div style={{ color: 'var(--amber)', display:'flex', alignItems:'center' }}>{item.icon}</div>
            <div>
              <div style={{ fontSize: '0.72rem', color: 'var(--slate-light)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>{item.label}</div>
              <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--navy)', fontFamily: 'var(--font-display)' }}>{item.value}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Town cards */}
      <div className="stats-grid">
        {TOWN_STATS.map(t => (
          <div className="stat-card" key={t.town}>
            <div className="stat-card-town">
              {t.town}
              <span className="listings-badge">{t.totalListings.toLocaleString()} listings</span>
            </div>
            <div className="stat-row">
              <span className="label">Avg Assessed Value</span>
              <span className="value amber">{fmt(t.avgAssessedValue)}</span>
            </div>
            <div className="stat-row">
              <span className="label">Avg Sale Price</span>
              <span className="value green">{fmt(t.avgSaleAmount)}</span>
            </div>
            <div className="stat-row">
              <span className="label">Avg Sales Ratio</span>
              <span className="value">{pct(t.avgSalesRatio)}</span>
            </div>
            <div className="stat-row">
              <span className="label">Markup over Assessed</span>
              <span className="value">
                +{Math.round((t.avgSaleAmount / t.avgAssessedValue - 1) * 100)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
