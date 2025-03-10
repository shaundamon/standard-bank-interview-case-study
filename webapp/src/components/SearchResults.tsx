import React from "react";
import { motion } from "framer-motion";
import { API_URL } from "../lib/constants";
import { SearchResponse } from "../types";

export const SearchResults: React.FC<SearchResponse> = ({
  results,
  loading,
}) => {
  if (loading) {
    return <div className="mt-8 text-center">Loading...</div>;
  }

  if (!results.length) {
    return (
      <div className="mt-8">
        {/* <div className="text-center text-gray-600 dark:text-gray-400 mb-6">
          No images available. Start by searching for something above.
        </div> */}
        <motion.div 
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 opacity-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.5 }}
        >
          {[...Array(5)].map((_, index) => (
            <motion.div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="w-full h-48 bg-gray-200 dark:bg-gray-700" />
              <div className="p-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
                <div className="mt-2 h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {results.map((result, index) => (
        <motion.div
          key={index}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <img
            src={`${API_URL}/api/v1/images/${result.path.split("\\").pop()}`}
            alt={`Search result ${index + 1}`}
            className="w-full h-48 object-cover"
            onError={(e) => {
              e.currentTarget.src =
                "https://via.placeholder.com/400x300?text=Image+Not+Available";
            }}
          />
          <div className="p-4">
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              {result.path.split("\\").pop()}
            </p>
            <p className="mt-1 text-xs text-indigo-600 dark:text-indigo-400">
              Similarity: {(result.similarity * 100).toFixed(1)}%
            </p>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
};
