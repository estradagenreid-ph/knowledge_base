from pathlib import Path

from pypdf import PdfReader
from docx import Document

from database import (
    add_document,
    add_entity,
    add_relationship
)

from ollama_client import extract_knowledge


def extract_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx(file_path):
    document = Document(file_path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )


def extract_txt(file_path):
    return Path(file_path).read_text(
        encoding="utf-8"
    )


def extract_document(file_path):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    if extension == ".txt":
        return extract_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def ingest_document(file_path, filename):
    text = extract_document(file_path)

    add_document(filename, text)

    knowledge = extract_knowledge(text)

    entity_ids = {}

    for entity in knowledge["entities"]:

        entity_id = add_entity(
            entity["name"],
            entity["type"],
            entity.get("description", "")
        )

        entity_ids[entity["name"]] = entity_id

    for relationship in knowledge["relationships"]:

        source = relationship["source"]
        target = relationship["target"]

        if source not in entity_ids:
            continue

        if target not in entity_ids:
            continue

        add_relationship(
            entity_ids[source],
            relationship["relationship"],
            entity_ids[target],
            filename
        )

    return knowledge