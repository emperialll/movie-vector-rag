import utils
from weaviate.classes.config import Configure, Property, DataType, ReferenceProperty

client = utils.connect_to_my_db()

try:
    if not client.collections.exists("Movie"):
        client.collections.create(
            "Movie",
            vector_config=Configure.Vectors.text2vec_openai(),
            generative_config=Configure.Generative.openai(),
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
                Property(name="movie_id", data_type=DataType.INT, skip_vectorization=True),
                Property(name="year", data_type=DataType.INT),
                Property(name="rating", data_type=DataType.NUMBER),
                Property(name="director", data_type=DataType.TEXT, skip_vectorization=True),
            ]
        )

    if not client.collections.exists("Review"):
        client.collections.create(
            "Review",
            vector_config=Configure.Vectors.text2vec_openai(),
            generative_config=Configure.Generative.openai(),
            properties=[
                Property(name="review_text", data_type=DataType.TEXT),
                Property(name="review_no", data_type=DataType.INT, skip_vectorization=True),
                Property(name="movie_id", data_type=DataType.INT, skip_vectorization=True),
            ],
            references=[
                ReferenceProperty(
                    name="forMovie",
                    target_collection="Movie"
                )
            ]
        )

    if not client.collections.exists("Synopsis"):
        client.collections.create(
            "Synopsis",
            vector_config=Configure.Vectors.text2vec_openai(),
            generative_config=Configure.Generative.openai(),
            properties=[
                Property(name="synopsis_text", data_type=DataType.TEXT),
                Property(name="movie_id", data_type=DataType.INT, skip_vectorization=True),
            ],
            references=[
                ReferenceProperty(
                    name="forMovie",
                    target_collection="Movie"
                )
            ]
        )

    # Add the 2nd way relationship from Movie to Synopsis
    movies = client.collections.get("Movie")

    try:
        movies.config.add_reference(
            ReferenceProperty(
                name="hasSynopsis",
                target_collection="Synopsis"
            )
        )
    except Exception as e:
        print("Movie.hasSynopsis may already exist:", e)

finally:
    client.close()
