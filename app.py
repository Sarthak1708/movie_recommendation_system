import streamlit as st
import pickle
import pandas as pd
import requestsimport streamlit as st
import pickle
import pandas as pd
import requests
import os
import gzip


# TMDB API key
API_KEY =os.getenv("API_KEY")

# Load the pre-saved data
movie_dict = pickle.load(open(r'D:\Python\Major_Project\Movie_recommendation_system\movie_list.pkl', 'rb'))
with gzip.open(r'D:\Python\Major_Project\Movie_recommendation_system\similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movie_dict)

# Custom CSS for movie theme
st.markdown("""
    <style>
    body {
        background-image: url('https://wallpaperaccess.com/full/329583.jpg');
        background-size: cover;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: white !important;
    }
    h1 {
        color: #FF4B4B;
        text-shadow: 1px 1px 2px black;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stSelectbox > div {
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("API Response:", data)  # Debug
        poster_path = data.get('poster_path')

        if poster_path:
            full_url = "https://image.tmdb.org/t/p/w500/" + poster_path
            print("Poster URL:", full_url)
            return full_url
        else:
            print("Poster not found.")
            return "https://via.placeholder.com/500x750?text=No+Image"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox("Choose a movie", movies['title'].values)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    
    st.subheader("You might also like:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

import os
import gzip

# TMDB API key
API_KEY = os.getenv("API_KEY", "3424da94086a292a13b385906898cb6f")

# Load the pre-saved data (ensure files are in the same folder as app.py)
with open('movie_list.pkl', 'rb') as f:
    movie_dict = pickle.load(f)

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movie_dict)

# Custom CSS for movie theme
st.markdown("""
    <style>
    body {
        background-image: url('https://wallpaperaccess.com/full/329583.jpg');
        background-size: cover;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
    }
    h1 {
        color: #FF4B4B;
        text-shadow: 1px 1px 2px black;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stSelectbox > div {
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

# Recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit App UI
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox("Choose a movie", movies['title'].values)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    st.subheader("You might also like:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
