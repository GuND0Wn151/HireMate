class Consts:
    @staticmethod
    def get_extract_job(markdown_content: str):
        return f"""
            Extract ONLY the job description from the following job posting and format it as bullet points.

            EXTRACT ONLY:
            - Job title and role
            - Key responsibilities and duties
            - Required qualifications and experience
            - Required skills and technologies
            - Preferred qualifications (if any)

            IGNORE COMPLETELY:
            - Browser compatibility messages
            - Company descriptions and boilerplate
            - Benefits and perks information
            - Application instructions
            - Location details beyond what's essential
            - Navigation elements or UI text
            - Any text starting with "Sorry" or browser-related content
            - Google Maps or cookie-related textgemini-2.5-flash-lite

            FORMAT:   
            - Use bullet point format (• or -)
            - Keep each bullet point concise but clear
            - Focus on job-specific information only

            Job posting content:
            {markdown_content}

            Return ONLY the clean job description in bullet points, nothing else.
            """
    
    @staticmethod
    def extract_job_v2(markdown_content: str) -> str:
        return f"""
        You are a precise data extraction assistant.

        Your task is to extract and organize raw job posting data from the following markdown content.  
        Do NOT summarize, rephrase, or alter the wording.  
        Preserve all original phrasing exactly as it appears in the text.

        Your goal is to extract the text into clearly structured categories without changing or losing any information.

        ---

        ### OUTPUT FORMAT (strict JSON)
        Return ONLY the JSON object in the following format:

        {{
          "job_title_and_role": [list of bullet points or full lines],
          "about_company": [list of bullet points or full lines],
          "key_responsibilities": [list of bullet points or full lines],
          "requirements": [list of bullet points or full lines],
          "skills_and_technologies": [list of bullet points or full lines],
          "preferred_qualifications": [list of bullet points or full lines],
          "benefits_or_perks": [list of bullet points or full lines],
          "job_metadata": {{
            "company_name": "",
            "location": "",
            "employment_type": "",
            "salary_range": ""
          }}
        }}

        ---

        ### EXTRACTION INSTRUCTIONS

        - DO NOT SUMMARIZE OR PARAPHRASE.
          - Copy the text exactly as found under each section.
          - Preserve wording, formatting, and sequence where possible.
        - Group content under the correct sections based on headings such as:
          - "Job Description", "About Company", "Key Responsibilities", "Requirements", "Skills", "Benefits", "Perks", "Qualifications"
        - If multiple sections overlap, include all relevant lines in their respective fields.
        - If a section does not exist, omit it.
        - Include multiple bullet points if the content is in list form.
        - If the same sentence contains multiple pieces of data (e.g., responsibilities), keep it as a single bullet.
        - Extract only job-related content. Ignore:
          - Navigation or browser UI
          - Cookie or GDPR text
          - Apply buttons, email addresses, or submission info
          - Company legal disclaimers or unrelated text
        - Keep bullets or lines in their original order.

        ---

        ### INPUT:
        {markdown_content}

        ### OUTPUT:
        Return ONLY the structured JSON object.
        No explanations, no extra commentary, no markdown formatting.
        """
