/*
# Create signal_history table for prediction accuracy tracking

## Overview
Stores each generated signal so it can later be matched against the actual
round result. When a user logs a real round, the nearest unresolved prediction
for that casino is marked as a "hit" (prediction <= actual, meaning the aviator
flew at least as long as predicted) or a "miss" (the plane crashed before the
target). This produces a real, provable accuracy percentage per strategy.

## New Tables
- `signal_history`
  - `id` (uuid, primary key, auto-generated)
  - `user_id` (uuid, not null, defaults to the authenticated user, references auth.users with cascade delete)
  - `casino` (text, not null)
  - `strategy` (text, not null — "PREDICTOR", "MR CRUSHER", or "AVI10")
  - `predicted_multiplier` (real, not null — the target the signal generated)
  - `actual_multiplier` (real, nullable — filled in when a round result is logged)
  - `hit` (boolean, nullable — true if predicted <= actual, false if predicted > actual)
  - `created_at` (timestamptz, defaults to now)
  - `resolved_at` (timestamptz, nullable — when the actual result was matched)

## Security
- Row Level Security ENABLED on `signal_history`.
- Four separate policies (SELECT, INSERT, UPDATE, DELETE), all scoped to `authenticated`.
- Each policy enforces `auth.uid() = user_id` — users can only track their own predictions.
- The `user_id` column defaults to `auth.uid()` so inserts that omit it succeed.

## Index
- Index on `(user_id, casino, resolved_at, created_at DESC)` for fast resolution queries
  (find oldest unresolved prediction for a casino) and fast accuracy aggregation.
*/

CREATE TABLE IF NOT EXISTS signal_history (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
    casino text NOT NULL,
    strategy text NOT NULL,
    predicted_multiplier real NOT NULL,
    actual_multiplier real,
    hit boolean,
    created_at timestamptz DEFAULT now(),
    resolved_at timestamptz
);

ALTER TABLE signal_history ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "select_own_signals" ON signal_history;
CREATE POLICY "select_own_signals"
ON signal_history FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "insert_own_signals" ON signal_history;
CREATE POLICY "insert_own_signals"
ON signal_history FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "update_own_signals" ON signal_history;
CREATE POLICY "update_own_signals"
ON signal_history FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "delete_own_signals" ON signal_history;
CREATE POLICY "delete_own_signals"
ON signal_history FOR DELETE
TO authenticated
USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_signal_history_user_casino_unresolved
ON signal_history (user_id, casino, resolved_at, created_at DESC);
