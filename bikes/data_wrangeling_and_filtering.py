import pandas as pd
import datetime as dt


# applying some data wrangling
def create_new_date_columns(df):
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Hour Start Time'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df[['Start Time']].apply(
        lambda x: dt.datetime.strftime(x['Start Time'], '%A'), axis=1)
    return df


# filtering the df based on user input
def filter_data_frame_with_user_input(df, month=None, day=None):
    if month is not None and day is None:
        df = df[df['month'] == month]
        return df
    elif day is not None and month is None:
        df = df[df['day_of_week'] == day]
        return df
    elif day is not None and month is not None:
        df = df[df['month'] == month]
        df = df[df['day_of_week'] == day]
        return df
    elif day is None and month is None:
        return df
