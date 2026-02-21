#!/usr/bin/env python3
"""
SemanticCrew ChromaDB Query Wrapper
Hippocampal → Prefrontal retrieval bridge.

Usage:
  python3 chroma_query.py "search terms" [--collection NAME] [--n 5] [--crew MEMBER]

Called by PyGPT sessions to pull long-term memory into working context.
Results are printed as formatted text suitable for context injection.

Collections: research, crew_memory, conversations, library
Crew members: huginn, muninn, maigret, kusanagi, all
"""

import argparse
import sys

def query_chromadb(query_text, collection_name=None, n_results=5, crew_filter=None):
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        print(f"[chroma_query] Import error: {e}", file=sys.stderr)
        sys.exit(1)

    CHROMA_PATH = "/mnt/fastdata/SemanticMemory/chromadb"
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Determine which collections to query
    all_collections = ["research", "crew_memory", "conversations", "library"]
    if collection_name and collection_name in all_collections:
        collections_to_query = [collection_name]
    else:
        collections_to_query = all_collections

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode([query_text])[0].tolist()

    results = []
    for col_name in collections_to_query:
        try:
            col = client.get_collection(col_name)
            where = None
            if crew_filter and crew_filter != "all":
                # Filter by crew member tag if metadata supports it
                where = {"crew_member": {"$eq": crew_filter}}
            res = col.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, col.count()),
                include=["documents", "metadatas", "distances"],
                where=where if where else None
            )
            for i, doc in enumerate(res["documents"][0]):
                meta = res["metadatas"][0][i] if res["metadatas"] else {}
                dist = res["distances"][0][i] if res["distances"] else 0
                results.append({
                    "collection": col_name,
                    "distance": dist,
                    "document": doc,
                    "metadata": meta
                })
        except Exception as e:
            print(f"[chroma_query] Warning: collection '{col_name}' error: {e}", file=sys.stderr)

    # Sort by relevance (lower distance = more relevant)
    results.sort(key=lambda x: x["distance"])
    results = results[:n_results]

    return results


def format_results(results, query_text):
    if not results:
        return f"[SemanticCrew Memory] No results found for: '{query_text}'"

    lines = [
        f"[SemanticCrew Memory] Query: '{query_text}'",
        f"Retrieved {len(results)} relevant document(s) from long-term memory:",
        "=" * 60
    ]
    for i, r in enumerate(results, 1):
        meta = r["metadata"]
        source = meta.get("name") or meta.get("filename") or meta.get("path", "unknown")
        col = r["collection"]
        score = round(1 - r["distance"], 3)
        lines.append(f"\n[{i}] Source: {source} | Collection: {col} | Relevance: {score}")
        lines.append("-" * 40)
        # Truncate long documents for context injection
        doc_preview = r["document"][:800]
        if len(r["document"]) > 800:
            doc_preview += "... [truncated]"
        lines.append(doc_preview)

    lines.append("\n" + "=" * 60)
    lines.append("[End of long-term memory retrieval]")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Query SemanticCrew ChromaDB hippocampal memory")
    parser.add_argument("query", help="Search query text")
    parser.add_argument("--collection", "-c", default=None,
                        help="Specific collection: research, crew_memory, conversations, library")
    parser.add_argument("--n", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--crew", default=None,
                        help="Filter by crew member: huginn, muninn, maigret, kusanagi")
    parser.add_argument("--raw", action="store_true",
                        help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    results = query_chromadb(args.query, args.collection, args.n, args.crew)

    if args.raw:
        import json
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results, args.query))


if __name__ == "__main__":
    main()
