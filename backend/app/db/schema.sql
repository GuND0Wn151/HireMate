-- PostgreSQL schema for JobPrep AI - Phase 1

create table if not exists users (
	id uuid primary key default gen_random_uuid(),
	name text not null,
	email text unique not null,
	password_hash text,
	oauth_id text,
	created_at timestamptz not null default now()
);

create table if not exists resumes (
	id uuid primary key default gen_random_uuid(),
	user_id uuid not null references users(id) on delete cascade,
	file_url text,
	text_content text,
	ats_score numeric,
	created_at timestamptz not null default now()
);

create table if not exists job_descriptions (
	id uuid primary key default gen_random_uuid(),
	user_id uuid not null references users(id) on delete cascade,
	text_content text not null,
	extracted_skills jsonb default '[]'::jsonb,
	created_at timestamptz not null default now()
);

create type application_status as enum ('applied','interviewed','rejected','offer');

do $$ begin
	if not exists (select 1 from pg_type where typname = 'application_status') then
		create type application_status as enum ('applied','interviewed','rejected','offer');
	end if;
end $$;

create table if not exists applications (
	id uuid primary key default gen_random_uuid(),
	user_id uuid not null references users(id) on delete cascade,
	company text not null,
	role text not null,
	status application_status not null default 'applied',
	applied_date date not null,
	updated_at timestamptz not null default now()
);

create table if not exists practice_problems (
	id serial primary key,
	title text not null,
	topic text not null,
	difficulty text not null check (difficulty in ('easy','med','hard')),
	description text not null,
	solution text
);

create table if not exists practice_history (
	id uuid primary key default gen_random_uuid(),
	user_id uuid not null references users(id) on delete cascade,
	problem_id int not null references practice_problems(id) on delete cascade,
	status text not null check (status in ('attempted','correct','incorrect')),
	attempted_at timestamptz not null default now()
);


