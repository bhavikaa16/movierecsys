import os
import requests
import pickle
import pandas as pd
from fastapi import FastAPI
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 1. SETUP ---
load_dotenv()
app = FastAPI(title="Movie Recommendation API")

# Load TMDb API Key and check if it exists
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    print("FATAL ERROR: TMDB_API_KEY not found in .env file.")

# FIX 1: Create a single, reusable session object for all API calls
session = requests.Session()
retry_strategy = Retry(
    total=3,  # Total number of retries
    backoff_factor=1,  # Time to wait between retries (e.g., 1s, 2s, 4s)
    status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
# Load your pre-computed data
try:
    movies_df = pd.read_pickle('movies.pkl')
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    print("FATAL ERROR: Model files (movies.pkl, similarity.pkl) not found.")


# --- 2. HELPER FUNCTION ---
def fetch_poster_from_tmdb(movie_id: int):
    """Fetches a poster URL from TMDb using the shared session."""
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/500x750?text=API+Key+Missing"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    try:
        # Use the session object that is now defined
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching poster for movie_id {movie_id}: {e}")
    
    return "https://via.placeholder.com/500x750?text=Poster+Not+Found"


# --- 3. API ENDPOINTS ---
# FIX 4: Implemented the missing logic for the /movies endpoint
@app.get("/movies")
def get_movie_titles():
    """Returns a list of all movie titles for the dropdown menu."""
    return {"titles": movies_df['title'].tolist()}


# FIX 2: Merged into a single, correct /recommend endpoint
@app.get("/recommend/{movie_title}")
def get_recommendations(movie_title: str):
    """Generates movie recommendations and fetches their posters."""
    try:
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    except IndexError:
        return {"error": f"Movie '{movie_title}' not found."}

    recommended_movies = []
    for i in movies_list:
        movie_info = movies_df.iloc[i[0]]
        recommended_movies.append({
            "title": movie_info.title,
            "movie_id": int(movie_info.movie_id),
            "poster_url": fetch_poster_from_tmdb(int(movie_info.movie_id))
        })
        # FIX 3: Removed time.sleep() as it's not needed with a session object
    return {"recommendations": recommended_movies}