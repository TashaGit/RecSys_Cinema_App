import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://amiel.club/uploads/posts/2022-03/1647696986_1-amiel-club-p-neitralnie-kartinki-na-rabochii-stol-1.jpg");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,

)

st.markdown(
    "<h1 style='text-align: center; color: black;'> Сервис рекомендации кинофильмов </h1>",
    unsafe_allow_html=True
)
st.write(
    """
    Это пример сервиса для рекомендации кинофильмов согласно Вашим вкусам
    """
)

selected_movie = selectbox(
    "Выберите интересный Вам фильм:",
     recsys.get_title()
)

genre = selectbox(
    "Выберите интересный Вам жанр:",
     recsys.get_genres()
)

#production = selectbox(
    #"Выберите кинокомпанию",
    #recsys.get_production()
#)
rate = st.slider(
    'Select a range of movies',
    0.0, 10.0, (0.0, 10.0)
)


if st.button('Показать рекоммендации'):
    st.write("Рекомендованные фильмы:")
    recommended_movie_names = recsys.recommendation(selected_movie, genre, rate, top_k=TOP_K)
    recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)

    if len(recommended_movie_names) == 0:
        st.write("Нет рекомендаций для выбранных параметров")
    else:
        movies_col = st.columns(TOP_K, gap="medium")
        for index, col in enumerate(movies_col):
            if index < len(recommended_movie_names):
                with col:
                    st.subheader(recommended_movie_names[index])
                    st.image(recommended_movie_posters[index])
            else:
                st.write("Недостаточно фильмов для рекомендаций")

