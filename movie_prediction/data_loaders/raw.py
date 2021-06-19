import pandas as pd

from movie_prediction.utils import sanitize_string_column, extract_names
from movie_prediction.constants import *

__all__ = ['load_principal_character_data', 'load_movie_line_data']


def load_principal_character_data() -> pd.DataFrame:
    """
    This function reads the IMBD movie metadata dataset to create a dataframe which maps
    principals by their birth name to characters they played in a movie.

    ref: https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset?select=IMDb+title_principals.csv
    :return:
    """
    # First read all movie characters
    movie_characters = pd.read_csv(
        DATA_DIR + '/imdb_movie_meta/IMDb title_principals.csv',
        converters={"characters": lambda x: x.strip("[]").replace('"', '').split(", ")})
    movie_characters = movie_characters[
        movie_characters['category'].isin(['actor', 'actress'])
        & movie_characters['characters'].notnull()
        ].explode('characters')

    # Next read all movie principals and merge
    movie_principals = pd.read_csv('../data/imdb_movie_meta/IMDb names.csv')
    movie_characters = movie_characters.merge(
        movie_principals[['imdb_name_id', 'birth_name']], on='imdb_name_id')

    # Then read all movie titles and merge
    movie_titles = pd.read_csv('../data/imdb_movie_meta/IMDb movies.csv', converters={'year': str})
    movie_characters = movie_characters.merge(
        movie_titles[['imdb_title_id', 'original_title', 'year']], on='imdb_title_id')
    movie_characters['Year'] = movie_characters['year'].str.extract(r'.*(\d{4}).*').astype(int)[0]

    # Sanitize Character and Extract name elements
    movie_characters[CHARAC_RAW] = sanitize_string_column(
        movie_characters['characters'], upper=True, alphanumeric_only=True, strip=True, whitespace=True)
    movie_characters = pd.concat([
        movie_characters,
        pd.DataFrame(
            list(movie_characters[CHARAC_RAW].apply(extract_names).values),
            columns=[CHARAC_FIRST, CHARAC_LAST, CHARAC_FIRST_LAST, CHARAC_FULL])
    ], axis=1)

    # Finally process character, principals and titles data
    movie_characters[PRINCIPAL] = sanitize_string_column(
        movie_characters['birth_name'], upper=True, alphanumeric_only=True, strip=True, whitespace=True)
    movie_characters[TITLE] = sanitize_string_column(
        movie_characters['original_title'], upper=True, alphanumeric_only=True, strip=True, whitespace=True)
    movie_characters = movie_characters[[
        CHARAC_RAW, CHARAC_FIRST,
        CHARAC_LAST, CHARAC_FIRST_LAST,
        CHARAC_FULL, PRINCIPAL, TITLE, YEAR]]

    return movie_characters


def load_movie_line_data() -> pd.DataFrame:
    """
    This function reads the cornell movie scripts dataset to create a dataframe which maps movie lines to their
    character, title, and year.

    ref: https://www.kaggle.com/Cornell-University/movie-dialog-corpus
    :return:
    """
    # Read in movie lines
    movie_lines = pd.read_csv(
        DATA_DIR + '/cornell_movie_scripts/movie_lines.tsv',
        sep='\t', encoding='utf-8',
        error_bad_lines=False, warn_bad_lines=False,
        names=['lineID', 'characterID', 'movieID',
               'character name', 'utterance']
    )

    # Read in movie titles and merge
    movie_titles = pd.read_csv(
        '../data/cornell_movie_scripts/movie_titles_metadata.tsv',
        sep='\t', encoding='utf-8',
        error_bad_lines=False,
        names=['movieID', 'movie title', 'movie year', 'IMDB rating',
               'IMDB votes', 'genres'],
        converters={'movie year': str}
    )
    movie_lines = movie_lines.merge(movie_titles[['movieID', 'movie title', 'movie year']], on='movieID')

    # Sanitize Character, Title, Year, and Utterance columns
    movie_lines[CHARAC] = sanitize_string_column(
        movie_lines['character name'], upper=True, alphanumeric_only=True, strip=True, whitespace=True)
    movie_lines[TITLE] = sanitize_string_column(
        movie_lines['movie title'], upper=True, alphanumeric_only=True, strip=True, whitespace=True)
    movie_lines[YEAR] = movie_lines['movie year'].str.extract(r'.*(\d{4}).*').astype(int)[0]
    movie_lines[UTTERANCE] = sanitize_string_column(movie_lines['utterance'].astype(str), whitespace=True)

    return movie_lines[[CHARAC, TITLE, YEAR, UTTERANCE]]
