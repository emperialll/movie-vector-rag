"""
Weaviate Cloud Connection Utility

This module provides functionality to connect to a Weaviate Cloud instance
using credentials stored in environment variables. It uses the official
Weaviate Python client and supports OpenAI integration via API key.

Environment Variables Required:
    - WEAVIATE_CLUSTER_URL: URL of the Weaviate Cloud cluster
    - WEAVIATE_AUTH_CREDENTIAL: API key for authentication
    - OPENAI_API_KEY: OpenAI API key (for vectorization/embedding modules)
"""

import os

import weaviate
from weaviate.classes.init import Auth
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


def connect_to_my_db():
    """
    Establish a connection to the Weaviate Cloud instance.

    This function creates and returns a Weaviate client configured with:
    - Cloud cluster URL
    - API key authentication
    - OpenAI API key for generative and embedding capabilities

    Returns:
        weaviate.WeaviateClient: Connected Weaviate client instance

    Raises:
        ValueError: If required environment variables are missing
        weaviate.exceptions.WeaviateConnectionError: If connection fails
    """
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
        auth_credentials=Auth.api_key(os.getenv("WEAVIATE_AUTH_CREDENTIAL")),
        headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
    )

    return client


def main():
    """
    Test the Weaviate connection.

    Creates a connection to Weaviate Cloud and checks if the instance is ready.
    Used as an entry point for quick connectivity testing.
    """
    with connect_to_my_db() as client:
        print(f"Connection successful: {client.is_ready()}")


if __name__ == "__main__":
    main()
