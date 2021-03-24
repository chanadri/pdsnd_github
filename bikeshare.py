import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

valid_city = ['chicago', 'new york city', 'washington']
valid_months = ['january','february','march','april','may','june','july','august','september','october','november','december']
valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    global city, month, day
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter a city (chicago, new york city, washington):\n').lower()
    while city not in valid_city:
        city = input('Please enter a valid city:\n').lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please enter a month (all, january, february, ... , june):\n').lower()
    while month not in valid_months:
        if month == "all":
            break
        else:
            month = input('Please enter a valid month or "all" for all values:\n').lower()
        
            
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day of week (all, monday, tuesday, ... sunday):\n').lower()
    while day not in valid_days:
        if day == "all":
            break
        else:
            day = input('Please enter a valid day of week or "all" for all values:\n').lower()
    
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
    global raw_df
    df = pd.read_csv(CITY_DATA[city])
    raw_df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
                    
    if month != 'all':
        month = valid_months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common travel month is", valid_months[df['month'].mode()[0] - 1].title())

    # TO DO: display the most common day of week
    print("The most common travel day of the week is", df['day_of_week'].mode()[0].title())

    # TO DO: display the most common start hour
    common_hour = datetime.time(df['hour'].mode()[0])
    print("The most common travel starting hour is", common_hour.strftime('%I:00 %p'))

    print(time_taken(start_time, time.time()))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most commonly used end station is", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + " / " + df['End Station']
    
    print("The most frequent combination of start and end stations is", df['start_end_station'].mode()[0])
    
    time_taken(start_time, time.time())


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total Travel Time:", np.sum(df['Trip Duration']),"minutes")

    # TO DO: display mean travel time
    print("Mean Travel Time:", np.mean(df['Trip Duration']),"minutes")

    print(time_taken(start_time, time.time()))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    column_name = 'User Type'
    if check_column(df, column_name):
        user_count = pd.value_counts(df[column_name])
        print("Number of each user type:")
    
        for index, value in user_count.items():
            print(f"{index} : {value}")
        
    # TO DO: Display counts of gender
    column_name = 'Gender'
    if check_column(df, column_name):
        gender_count = pd.value_counts(df[column_name])
        print("\nNumber of each gender:")
    
        for index, value in gender_count.items():
            print(f"{index} : {value}")
        print()

    # TO DO: Display earliest, most recent, and most common year of birth
    column_name = 'Birth Year'
    if check_column(df, column_name):
        earliest_birthyear = int(df[column_name].dropna(axis=0).sort_values().iloc[0])
        print(f"Earliest birth year: {earliest_birthyear}")
        
        recent_birthyear = int(df[column_name].dropna(axis=0).sort_values().iloc[-1])
        print(f"\nMost recent birth year: {recent_birthyear}")

        common_birthyear = int(df[column_name].mode()[0])
        print(f"\nMost common birth year: {common_birthyear}")

    print(time_taken(start_time, time.time()))

def time_taken(start_time, end_time):
    duration = "\nThis took %s seconds." % (end_time - start_time) + "\n" + '-'*40
    return duration

def check_column(df, column_name):
    if column_name in df:
        return True
    else:
        print(f"\nThere are no {column_name} records for {city.title()}")
        return False

def display_data(df):
    start_loc = 0
    view_data = input('\nWould you like to view the first 5 rows of individual trip data? Enter yes or no.\n')
    while True:
        if view_data.lower() == 'yes':
            end_loc = start_loc + 5
            #if we have viewed all user information in the city
            if end_loc > df.shape[0]:
                end_loc = df.shape[0]
                print(df.iloc[start_loc:end_loc])
                print('No more user information')
                break
                
            print(df.iloc[start_loc:end_loc])    
            start_loc += 5
            view_data = input('\nWould you like to continue? Enter yes or no.\n')
        else:
            break
     
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(raw_df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
