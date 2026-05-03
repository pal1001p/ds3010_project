import { Map, Zap } from 'lucide-react';
import type { ActiveView } from '../types';

interface SidebarProps {
  active: ActiveView;
  onChange: (v: ActiveView) => void;
}

const NAV_ITEMS: { id: ActiveView; label: string; icon: React.ReactNode }[] = [
  { id: 'map',     label: 'Property Map',       icon: <Map size={16} /> },
  { id: 'predict', label: 'Price Predictor',    icon: <Zap size={16} /> },
];

export default function Sidebar({ active, onChange }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>WPI Real Estate</h1>
        <span>Connecticut Property Analytics</span>
      </div>

      <p className="sidebar-section-label">Navigation</p>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map(item => (
          <button
            key={item.id}
            className={`nav-btn ${active === item.id ? 'active' : ''}`}
            onClick={() => onChange(item.id)}
          >
            {item.icon}
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <strong style={{ color: 'rgba(255,255,255,0.5)' }}>Dataset</strong><br />
        251,976 cleaned records<br />
        Source: CT OPM Real Estate Sales<br />
        <br />
        <strong style={{ color: 'rgba(255,255,255,0.5)' }}>Stack</strong><br />
        React · Vite · TypeScript
      </div>
    </aside>
  );
}
