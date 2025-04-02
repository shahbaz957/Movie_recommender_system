import streamlit as st
import pickle
import pandas as pd
import requests

with open('movies_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)
with open('similarity.pkl', 'rb') as file2:
    similarity = pickle.load(file2)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=00570ec3696eebffd029fabb64fca986')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x : x[1])[1:6]
    recommended = []
    rec_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended.append(movies['title'].iloc[i[0]])
        rec_poster.append(fetch_poster(movie_id))

    return recommended , rec_poster

movies = pd.DataFrame(movies_dict)

st.title("Movie recommender System")

selected_movie = st.selectbox(
    'Select a movie Below for recommendation',
    movies['title'].values
)
if st.button('Recommend'):
    names , posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

