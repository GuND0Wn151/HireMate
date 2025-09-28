import re
import html
import urllib.parse
import hashlib
from datetime import datetime

class Normalizer:
    @staticmethod
    def norm_text(s: str) -> str:
        """Lowercase, strip, unescape HTML, collapse spaces"""
        s = html.unescape(s or "")
        s = re.sub(r"\s+", " ", s).strip()
        return s.lower()

    @staticmethod
    def norm_url(s: str) -> str:
        """Normalize URL: lowercase host, collapse dashes, remove fragments"""
        s = (s or "").strip()
        if not s:
            return "emptyurl"
        try:
            u = urllib.parse.urlparse(s)
            scheme = u.scheme.lower()
            netloc = u.netloc.lower()

            # Clean path: collapse multiple slashes, fix --- to -
            path = re.sub(r"/{2,}", "/", u.path)
            path = re.sub(r"-{2,}", "-", path)

            # Drop trailing slash unless it's the root
            if path != "/" and path.endswith("/"):
                path = path[:-1]

            # Keep query but drop fragment
            return urllib.parse.urlunparse((scheme, netloc, path, "", u.query, ""))
        except Exception:
            return s

    @staticmethod
    def norm_date(s: str) -> str:
        """Keep YYYY-MM-DD if possible, else raw string"""
        s = (s or "").strip()
        if not s:
            return "emptydate"
        try:
            # Handles 2025-09-25 or 2025-09-25T02:50:00
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
            return dt.date().isoformat()
        except Exception:
            return s

    @staticmethod
    def norm_location(s: str) -> str:
        """Lowercase, collapse spaces, collapse dashes"""
        s = html.unescape(s or "")
        s = re.sub(r"\s+", " ", s).strip().lower()
        s = re.sub(r"-{2,}", "-", s)  # collapse --- to -
        return s or "emptylocation"


class DeNormalizer:
    @staticmethod
    def denorm_text(s: str) -> str:
        return (s or "").strip()

    @staticmethod
    def denorm_url(s: str) -> str:
        return (s or "").strip()

    @staticmethod
    def denorm_date(s: str) -> str:
        return (s or "").strip()

    @staticmethod
    def denorm_location(s: str) -> str:
        # Turn "india-haryana-gurgaon" -> "India-Haryana-Gurgaon"
        s = (s or "").strip()
        return "-".join([p.capitalize() for p in s.split("-")]) if s else ""


class HashUtils:
    @staticmethod
    def fingerprint(data: dict) -> str:
        base = "|".join([
            "jobapi",
            Normalizer.norm_text(data.get("title") or data.get("position") or data.get("role") or "emptytitle"),
            Normalizer.norm_text(data.get("company") or "emptycompany"),
            Normalizer.norm_location(data.get("location") or "emptylocation"),
            Normalizer.norm_text((data.get("description") or data.get("job_description") or "")[:200] or "emptydescription"),
            Normalizer.norm_url(data.get("apply_link") or data.get("job_url") or "emptyurl"),
            Normalizer.norm_date(data.get("date_posted") or "emptydate"),
        ])
        return hashlib.sha256(base.encode('utf-8')).hexdigest()

