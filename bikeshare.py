import time
import pandas as pd
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_columns', 0) # Allow for all columns to be shown when data display is selected
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello and welcome to my bikeshare interactive exploration session...')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nPlease type "Chicago", "New York", or "Washington".\n').lower()
        if city.lower() in ['chicago', 'new york', 'washington']:
            print('\nThanks for choosing {}.'.format(city))
        else:
            print('\nSorry, that input was wrong, please try again.\n')

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input('\nPlease type a month from January to June or "all".\n').lower()
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print('\nThanks for choosing {}.'.format(month))
        else:
            print('\nSorry, that input was wrong, please try again.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input('\nPlease type a day of the week or "all".\n').lower()
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print('\nThanks for choosing {}.'.format(day))
        else:
            print('\nSorry, that input was wrong, please try again.\n')

    print('-'*40)
    print('You chose "{}" and "{}" and "{}"'.format(city, month, day))
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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    print('\nThe filtered dataframe is loaded!')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)


    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['weekday'] = df['Start Time'].dt.weekday

    popular_weekday = df['weekday'].mode()[0]

    print('Most Popular Weekday:', popular_weekday)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode().to_string(index = False)
    print('The most common start station is {}'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode().to_string(index = False)
    print('The most common end station is {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['Combo'] = df['Start Station'].str.cat(df['End Station'], sep=' ---> ')
    common_combo = df['Combo'].mode().to_string(index = False)
    print('The most common trip combination is {}'.format(common_combo))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = np.sum(df['Trip Duration'])

    # display mean travel time
    mean = np.around(np.mean(df['Trip Duration']))

    print('The total travel time is {} and the mean travel time is {} (rounded)'.format(total, mean))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()




    # Display counts of user types
    user_counts = df.groupby('User Type')['User Type'].count()
    print('{}'.format(user_counts))


    if 'Birth Year' in df.columns and 'Gender' in df.columns:
    # Display counts of gender
        gender_count = df.groupby('Gender')['Gender'].count()
        print('{}'.format(gender_count))
    # Display earliest, most recent, and most common year of birth
        early = int(df['Birth Year'].min())
        late = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode())
        print('The oldest users are born in {}.\nThe youngest users are born in {}.'
      '\nThe most popular birth year is {}.'.format(early, late, common))

    else:
        print('No additional user data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_lines(df):
    """Displays five lines of data if the user specifies that they would like to."""

    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data?'
                        ' Enter yes or no (enlarge terminal window to see more columns).\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print('Please type "yes" or'
                  ' "no".')
    if display.lower() == 'yes':
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type "yes" or "no".\n')
                valid_input_2 = is_valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print('\nSorry, that input was wrong, please try again.\n')
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break

def main():
    """This is the main program which will run if this script is being run in a
     users interactive session."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_lines(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
