import requests

# Paste your regenerated API key here
api_key = "16cc875ce015a682613f74ca83c82c0a" 

# A known movie ID (The Dark Knight)
movie_id = 155
url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

print(f"Attempting to connect to: {url}")

try:
    # We will set a timeout of 10 seconds
    response = requests.get(url, timeout=10)
    
    # This will raise an error if the status code is 4xx or 5xx
    response.raise_for_status() 
    
    data = response.json()
    print("\n✅ SUCCESS! Connection is working.")
    print(f"Movie Title: {data.get('title')}")

except requests.exceptions.HTTPError as e:
    print("\n❌ FAILED! The API key is likely invalid.")
    print(f"HTTP Error: {e}")

except requests.exceptions.RequestException as e:
    print("\n❌ FAILED! There is a network or connection problem.")
    print(f"Connection Error: {e}")