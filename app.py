import requests
import json
import streamlit as st
import os
from PIL import Image


def save_uploaded_image(uploaded_image):
    try:
        with open(os.path.join('uploads', uploaded_image.name), 'wb') as g:
            g.write(uploaded_image.getbuffer())
        return True
    except:
        return False


def query(url, headers, filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", url, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def classify(image):
    url = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
    headers = {"Authorization": "Bearer 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"}
    return query(url, headers, image)


def identify(image):
    url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
    headers = {"Authorization": "Bearer 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"}
    return query(url, headers, image)


st.write('Indraneel Dey')
st.write('Indian Institute of Technology, Madras')
st.title('Image Analysis')

st.write('If you want to know what an image is about:')
picture = st.file_uploader('Choose the image you want to classify')
if picture is not None:
    if save_uploaded_image(picture):
        st.image(Image.open(picture))
        st.text(classify(str(os.path.join('uploads', picture.name)))[0]['label'])
    else:
        st.write('Image did not upload properly')

st.write('If you want to identify objects present in an image:')
photo = st.file_uploader('Choose the image whose objects you want to identify')
if photo is not None:
    if save_uploaded_image(photo):
        st.image(Image.open(photo))
        result = identify(str(os.path.join('uploads', photo.name)))
        st.text(', '.join([i['label'] for i in result]))
    else:
        st.write('Image did not upload properly')
