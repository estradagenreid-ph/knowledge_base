from database import (
    get_all_entities,
    get_all_relationships,
    search_entities,
    get_entity_relationships
)

from ollama_client import ask_gemma


def build_knowledge_context():

    entities = get_all_entities()
    relationships = get_all_relationships()

    context = "ENTITIES:\n"

    for entity in entities:
        context += (
            f"- {entity['name']} "
            f"({entity['entity_type']}): "
            f"{entity['description']}\n"
        )

    context += "\nRELATIONSHIPS:\n"

    for relationship in relationships:
        context += (
            f"- {relationship['source']} "
            f"--{relationship['relationship']}--> "
            f"{relationship['target']} "
            f"[Source: {relationship['source_document']}]\n"
        )

    return context


def answer_question(question):

    context = build_knowledge_context()

    prompt = f"""
You are an AI knowledge-base assistant.

Answer the user's question using ONLY the
knowledge provided below.

If the knowledge base does not contain enough
information, say so clearly.

Do not invent facts.

KNOWLEDGE BASE:

{context}

USER QUESTION:

{question}

Provide a clear answer.

When possible, mention the relationships
that support your answer.
"""

    return ask_gemma(prompt)