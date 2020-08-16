import pytest
import numpy as np
import pandas as pd

from src.main import data_wrangeling_and_filtering as dwaf

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
january = '1'
monday = 'Monday'


def input_df_columns_creation():
    return pd.DataFrame({'Start Time': ['2017-06-23 15:09:32'],
                         'End Time': ['2017-06-23 15:09:32']})


def input_df_for_filtering():
    return pd.DataFrame({'Start Time': ['2017-03-23 15:09:32',
                                        '2017-01-23 15:09:32'],
                         'End Time': ['2017-06-23 15:09:32',
                                      '2017-07-23 15:23:32'],
                         'month': ['3',
                                   '1'],
                         'day_of_week': ['Thursday',
                                         'Monday']
                         })


def test_should_apply_timestamp_to_start_time():
    df = dwaf.create_new_date_columns(input_df_columns_creation())

    assert type(df['Start Time'][0]) is pd._libs.tslibs.timestamps.Timestamp


def test_should_apply_timestamp_to_end_time():
    df = dwaf.create_new_date_columns(input_df_columns_creation())

    assert type(df['End Time'][0]) is pd._libs.tslibs.timestamps.Timestamp


def test_should_create_hour_start_time_column():
    df = dwaf.create_new_date_columns(input_df_columns_creation())

    assert type(df['Hour Start Time'][0]) is np.int64


def test_should_create_month_column():
    df = dwaf.create_new_date_columns(input_df_columns_creation())

    assert type(df['month'][0]) is np.int64


def test_should_create_day_of_week_column():
    df = dwaf.create_new_date_columns(input_df_columns_creation())

    assert df['day_of_week'][0] in days


def test_should_return_df_filtered_by_month():
    df = dwaf.filter_data_frame_with_user_input(input_df_for_filtering(), january, None)
    df.reset_index(drop=True, inplace=True)

    assert len(df) == 1
    assert df['month'][0] == january


def test_should_return_df_filtered_by_day():
    df = dwaf.filter_data_frame_with_user_input(input_df_for_filtering(), None, monday)
    df.reset_index(drop=True, inplace=True)

    assert len(df) == 1
    assert df['day_of_week'][0] == monday


def test_should_return_df_filtered_by_month_and_day():
    df = dwaf.filter_data_frame_with_user_input(input_df_for_filtering(), january, monday)
    df.reset_index(drop=True, inplace=True)

    assert len(df) == 1
    assert df['day_of_week'][0] == monday
    assert df['month'][0] == january


def test_should_return_df_without_month_or_day_filter():
    df = dwaf.filter_data_frame_with_user_input(input_df_columns_creation())

    assert df.equals(input_df_columns_creation())
