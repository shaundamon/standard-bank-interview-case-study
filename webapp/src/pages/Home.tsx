import React, { useState } from "react";
import { Layout } from "../components/Layout";
import { SearchBar } from "../components/SearchBar";
import { SearchResults } from "../components/SearchResults";
import { LoadingAnimation } from "../components/LoadingAnimation";
import { imageApi } from "../lib/api";
import { SearchResult } from "../types";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";

export const Home: React.FC = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const { speak } = useSpeechSynthesis();

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


  return (
    <Layout title="Image Retrieval">
      <div className="max-w-7xl mx-auto mb-2">
        <SearchBar
          query={query}
          setQuery={setQuery}
          loading={loading}
          onSearch={handleSearch}
        />
        {loading ? (
          <LoadingAnimation />
        ) : (
          <SearchResults results={results} loading={loading} />
        )}
      </div>
    </Layout>
  );
};
