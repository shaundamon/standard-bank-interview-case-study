import React, { useState, useEffect } from "react";
import { Download, RefreshCw } from "lucide-react";
import { datasetApi } from "../lib/api";

export const DatasetManager: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<{
    exists: boolean;
    image_count: number;
  } | null>(null);

const checkStatus = async () => {
  try {
    const status = await datasetApi.getDatasetStatus();
    setStatus(status);

    if (!status.exists) {
      handleDownload();
    }
  } catch (error) {
    console.error("Error checking dataset status:", error);
  }
};

  const handleDownload = async () => {
    setLoading(true);
    try {
      await datasetApi.downloadDataset();
      await checkStatus();
    } catch (error) {
      console.error("Error downloading dataset:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Dataset Management
      </h3>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600 dark:text-gray-300">
            Status: {status?.exists ? "Downloaded" : "Not Downloaded"}
          </span>
          <button
            onClick={checkStatus}
            className="p-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            aria-label="Refresh status"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>

        {status?.exists && (
          <div className="text-sm text-gray-600 dark:text-gray-300">
            Images: {status.image_count}
          </div>
        )}

        <button
          onClick={handleDownload}
          disabled={loading}
          className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
          ) : (
            <>
              <Download className="h-5 w-5 mr-2" />
              {status?.exists ? "Refresh Dataset" : "Download Dataset"}
            </>
          )}
        </button>
      </div>
    </div>
  );
};
