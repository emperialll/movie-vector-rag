import streamlit as st

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
            options=["Vector", "Hybrid"]
        )

    with srch_col2:
        value_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)

# Search results - movie summaries
    st.header("Search results")

    response = [
        {
            "title": f"Title {i}",
            "rating": 4.0,
            "movie_id": i,
            "director": f"Director {i}",
        }
        for i in range(1, 5)
    ]  # Placeholder response

    for movie in response:
        with st.expander(movie["title"]):
            rating = movie["rating"]
            movie_id = movie["movie_id"]
            synopsis = "Synopsis here"
            st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")
            st.write("**Synopsis**")
            st.write(synopsis[:200] + "...")
