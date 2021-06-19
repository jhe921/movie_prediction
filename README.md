# Movie Prediction
This is my personal movie prediction repository.

# Installation 

## Basic
First Install [PyTorch](https://pytorch.org/), example:
```bash
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
```
Then install this repository:
```bash
pip install git+https://github.com/jhe921/movie_prediction.git
```

## Notebook
Training a principal prediction model requires runniing the `principal_prediction` notebook. In order to run the notebook you will need:
 - [jupyter](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) installed
 - The [cornell movie dialog corpus](https://www.kaggle.com/Cornell-University/movie-dialog-corpus) downloaded to `data/movie_prediction`
 - The [IMDb movies extensive dataset](https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset?select=IMDb+title_principals.csv) downloaded to `data/imdb_movie_meta`

## Language Model Tuning
To run this language model training without the notebook, export the `Utterances` column of your `actor_lines.tsv` file to a .txt file and run:
```bash
python run_mlm.py --model_name_or_path distilbert-base-uncased \
    --train_file <PATH-TO-YOUR-.txt-FILE> --do_train \
    --output_dir movie_prediction/models/distilbert-base-uncased-movie-tuned \
    --line_by_line --max_seq_len 75
```

## Interactive Streamlit App
To run the interactive streamlit app:
 1. Copy a principal prediction model to `movie_prediction/models/principal-prediction-tuned-inference` 
 1. Type `streamlit run app.py` into your shell

## FastAPI Model Serving
To serve a model with fastapi:
 1. Copy a principal prediction model to `movie_prediction/models/principal-prediction-tuned-inference` 
 1. Type `uvicorn main:app` into your shell