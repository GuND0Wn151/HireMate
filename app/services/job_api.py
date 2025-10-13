import hashlib, html, json, re, time, urllib.parse

class JobAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.com/v1/jobs"

    def search_jobs(self, query: str, location: str = "", page: int = 1, per_page: int = 10) -> dict:
        """Search for jobs using the Firecrawl API."""
        params = {
            "query": query,
            "location": location,
            "page": page,
            "per_page": per_page,
            "api_key": self.api_key
        }
        url = f"{self.base_url}/search?{urllib.parse.urlencode(params)}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    def _post_process_job_description(raw_text: str) -> str:
        """
        Post-process the AI response to ensure we get exactly 5-6 concise bullet points
        """
        # Split by bullet points or newlines
        lines = raw_text.split('\n')
    
        # Filter and clean lines
        bullet_points = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove common bullet point markers and clean
            line = line.lstrip('•-*◦▪▫‣⁃')
            line = line.strip()
        
            if line and len(line) > 10:  # Only include substantial lines
                # Limit line length to 2 lines max
                if len(line) > 120:
                    line = line[:117] + "..."
                bullet_points.append(f"• {line}")
    
        # Limit to exactly 5-6 points
        if len(bullet_points) > 6:
            bullet_points = bullet_points[:6]
        elif len(bullet_points) < 3:
            # If we have too few, try to split longer points
            if bullet_points:
                # Take the first point and split it
                first_point = bullet_points[0].replace("• ", "")
                if len(first_point) > 80:
                    mid = len(first_point) // 2
                    # Find a good break point
                    for i in range(mid-20, mid+20):
                        if i < len(first_point) and first_point[i] in '.,;':
                            bullet_points = [
                            f"• {first_point[:i+1]}",
                            f"• {first_point[i+1:].strip()}"
                        ] + bullet_points[1:]
                        break
    
        return '\n'.join(bullet_points[:6])  # Ensure max 6 points