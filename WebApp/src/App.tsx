import { useState } from 'react';
import './index.css';
import 'leaflet/dist/leaflet.css';

import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import MapView from './components/MapView';
import ListingForm from './components/ListingForm';

import type {ActiveView, Property} from './types';

const VIEW_TITLES: Record<ActiveView, string> = {
  map:     'Property Map',
  predict: 'Price Predictor',
};

export default function App() {
  const [activeView, setActiveView]         = useState<ActiveView>('map');
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [activeTown, setActiveTown]         = useState<string | null>(null);

  const handleSelectTown = (town: string) => {
    setActiveTown(town || null);
    setSelectedProperty(null);
    // Switch to map view when a town is selected
    setActiveView('map');
  };

  const handleSelectProperty = (p: Property) => {
    setSelectedProperty(p);
    setActiveTown(null);
    setActiveView('map');
  };

  return (
    <div className="app-shell">
      <Sidebar active={activeView} onChange={setActiveView} />

      <div className="main-panel">
        {/* Top bar */}
        <div className="topbar">
          <span className="topbar-title">{VIEW_TITLES[activeView]}</span>
          <span className="topbar-spacer" />
          <SearchBar onSelectProperty={handleSelectProperty} />
        </div>

        {/* Favorites bar — only shown on map view */}
        {activeView === 'map' && (
          <FavoritesBar activeTown={activeTown} onSelectTown={handleSelectTown} />
        )}

        {/* Content */}
        {activeView === 'map'     && <MapContentArea selectedProperty={selectedProperty} activeTown={activeTown} />}
        {activeView === 'predict' && <ListingForm />}
      </div>
    </div>
  );
}

// ── Inline subcomponents for map layout ─────────────────────────

import { FAVORITE_TOWNS } from './data/mockData';

function FavoritesBar({ activeTown, onSelectTown }: { activeTown: string | null; onSelectTown: (t: string) => void }) {
  return (
    <div className="favorites-bar">
      {FAVORITE_TOWNS.map(town => (
        <button
          key={town}
          className={`fav-pill ${activeTown === town ? 'active' : ''}`}
          onClick={() => onSelectTown(town === activeTown ? '' : town)}
        >
          {town}
        </button>
      ))}
    </div>
  );
}

function MapContentArea({ selectedProperty, activeTown }: { selectedProperty: Property | null; activeTown: string | null }) {
  return (
    <div className="content-area" style={{ padding: 16, flex: 1 }}>
      <MapView selectedProperty={selectedProperty} activeTown={activeTown} />
    </div>
  );
}
