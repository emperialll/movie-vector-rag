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
