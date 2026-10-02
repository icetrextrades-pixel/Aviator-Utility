/*
# Create round_history table for Aviator prediction data

## Overview
Creates a new table to store actual aviator round results per casino, per user.
This replaces the old SQLite local database with a cloud-backed Supabase table.
Each user's round data is isolated via Row Level Security (owner-scoped).

## New Tables
- `round_history`
  - `id` (uuid, primary key, auto-generated)
  - `user_id` (uuid, not null, defaults to the authenticated user, references auth.users with cascade delete)
  - `casino` (text, not null — e.g. "AFRICABET", "1XBET", "PREMIER BET")
  - `multiplier` (real, not null — the crash multiplier for that round, e.g. 1.50)
  - `created_at` (timestamptz, defaults to now)

## Security
- Row Level Security ENABLED on `round_history`.
- Four separate policies (SELECT, INSERT, UPDATE, DELETE), all scoped to `authenticated` role.
- Each policy enforces `auth.uid() = user_id` so users can only access their own round data.
- The `user_id` column has `DEFAULT auth.uid()` so frontend inserts that omit `user_id` still satisfy the INSERT WITH CHECK.

## Index
- Index on `(user_id, casino, created_at DESC)` for fast history fetches filtered by casino.
*/

CREATE TABLE IF NOT EXISTS round_history (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
    casino text NOT NULL,
    multiplier real NOT NULL,
    created_at timestamptz DEFAULT now()
);

ALTER TABLE round_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_rounds" ON round_history;
CREATE POLICY "select_own_rounds"
ON round_history FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_rounds" ON round_history;
CREATE POLICY "insert_own_rounds"
ON round_history FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_rounds" ON round_history;
CREATE POLICY "update_own_rounds"
ON round_history FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_rounds" ON round_history;
CREATE POLICY "delete_own_rounds"
ON round_history FOR DELETE
TO authenticated
USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_round_history_user_casino_created
ON round_history (user_id, casino, created_at DESC);
