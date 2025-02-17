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


export interface SearchResult {
  path: string;
  similarity: number;
  // model? : string
}

export interface SearchResponse {
  results: SearchResult[];
}