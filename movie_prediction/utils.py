import re
from typing import Tuple

import pandas as pd

__all__ = ['sanitize_string', 'sanitize_string_column', 'extract_names']

__ALPHANUMERIC_REGEX = re.compile(r'[^0-9A-Za-z\s]')
__SPACING_REGEX = re.compile(r'\s+')


def sanitize_string(text: str,
                    upper: bool = False,
                    alphanumeric_only: bool = False, strip: bool = False,
                    whitespace: bool = False) -> str:
    """
    Function for conditionally sanitizing a string.

    :param text: str,
        the string to sanitize
    :param upper: bool, default False
        whether to convert the series to uppercase
    :param alphanumeric_only:
        whether to remove all non alpha-numeric characters
    :param strip: bool, default False
        whether to strip whitespace around the series
    :param whitespace: bool, default False
        whether to sanitize all whitespace characters to single spaces
    :return:
        text: str
        The sanitized string.
    """
    if alphanumeric_only:
        text = re.sub(__ALPHANUMERIC_REGEX, ' ', text)
    if whitespace:
        text = re.sub(__SPACING_REGEX, ' ', text)
    if strip:
        text = text.strip()
    if upper:
        text = text.upper()

    return text


def sanitize_string_column(series: pd.Series, upper: bool = False,
                           alphanumeric_only: bool = False, strip: bool = False,
                           whitespace: bool = False) -> pd.Series:
    """
    Function for conditionally sanitizing string series in pandas.

    :param series: pd.Series,
        the pandas series containing strings to sanitize
    :param upper: bool, default False
        whether to convert the series to uppercase
    :param alphanumeric_only:
        whether to remove all non alpha-numeric characters
    :param strip: bool, default False
        whether to strip whitespace around the series
    :param whitespace: bool, default False
        whether to sanitize all whitespace characters to single spaces
    :return:
        series: pd.Series
        The sanitized Pandas series.

    """

    if alphanumeric_only:
        series = series.str.replace(__ALPHANUMERIC_REGEX, ' ')
    if whitespace:
        series = series.str.replace(__SPACING_REGEX, ' ')
    if strip:
        series = series.str.strip()
    if upper:
        series = series.str.upper()
    return series


def extract_names(text: str) -> Tuple[str, str, str, str]:
    """
    Function for extracting names from a string.
    Assumes string spaces have been sanitized.
    :param text:
    :return:
        (first, last, first_last, full)
        A tuple containing the first name, last name, first name + last name combination, and the full name.
    """
    '''

    '''
    if text.startswith('LT '):
        text = text.lstrip('LT ')
    if text.startswith('MR '):
        text = text.lstrip('MR ')
    if text.startswith('MS '):
        text = text.lstrip('MS ')
    if text.startswith('MRS '):
        text = text.lstrip('MRS ')
    if text.startswith('MISS '):
        text = text.lstrip('MISS ')

    first, last, first_last, full = None, None, None, text
    n_spaces = text.count(' ')
    if n_spaces == 0:
        first = text
    elif n_spaces == 1:
        first, last = text.split(' ')
        first_last, full = text, text
    elif n_spaces > 1:
        first, middle, last = text.split(' ')[:3]
        first_last, full = ' '.join([first, last]), ' '.join([first, middle, last])

    return first, last, first_last, full

