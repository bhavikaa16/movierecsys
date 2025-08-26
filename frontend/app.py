import streamlit as st
import requests
import os


API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# TMDb API Key setup (this part remains the same)
try:
    API_KEY = st.secrets["api_key"]
except (KeyError, FileNotFoundError):
    st.error("API key not found. Please add it to your Streamlit secrets.")
    st.stop()
session = requests.Session()
session.params = {"api_key": API_KEY}

# --- 2. Functions to interact with APIs ---
@st.cache_data(show_spinner="Loading movie list...")
def get_movie_list():
    """Fetches the list of all movie titles from our backend API."""
    try:
        response = session.get(f"{API_URL}/movies", timeout=10)
        response.raise_for_status()
        return response.json().get("titles", [])
    except requests.exceptions.RequestException:
        st.error("Could not connect to the backend API to fetch movie list.")
        return []

def get_recommendations(movie_title):
    """Fetches recommendations for a movie from our backend API."""
    try:
        response = session.get(f"{API_URL}/recommend/{movie_title}", timeout=10)
        response.raise_for_status()
        return response.json().get("recommendations", [])
    except requests.exceptions.RequestException:
        return None # Return None to indicate an error

##@st.cache_data(show_spinner=False)
 
## def fetch_poster(movie_id):
   # """Fetches a movie poster from TMDb (this function remains the same)."""
    #url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    #try:
        #response = session.get(url, timeout=10)
       # response.raise_for_status()
   ##     data = response.json()
       # poster_path = data.get('poster_path')
      #  if poster_path:
     #       return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    ##    return "https://via.placeholder.com/500x750?text=No+Poster"
    ##except requests.exceptions.RequestException:
    #    return "https://via.placeholder.com/500x750?text=API+Error"

# --- 3. Streamlit UI ---
st.title('🎬 Movie Recommender System')

movie_titles = get_movie_list()
if movie_titles:
    selected_movie = st.selectbox(
        "Type or select a movie to get a recommendation",
        movie_titles
    )

    if st.button('Show Recommendation', type="primary"):
        recommendations = get_recommendations(selected_movie)
        
        if recommendations is not None:
            if recommendations:
                cols = st.columns(5)
                for i, movie in enumerate(recommendations):
                    with cols[i]:
                        st.text(movie['title'])
                        st.image(movie['poster_url'])  # ✅ use backend poster_url

            else:
                 st.warning("Could not find recommendations for the selected movie.")
        else:
            st.error("Failed to get recommendations from the backend service.")