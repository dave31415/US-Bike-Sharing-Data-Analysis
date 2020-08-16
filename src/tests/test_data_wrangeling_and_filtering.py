import pytest
import calendar
import numpy as np
import pandas as pd
from src.main import data_wrangeling_and_filtering as dwaf

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def input_df():
    return pd.DataFrame({'Start Time': ['2017-06-23 15:09:32'],
                         'End Time': ['2017-06-23 15:09:32']})


def weekday_from_date(df):
    return calendar.day_name(df)


def test_should_apply_timestamp_to_start_time():
    df = dwaf.create_new_date_columns(input_df())

    assert type(df['Start Time'][0]) is pd._libs.tslibs.timestamps.Timestamp


def test_should_apply_timestamp_to_end_time():
    df = dwaf.create_new_date_columns(input_df())

    assert type(df['End Time'][0]) is pd._libs.tslibs.timestamps.Timestamp


def test_should_create_hour_start_time_column():
    df = dwaf.create_new_date_columns(input_df())

    assert type(df['Hour Start Time'][0]) is np.int64


def test_should_create_month_column():
    df = dwaf.create_new_date_columns(input_df())

    assert type(df['month'][0]) is np.int64


def test_should_create_day_of_week_column():
    df = dwaf.create_new_date_columns(input_df())

    assert df['day_of_week'][0] in days
