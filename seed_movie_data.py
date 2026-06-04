import utils
import pandas as pd
from weaviate.util import generate_uuid5
from weaviate.classes.data import DataObject, DataReference


CSV_PATH = "data/movies_data.csv"

INSERT_MOVIES = True


def clean(value):
    return None if pd.isna(value) else value


def as_int(value):
    value = clean(value)
    return None if value is None else int(value)


def as_float(value):
    value = clean(value)
    return None if value is None else float(value)


def insert_many_or_print_errors(collection, objects, label):
    if not objects:
        print(f"No {label} objects to insert.")
        return

    response = collection.data.insert_many(objects)

    if response.has_errors:
        print(f"Some {label} objects failed to insert:")
        print(response.errors)
    else:
        print(f"Inserted {len(response.uuids)} {label} objects")


movies_df = pd.read_csv(CSV_PATH)
client = utils.connect_to_my_db()

try:
    movies = client.collections.get("Movie")
    reviews = client.collections.get("Review")
    synopses = client.collections.get("Synopsis")

    movie_objects = []
    review_objects = []
    synopsis_objects = []

    movie_to_review_refs = []
    synopsis_to_movie_refs = []
    movie_to_synopsis_refs = []

    for _, row in movies_df.iterrows():
        movie_id = as_int(row["ID"])

        if movie_id is None:
            continue

        movie_uuid = generate_uuid5(str(movie_id))
        synopsis_uuid = generate_uuid5(f"synopsis-{movie_id}")

        # -------------------------
        # Movie object
        # -------------------------
        movie_props = {
            "title": clean(row["Movie Title"]),
            "description": clean(row["Description"]),
            "rating": as_float(row["Star Rating"]),
            "director": clean(row["Director"]),
            "movie_id": movie_id,
            "year": as_int(row["Year"]),
        }

        movie_objects.append(
            DataObject(
                properties=movie_props,
                uuid=movie_uuid,
            )
        )

        # -------------------------
        # Synopsis object
        # Schema:
        # Synopsis.forMovie -> Movie
        # Movie.hasSynopsis -> Synopsis
        # -------------------------
        synopsis_text = clean(row["Synopsis"])

        if synopsis_text is not None:
            synopsis_props = {
                "synopsis_text": synopsis_text,
                "movie_id": movie_id,
            }

            synopsis_objects.append(
                DataObject(
                    properties=synopsis_props,
                    uuid=synopsis_uuid,
                )
            )

            # Synopsis -> Movie
            synopsis_to_movie_refs.append(
                DataReference(
                    from_uuid=synopsis_uuid,
                    from_property="forMovie",
                    to_uuid=movie_uuid,
                )
            )

            # Movie -> Synopsis
            movie_to_synopsis_refs.append(
                DataReference(
                    from_uuid=movie_uuid,
                    from_property="hasSynopsis",
                    to_uuid=synopsis_uuid,
                )
            )

        # -------------------------
        # Review objects
        # Schema:
        # Movie.hasReview -> Review
        # There is NO Review.forMovie in your new schema.
        # -------------------------
        review_columns = [
            ("Critic Review 1", 1),
            ("Critic Review 2", 2),
            ("Critic Review 3", 3),
        ]

        for column_name, review_no in review_columns:
            review_text = clean(row[column_name])

            if review_text is None:
                continue

            review_uuid = generate_uuid5(f"review-{movie_id}-{review_no}")

            review_props = {
                "review_text": review_text,
                "review_no": review_no,
                "movie_id": movie_id,
            }

            review_objects.append(
                DataObject(
                    properties=review_props,
                    uuid=review_uuid,
                )
            )

            # Movie -> Review
            movie_to_review_refs.append(
                DataReference(
                    from_uuid=movie_uuid,
                    from_property="hasReview",
                    to_uuid=review_uuid,
                )
            )

    # -------------------------
    # Insert objects first
    # -------------------------
    if INSERT_MOVIES:
        insert_many_or_print_errors(movies, movie_objects, "Movie")

    insert_many_or_print_errors(synopses, synopsis_objects, "Synopsis")
    insert_many_or_print_errors(reviews, review_objects, "Review")

    # -------------------------
    # Add references after objects exist
    # -------------------------

    # Movie -> Review
    if movie_to_review_refs:
        movies.data.reference_add_many(movie_to_review_refs)
        print(f"Added {len(movie_to_review_refs)} Movie.hasReview references.")

    # Synopsis -> Movie
    if synopsis_to_movie_refs:
        synopses.data.reference_add_many(synopsis_to_movie_refs)
        print(f"Added {len(synopsis_to_movie_refs)} Synopsis.forMovie references.")

    # Movie -> Synopsis
    if movie_to_synopsis_refs:
        movies.data.reference_add_many(movie_to_synopsis_refs)
        print(f"Added {len(movie_to_synopsis_refs)} Movie.hasSynopsis references.")

    print("Finished adding objects and references.")

finally:
    client.close()
