USERS_TABLE_SQL = """
create extension if not exists pgcrypto;
create table if not exists users (
	id uuid primary key default gen_random_uuid(),
	email text not null,
	name text,
	phno text,
	company text,
	role text,
	created_at timestamptz not null default now()
);

-- add columns defensively (idempotent)
alter table if exists users
	add column if not exists id uuid primary key default gen_random_uuid(),
	add column if not exists email text not null,
	add column if not exists name text,
	add column if not exists phno text,
	add column if not exists company text,
	add column if not exists role text,
	add column if not exists created_at timestamptz not null default now();

-- ensure unique constraint on email
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
"""
