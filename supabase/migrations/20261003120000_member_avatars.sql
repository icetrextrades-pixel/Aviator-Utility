-- Private member profile pictures. Apply once in Supabase SQL Editor.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('member-avatars', 'member-avatars', false, 2097152, array['image/png', 'image/jpeg', 'image/webp'])
on conflict (id) do update
set public = false,
    file_size_limit = 2097152,
    allowed_mime_types = array['image/png', 'image/jpeg', 'image/webp'];

drop policy if exists "Members can read own avatar files" on storage.objects;
create policy "Members can read own avatar files"
on storage.objects for select
to authenticated
using (
  bucket_id = 'member-avatars'
  and (storage.foldername(name))[1] = auth.uid()::text
);

drop policy if exists "Members can upload own avatar files" on storage.objects;
create policy "Members can upload own avatar files"
on storage.objects for insert
to authenticated
with check (
  bucket_id = 'member-avatars'
  and (storage.foldername(name))[1] = auth.uid()::text
);

drop policy if exists "Members can update own avatar files" on storage.objects;
create policy "Members can update own avatar files"
on storage.objects for update
to authenticated
using (
  bucket_id = 'member-avatars'
  and (storage.foldername(name))[1] = auth.uid()::text
)
with check (
  bucket_id = 'member-avatars'
  and (storage.foldername(name))[1] = auth.uid()::text
);

drop policy if exists "Members can delete own avatar files" on storage.objects;
create policy "Members can delete own avatar files"
on storage.objects for delete
to authenticated
using (
  bucket_id = 'member-avatars'
  and (storage.foldername(name))[1] = auth.uid()::text
);
