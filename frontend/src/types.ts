export interface Song {
  id: number;
  title: string;
  category: string;
  language: string;
  key_signature: string;
  lyrics: string;
  misa_id: string;
  ord_part: string;
  has_score: boolean;
  score_url: string | null;
  uploaded_by: number | null;
  uploaded_by_name: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'superadmin';
}

export type FilterType =
  | { type: 'all' }
  | { type: 'proper'; category: string }
  | { type: 'misa'; misa_id: string }
  | { type: 'misa_part'; misa_id: string; category: string };
