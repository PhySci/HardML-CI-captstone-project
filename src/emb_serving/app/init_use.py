#!/bin/python
from sentence_transformers import SentenceTransformer


def main():
    SentenceTransformer("distiluse-base-multilingual-cased-v1", device="cpu")

if __name__ == "__main__":
    main()
