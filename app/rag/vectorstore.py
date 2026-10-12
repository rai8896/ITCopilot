
import time

from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.core.config import get_settings


settings = get_settings()

_embeddings = None
_vectorstore = None

EMBEDDING_DIMENSIONS = {
    "sentence-transformers/all-minilm-l6-v2": 384,
    "all-minilm-l6-v2": 384,
}


def get_embedding_dimension(model_name: str | None = None) -> int:
    name = (model_name or settings.embedding_model or "").strip().lower()

    if name in EMBEDDING_DIMENSIONS:
        return EMBEDDING_DIMENSIONS[name]

    if "all-minilm" in name:
        return 384

    raise ValueError(
        f"Unsupported embedding model: {model_name or settings.embedding_model}"
    )


def get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    return _embeddings


def ensure_index():
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is missing")

    desired_dimension = get_embedding_dimension()
    pc = Pinecone(api_key=settings.pinecone_api_key)

    existing_names = [item["name"] for item in pc.list_indexes()]

    if settings.pinecone_index_name in existing_names:
        info = pc.describe_index(settings.pinecone_index_name)
        current_dimension = getattr(info, "dimension", None)

        if current_dimension is None and isinstance(info, dict):
            current_dimension = info.get("dimension")

        if current_dimension != desired_dimension:
            raise RuntimeError(
                f"Pinecone index '{settings.pinecone_index_name}' has "
                f"dimension {current_dimension}, but the selected embedding "
                f"model requires {desired_dimension}. Create a new index "
                "with dimension 384 or choose a compatible embedding model. "
                "The existing index was NOT deleted."
            )

    else:
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=desired_dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

        while True:
            info = pc.describe_index(settings.pinecone_index_name)
            status = getattr(info, "status", {})
            ready = (
                status.get("ready", False)
                if isinstance(status, dict)
                else getattr(status, "ready", False)
            )

            if ready:
                break

            time.sleep(1)

    return pc.Index(settings.pinecone_index_name)


def get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        index = ensure_index()

        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=get_embeddings(),
            namespace=settings.pinecone_namespace,
        )

    return _vectorstore


def get_retriever():
    return get_vectorstore().as_retriever(
        search_kwargs={"k": settings.top_k}
    )


def add_documents(chunks):
    return get_vectorstore().add_documents(chunks)
