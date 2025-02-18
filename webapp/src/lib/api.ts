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

export const datasetApi = {
    downloadDataset: async (): Promise<EventSource> => {
        try {
            const eventSource = new EventSource(`${API_URL}/api/v1/dataset/stream/`);
            eventSource.onerror = (error) => {
                console.error('EventSource failed:', error);
                eventSource.close();
                throw new Error('Failed to establish connection');
            };
            return eventSource;
        } catch (error) {
            console.error('Error creating EventSource:', error);
            throw error;
        }
    },

    getDatasetStatus: async (): Promise<{ exists: boolean; image_count: number; data_path: string }> => {
        try {
            const response = await fetch(`${API_URL}/api/v1/dataset/`);
            if (!response.ok) {
                throw new Error('Failed to get dataset status');
            }
            return await response.json();
        } catch (error) {
            console.error('Error checking dataset status:', error);
            throw error;
        }
    },
};
