# Movie Vector RAG

A Streamlit web app for semantic movie search and AI-powered movie recommendations using **Weaviate**, **OpenAI embeddings/generation**, and **Retrieval-Augmented Generation (RAG)**.

The app lets users search a movie dataset with vector or hybrid search, inspect individual movie details, and ask for recommendations based on the type of movie they want and the viewing occasion.

---

## Demo Overview

The application has three main sections:

1. **Search**  
   Search movies using vector search or hybrid search, with a rating filter.

2. **Movie Details**  
   Look up a movie by its dataset ID and view its title, director, rating, release year, and full synopsis.

3. **Recommend**  
   Ask for a movie recommendation in natural language, such as:

   > Recommend me a funny family movie for a weekend night

   The app retrieves relevant movie synopses from Weaviate and uses a generative model to recommend a movie based only on the retrieved context.

---

## Features

- Semantic movie search with Weaviate vector search
- Hybrid search combining semantic and keyword-based matching
- Rating-based filtering
- Movie detail lookup by ID
- AI-powered movie recommendations using RAG
- Cross-references between movies and synopses
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

### Synopsis

Stores long-form movie synopsis text:

- `synopsis_text`
- `movie_id`

References:

- `Synopsis -> Movie` through `forMovie`
- `Movie -> Synopsis` through `hasSynopsis`

### Review

Stores critic review snippets:

- `review_text`
- `review_no`
- `movie_id`

References:

- `Review -> Movie` through `forMovie`

---

## How RAG Works in This Project

RAG stands for **Retrieval-Augmented Generation**.

In this project, RAG happens in the recommendation tab:

1. The user enters what kind of movie they want.
2. The app searches the `Synopsis` collection in Weaviate using hybrid search.
3. Weaviate retrieves the most relevant movie synopses.
4. Those retrieved synopses are passed to a generative model with a prompt.
5. The model generates a recommendation based on the retrieved movie data.

Simplified flow:

```text
User request
   ↓
Hybrid search in Weaviate
   ↓
Retrieve relevant movie synopses
   ↓
Send retrieved context to generative model
   ↓
Generate recommendation
   ↓
Display recommendation in Streamlit
```

This means the recommendation is grounded in the movies stored in the vector database instead of being only a general response from the language model.

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

````bash
pip install -r requirements.txt

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
````

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

Then switch between **Vector** and **Hybrid** search to compare the results.

### Recommendation

Try recommendation prompts such as:

```text
Recommend me a lighthearted comedy
```

with context:

```text
for a relaxing weekend evening
```

or:

```text
Recommend me an emotional drama
```

with context:

```text
for watching alone on a rainy night
```

---

## Key Concepts Demonstrated

This project demonstrates:

- How to connect a Python app to Weaviate Cloud
- How to create vectorized collections
- How to seed structured and unstructured data into a vector database
- How to model references between collections
- How to run vector and hybrid searches
- How to build a Streamlit app on top of a vector database
- How to use RAG for recommendation generation
- How retrieved database results can be used as grounding context for an AI response

---

## Current Limitations

- The recommendation output is generated by an AI model, so the prompt should be kept strict to avoid recommending movies outside the database.
- The app currently uses a fixed result limit for search and recommendation queries.
- Movie lookup is based on dataset row ID rather than a user-friendly title search.
- There is no authentication layer for the Streamlit app.
- The project does not currently include automated tests or a `requirements.txt` file.

---

## Possible Future Improvements

- Add stricter validation to ensure recommendations only include movies retrieved from Weaviate
- Add title-based movie detail lookup
- Add filters for director and release year
- Add review-based recommendation logic
- Add screenshots or a short demo GIF to the README
- Improve error handling for missing environment variables or unavailable Weaviate connections
- Add unit tests for data loading and query helper functions
- Deploy the Streamlit app publicly

---

## What I Learned

Through this project, I practiced building a complete vector-database-backed application, including:

- Designing collections and references in Weaviate
- Loading CSV data into a vector database
- Running vector and hybrid search queries
- Connecting search results to a Streamlit interface
- Using retrieved context to generate AI-powered recommendations
- Understanding the difference between normal search, semantic search, and RAG
