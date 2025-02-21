import { createClient } from '@supabase/supabase-js';
import { mockAuth } from './mockAuth';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

const isSupabaseConfigured = supabaseUrl && supabaseAnonKey;

const supabaseClient = isSupabaseConfigured
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export const supabase = supabaseClient
  ? supabaseClient
  : { auth: mockAuth };