import pickle
import streamlit as st
import numpy as np


st.header('Anime Recommender System Using Machine Learning')
model = pickle.load(open('artifacts/model.pkl','rb'))

anime_names = pickle.load(open('artifacts/anime_name.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_data.pkl','rb'))
anime_pivot = pickle.load(open('artifacts/anime_pivot.pkl','rb'))


def fetch_poster(suggestion):
    anime_name = []
    ids_index = []
    poster_url = []

    for anime_id in suggestion:
        anime_name.append(anime_pivot.index[anime_id])

    for name in anime_name[0]: 
        ids = np.where(final_rating['Name'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



def recommend_anime(anime_name):
    animes_list = []
    anime_id = np.where(anime_pivot.index == anime_name)[0][0]
    distance, suggestion = model.kneighbors(anime_pivot.iloc[anime_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            animes = anime_pivot.index[suggestion[i]]
            for j in animes:
                animes_list.append(j)
    return animes_list , poster_url       



selected_animes = st.selectbox(
    "Type or select an anime from the dropdown",
    anime_names
)

if st.button('Show Recommendation'):
    recommended_animes,poster_url = recommend_anime(selected_animes)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_animes[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_animes[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_animes[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_animes[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_animes[5])
        st.image(poster_url[5])