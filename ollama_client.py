import json
import ollama

MODEL = "gemma4:e2b-q4"


def ask_gemma(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.3
        }
    )

    return response["message"]["content"]


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

    result = ask_gemma(prompt)

    # Remove accidental markdown fences
    result = result.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)