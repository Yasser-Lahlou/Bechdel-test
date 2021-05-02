import numpy as np
import streamlit as st
import os
from PIL import Image
from streamlit import caching

from settings import *
from processing_color import *

# functions
@st.cache
def colorize_image(image, model_selection):
    if model_selection == model_names[0]:
        return process_img(image)[1]
    if model_selection == model_names[1]:
        return process_img(image)[2]

# image selection
st.sidebar.title('Choose your image')
choice = st.sidebar.radio('', options=['Upload your image', 'Use a demo image'])
if choice == 'Upload your image':
    image_file = st.sidebar.file_uploader('', type=["png", "jpg", "jpeg"])

elif choice == 'Use a demo image':
    demo_selection = st.sidebar.selectbox('', demo_images_names)
    image_file = demo_images_dict[demo_selection]

st.sidebar.write('Note: if you upload an RGB image, the app will first convert it to a greyscale image, then apply colorization')

# model selection
st.sidebar.title('Choose your model')
model_selection = st.sidebar.selectbox('', model_names)

# colorize button
button = st.sidebar.button('Colorize !')

# trivia
st.sidebar.title('About this app')
st.sidebar.write("""The deep learning models used by this app were designed
by authors Zhang, Richard and Isola. Check out [this link]
(http://richzhang.github.io/colorization) for further information.""")

# image credits
st.sidebar.title('Image Credits')
st.sidebar.write("""Photos by Nam Đặng, Ryan Hoffman,
Lizgrin F & Jean Carlo Emer on [Unsplash](https://unsplash.com)""")

# title and one-line explanation
st.title("Image Colorization")
st.write("Use a pre-trained deep learning model to bring grayscale images to life !")

col1, col2 = st.beta_columns([1,2])
# original image
col1.subheader("**Original image**")
if image_file is not None:
    image = np.array(Image.open(image_file))
    col1.image(image, use_column_width=True)

# processed image
col2.subheader("**Colorized image**")
if button:
    if image_file is not None:
        proc_image = colorize_image(image, model_selection)
        col2.image(proc_image, use_column_width=True)
    else :
        st.warning("Upload an image first !")
        st.stop()
