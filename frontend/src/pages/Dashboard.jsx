import { useState, useEffect } from 'react';
import { packagesAPI } from '../services/api';
import AddPackageModal from '../components/AddPackageModal';

function Dashboard({ onLogout }) {
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    fetchPackages();
  }, []);

  const fetchPackages = async () => {
    try {
      setLoading(true);
      const response = await packagesAPI.getAll();
      setPackages(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load packages');
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePackage = async (id) => {
    if (!window.confirm('Are you sure you want to delete this package?')) {
      return;
    }
    try {
      await packagesAPI.delete(id);
      setPackages(packages.filter((pkg) => pkg.id !== id));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete package');
    }
  };

  const handleAddPackage = () => {
    setShowAddModal(false);
    fetchPackages();
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Package Tracker Dashboard</h1>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Add Package Button */}
          <div className="mb-6">
            <button
              onClick={() => setShowAddModal(true)}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
            >
              + Add Package
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Loading packages...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && packages.length === 0 && (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No packages</h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by adding a new package to track.
              </p>
            </div>
          )}

          {/* Packages Grid */}
          {!loading && packages.length > 0 && (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {packages.map((pkg) => (
                <div
                  key={pkg.id}
                  className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
                >
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">
                        {pkg.description || 'Unnamed Package'}
                      </h3>
                      <button
                        onClick={() => handleDeletePackage(pkg.id)}
                        className="text-red-600 hover:text-red-800 focus:outline-none"
                        title="Delete package"
                      >
                        <svg
                          className="h-5 w-5"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    </div>
                    
                    <div className="space-y-2">
                      <div>
                        <p className="text-xs font-medium text-gray-500">Tracking Number</p>
                        <p className="text-sm text-gray-900 font-mono">{pkg.tracking_number}</p>
                      </div>
                      
                      <div>
                        <p className="text-xs font-medium text-gray-500">Carrier</p>
                        <p className="text-sm text-gray-900 uppercase">{pkg.carrier || 'Unknown'}</p>
                      </div>
                      
                      {pkg.status && (
                        <div>
                          <p className="text-xs font-medium text-gray-500">Status</p>
                          <p className="text-sm text-gray-900">{pkg.status}</p>
                        </div>
                      )}
                      
                      {pkg.last_location && (
                        <div>
                          <p className="text-xs font-medium text-gray-500">Location</p>
                          <p className="text-sm text-gray-900">{pkg.last_location}</p>
                        </div>
                      )}
                      
                      {pkg.updated_at && (
                        <div>
                          <p className="text-xs font-medium text-gray-500">Last Updated</p>
                          <p className="text-sm text-gray-900">
                            {new Date(pkg.updated_at).toLocaleString()}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Add Package Modal */}
      {showAddModal && (
        <AddPackageModal
          onClose={() => setShowAddModal(false)}
          onSuccess={handleAddPackage}
        />
      )}
    </div>
  );
}

export default Dashboard;
