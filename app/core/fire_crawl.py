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
    
    try:
        result = client.scrape_url(url, {"formats": ["markdown"]})  # type: ignore[arg-type]
    except TypeError:
        result = client.scrape_url(url, formats=["markdown"])  # type: ignore[misc]

    if isinstance(result, dict):
        md = result.get("markdown") or result.get("md")
        if md:
            return md

    raise RuntimeError("Unable to fetch markdown content via Firecrawl client.")



