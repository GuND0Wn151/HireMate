import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()


def get_supabase_client() -> Client:
	url = os.getenv("SUPABASE_URL")
	key = os.getenv("SUPABASE_ANON_KEY")
	if not url or not key:
		raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment")
	return create_client(url, key)



def test_supabase_connection(table: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
	"""Fetch up to `limit` items from the given table to verify connectivity.

	If `table` is not provided, uses SUPABASE_TEST_TABLE from the environment.
	Returns a diagnostics dictionary like:
	{"ok": bool, "status_code": int | None, "count": int | None, "data": list | None, "error": str | None}
	"""
	print('test_connection')
	client = get_supabase_client()
	table_name = 'test_table' or os.getenv("SUPABASE_TEST_TABLE")
	if not table_name:
		return {"ok": False,  "error": "Provide table name or set SUPABASE_TEST_TABLE"}
	try:
		response = client.table(table_name).select("*").limit(limit).execute()
		status_code = getattr(response, "status_code", None)
		data = getattr(response, "data", None)
		row_count = len(data) if isinstance(data, list) else None
		return {"ok": True, "status_code": status_code, "count": row_count, "data": data, "error": None}
	except Exception as exc:
		return {"ok": False, "status_code": None, "count": None, "data": None, "error": str(exc)}

