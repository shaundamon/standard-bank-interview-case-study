import { API_URL } from './constants';
import { SearchResponse } from '../types';

export const imageApi = {
    search: async (query: string): Promise<SearchResponse> => {
        try {
            const response = await fetch(`${API_URL}/api/v1/search/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error('Search request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Error during image search:', error);
            throw error;
        }
    },
};