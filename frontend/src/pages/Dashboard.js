import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { packagesAPI } from '../services/api';

function Dashboard() {
  const [packages, setPackages] = useState([]);
  const [carriers, setCarriers] = useState([]);
  const [newPackage, setNewPackage] = useState({
    tracking_number: '',
    carrier: '',
    description: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [trackingData, setTrackingData] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    loadCarriers();
    loadPackages();
  }, []);

  const loadCarriers = async () => {
    try {
      const response = await packagesAPI.getCarriers();
      setCarriers(response.data.carriers);
      if (response.data.carriers.length > 0) {
        setNewPackage(prev => ({ ...prev, carrier: response.data.carriers[0] }));
      }
    } catch (err) {
      console.error('Failed to load carriers:', err);
    }
  };

  const loadPackages = async () => {
    setLoading(true);
    try {
      const response = await packagesAPI.list();
      setPackages(response.data);
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        setError('Failed to load packages');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddPackage = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await packagesAPI.create(newPackage);
      setNewPackage({
        tracking_number: '',
        carrier: carriers[0] || '',
        description: ''
      });
      loadPackages();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add package');
    }
  };

  const handleDeletePackage = async (id) => {
    if (window.confirm('Are you sure you want to delete this package?')) {
      try {
        await packagesAPI.delete(id);
        loadPackages();
      } catch (err) {
        setError('Failed to delete package');
      }
    }
  };

  const handleTrackPackage = async (id) => {
    try {
      const response = await packagesAPI.track(id);
      setTrackingData(prev => ({
        ...prev,
        [id]: response.data
      }));
    } catch (err) {
      setError('Failed to track package');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>📦 Package Tracker Dashboard</h1>
        <button onClick={handleLogout} className="btn-logout">
          Logout
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="add-package-section">
        <h2>Add New Package</h2>
        <form onSubmit={handleAddPackage} className="add-package-form">
          <div className="form-group">
            <label>Carrier</label>
            <select
              value={newPackage.carrier}
              onChange={(e) => setNewPackage({ ...newPackage, carrier: e.target.value })}
              required
            >
              {carriers.map(carrier => (
                <option key={carrier} value={carrier}>
                  {carrier.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Tracking Number</label>
            <input
              type="text"
              value={newPackage.tracking_number}
              onChange={(e) => setNewPackage({ ...newPackage, tracking_number: e.target.value })}
              placeholder="Enter tracking number"
              required
            />
          </div>
          <div className="form-group">
            <label>Description (Optional)</label>
            <input
              type="text"
              value={newPackage.description}
              onChange={(e) => setNewPackage({ ...newPackage, description: e.target.value })}
              placeholder="e.g., Birthday gift"
            />
          </div>
          <button type="submit" className="btn-add">
            Add Package
          </button>
        </form>
      </div>

      <div className="packages-list">
        <h2>Your Packages</h2>
        {loading ? (
          <div className="loading">Loading packages...</div>
        ) : packages.length === 0 ? (
          <div className="no-packages">
            No packages yet. Add your first package above!
          </div>
        ) : (
          packages.map(pkg => (
            <div key={pkg.id} className="package-card">
              <div className="package-header">
                <div className="package-tracking">
                  {pkg.tracking_number}
                </div>
                <div className="package-carrier">
                  {pkg.carrier}
                </div>
              </div>
              
              {pkg.description && (
                <div style={{ marginBottom: '10px', color: '#666' }}>
                  {pkg.description}
                </div>
              )}
              
              {pkg.status && (
                <div className="package-status">
                  <span className="package-status-label">Status: </span>
                  {pkg.status}
                  {pkg.last_location && ` - ${pkg.last_location}`}
                </div>
              )}
              
              <div className="package-actions">
                <button
                  onClick={() => handleTrackPackage(pkg.id)}
                  className="btn-track"
                >
                  Track Package
                </button>
                <button
                  onClick={() => handleDeletePackage(pkg.id)}
                  className="btn-delete"
                >
                  Delete
                </button>
              </div>
              
              {trackingData[pkg.id] && (
                <div className="tracking-history">
                  <h4>Tracking History</h4>
                  {trackingData[pkg.id].error ? (
                    <div className="error-message">
                      {trackingData[pkg.id].error}
                    </div>
                  ) : (
                    trackingData[pkg.id].history.map((event, index) => (
                      <div key={index} className="tracking-event">
                        <div className="tracking-event-time">
                          {new Date(event.timestamp).toLocaleString()}
                        </div>
                        <div className="tracking-event-status">
                          {event.status}
                        </div>
                        <div className="tracking-event-location">
                          📍 {event.location}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;
