import React from "react";
import { Search, Mic } from "lucide-react";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { SearchBarProps } from "../types";

export const SearchBar: React.FC<SearchBarProps> = ({
  query,
  setQuery,
  loading,
  onSearch,
}) => {
  const { isRecording, startRecording, stopRecording } = useSpeechRecognition();

  return (
    <form onSubmit={onSearch} className="w-full max-w-3xl mx-auto">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-4 py-2 pr-12 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
            placeholder="Describe the image you're looking for..."
          />
          <button
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            className={`absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full transition-all
              ${
                isRecording
                  ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
                  : "bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600"
              }`}
          >
            <Mic className="h-5 w-5" />
          </button>
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <>
              <Search className="h-5 w-5 mr-2" />
              Search
            </>
          )}
        </button>
      </div>
    </form>
  );
};
