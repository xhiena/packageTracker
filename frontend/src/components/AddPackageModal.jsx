import { useState, useEffect } from 'react';
import { packagesAPI, carriersAPI } from '../services/api';

function AddPackageModal({ onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    tracking_number: '',
    carrier: '',
    nickname: '',
  });
  const [carriers, setCarriers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCarriers();
  }, []);

  const fetchCarriers = async () => {
    try {
      const response = await carriersAPI.getAll();
      setCarriers(response.data);
    } catch (err) {
      console.error('Failed to load carriers:', err);
      // Use default carriers if API fails
      setCarriers([
        { id: 'ups', name: 'UPS' },
        { id: 'usps', name: 'USPS' },
        { id: 'fedex', name: 'FedEx' },
        { id: 'dhl', name: 'DHL' },
      ]);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.tracking_number.trim()) {
      setError('Please enter a tracking number');
      return;
    }
    
    if (!formData.carrier) {
      setError('Please select a carrier');
      return;
    }

    try {
      setLoading(true);
      await packagesAPI.add(formData);
      onSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add package');
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 transition-opacity" 
          aria-hidden="true"
          onClick={onClose}
        >
          <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        {/* Center modal */}
        <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">
          &#8203;
        </span>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form onSubmit={handleSubmit}>
            <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div className="sm:flex sm:items-start">
                <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
                  <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                    Add New Package
                  </h3>
                  
                  {error && (
                    <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                      {error}
                    </div>
                  )}

                  <div className="space-y-4">
                    <div>
                      <label htmlFor="nickname" className="block text-sm font-medium text-gray-700">
                        Nickname (Optional)
                      </label>
                      <input
                        type="text"
                        name="nickname"
                        id="nickname"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        placeholder="My Package"
                        value={formData.nickname}
                        onChange={handleInputChange}
                      />
                    </div>

                    <div>
                      <label htmlFor="tracking_number" className="block text-sm font-medium text-gray-700">
                        Tracking Number <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        name="tracking_number"
                        id="tracking_number"
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm font-mono"
                        placeholder="1Z999AA10123456784"
                        value={formData.tracking_number}
                        onChange={handleInputChange}
                      />
                    </div>

                    <div>
                      <label htmlFor="carrier" className="block text-sm font-medium text-gray-700">
                        Carrier <span className="text-red-500">*</span>
                      </label>
                      <select
                        name="carrier"
                        id="carrier"
                        required
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        value={formData.carrier}
                        onChange={handleInputChange}
                      >
                        <option value="">Select a carrier</option>
                        {carriers.map((carrier) => (
                          <option key={carrier.id || carrier.name} value={carrier.id || carrier.name.toLowerCase()}>
                            {carrier.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                disabled={loading}
                className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Adding...' : 'Add Package'}
              </button>
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AddPackageModal;
