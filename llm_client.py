import json
import os
from google import genai

MODEL = "gemini-3.6-flash"


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Please enter your Gemini API key in the Colab notebook."
        )

    return genai.Client(api_key=api_key)


def generate_response(prompt):
    client = get_client()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "temperature": 0.3
        }
    )

    return response.text


def extract_knowledge(text):
    prompt = f"""
You are a knowledge extraction system.

Analyze the following text and extract important entities
and relationships.

Return ONLY valid JSON.

Use this exact structure:

{{
    "entities": [
        {{
            "name": "Entity name",
            "type": "Person/Company/Product/Technology/Place/Event/Concept/Other",
            "description": "Short description"
        }}
    ],
    "relationships": [
        {{
            "source": "Entity name",
            "relationship": "relationship type",
            "target": "Entity name"
        }}
    ]
}}

Rules:

1. Only extract information supported by the text.
2. Do not invent relationships.
3. Use the exact same entity names in relationships.
4. Keep relationship names short.
5. Return valid JSON only.

TEXT:

{text}
"""

    result = generate_response(prompt)

    result = result.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)