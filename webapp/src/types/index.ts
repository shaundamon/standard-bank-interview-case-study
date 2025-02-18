export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface ImageResult {
  id: string;
  path: string;
  similarity: number;  
  description: string;
}

export interface SearchBarProps {
  query: string;
  setQuery: (query: string) => void;
  loading: boolean;
  onSearch: (e: React.FormEvent) => void;
}

export interface SearchResult {
  path: string;
  similarity: number;
  // model? : string
}

export interface SearchResponse {
  results: SearchResult[];
  loading: boolean;

}

export interface LayoutProps {
  children: React.ReactNode;
  title: string;
}

export interface SpeechInputProps {
  onTranscript: (text: string) => void;
}