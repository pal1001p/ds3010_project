import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import type { Property } from '../types';
import { CT_CENTER, MOCK_PROPERTIES } from '../data/mockData';
import { useEffect, useState } from 'react';

// Fix Leaflet's default icon path issue with bundlers
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

// Custom crimson pin for selected property
const selectedIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// Helper component to fly the map to a location
function FlyTo({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo([lat, lng], 13, { duration: 1.2 });
  }, [lat, lng, map]);
  return null;
}

function formatMoney(n: number) {
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
}

function displayValue(value: string | number | undefined): string {
  if (value === undefined || value === '') return '—';
  return String(value);
}

interface MapViewProps {
  selectedProperty: Property | null;
  activeTown: string | null;
}

export default function MapView({ selectedProperty, activeTown }: MapViewProps) {
  const [showSampleBanner, setShowSampleBanner] = useState(true);
  const filtered = activeTown
    ? MOCK_PROPERTIES.filter(p => p.town === activeTown)
    : MOCK_PROPERTIES;

  return (
    <div className="map-view-shell">
      {showSampleBanner && (
        <div className="sample-banner">
          <div>
            <strong>Sample dataset loaded.</strong> The full dataset is very large, so this map currently shows a smaller sample.
          </div>
          <button onClick={() => setShowSampleBanner(false)} aria-label="Dismiss sample notice">
            Dismiss
          </button>
        </div>
      )}
      <div className="map-container">
        <MapContainer
          center={CT_CENTER}
          zoom={9}
          scrollWheelZoom
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {filtered.map(p => (
            <Marker
              key={p.id}
              position={[p.lat, p.lng]}
              icon={selectedProperty?.id === p.id ? selectedIcon : new L.Icon.Default()}
            >
              <Popup>
                <div className="property-popup clean">
                  <h3>{p.address}</h3>
                  <p className="popup-subtitle">{p.town}</p>

                  <div className="popup-section-title">Sale details</div>
                  <div className="popup-grid">
                    <div className="popup-row"><span>Serial #</span><strong>{p.serialNumber}</strong></div>
                    <div className="popup-row"><span>Date</span><strong>{displayValue(p.dateRecorded)}</strong></div>
                    <div className="popup-row"><span>Assessed</span><strong>{formatMoney(p.assessedValue)}</strong></div>
                    <div className="popup-row"><span>Sale</span><strong>{formatMoney(p.saleAmount)}</strong></div>
                    <div className="popup-row"><span>Sales Ratio</span><strong>{displayValue(p.salesRatio)}</strong></div>
                    <div className="popup-row"><span>List Year</span><strong>{displayValue(p.listYear)}</strong></div>
                    <div className="popup-row"><span>Property Type</span><strong>{displayValue(p.propertyType)}</strong></div>
                    <div className="popup-row"><span>Residential</span><strong>{displayValue(p.residentialType)}</strong></div>
                  </div>

                  <div className="popup-section-title">Community metrics</div>
                  <div className="popup-grid">
                    <div className="popup-row"><span>School Rank</span><strong>{displayValue(p.schoolRank)}</strong></div>
                    <div className="popup-row"><span>Rank Score</span><strong>{displayValue(p.rankScore2025)}</strong></div>
                    <div className="popup-row"><span>Elem Schools</span><strong>{displayValue(p.elementarySchools)}</strong></div>
                    <div className="popup-row"><span>Middle Schools</span><strong>{displayValue(p.middleSchools)}</strong></div>
                    <div className="popup-row"><span>High Schools</span><strong>{displayValue(p.highSchools)}</strong></div>
                    <div className="popup-row"><span>Private Schools</span><strong>{displayValue(p.privateSchools)}</strong></div>
                    <div className="popup-row"><span>Air Quality</span><strong>{displayValue(p.airQuality)}</strong></div>
                    <div className="popup-row"><span>Crime Rate</span><strong>{displayValue(p.crimeRate)}</strong></div>
                    <div className="popup-row"><span>Total Crimes</span><strong>{displayValue(p.totalCrimes)}</strong></div>
                    <div className="popup-row"><span>Population</span><strong>{displayValue(p.townPopulation)}</strong></div>
                    <div className="popup-row"><span>ZIP</span><strong>{displayValue(p.zipCode)}</strong></div>
                    <div className="popup-row"><span>ZIP Population</span><strong>{displayValue(p.zipPopulation)}</strong></div>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Fly to selected property */}
          {selectedProperty && (
            <FlyTo lat={selectedProperty.lat} lng={selectedProperty.lng} />
          )}

          {/* Fly to town center when a favorite is selected */}
          {activeTown && !selectedProperty && (() => {
            const first = MOCK_PROPERTIES.find(p => p.town === activeTown);
            return first ? <FlyTo lat={first.lat} lng={first.lng} /> : null;
          })()}
        </MapContainer>
      </div>
    </div>
  );
}
