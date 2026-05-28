import streamlit as st
import pandas as pd
import pickle

import requests
def fetch_poster(movie_id):

    headers = {
        "accept": "application/json",
        "Authorization": " PROVIDE YOUR TMDB API Read Access Token"
    }

    response = requests.get("https://api.themoviedb.org/3/movie/{}?external_source=imdb_id&language=en-US".format(movie_id), headers=headers)

    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

st.title('Movie Recommendation System')

movie_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movie_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[0:5]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:

        movie_id=movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        #fetch poster from api
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_posters

selected_movie_name = st.selectbox("How would you like to be contacted?",movies['title'].values)

if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)

    # Create the columns and store them in a list
    cols = st.columns(5)

    # Loop through columns, names, and posters simultaneously
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)

