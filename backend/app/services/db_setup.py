import os
from typing import Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

def get_database_url() -> str:
	url =os.getenv("DATABASE_URL")
	if not url:
		raise RuntimeError("SUPABASE_DB_URL or DATABASE_URL must be set for direct SQL access")
	return url


def ensure_users_table() -> Dict[str, Any]:
	"""Create the users table if it doesn't exist and ensure constraints.

	Returns a dict with basic diagnostics.
	"""
	db_url = get_database_url()
	sql = (
		"""
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
	)
	try:
		with psycopg2.connect(db_url, cursor_factory=RealDictCursor) as conn:
			conn.autocommit = True
			with conn.cursor() as cur:
				cur.execute(sql)
		return {"ok": True, "error": None}
	except Exception as exc:
		return {"ok": False, "error": str(exc)}

