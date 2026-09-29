# Local AI Knowledge Base

A document knowledge base with a Streamlit interface. Add PDF, DOCX, or TXT files, extract entities and relationships with Gemma, and ask questions about the knowledge stored in SQLite.

**Instructions:**

1. Install Python and [Ollama](https://ollama.com/download), then clone the repository:

```sh
git clone https://github.com/estradagenreid-ph/knowledge_base.git
cd knowledge_base
python -m venv .venv
```

2. Install the local app's dependencies.

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```sh
./.venv/bin/python -m pip install -r requirements.txt
```

3. Open the Ollama desktop app, or run `ollama serve` in another terminal if the service is not already running. Download the model configured in `ollama_client.py`:

```sh
ollama pull gemma4:e2b-q4
ollama list
```

If that tag is unavailable, download a compatible model and change `MODEL` in `ollama_client.py` to match. The model must be able to return the JSON structure requested by the extraction prompt.

4. Run the app from the repository root.

Windows:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

macOS/Linux:

```sh
./.venv/bin/python -m streamlit run app.py
```

5. Open the local address printed by Streamlit. Choose **Ingest**, upload a document, and click **Build Knowledge**. Use **Explore** to inspect the extracted entities and relationships, then **Inquire** to ask questions.

The app creates `data/knowledge.db` and its tables automatically. Text extraction supports text-based PDFs, DOCX paragraphs, and UTF-8 TXT files; scanned PDFs need OCR before ingestion.

**FILES:**

| File | What it does |
| --- | --- |
| `app.py` | Streamlit interface for ingestion, questions, search, and exploration. |
| `database.py` | Creates and queries the SQLite tables for documents, entities, and relationships. |
| `ingest.py` | Extracts document text, calls the Ollama extraction client, and stores the results. |
| `inquire.py` | Builds context from all stored entities and relationships, then asks Gemma a question. |
| `ollama_client.py` | Active local model client for answers and JSON knowledge extraction. |
| `llm_client.py` | Separate Google Gemini API client. The current app does not import it. |
| `requirements.txt` | Dependencies for the current Ollama app. |
| `requirements-genai.txt` | Dependencies for the separate Gemini client; this does not switch the app's backend. |
| `data/knowledge.db` | Local database containing stored document text and extracted knowledge. |

**OLLAMA & OPTIONAL GEMINI CLIENT:**

Ollama runs the configured Gemma model locally. Its Python package connects to that service, so Ollama itself must be running. No cloud key is required by the current app. Model downloads need internet access. Ollama is [open-source software](https://github.com/ollama/ollama/blob/main/LICENSE); model terms are separate.

`llm_client.py` uses Google's `google-genai` SDK, reads `GEMINI_API_KEY` from the environment, and has `gemini-3.6-flash` configured. To use that module separately, install `requirements-genai.txt` and set the environment variable in your terminal. Verify that the configured model is available to your Google account. It needs internet access, and API usage is subject to Google's terms and pricing. Switching the app to Gemini requires code changes in ingestion and inquiry; installing the extra requirements alone is not enough. The code does not automatically load a `.env` file.

**CURRENT LIMITS:**

Inquiry sends the full entity/relationship context rather than performing vector retrieval. Large knowledge bases can exceed the model's context capacity. Extraction depends on valid model-generated JSON, and repeated ingestion can add duplicate relationships. The uploader writes temporary copies of documents; the current code does not delete them after processing.

**TOOLS & ACKNOWLEDGMENTS:**

Gemini, ChatGPT, and Codex helped me develop this project. Ollama and Gemma provide its local AI processing; the separate client uses Google's Gemini API. Codex also helped with documentation and cleanup.

The app uses [Streamlit](https://docs.streamlit.io/), [Ollama](https://docs.ollama.com/), [pypdf](https://pypdf.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/), and Python's built-in SQLite module. The dependency lists also include pandas.

**LOCAL DATA:**

`.gitignore` covers new local database files, SQLite sidecar files, Python caches, environments, and credentials. The existing `data/knowledge.db` and committed Python caches are intentionally retained and remain tracked, so Git can still commit changes to them. The database stores document text, so review it as carefully as the source documents. Ignore rules do not remove tracked files or erase earlier commits.
