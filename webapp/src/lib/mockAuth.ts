import { User } from '../types';

class MockAuthService {
    private storageKey = 'mock_auth_user';

    async signUp(email: string) {
        const user: User = {
            id: crypto.randomUUID(),
            email,
            created_at: new Date().toISOString(),
        };
        localStorage.setItem(this.storageKey, JSON.stringify(user));
        return { error: null };
    }

    async signInWithPassword(email: string) {
        const user: User = {
            id: crypto.randomUUID(),
            email,
            created_at: new Date().toISOString(),
        };
        localStorage.setItem(this.storageKey, JSON.stringify(user));
        return { data: { user }, error: null };
    }

    async signOut() {
        localStorage.removeItem(this.storageKey);
        return { error: null };
    }

    getUser() {
        const userData = localStorage.getItem(this.storageKey);
        return userData ? JSON.parse(userData) : null;
    }
}

export const mockAuth = new MockAuthService();