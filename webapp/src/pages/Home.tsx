import React, { useState, useEffect } from 'react';
import { Search, ImageIcon } from 'lucide-react';
import { ThemeToggle } from '../components/ThemeToggle';
import { supabase } from '../lib/supabase';
import { useAuthStore } from '../store/authStore';
import { Sidebar } from '../components/Sidebar';
import { LoadingAnimation } from '../components/LoadingAnimation';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { motion } from 'framer-motion';
import { API_URL } from "../lib/constants";
import { useSettingsStore } from '../store/settingsStore';
import { imageApi } from "../lib/api";
import { SearchResult } from '../types';

export const Home: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const user = useAuthStore((state) => state.user);
  const { speak } = useSpeechSynthesis();
  const isSidebarOpen = useSettingsStore((state) => state.isSidebarOpen);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    speak(`Searching for images matching ${query}`);

    try {
      const { results: searchResults } = await imageApi.search(query);
      setResults(searchResults);
      speak(`Found ${searchResults.length} images matching your search`);
    } catch (err) {
      console.error("Error searching images:", err);
      speak("An error occurred while searching for images");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchRecentImages = async () => {
      try {
        const { data, error } = await supabase
          .from('images')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(6);

        if (error) throw error;

        setResults(data || []);
      } catch (err) {
        console.error('Error fetching recent images:', err);
      }
    };

    fetchRecentImages();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      <Sidebar />

      <div
        className={`flex-1 transition-all duration-300 ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
      >
        <header className="bg-white dark:bg-gray-800 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <ImageIcon className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                Image Retrieval
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-300">
                {user?.email}
              </span>
              <ThemeToggle />
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <form onSubmit={handleSearch} className="max-w-3xl mx-auto">
            <div className="flex gap-4">
              <div className="flex-1">
                <label htmlFor="search" className="sr-only">
                  Search images
                </label>
                <input
                  type="text"
                  id="search"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-900 dark:text-white focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Describe the image you're looking for..."
                  aria-label="Search query"
                />
              </div>
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Search for images"
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                ) : (
                  <>
                    <Search className="h-5 w-5 mr-2" />
                    Search
                  </>
                )}
              </button>
            </div>
          </form>

          {loading ? (
            <LoadingAnimation />
          ) : results.length > 0 ? (
            <motion.div
              className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  role="img"
                  aria-label={`Image ${index + 1}`}
                  tabIndex={0}
                >
                  <img
                    src={`${API_URL}/api/v1/images/${result.path
                      .split("\\")
                      .pop()}`}
                    alt={`Search result ${index + 1}`}
                    className="w-full h-48 object-cover"
                    onError={(e) => {
                      e.currentTarget.src =
                        "https://via.placeholder.com/400x300?text=Image+Not+Available";
                    }}
                  />
                  <div className="p-4">
                    <p className="text-sm font-medium text-gray-900 dark:text-white mb-1">
                      {result.path.split("\\").pop()}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {result.path}
                    </p>
                    <p className="mt-2 text-xs text-indigo-600 dark:text-indigo-400">
                      Similarity: {(result.similarity * 100).toFixed(1)}%
                    </p>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <div className="mt-8 text-center text-gray-600 dark:text-gray-400">
              No images found. Try a different search query.
            </div>
          )}
        </main>
      </div>
    </div>
  );
};