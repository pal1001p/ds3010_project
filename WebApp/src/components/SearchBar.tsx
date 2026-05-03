import { useState, useRef, useEffect } from 'react';
import { Search, MapPin } from 'lucide-react';
import { MOCK_PROPERTIES } from '../data/mockData';
import type { Property } from '../types';

interface SearchBarProps {
  onSelectProperty: (p: Property) => void;
}

export default function SearchBar({ onSelectProperty }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  const results = query.length > 1
    ? MOCK_PROPERTIES.filter(p =>
        p.address.toLowerCase().includes(query.toLowerCase()) ||
        p.town.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 6)
    : [];

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="search-wrapper" ref={wrapperRef}>
      <Search size={15} className="search-icon" />
      <input
        className="search-input"
        type="text"
        placeholder="Search towns or addresses…"
        value={query}
        onChange={e => { setQuery(e.target.value); setOpen(true); }}
        onFocus={() => setOpen(true)}
      />
      {open && results.length > 0 && (
        <div className="search-dropdown">
          {results.map(p => (
            <div
              key={p.id}
              className="search-dropdown-item"
              onMouseDown={() => {
                onSelectProperty(p);
                setQuery(`${p.address}, ${p.town}`);
                setOpen(false);
              }}
            >
              <MapPin size={13} />
              <span>{p.address}</span>
              <span className="town-badge">{p.town}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
