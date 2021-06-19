import os
import pandas as pd

from movie_prediction.data_loaders.raw import load_principal_character_data, load_movie_line_data
from movie_prediction.constants import *

__all__ = ['load_principal_movie_lines']


def load_principal_movie_lines(cache_fp: str = None) -> pd.DataFrame:
    """
    Function for creating/loading principal and movie lines dataset.

    :param cache_fp: str
        Path to file used for caching processed data.
    :return:
        pd.DataFrame
    """
    if cache_fp and os.path.isfile(cache_fp):
        print(f"Loading principal lines from cache: {cache_fp}")
        principal_lines = pd.read_csv(cache_fp, sep='\t', converters={UTTERANCE: str})
    else:
        print("Creating principal movie lines dataset...")
        # Load Principals Characters Dataset
        print("Loading principals Data...")
        characters = load_principal_character_data()
        raw_char_num = len(characters)
        print(f"Raw Number of Characters: {raw_char_num}")

        # Load Character Movie Lines
        print("Loading Characters Movie Lines Data...")
        movie_lines = load_movie_line_data()
        movie_lines = movie_lines.reset_index().rename(columns={'index': LINE_ID})
        raw_line_num = len(movie_lines)
        print(f"Raw number of lines: {raw_line_num}")

        # Attempt to Merge Principals Using Character Names
        print("Merging Principals and Character Lines...")
        MERG_COLS = [
            CHARAC_RAW, CHARAC_FIRST,
            CHARAC_LAST, CHARAC_FIRST_LAST,
            CHARAC_FULL,
        ]
        merged_line_ids = set()
        principal_lines = []
        for merge_col in MERG_COLS:
            merged_filt = movie_lines[LINE_ID].isin(merged_line_ids)
            data = movie_lines[~merged_filt].merge(
                characters, left_on=[CHARAC, TITLE, YEAR],
                right_on=[merge_col, TITLE, YEAR],
                how='inner'
            )
            merged_line_ids.update(data[LINE_ID].values)
            principal_lines.append(data)
        principal_lines = pd.concat(principal_lines)

        # Some characters have more than one principal
        # Assign lines to the principal with more total lines in our dataset
        print("Assigning Lines with Conflicting Principals...")
        num_duplicates = principal_lines[LINE_ID].duplicated(keep=False).value_counts()[True]
        print(f"Number of Ambiguous Principal Lines: {num_duplicates}")
        principal_lines = principal_lines.merge(
            principal_lines[PRINCIPAL].value_counts().reset_index().rename(
                columns={PRINCIPAL: PRINCIPAL_LINES, 'index': PRINCIPAL}),
                on=PRINCIPAL, how='left')
        principal_lines = principal_lines.sort_values(
            by=[PRINCIPAL_LINES, PRINCIPAL],
            ascending=False
        ).drop_duplicates(subset=[LINE_ID], keep='first')

        # Count Merge statistics
        merged_line_num = len(principal_lines)
        print(f"Lines after principal merge: {merged_line_num} ({100 * merged_line_num / raw_line_num:.2f} %)")
        if cache_fp:
            print(f"Exporting principal lines to: {cache_fp}")
            principal_lines.to_csv(cache_fp, sep='\t', index=False)

    return principal_lines
