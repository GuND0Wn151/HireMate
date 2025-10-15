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


