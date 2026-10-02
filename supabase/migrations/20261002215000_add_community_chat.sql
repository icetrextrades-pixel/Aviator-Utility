-- Shared chat for authenticated predictor members.
CREATE TABLE IF NOT EXISTS public.community_chat_messages (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE CASCADE,
    username text NOT NULL CHECK (char_length(btrim(username)) BETWEEN 1 AND 40),
    message text NOT NULL CHECK (char_length(btrim(message)) BETWEEN 1 AND 1000),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS community_chat_messages_created_at_idx
    ON public.community_chat_messages (created_at DESC);

ALTER TABLE public.community_chat_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated members can read community chat"
    ON public.community_chat_messages;
CREATE POLICY "Authenticated members can read community chat"
    ON public.community_chat_messages
    FOR SELECT TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Members can post as themselves"
    ON public.community_chat_messages;
CREATE POLICY "Members can post as themselves"
    ON public.community_chat_messages
    FOR INSERT TO authenticated
    WITH CHECK (
        auth.uid() = user_id
        AND lower(username) = lower(coalesce(
            auth.jwt() -> 'user_metadata' ->> 'username',
            split_part(coalesce(auth.jwt() ->> 'email', 'member'), '@', 1)
        ))
        AND char_length(btrim(message)) BETWEEN 1 AND 1000
    );

GRANT SELECT, INSERT ON public.community_chat_messages TO authenticated;
