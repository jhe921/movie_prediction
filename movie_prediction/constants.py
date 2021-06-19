import os

# Directories
HOME_DIR = os.path.abspath(
    os.path.dirname(__file__) + '/../').replace('\\', '/')
DATA_DIR = HOME_DIR + '/data'
MODEL_DIR = HOME_DIR + '/models'

# Column Names
LINE_ID = 'Line ID'
PRINCIPAL = 'Principal'
TITLE = 'Title'
YEAR = 'Year'
UTTERANCE = 'Utterance'
UTTERANCE_HASH = 'Utterance Hash'
UTTERANCE_SAN = 'Utterance (sanitized)'
PRINCIPAL_LINES = 'Principal Lines'
PREDICTION = 'Prediction'

CHARAC = 'Character'
CHARAC_RAW = 'Character (Raw)'
CHARAC_FIRST = 'Character (First)'
CHARAC_LAST = 'Character (Last)'
CHARAC_FIRST_LAST = 'Character (First+Last)'
CHARAC_FULL = 'Character (Full)'

# Model Names


## Language Models
HUGGINGFACE_PRETRAINED = 'distilbert-base-uncased'
MOVIE_TUNED = 'distilbert-base-uncased-movie-tuned'

## Build on pretrained LM
PRINC_PRED_MODEL = 'principal-prediction'
PRINC_PRED_MODEL_INF = 'principal-prediction-inference'

## Built on tuned LM
PRINC_PRED_MODEL_TUNED = 'principal-prediction-tuned'
PRINC_PRED_MODEL_TUNED_INF = 'principal-prediction-tuned-inference'

# Default Values
WORD_LIMIT_DEFAULT = 75
TOKENIZER_ARGS_DEFAULT = {
    'padding': True, 'truncation': True,
    'max_length': WORD_LIMIT_DEFAULT
}
PRINCIPALS_LINES_DEFAULT = 'principal_lines.tsv'