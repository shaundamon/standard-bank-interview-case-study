import { createClient } from '@supabase/supabase-js';
import { User } from '../types';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

class MockAuthService {
  private user: User | null = null;

  async signInWithPassword({ email }: { email: string }) {
    this.user = {
      id: '1',
      email,
      created_at: new Date().toISOString(),
    };
    return { data: { user: this.user }, error: null };
  }

  async signUp({ email }: { email: string }) {
    this.user = {
      id: '1',
      email,
      created_at: new Date().toISOString(),
    };
    return { data: { user: this.user }, error: null };
  }

  async updateUser() {
    return { data: { user: this.user }, error: null };
  }
}

const isSupabaseConfigured = supabaseUrl && supabaseAnonKey;

const supabaseClient = isSupabaseConfigured ? createClient(supabaseUrl, supabaseAnonKey) : null;
const mockAuthService = new MockAuthService();

export const supabase = supabaseClient || { auth: mockAuthService } as any;