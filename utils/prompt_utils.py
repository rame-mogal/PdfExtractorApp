def build_prompt(text: str) -> str:
    return f"""
Extract the following fields from the text:

- Firm Name
- Address
- Date
- Turnover
- Contact Details

Text:
{text}

Respond ONLY in this JSON format:
{{
  "Firm Name": "...",
  "Address": "...",
  "Date": "...",
  "Turnover": "...",
  "Contact Details": "..."
}}
"""
