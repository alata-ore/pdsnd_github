import time
import calendar
import pandas as pd
import numpy as np

from datetime import date

CITY_DATA = { 'chicago': './Project 2 - Bikeshare Data/chicago.csv',
              'new york city': './Project 2 - Bikeshare Data/new_york_city.csv',
              'washington': './Project 2 - Bikeshare Data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    available_cities = ['chicago', 'new york city', 'washington']
    city = input('Would you like to see data for {}, {}, or {}? > '.format(available_cities[0].title(), available_cities[1].title(), available_cities[-1].title()))
    while city.lower() not in available_cities:
        city = input('Sorry! We don\'t have data for that city, please choose {}, {}, or {}. > '.format(available_cities[0].title(), available_cities[1].title(), available_cities[-1].title()))

    # TO DO: get user input for month (all, january, february, ... , june)
    available_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('Which month (January -> June) would you like to see (or type \'All\' for all months)? > ')
    while month.lower() not in available_months:
        month = input('Sorry! We don\'t have data for that month, please choose from January to June. > ')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day would you like to see (or type \'All\' for all days)? > ')
    while day.title() not in calendar.day_name and day.lower() != 'all':
        day = input('Hmmm, that doesn\'t look right, please try again. > ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city.lower()))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday

    # extract hour from Start Time as a new column for use in determining most common hour
    df['hour'] = df['Start Time'].dt.hour

    # extract Start & End Stations as a new column for use in determining most common start/end
    df['Start End'] = df['Start Station'] + '--' + df['End Station']

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day.lower()) + 1

        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day]

    # fill any NaN's in gender with not supplied
    if city.lower() == 'washington':
        df['Gender'] = 'Not Supplied'
    else:
        df['Gender'].fillna('Not Supplied', inplace=True)

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for {}...\n'.format(city.title()))
    start_time = time.time()

    # set values for strings used in data descriptions: either day/month chosen or "all weekdays/months"
    if day.lower() == 'all':
        day_chosen = 'all weekday\'s'
    else:
        day_chosen = day.title()

    if month.lower() == 'all':
        month_chosen = 'all month\'s'
    else:
        month_chosen = month.title()

    # TO DO: display the most common month
    if month != 'all':
        # user has chosen a single month, needs to choose all months to get the most common
        print('Choose all months to see which is the most common month.\n')
    else:
        month_common = calendar.month_name[df['month'].mode()[0]]
        month_count = (df['month'] == df['month'].mode()[0]).sum()
        month_percent = round((month_count / df['month'].count()) * 100, 2)
        print('Our most popular month for {} rentals with {}% of rental occurrences is: {}\n'.format(day_chosen, month_percent, month_common))

    # TO DO: display the most common day of week
    if day != 'all':
        # user has chosen a single day, needs to choose all days to get the most common
        print('Choose all days to see which is the most common day.\n')
    else:
        day_common = calendar.day_name[df['weekday'].mode()[0]]
        day_count = (df['weekday'] == df['weekday'].mode()[0]).sum()
        day_percent = round((day_count / df['weekday'].count()) * 100, 2)
        print('Our most popular day for {} rentals with {}% of rental occurrences is: {}\n'.format(month_chosen, day_percent, day_common))

    # TO DO: display the most common start hour
    # convert hour to 12hr format
    if df['hour'].mode()[0] == 0:
        hour_common = '{}am'.format(df['hour'].mode()[0] + 12)
    elif df['hour'].mode()[0] < 12:
        hour_common = '{}am'.format(df['hour'].mode()[0])
    elif df['hour'].mode()[0] == 12:
        hour_common = '{}pm'.format(df['hour'].mode()[0])
    else:
        hour_common = '{}pm'.format(df['hour'].mode()[0] - 12)

    hour_count = (df['hour'] == df['hour'].mode()[0]).sum()
    hour_percent = round((hour_count / df['hour'].count()) * 100, 2)
    print('Our most popular starting hour for rentals with {}% of rental occurrences is: {}\n'.format(hour_percent, hour_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip for {}...\n'.format(city.title()))
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_common = df['Start Station'].mode()[0]
    start_count = (df['Start Station'] == df['Start Station'].mode()[0]).sum()
    start_percent = round((start_count / df['Start Station'].count()) * 100, 2)
    print('Our most common starting station with {}% of bikers starting there is: {}\n'.format(start_percent, start_common))

    # TO DO: display most commonly used end station
    end_common = df['End Station'].mode()[0]
    end_count = (df['End Station'] == df['End Station'].mode()[0]).sum()
    end_percent = round((end_count / df['End Station'].count()) * 100, 2)
    print('Our most common end station with {}% of bikers finishing there is: {}\n'.format(end_percent, end_common))

    # TO DO: display most frequent combination of start station and end station trip
    # use the new column with combo of start/end stations
    combo_common = df['Start End'].mode()[0]
    combo_count = (df['Start End'] == df['Start End'].mode()[0]).sum()
    combo_percent = round((combo_count / df['Start End'].count()) * 100, 2)
    print('Our most common start & end station combination with {}% of bikers starting & finishing there is {} \n'.format(combo_percent, combo_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration for {}...\n'.format(city.title()))
    start_time = time.time()

    # Calculate hours, minutes, seconds
    def travel_time(trip_duration):
        travel_hours = int(trip_duration // 3600)
        travel_minutes = int((trip_duration % 3600) // 60)
        # returning whole seconds (not rounded to a decimal place)
        # as less than a second isn't a valuable slice of time for bike hire analysis
        travel_seconds = int(trip_duration - (travel_hours * 3600) - (travel_minutes * 60))
        if travel_hours != 0:
            return str(travel_hours) + 'h ' + str(travel_minutes) + 'm ' + str(travel_seconds) + 's'
        else:
            return str(travel_minutes) + 'm ' + str(travel_seconds) + 's'

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is: {}\n'.format(travel_time(total_time)))

    # TO DO: display mean travel time
    average_time = df['Trip Duration'].mean()
    print('The average travel time is (seconds have been rounded down to nearest whole second): {}\n'.format(travel_time(average_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for {}...\n'.format(city.title()))
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The number of customers for each user type are: ')
    print(df['User Type'].value_counts().to_string(), '\n')

    # TO DO: Display counts of gender
    print('The number of customers for each gender are: ')
    print(df['Gender'].value_counts().to_string(), '\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        # Get earliest year of birth
        earliest_birthyear = int(df['Birth Year'].min())
        earliest_age = int(date.today().year - earliest_birthyear)
        print('Our oldest customer is {}, having been born in {}. \n'.format(earliest_age, earliest_birthyear))

        # Get latest year of birth
        latest_birthyear = int(df['Birth Year'].max())
        latest_age = int(date.today().year - latest_birthyear)
        print('Our youngest customer is {}, having been born in {}. \n'.format(latest_age, latest_birthyear))

        # Get most common year of birth
        common_birthyear = int(df['Birth Year'].mode()[0])
        common_age = int(date.today().year - common_birthyear)
        birth_count = (df['Birth Year'] == df['Birth Year'].mode()[0]).sum()
        birth_missing = df['Birth Year'].isnull().sum()
        birth_percent = round((birth_count / (df['Birth Year'].count() + birth_missing)) * 100, 2)
        print('{} is the most common age amongst Bikeshare customers with {}% born in {}.'.format(common_age, birth_percent, common_birthyear))
        print('{} customers did not provide their birth year.'.format(birth_missing))
    else:
        # user chose a city which does not have birthdate data avaialable
        print('No age statistics, birth year is not recorded for Washington customers.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    while True:
        see_rows = input('Would you like to see 5 rows of raw data?\n')
        if see_rows.lower() == 'yes':
            print(df.sample(5))
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
