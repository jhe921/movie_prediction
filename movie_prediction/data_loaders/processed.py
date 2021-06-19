import os
import pandas as pd

from movie_prediction.data_loaders.raw import load_actor_character_data, load_movie_line_data
from movie_prediction.constants import *

__all__ = ['load_actor_movie_lines']


def load_actor_movie_lines(cache_fp: str = None, export_fp: str = None) -> pd.DataFrame:
    """
    Function for creating/loading actor and movie lines dataset.

    :param cache_fp:
    :param export_fp:
    :return:
    """
    if cache_fp == export_fp:
        raise ValueError("Cache filepath cannot be the same as export filepath.")

    if cache_fp and os.path.isfile(cache_fp):
        print(f"Loading actor lines from cache: {cache_fp}")
        actor_lines = pd.read_csv(cache_fp, sep='\t')
    else:
        print("Creating actor movie lines dataset...")
        # Load Actors Characters Dataset
        print("Loading Actors Data...")
        characters = load_actor_character_data()
        raw_char_num = len(characters)
        print(f"Raw Number of Characters: {raw_char_num}")

        # Load Character Movie Lines
        print("Loading Characters Movie Lines Data...")
        movie_lines = load_movie_line_data()
        movie_lines = movie_lines.reset_index().rename(columns={'index': LINE_ID})
        raw_line_num = len(movie_lines)
        print(f"Raw number of lines: {raw_line_num}")

        # Attempt to Merge Actors Using Character Names
        print("Merging Actors and Character Lines...")
        MERG_COLS = [
            CHARAC_RAW, CHARAC_FIRST,
            CHARAC_LAST, CHARAC_FIRST_LAST,
            CHARAC_FULL,
        ]
        merged_line_ids = set()
        actor_lines = []
        for merge_col in MERG_COLS:
            merged_filt = movie_lines[LINE_ID].isin(merged_line_ids)
            data = movie_lines[~merged_filt].merge(
                characters, left_on=[CHARAC, TITLE, YEAR],
                right_on=[merge_col, TITLE, YEAR],
                how='inner'
            )
            merged_line_ids.update(data[LINE_ID].values)
            actor_lines.append(data)
        actor_lines = pd.concat(actor_lines)

        # Some characters have more than one actor
        # Assign lines to the principal with more total lines in our dataset
        print("Assigning Lines with Conflicting Actors...")
        num_duplicates = actor_lines[LINE_ID].duplicated(keep=False).value_counts()[True]
        print(f"Number of Ambiguous Actor Lines: {num_duplicates}")
        actor_lines = actor_lines.merge(
            actor_lines[PRINCIPAL].value_counts().reset_index().rename(
                columns={PRINCIPAL: PRINCIPAL_LINES, 'index': PRINCIPAL}),
                on=PRINCIPAL, how='left')
        actor_lines = actor_lines.sort_values(
            by=[PRINCIPAL_LINES, PRINCIPAL],
            ascending=False
        ).drop_duplicates(subset=[LINE_ID], keep='first')

        # Count Merge statistics
        merged_line_num = len(actor_lines)
        print(f"Lines after actor merge: {merged_line_num} ({100 * merged_line_num / raw_line_num:.2f} %)")

    if export_fp:
        print(f"Exporting actor lines to: {export_fp}")
        actor_lines.to_csv(export_fp, sep='\t', index=False)

    return actor_lines