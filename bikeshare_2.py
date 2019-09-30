import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            city = (input("Which city are you interested in? Please choose from: chicago, new york city, washington : "))
            city=city.lower()
        except:
            print("Oops!  That was not a valid city.  Try again...")
        else:
            if city in CITY_DATA:
                print(city)
                break
            else:
                print("Oops!  That was not a valid city.  Try again...")

    while True:
        try:
            month = (input("Which month are you interested in? (january, february, march, april, may, june or all)"))
            month=month.lower()
        except:
            print("Oops!  That was not a valid month.  Try again...")
        else:
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                print(month)
                break
            else:
                print("Oops!  That was not a valid month.  Try again...")

    while True:
        try:
            day = (input("Which day are you interested in? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all)"))
            day=day.lower()
        except:
            print("Oops!  That was not a valid day.  Try again...")
        else:
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                print(day)
                break
            else:
                print("Oops!  That was not a valid day.  Try again...")

    # get user input for city, month and day with handeling exceptions



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

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month=df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day=df['day'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    route='From ' + df['Start Station']+ ' til ' + df['End Station']
    popular_route = route.mode()[0]
    print('Most Popular route:', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hour=total_travel_time*0.00028
    print('The total travel time in hours was:', total_travel_time_hour)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() * 0.0167
    print('The mean travel time in minutes was:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender


    # Display earliest, most recent, and most common year of birth
    if  'Gender' in df:
        gender = df['Gender'].value_counts()
        print(gender)
        earliest_year_of_birth=df['Birth Year'].min()
        print('The earliest year of birth is :', earliest_year_of_birth)
        most_recent_year_of_birth=df['Birth Year'].max()
        print('The most recent year of birth is :', most_recent_year_of_birth)
        most_common_year_of_birth=df['Birth Year'].mode()[0]
        print('The most common year of birth is :', most_common_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        answer = input("Do you want to see raw data?")
        if answer.lower() != 'yes':
            break
        else:
            print(df.head())

            counter=5
            while True:
                try:
                    answer_more = (input("Do you want to see 5 more rows of data?"))
                except:
                    break
                else:
                    if answer_more.lower() == 'yes' :
                        counter+=5
                        print(df.head(counter))
                    else:
                        print('No more raw data to be displayed.')
                        break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
