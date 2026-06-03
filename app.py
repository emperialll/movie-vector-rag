import streamlit as st

# Show page title - ReelRecommender
st.title("Shahriar Movie Recommander")

# Have multiple tabs, each one for different features (search / movie details / recommendations)
search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

