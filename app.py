import tempfile
from pathlib import Path

import streamlit as st

from database import (
    initialize_database,
    get_all_entities,
    get_all_relationships,
    search_entities,
    get_entity_relationships
)

from ingest import ingest_document
from inquire import answer_question


# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

initialize_database()


st.set_page_config(
    page_title="Local AI Knowledge Base",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧠 Local AI Knowledge Base")

st.caption(
    "Powered locally by Ollama + Gemma 4 E2B"
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

mode = st.sidebar.radio(
    "Select Mode",
    [
        "Inquire",
        "Ingest",
        "Explore"
    ]
)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.sidebar.divider()

search_term = st.sidebar.text_input(
    "🔎 Search Knowledge Base"
)

if search_term:

    results = search_entities(search_term)

    st.sidebar.subheader("Search Results")

    if not results:

        st.sidebar.info(
            "No matching entities found."
        )

    else:

        for result in results:

            st.sidebar.write(
                f"**{result['name']}**"
            )

            st.sidebar.caption(
                result["entity_type"]
            )


# --------------------------------------------------
# INQUIRE MODE
# --------------------------------------------------

if mode == "Inquire":

    st.header("💬 Inquire")

    question = st.text_area(
        "Ask your knowledge base",
        placeholder=(
            "Example: What technologies are "
            "related to NVIDIA?"
        ),
        height=120
    )

    if st.button(
        "Ask",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching knowledge base..."
            ):

                answer = answer_question(
                    question
                )

            st.subheader("Answer")

            st.write(answer)


# --------------------------------------------------
# INGEST MODE
# --------------------------------------------------

elif mode == "Ingest":

    st.header("📥 Ingest")

    st.write(
        "Add documents to the knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=[
            "pdf",
            "txt",
            "docx"
        ],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write(
            f"{len(uploaded_files)} "
            "document(s) selected."
        )

        if st.button(
            "Build Knowledge",
            type="primary",
            use_container_width=True
        ):

            for uploaded_file in uploaded_files:

                st.subheader(
                    uploaded_file.name
                )

                suffix = Path(
                    uploaded_file.name
                ).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_path = temp_file.name

                try:

                    with st.spinner(
                        f"Analyzing {uploaded_file.name}..."
                    ):

                        knowledge = ingest_document(
                            temp_path,
                            uploaded_file.name
                        )

                    st.success(
                        "Knowledge successfully added."
                    )

                    st.write(
                        f"Entities found: "
                        f"{len(knowledge['entities'])}"
                    )

                    st.write(
                        "Relationships found: "
                        f"{len(knowledge['relationships'])}"
                    )

                    with st.expander(
                        "View extracted knowledge"
                    ):

                        st.json(knowledge)

                except Exception as error:

                    st.error(
                        f"Error processing document: "
                        f"{error}"
                    )


# --------------------------------------------------
# KNOWLEDGE EXPLORER
# --------------------------------------------------

elif mode == "Explore":

    st.header("🌐 Knowledge Explorer")

    tab1, tab2 = st.tabs(
        [
            "Entities",
            "Relationships"
        ]
    )

    with tab1:

        entities = get_all_entities()

        if not entities:

            st.info(
                "No entities have been added yet."
            )

        else:

            for entity in entities:

                with st.expander(
                    f"{entity['name']} "
                    f"— {entity['entity_type']}"
                ):

                    if entity["description"]:

                        st.write(
                            entity["description"]
                        )

                    relationships = (
                        get_entity_relationships(
                            entity["name"]
                        )
                    )

                    if relationships:

                        st.write(
                            "**Connections**"
                        )

                        for relationship in relationships:

                            st.write(
                                f"{relationship['source']} "
                                f"→ "
                                f"**{relationship['relationship']}** "
                                f"→ "
                                f"{relationship['target']}"
                            )

    with tab2:

        relationships = (
            get_all_relationships()
        )

        if not relationships:

            st.info(
                "No relationships have been added yet."
            )

        else:

            for relationship in relationships:

                st.write(
                    f"**{relationship['source']}** "
                    f"→ "
                    f"{relationship['relationship']} "
                    f"→ "
                    f"**{relationship['target']}**"
                )

                if relationship["source_document"]:

                    st.caption(
                        f"Source: "
                        f"{relationship['source_document']}"
                    )