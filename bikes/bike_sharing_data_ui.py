import streamlit as st
import pandas as pd
import numpy as np
import collections
from collections import Counter
from bikes import data_wrangeling_and_filtering as dwaf


def get_data_dir():
    this_dir = os.path.dirname(__file__)
    return os.path.realpath("%s/../data/" % this_dir)


def get_filename(city_name):
    return "%s/%s.csv" % (get_data_dir(), city_name)


def read_data_into_df(city_name):
    city_name = city_name.lower().replace(' ', '_')
    file_name = get_filename(city_name)
    df = pd.read_csv(file_name)
    return df


def run():
    st.title('Explore Motivates US Bike-Sharing Data')
    # Initial selection of city
    city_name = st.sidebar.selectbox(
        'Please select a city:',
        ('Chicago', 'New York City', 'Washington')
    )
    # Initial selection of additional filters
    more_filters = st.sidebar.selectbox(
        'Would you like to filter?',
        ('Month', 'Day', 'Month & Day', 'No additional filter')
    )

    # Displaying additional filter options based on filter selection
    if more_filters == 'Month & Day':
        month = st.sidebar.selectbox(
            'Please select a month:',
            ('January', 'February', 'March', 'April', 'May', 'June')
        )
        day = st.sidebar.selectbox(
            'Please select a day:',
            ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        )
        if month != 'all':
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month_index = months.index(month) + 1

    elif more_filters == 'Month':
        month = st.sidebar.selectbox(
            'Please select a month:',
            ('January', 'February', 'March', 'April', 'May', 'June')
        )
        if month != 'all':
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month_index = months.index(month) + 1

    elif more_filters == 'Day':
        day = st.sidebar.selectbox(
            'Please select a day:',
            ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        )
    elif more_filters == 'No additional filter':
        st.write("No more filters")


    # calling the functions and create a new df based on the user input
    load = read_data_into_df(city_name.lower())
    clean = dwaf.create_new_date_columns(load)

    # preparing optional filter values for filter function
    try:
        month_index
    except NameError:
        month_index = None

    try:
        day
    except NameError:
        day = None

    # final data frame for display
    final_df = dwaf.filter_data_frame_with_user_input(clean, month_index, day)

    # STARTING THE ANALYTICS SECTION
    st.subheader("Explore your selection below:")
    st.write('Here are the first random 5 rows.')
    st.dataframe(final_df.head(5))

    # 1 Popular times of travel
    common_hour = final_df['Hour Start Time'].value_counts().idxmax()

    if month_index is None and day is not None:
        common_month = final_df['month'].value_counts().idxmax()
        st.write("The most common travel month is {} and the most common travel hour is {}:00. Below is a histogram of \n"
                 "how start-time is distributed throughout a 24h day within your \n"
                 "selection:".format(common_month, common_hour))

    if day is None and month_index is not None:
        common_day = final_df['day_of_week'].value_counts().idxmax()
        st.write("The most common travel day is {} and the most common travel hour is {}:00. Below is a histogram of how \n"
                 "start-time is distributed throughout a 24h day within your selection:".format(common_day, common_hour))

    if day is None and month_index is None:
        common_month = final_df['month'].value_counts().idxmax()
        common_day = final_df['day_of_week'].value_counts().idxmax()
        st.write("The most common travel month is {} and the most common travel month is {}:00. Moreover, the most common \n"
                 "travel hour is {}. Below is a histogram of how start-time is distributed throughout a 24h day within your \n"
                 "selection:".format(common_month,common_day, common_hour))

    # start-time distribution as histogram
    hist_values = np.histogram(
        final_df['Start Time'].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)


    #2 Popular stations and trip
    common_start_station = [station for station, station_count in Counter(final_df['Start Station']).most_common(3)]
    common_end_station = [station for station, station_count in Counter(final_df['End Station']).most_common(3)]
    most_frequent_combination = final_df.groupby(['Start Station', 'End Station']).count().idxmax()

    st.write('The most common start station is - {} - and the most common end station is - {} -. The most frequent combination of \n'
             'start station and end station is shown in the table below.'.format(common_start_station[1],common_end_station[1]))
    st.table(most_frequent_combination[0])

    # 3 Trip duration

    # creating a new column for time delta in hours
    final_df['diff_hours'] = final_df['End Time'] - final_df['Start Time']
    final_df['diff_hours'] = final_df['diff_hours'] / np.timedelta64(1, 'h')

    # then using this column to get statistics
    total_travel = final_df['diff_hours'].sum()
    mean = final_df['diff_hours'].mean().round(2)
    total_travel_display = "There are a total of {0:02.0f} hours and {1:02.0f} minutes of travel time in your \n" \
                           "selection.".format(*divmod(total_travel * 60, 60))
    mean_display = "Moreover, people have traveled an average of {} hours in your selection.".format(mean)
    st.write(total_travel_display, mean_display)

    # 4 User info

    # count user types
    st.subheader("Count User Types:")
    st.write("Explore different user types")
    count_user_types = pd.DataFrame(final_df)
    st.table(count_user_types['User Type'].value_counts())

    # counts of each gender (only available for NYC and Chicago)
    if city_name is not 'Washington':
        st.subheader("Count Gender:")
        st.write("Explore the gender distribution")
        count_gender = pd.DataFrame(final_df)
        st.table(count_gender['Gender'].value_counts())

    # earliest, most recent, most common year of birth (only available for NYC and Chicago)
    if city_name is not 'Washington':
        st.subheader("Birth Year Distribution:")

        most_common = int(final_df['Birth Year'].mode())
        earliest = int(final_df['Birth Year'].min())
        most_recent = int(final_df['Birth Year'].max())
        st.write("The oldest customer in your selection was born in {}. The youngest was born in {}. \n"
                 "The most common birth year in your selection is {}. Below is a histogram showing how \n"
                 "birth year is distributed within your selection:".format(earliest, most_recent, most_common))

    # birthday distribution histogram
    if city_name is not 'Washington':
        final_df = final_df.dropna(axis=0)
        final_df['Birth Year'] = final_df['Birth Year'].astype(int)
        st.bar_chart(final_df['Birth Year'].value_counts())


if __name__ == "__main__":
    run()
