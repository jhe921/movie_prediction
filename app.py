import os
import streamlit as st
import pandas as pd
from movie_prediction.constants import PREDICTION, DATA_DIR, ACTORS_LINES_DEFAULT, UTTERANCE, PRINCIPAL
from movie_prediction.data_loaders.processed import load_actor_movie_lines
from movie_prediction.utils import sanitize_string
from movie_prediction.wrappers import DistilBertForPrincipalPredictionWrapper

DATA_PATH = DATA_DIR + '/' + ACTORS_LINES_DEFAULT

@st.cache(allow_output_mutation=True)
def load_model_wrapper():
    model_wrapper = DistilBertForPrincipalPredictionWrapper()
    return model_wrapper

@st.cache(allow_output_mutation=True)
def load_dataset():
    if os.path.isfile(DATA_PATH):
        dataset = load_actor_movie_lines(DATA_PATH)
    else:
        dataset = None
    return dataset


if __name__ == '__main__':
    st.title('Movie Principal Prediction App')
    utterance = None
    sample_utterance = None
    dataset = load_dataset()
    button = False
    principal = None

    if dataset is not None:
        button = st.button("Sample From Dataset")
    if button:
        sample = dataset.sample(1)
        sample_utterance = sample[UTTERANCE].values[0]
        principal = sample[PRINCIPAL].values[0]
    text_utterance = st.text_input('Enter some text')
    utterance = sample_utterance or text_utterance

    if utterance:
        model_wrapper = load_model_wrapper()
        st.info(utterance)
        if principal is not None:
            st.info(f"Principal Who Said This: {principal}")

        utterance = sanitize_string(utterance, upper=True, alphanumeric_only=True, strip=True, whitespace=True)
        predicted = model_wrapper.predict(utterance)
        predicted = pd.DataFrame.from_dict(
            predicted, orient='index', columns=[PREDICTION])
        predicted[PREDICTION] = (100 * predicted[PREDICTION]).round(2).astype(str) + ' %'
        st.dataframe(predicted)
