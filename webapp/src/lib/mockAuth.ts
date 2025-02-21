import { User } from '../types';

class MockAuthService {
    private user: User | null = null;

    async signInWithPassword({ email, password }: { email: string; password: string }) {
        // For demo purposes, accept any password
        this.user = {
            id: crypto.randomUUID(),
            email,
            created_at: new Date().toISOString(),
        };
        return { data: { user: this.user }, error: null };
    }

    async signUp({ email, password }: { email: string; password: string }) {
        this.user = {
            id: crypto.randomUUID(),
            email,
            created_at: new Date().toISOString(),
        };
        return { data: { user: this.user }, error: null };
    }

    async signOut() {
        this.user = null;
        return { error: null };
    }

    getUser() {
        return { data: { user: this.user }, error: null };
    }
}

export const mockAuth = new MockAuthService();