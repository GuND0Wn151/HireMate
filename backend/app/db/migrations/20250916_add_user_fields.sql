-- Migration: Create/extend users table with requested fields
-- Fields: id (primary key), email (unique), phno, created_at, name, company, role

-- Create table if not exists (safe if it already exists)
create table if not exists users (
	id uuid primary key default gen_random_uuid(),
	email text unique not null,
	name text,
	phno text,
	company text,
	role text,
	created_at timestamptz not null default now()
);

-- Ensure required columns exist; safe to run multiple times for existing tables
alter table if exists users
	add column if not exists email text,
	add column if not exists name text,
	add column if not exists phno text,
	add column if not exists company text,
	add column if not exists role text,
	add column if not exists created_at timestamptz not null default now();

-- Ensure email is unique (if not already). Schema may already define it.
do $$ begin
	if not exists (
		select 1 from pg_constraint c
		join pg_class t on t.oid = c.conrelid
		where c.contype = 'u'
		and c.conname = 'users_email_key'
		and t.relname = 'users'
	) then
		alter table users add constraint users_email_key unique (email);
	end if;
end $$;

