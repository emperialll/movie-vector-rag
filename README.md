# Movie Vector RAG

A Streamlit web app for semantic movie search and AI-powered movie recommendations using **Weaviate**, **OpenAI embeddings/generation**, and **Retrieval-Augmented Generation (RAG)**.

The app lets users search a movie dataset with vector, keyword, or hybrid search, inspect individual movie details, view critic reviews, and ask for AI-powered recommendations based on the type of movie they want and the viewing occasion.

---

## Demo Overview

The application has three main sections:

1. **Search**  
   Search movies using vector search, keyword search, or hybrid search, with rating and release-year filters.

2. **Movie Details**  
   Look up a movie by its dataset ID and view its title, director, rating, release year, full synopsis, and critic reviews.

3. **Recommend**  
   Ask for a movie recommendation in natural language, such as:

   > Recommend me a funny family movie for a weekend night

   The app retrieves relevant movie synopses from Weaviate and uses a generative model to recommend a movie based only on the retrieved context.

---

## Features

- Semantic movie search with Weaviate vector search
- Keyword search with BM25
- Hybrid search combining semantic and keyword-based matching
- Rating-based filtering
- Release-year filtering
- Movie detail lookup by dataset ID
- Full synopsis display for each movie
- Critic review display for each movie
- AI-powered movie recommendations using RAG
- Cross-references between movies, synopses, and reviews
- Streamlit UI with separate tabs for search, details, and recommendations
- Data seeding from a local CSV file
- Weaviate Cloud connection through environment variables

---

## Tech Stack

- **Python**
- **Streamlit** for the web app UI
- **Weaviate Cloud** as the vector database
- **OpenAI** for text vectorization and generative responses
- **Pandas** for reading and preparing movie data
- **python-dotenv** for environment variable management

---

## Project Architecture

```text
movie-vector-rag/
├── app.py                  # Streamlit web app
├── movie_collections.py    # Creates Weaviate collections and references
├── seed_movie_data.py      # Loads movie data into Weaviate
├── utils.py                # Weaviate connection helper
├── requirements.txt        # Python dependencies
├── data/
│   └── movies_data.csv     # Movie dataset
├── .env.example            # Example environment variables
├── .gitignore
└── README.md
```

---

## Data Model

The project uses three Weaviate collections:

### Movie

Stores core movie metadata:

- `title`
- `description`
- `movie_id`
- `year`
- `rating`
- `director`

References:

- `Movie -> Synopsis` through `hasSynopsis`
- `Movie -> Review` through `hasReview`

### Synopsis

Stores long-form movie synopsis text:

- `synopsis_text`
- `movie_id`

References:

- `Synopsis -> Movie` through `forMovie`

### Review

Stores critic review snippets:

- `review_text`
- `review_no`
- `movie_id`

The `Review` collection does not currently point back to `Movie`. Instead, movies reference their reviews through `Movie.hasReview`.

---

## Collection Relationships

The current collection relationship structure is:

```text
Movie
 ├── hasSynopsis ──> Synopsis
 └── hasReview ────> Review

Synopsis
 └── forMovie ─────> Movie
```

This allows the app to:

- Fetch a movie and its synopsis from the `Movie` collection
- Fetch a movie and its critic reviews from the `Movie` collection
- Search synopses for recommendation generation
- Link retrieved synopses back to their related movies

---

## How RAG Works in This Project

RAG stands for **Retrieval-Augmented Generation**.

In this project, RAG happens in the recommendation tab:

1. The user enters what kind of movie they want.
2. The app searches the `Synopsis` collection in Weaviate using hybrid search.
3. Weaviate retrieves the most relevant movie synopses.
4. Those retrieved synopses are passed to a generative model with a prompt.
5. The model generates a recommendation based on the retrieved movie data.
6. The app displays the generated recommendation and the movies that were analyzed.

Simplified flow:

```text
User request
   ↓
Hybrid search in Weaviate
   ↓
Retrieve relevant movie synopses
   ↓
Follow Synopsis.forMovie references
   ↓
Send retrieved context to generative model
   ↓
Generate recommendation
   ↓
Display recommendation in Streamlit
```

This means the recommendation is grounded in the movies stored in the vector database instead of being only a general response from the language model.

---

## Search Modes

The search tab supports three search modes:

### Vector Search

Uses semantic similarity to find movies related to the meaning of the user query.

