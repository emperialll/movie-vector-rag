import utils
import streamlit as st
import weaviate.classes as wvc
from weaviate.util import generate_uuid5


# Connection to weaviate instance
client = utils.connect_to_my_db()

try:
    movies = client.collections.get("Movie")
    synopses = client.collections.get("Synopsis")

    # Show page title - ReelRecommender
    st.title("Shahriar Movie Recommander")

    # Have multiple tabs, each one for different features (search / movie details / recommendations)
    search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

    with search_tab:

        st.header("Search movie")
        query_string = st.text_input(label="Search for a movie")

        srch_col1, srch_col2 = st.columns(2)
        with srch_col1:
            search_type = st.radio(
                label="How do you want to search?",
                options=["Vector", "Keyword", "Hybrid"]
            )

        with srch_col2:
            rating_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)
            year_min = st.number_input(label="Year from", value=1960, step=1)
            year_max = st.number_input(label="Year to", value=2023, step=1)

    # Search results - movie summaries
        st.header("Search results")

        movie_filter = (
            wvc.query.Filter.by_property("rating").greater_or_equal(rating_range[0])
            & wvc.query.Filter.by_property("rating").less_or_equal(rating_range[1])
            & wvc.query.Filter.by_property("year").greater_or_equal(year_min)
            & wvc.query.Filter.by_property("year").less_or_equal(year_max)
        )

        synopsis_xref = wvc.query.QueryReference(
            link_on="hasSynopsis", return_properties=["synopsis_text"]
        )

        if len(query_string) > 0:
            if search_type == "Vector":
                response = movies.query.near_text(
                    query=query_string,
                    filters=movie_filter,
                    limit=5,
                    return_references=[synopsis_xref]
                )
            elif search_type == "Keyword":
                response = movies.query.bm25(
                    query=query_string,
                    filters=movie_filter,
                    limit=5,
                    return_references=[synopsis_xref]
                )
            else:
                response = movies.query.hybrid(
                    query=query_string,
                    filters=movie_filter,
                    limit=5,
                    return_references=[synopsis_xref]
                )
        else:
            response = movies.query.fetch_objects(
                filters=movie_filter,
                limit=5,
                return_references=[synopsis_xref]
            )
            
        for movie in response.objects:
            with st.expander(movie.properties["title"]):
                rating = movie.properties["rating"]
                movie_id = movie.properties["movie_id"]
                st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")
                synopsis = movie.references["hasSynopsis"].objects[0].properties["synopsis_text"]
                st.write("**Synopsis**")
                st.write(synopsis[:200] + "...")

    with movie_tab:
        # Detailed movie information

        st.header("Movie details")
        movie_id_input = st.text_input(label="Enter the movie row ID here", value="")

        if len(movie_id_input.strip()) > 0:
            try:
                movie_id_value = int(movie_id_input.strip())
            except ValueError:
                st.error("Please enter a valid numeric movie ID.")
            else:
                movie_uuid = generate_uuid5(str(movie_id_value))

                movie = movies.query.fetch_object_by_id(
                    uuid=movie_uuid,
                    return_references=[
                        wvc.query.QueryReference(
                            link_on="hasSynopsis",
                            return_properties=["synopsis_text"]
                        ),
                        wvc.query.QueryReference(
                            link_on="hasReview",
                            return_properties=["review_text", "review_no"]
                        )
                    ]
                )

                if movie is None:
                    st.warning(f"No movie found with ID {movie_id_value}.")
                else:
                    title = movie.properties["title"]
                    director = movie.properties["director"]
                    rating = movie.properties["rating"]
                    movie_id = movie.properties["movie_id"]
                    year = movie.properties["year"]

                    st.write(f"ID: {movie_id}")
                    st.write(f"{title} - directed by {director}")
                    st.write(f"Rate: {rating}")
                    st.write(f"Released: {year}")

                    # Display synopsis
                    with st.expander(f"See synopsis of {title}"):
                        synopsis_refs = movie.references.get("hasSynopsis")

                        if synopsis_refs and len(synopsis_refs.objects) > 0:
                            synopsis = synopsis_refs.objects[0].properties["synopsis_text"]
                            st.write(synopsis)
                        else:
                            st.info("No synopsis found for this movie.")

                    # Display reviews
                    st.subheader("Reviews")

                    review_refs = movie.references.get("hasReview")

                    if review_refs and len(review_refs.objects) > 0:
                        sorted_reviews = sorted(
                            review_refs.objects,
                            key=lambda r: r.properties.get("review_no", 0)
                        )

                        for r in sorted_reviews:
                            review_no = r.properties.get("review_no", "")
                            review_text = r.properties.get("review_text", "")

                            st.write(f"**Review {review_no}**")
                            st.write(review_text)
                    else:
                        st.info("No reviews found for this movie.")

    with rec_tab:
    # AI-powered recommendations
        st.header("Recommend me a movie")
        search_string = st.text_input(label="Recommend me a ...", value="")
        occasion = st.text_input(label="In this context ...", value="any occasion")

        # Only do something if the user fills in the search string and the context
        if len(search_string) > 0 and len(occasion) > 0:
            st.subheader("Recommendations")

            response = synopses.generate.hybrid(
                query=search_string,
                grouped_task=f"""
                The user is looking to watch {search_string} types of movies
                for {occasion}. Recommend the best possible movie based on the
                provided movie synopses.
                """,
                limit=3,
                return_references=[
                    wvc.query.QueryReference(
                        link_on="forMovie", return_properties=["title", "movie_id", "description"]
                    )
                ]
            )

            st.write(response.generated)

            st.subheader("Movies analysed")
            for i, m in enumerate(response.objects):
                movie_title = m.references["forMovie"].objects[0].properties["title"]
                movie_id = m.references["forMovie"].objects[0].properties["movie_id"]
                movie_description = m.references["forMovie"].objects[0].properties["description"]
                with st.expander(f"Movie title: {movie_title}, ID: {movie_id}"):
                    st.write(movie_description)
finally:
    client.close()
