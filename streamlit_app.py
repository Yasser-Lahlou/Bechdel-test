import streamlit as st
from streamlit import caching
from PIL import Image

from functions import *

# functions
@st.cache
def call_generators():
    female_names = female_names_generator('data/female_names.txt')
    male_names = male_names_generator('data/male_names.txt')
    df_movies = movie_titles_generator('data/movie_titles.csv')
    return female_names, male_names, df_movies

# trivia - Bechdel Test
st.sidebar.title('About the Bechdel test')
st.sidebar.write("""The Bechdel test, also known as the Bechdel–Wallace test,
is a measure of the representation of women in fiction. It asks whether a work
features at least two women who talk to each other about something other than a man.
For more information, please check the Bechdel Test page on [Wikipedia]
(https://en.wikipedia.org/wiki/Bechdel_test).""")

# trivia - IMSDB
st.sidebar.title('Credits')
st.sidebar.write("""The movie scripts were provided by [The Internet Movie
Script Database](https://imsdb.com/all-scripts.html).""")


# title and one-line explanation
st.title("Bechdel test")
st.write("""Perform the Bechdel test, a measure of the representation of women
in fiction, on 1000+ movies.""")
st.image(Image.open('data/Bechdel_test.png'))

# search for a movie
female_names, male_names, df = call_generators()
selected_movie = st.selectbox('Search for a movie', df['clean_title'])
selected_movie_title = df[df['clean_title'] == selected_movie]['title'].item()
selected_path = f"IMSDB_scripts/{selected_movie_title}.txt"

# perform the tests
script = read_script(selected_path)
result_1 = bechdel_test_1(script, female_names)
result_2 = bechdel_test_2(script, female_names)
result_3 = bechdel_test_3(script, female_names, male_names)

#show the results
test_passed = '**Bechdel Test Passed !**'
test_failed = '**Bechdel Test Failed !**'
answer_1_pos = ':white_check_mark: 2 women or more are named in the script'
answer_1_neg = ':x: Less than 2 women are named in the script'
answer_2_pos = ':white_check_mark: There is a scene where 2 women or more are talking'
answer_2_neg = ':x: There is no scene where at least 2 women are talking'
answer_3_pos = ':white_check_mark: There is a scene where 2 women or more are talking about anything but men'
answer_3_neg = ":x: There are scenes where 2 women are talking, but they are talking about men"
not_tested = ':heavy_minus_sign: Not tested'

if result_1:
    if result_2:
        if result_3:
            st.title(test_passed)
            st.write(answer_1_pos)
            st.write(answer_2_pos)
            st.write(answer_3_pos)
        else:
            st.title(test_failed)
            st.write(answer_1_pos)
            st.write(answer_2_pos)
            st.write(answer_3_neg)
    else:
        st.title(test_failed)
        st.write(answer_1_pos)
        st.write(answer_2_neg)
        st.write(not_tested)
else:
    st.title(test_failed)
    st.write(answer_1_neg)
    st.write(not_tested)
    st.write(not_tested)