Example:

```text
lonely lighthouse friendship
```

This can return relevant movies even if the exact words are not present in the movie title or description.

### Keyword Search

Uses BM25 keyword search to find movies matching the query text more directly.

Example:

```text
penguin comedy
```

This is useful when the user knows specific words they expect to appear in the movie data.

### Hybrid Search

Combines vector search and keyword search.

This is useful when the user wants both semantic understanding and keyword matching.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-vector-rag.git
cd movie-vector-rag
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

Install the project dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then fill in your credentials:

```env
WEAVIATE_CLUSTER_URL=your_weaviate_cluster_url
WEAVIATE_AUTH_CREDENTIAL=your_weaviate_api_key
OPENAI_API_KEY=your_openai_api_key
```

Do not commit your real `.env` file to GitHub.

---

## Running the Project

### 1. Create Weaviate collections

```bash
python movie_collections.py
```

This creates the `Movie`, `Synopsis`, and `Review` collections in Weaviate.

The script also creates the required references:

- `Movie.hasSynopsis -> Synopsis`
- `Movie.hasReview -> Review`
- `Synopsis.forMovie -> Movie`

### 2. Seed the movie data

```bash
python seed_movie_data.py
```

This reads `data/movies_data.csv`, inserts movies, synopses, and reviews, and creates references between the collections.

### 3. Start the Streamlit app

```bash
streamlit run app.py
```

The app will open in your browser.

---

## Example Usage

### Search

Try searching for:

```text
penguin comedy
```

or:

```text
lonely lighthouse friendship
```

Then switch between **Vector**, **Keyword**, and **Hybrid** search to compare the results.

You can also adjust:

- Rating range
- Minimum release year
- Maximum release year

### Movie Details

Enter a movie dataset ID to view detailed information about a movie.

The detail page displays:

- Movie ID
- Title
- Director
- Rating
- Release year
- Full synopsis
- Critic reviews

### Recommendation

Try recommendation prompts such as:

```text
lighthearted comedy
```

with context:

```text
for a relaxing weekend evening
```

or:

```text
emotional drama
```

with context:

```text
for watching alone on a rainy night
```

The recommendation tab retrieves relevant synopses, sends them to the generative model, and displays an AI-generated recommendation grounded in the retrieved movie data.

---

## Key Concepts Demonstrated

This project demonstrates:

- How to connect a Python app to Weaviate Cloud
- How to create vectorized collections
- How to configure OpenAI vectorization in Weaviate
- How to configure OpenAI generative capabilities in Weaviate
- How to seed structured and unstructured data into a vector database
- How to model references between collections
- How to run vector search
- How to run BM25 keyword search
- How to run hybrid search
- How to filter search results by numeric properties
- How to fetch referenced objects in Weaviate
- How to build a Streamlit app on top of a vector database
- How to use RAG for recommendation generation
- How retrieved database results can be used as grounding context for an AI response

---

## Current Limitations

- The recommendation output is generated by an AI model, so the prompt should be kept strict to avoid recommending movies outside the database.
- The app currently uses a fixed result limit for search and recommendation queries.
- Movie lookup is based on dataset row ID rather than a user-friendly title search.
- Reviews are displayed in the movie details page, but they are not yet used directly in the recommendation prompt.
- There is no authentication layer for the Streamlit app.
- The project does not currently include automated tests.

---

## Possible Future Improvements

- Add stricter validation to ensure recommendations only include movies retrieved from Weaviate
- Add title-based movie detail lookup
- Add filters for director and genre, if genre data is added
- Use critic reviews as additional context for recommendations
- Add review-based recommendation logic
- Add a comment section for users to leave feedback on movies
- Add screenshots or a short demo GIF to the README
- Improve error handling for missing environment variables or unavailable Weaviate connections
- Add unit tests for data loading and query helper functions
- Deploy the Streamlit app publicly

---

## What I Learned

Through this project, I practiced building a complete vector-database-backed application, including:

- Designing collections and references in Weaviate
- Loading CSV data into a vector database
- Running vector, keyword, and hybrid search queries
- Filtering search results by rating and release year
- Connecting search results to a Streamlit interface
- Fetching cross-referenced data from Weaviate
- Displaying related synopses and reviews in the app
- Using retrieved context to generate AI-powered recommendations
- Understanding the difference between normal search, semantic search, keyword search, hybrid search, and RAG
