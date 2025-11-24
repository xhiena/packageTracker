import { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { packagesAPI } from '../services/api';

function PackageDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [packageData, setPackageData] = useState(null);
  const [trackingInfo, setTrackingInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingCarrier, setEditingCarrier] = useState(false);
  const [newCarrier, setNewCarrier] = useState('');
  const [detectedCarriers, setDetectedCarriers] = useState([]);

  useEffect(() => {
    const fetchPackageDetails = async () => {
      try {
        setLoading(true);
        // Fetch package details first
        const packageResponse = await packagesAPI.get(id);
        setPackageData(packageResponse.data);
        setError('');

        // Try to fetch tracking info, but don't fail if it errors
        try {
          const trackingResponse = await packagesAPI.track(id);
          setTrackingInfo(trackingResponse.data);
        } catch (trackingErr) {
          // Set tracking info with error, but don't block the page
          setTrackingInfo({
            error: trackingErr.response?.data?.detail || 'Failed to load tracking information',
            status: null,
            location: null,
            history: []
          });
        }
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load package details');
      } finally {
        setLoading(false);
      }
    };

    fetchPackageDetails();
  }, [id]);

  // Sort history in reverse chronological order (newest first)
  const sortedHistory = useMemo(() =>
    trackingInfo?.history
      ? [...trackingInfo.history].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      : []
    , [trackingInfo?.history]);

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleEditCarrier = async () => {
    setEditingCarrier(true);
    setNewCarrier(packageData.carrier);

    // Fetch detected carriers from KeyDelivery
    try {
      const response = await fetch(`http://localhost:8000/api/carriers/detect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ tracking_number: packageData.tracking_number })
      });

      if (response.ok) {
        const data = await response.json();
        // data should be array of {carrier_id, carrier_name}
        setDetectedCarriers(data.carriers || []);
      }
    } catch (err) {
      console.error('Failed to detect carriers:', err);
      setDetectedCarriers([]);
    }
  };

  const handleSaveCarrier = async () => {
    try {
      await packagesAPI.update(id, { carrier: newCarrier });
      setPackageData({ ...packageData, carrier: newCarrier });
      setEditingCarrier(false);
      setDetectedCarriers([]);
      // Refresh tracking info with new carrier
      try {
        const trackingResponse = await packagesAPI.track(id);
        setTrackingInfo(trackingResponse.data);
      } catch (trackingErr) {
        setTrackingInfo({
          error: trackingErr.response?.data?.detail || 'Failed to load tracking information',
          status: null,
          location: null,
          history: []
        });
      }
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update carrier');
    }
  };

  const handleCancelEdit = () => {
    setEditingCarrier(false);
    setNewCarrier('');
    setDetectedCarriers([]);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading package details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
          <div className="text-red-600 text-center mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 text-center mb-2">Error</h3>
          <p className="text-gray-600 text-center mb-6">{error}</p>
          <button
            onClick={handleBack}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex items-center">
          <button
            onClick={handleBack}
            className="mr-4 p-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            title="Back to Dashboard"
            aria-label="Back to Dashboard"
          >
            <svg className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Package Details</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 sm:px-0">
          {/* Package Info Card */}
          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {packageData?.description || 'Package Information'}
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-gray-500">Tracking Number</p>
                <p className="text-base text-gray-900 font-mono mt-1">{packageData?.tracking_number}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-500">Carrier</p>
                {editingCarrier ? (
                  <div className="flex items-center gap-2 mt-1">
                    <select
                      value={newCarrier}
                      onChange={(e) => setNewCarrier(e.target.value)}
                      className="px-2 py-1 border border-gray-300 rounded text-sm uppercase"
                    >
                      <option value="">Select carrier...</option>
                      {detectedCarriers.length > 0 ? (
                        // Show detected carriers
                        detectedCarriers.map((carrier) => (
                          <option key={carrier.carrier_id} value={carrier.carrier_id}>
                            {carrier.carrier_name} ({carrier.carrier_id})
                          </option>
                        ))
                      ) : (
                        // Fallback to common carriers if detection failed
                        <>
                          <option value="dhl">DHL</option>
                          <option value="dhl_de">DHL Deutschland</option>
                          <option value="ups">UPS</option>
                          <option value="fedex">FedEx</option>
                          <option value="usps">USPS</option>
                          <option value="correos">Correos</option>
                          <option value="gls">GLS</option>
                          <option value="seur">SEUR</option>
                        </>
                      )}
                    </select>
                    <button
                      onClick={handleSaveCarrier}
                      className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                      disabled={!newCarrier}
                    >
                      Save
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="px-3 py-1 bg-gray-300 text-gray-700 text-sm rounded hover:bg-gray-400"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 mt-1">
                    <p className="text-base text-gray-900 uppercase">{packageData?.carrier}</p>
                    <button
                      onClick={handleEditCarrier}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                      title="Edit carrier"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>

              {trackingInfo?.status && (
                <div>
                  <p className="text-sm font-medium text-gray-500">Current Status</p>
                  <p className="text-base text-gray-900 mt-1">{trackingInfo.status}</p>
                </div>
              )}

              {trackingInfo?.location && (
                <div>
                  <p className="text-sm font-medium text-gray-500">Current Location</p>
                  <p className="text-base text-gray-900 mt-1">{trackingInfo.location}</p>
                </div>
              )}
            </div>
          </div>

          {/* Tracking Timeline */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Tracking Timeline</h2>

            {trackingInfo?.error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {trackingInfo.error}
              </div>
            )}

            {sortedHistory.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="mt-2">No tracking history available</p>
              </div>
            ) : (
              <div className="relative">
                {/* Timeline line */}
                <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-300"></div>

                {/* Timeline events */}
                <div className="space-y-6">
                  {sortedHistory.map((event) => (
                    <div key={`${event.timestamp}-${event.status}-${event.location || ''}`} className="relative flex items-start">
                      {/* Timeline dot */}
                      <div className="absolute left-8 -translate-x-1/2 w-4 h-4 rounded-full bg-blue-600 border-4 border-white shadow"></div>

                      {/* Event content */}
                      <div className="ml-16 flex-1">
                        <div className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors">
                          <div className="flex justify-between items-start mb-2">
                            <h3 className="text-base font-semibold text-gray-900">
                              {event.status}
                            </h3>
                            <span className="text-sm text-gray-500 whitespace-nowrap ml-4">
                              {new Date(event.timestamp).toLocaleString()}
                            </span>
                          </div>

                          {event.location && (
                            <div className="flex items-center text-sm text-gray-600">
                              <svg className="h-4 w-4 mr-1 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                              </svg>
                              {event.location}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default PackageDetail;
