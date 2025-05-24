# main.py
import argparse
import sys
from keywords.extractor import KeywordExtractor

def search_mode(query: str):
    extractor = KeywordExtractor()
    query_keywords = set([query.lower()])

    for line in sys.stdin:
        line = line.strip()
        if not line or "\t" not in line:
            continue
        doc_id, content = line.split("\t", 1)
        doc_keywords = extractor.extract_all(content.lower())
        if query_keywords & doc_keywords:
            print(f"{doc_id}\tMATCH")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", required=True)
    parser.add_argument("--query", help="Search keyword")

    args = parser.parse_args()

    if args.operation == "search":
        if not args.query:
            sys.exit("Error: --query is required for search")
        search_mode(args.query)
    else:
        sys.exit("Only 'search' operation is supported in Hadoop mode")
