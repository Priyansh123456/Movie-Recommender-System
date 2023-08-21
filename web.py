import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data =requests.get(url)
    data = data.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movie_dict = pickle.load(open("movie_dict.pkl",'rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(open("similarity.pkl",'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies_names=[]
    recommend_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movies_names.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommend_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommend_movies_names,recommend_movies_posters
st.title("Movie Recommender System")

movie_list = movies['title'].values
Select_movie_name=st.selectbox(
    "Select the movie",movie_list
)

if st.button('Recommend'):
   recommend_movies_names,recommend_movies_posters= recommend(Select_movie_name)


   col1, col2, col3, col4, col5 = st.columns(5)
   with col1:
       st.text(recommend_movies_names[0])
       st.image(recommend_movies_posters[0])
   with col2:
       st.text(recommend_movies_names[1])
       st.image(recommend_movies_posters[1])

   with col3:
       st.text(recommend_movies_names[2])
       st.image(recommend_movies_posters[2])
   with col4:
       st.text(recommend_movies_names[3])
       st.image(recommend_movies_posters[3])
   with col5:
       st.text(recommend_movies_names[4])
       st.image(recommend_movies_posters[4])
