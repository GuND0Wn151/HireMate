from app.core.config import settings


def _get_firecrawl_client():
      api_key = settings.FIRECRAWL_API_KEY
      if not api_key:
            raise RuntimeError("FIRECRAWL_API_KEY is not configured.")

      try:
            import firecrawl as fc
      except Exception as e:
            raise RuntimeError("firecrawl package not installed. Add it to requirements and install.") from e

      Client = None
      for attr_name in ["FirecrawlApp", "Firecrawl", "Client"]:
            if hasattr(fc, attr_name):
                  Client = getattr(fc, attr_name)
                  break

      if Client is None:
            try:
                  from firecrawl.firecrawl import Firecrawl as Client  # type: ignore
            except Exception as e:
                  raise RuntimeError("Unsupported firecrawl SDK version; cannot locate client class.") from e

      return Client(api_key=api_key)  # type: ignore[call-arg]


def fetch_markdown(url: str) -> str:
      """Fetch page content in markdown using available Firecrawl client methods."""
      client = _get_firecrawl_client()

      # 1) Prefer a dedicated scrape_url method if available
      if hasattr(client, "scrape_url"):
            try:
                  result = client.scrape_url(url, {"formats": ["markdown"]})  # type: ignore[arg-type]
            except TypeError:
                  result = client.scrape_url(url, formats=["markdown"])  # type: ignore[misc]
            if isinstance(result, dict):
                  md = result.get("markdown") or result.get("md")
                  if md:
                        return md

      # 2) Try generic scrape
      if hasattr(client, "scrape"):
            try:
                  result = client.scrape(url, formats=["markdown"])  # type: ignore[misc]
                  if isinstance(result, dict):
                        md = result.get("markdown") or result.get("md")
                        if md:
                              return md
            except Exception:
                  pass

      # 3) Try crawl with limit 1
      if hasattr(client, "crawl"):
            try:
                  # Some SDKs expect object-style params
                  params = {
                        "limit": 1,
                        "scrapeOptions": {"formats": ["markdown"]},
                  }
                  crawl_result = client.crawl(url, params=params)  # type: ignore[misc]
                  # Heuristics for different SDK return shapes
                  if isinstance(crawl_result, dict):
                        for key in ["results", "data", "pages"]:
                              pages = crawl_result.get(key)
                              if isinstance(pages, list) and pages:
                                    first = pages[0]
                                    if isinstance(first, dict):
                                          md = first.get("markdown") or first.get("md") or first.get("content")
                                          if md:
                                                return md
            except Exception:
                  pass

      raise RuntimeError("Unable to fetch markdown content via Firecrawl client.")


def extract_job_description_from_markdown(markdown_text: str) -> str:
      """
      Heuristically extract the job description body from noisy career-site markdown.
      Keeps title, summary, responsibilities, and qualifications. Drops nav, footers, share blocks.
      """
      if not markdown_text:
            return ""

      lines = [l.strip() for l in markdown_text.splitlines()]

      # Remove obvious navigation/footer/share and repeated menu noise
      drop_keywords = [
            "my profile", "my dashboard", "join our talent community", "work here", "life here",
            "job seeker resources", "share", "facebook", "linkedin", "twitter", "instagram", "youtube",
            "privacy policy", "equal employment", "apply clip", "play clip", "navigation", "toggle mobile menu",
            "our hiring process", "similar jobs", "back to search", "go to top", "page load link",
            "do not share or sell", "fraudulent", "copyright", "glassdoor",
      ]

      cleaned: list[str] = []
      for l in lines:
            low = l.lower()
            # Drop empty, pure link menus, or heavy nav lines
            if not l:
                  continue
            if low.startswith("[") and "](" in low and ("menu" in low or "work here" in low or "life here" in low):
                  continue
            if any(k in low for k in drop_keywords):
                  continue
            if low.startswith("# ") and ("similar jobs" in low or "our hiring process" in low):
                  continue
            # Drop lines with too many links (likely nav)
            if low.count("](") >= 2:
                  continue
            cleaned.append(l)

      # Identify title (first level-1 or level-2 heading)
      title_idx = None
      for idx, l in enumerate(cleaned):
            if l.startswith("# ") or l.startswith("## "):
                  title_idx = idx
                  break

      start = title_idx if title_idx is not None else 0

      # Find an end marker to stop before footers
      end_markers = [
            "### Additional Job Detail Information",
            "Similar Jobs",
            "Our Hiring Process",
            "Careers at ",
            "Back to Search",
      ]
      end = len(cleaned)
      for idx in range(start, len(cleaned)):
            l = cleaned[idx]
            if any(marker in l for marker in end_markers):
                  end = idx
                  break

      body = cleaned[start:end]

      # If result still too long/noisy, keep until after main sections
      # Include common section headings
      important_sections = [
            "Primary Responsibilities", "Responsibilities", "Required Qualifications", "Preferred Qualifications",
            "About the role", "Job Description", "Role", "Qualifications",
      ]
      has_any_section = any(any(s in l for s in important_sections) for l in body)
      if has_any_section:
            # keep content until the last seen important section plus following bullets/paragraphs
            last_idx = 0
            for idx, l in enumerate(body):
                  if any(s in l for s in important_sections):
                        last_idx = idx
            # extend slightly after last section
            end_slice = min(len(body), last_idx + 80)
            body = body[:end_slice]

      # Join and final trim of consecutive blank lines
      output_lines: list[str] = []
      prev_blank = False
      for l in body:
            blank = len(l.strip()) == 0
            if blank and prev_blank:
                  continue
            output_lines.append(l)
            prev_blank = blank

      return "\n".join(output_lines).strip()