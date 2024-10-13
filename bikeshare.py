## TODO: import all necessary packages and functions

import pandas as pd
import time
import datetime

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

CITY_DATA = {
    'chicago' : chicago,
    'new york' : new_york_city,
    'washington' : washington
}

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''


    while True:
        try:
            city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
            chosen_city = CITY_DATA[city.lower()]
            break
        except:
            print('Not a valid input. Try again.')
    return chosen_city


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        (str) time period user wants to filter to (month, day, none)
    '''
    period_filter = {'month' : 'month', 
                    'day' : 'day', 
                    'none' : 'none'}
    while True:
        try:
            time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
            time_period = period_filter[time_period.lower()]
            break
        except:
            print('Not a valid filter. Please try again.')
    return time_period


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (int) the month the user wants to filter down to
    '''
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    while True:
        try:
            month = input('\nWhich month? January, February, March, April, May, or June?\n')
            month = months.index(month.lower()) + 1
            break
        except:
            print('Invalid month. Please try again.')
    return month


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) the day the user wants to filter down to
        
    '''
    # Setting invalid day input to allow try statements to work
    
    day_check = ['0', '1', '2', '3', '4', '5', '6']

    day = 0

    # While loop runs until user selects a valid day within the month
    while True:
        try:
            day = input('\nWhich day? Please type your response as an integer (Ex. Sunday = 0).\n')
            day = day_check.index(day)
            break
        except:
            print('Please input an integer within the valid range (1-7).')

    return day


def popular_month(city_file, time_period):
    '''Returns for the most popular month based on user inputs from get_city() and get_month() functions

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month the user wanted to filter to from get_month() function

    Return:
        (Str) Returns the most popular month

    Question: What is the most popular month for start time?
    '''

    # Opens city file
    df = pd.read_csv(city_file)
    
    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Creating month column
    df['month'] = df['Start Time'].dt.month

    # Determining which month appears the most
    most_popular_month = df['month'].mode()[0]

    return most_popular_month


def popular_day(city_file, time_period):
    '''Return the most popular day based on the city chosen and month (if user wanted to filter by month)

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month the user wanted to filter to from get_month() function
    
    Return:
        (str) Returns the most popular day

    Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    '''
    
    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period != None:
        df['month'] = df['Start Time'].dt.month
        df = df[df['month'] == time_period]

    # Creating day column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Determining which day appears the most
    most_popular_day = df['day_of_week'].mode()[0]

    return most_popular_day

def popular_hour(city_file, time_period, user_filter):
    '''Returns the most popular hour based on the city chosen, month (if selected) or day (if selected)

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user
    Returns:
        (int) Returns the most popular hour 

    Question: What is the most popular hour of day for start time?
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

        # Creating an hour column
        df['hour'] = df['Start Time'].dt.hour

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
        # Creating an hour column
        df['hour'] = df['Start Time'].dt.hour
        print(df['hour'])
    else:
        # Creating an hour column
        df['hour'] = df['Start Time'].dt.hour        

    # Finding the most popular hour
    most_popular_hour = df['hour'].mode()[0]

    return most_popular_hour


def trip_duration(city_file, time_period, user_filter):
    '''Returns the total and average trip duration

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (list) Returns the most total trip duration in index 0 and the average trip durations in index 1

    Question: What is the total trip duration and average trip duration?
    '''
    
    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
    # Getting the total and average trip durations based on the filter selected
    durations = []
    # Appending the sum of all trip durations (based on user selected filter)
    durations.append(df['Trip Duration'].sum())
    # Appending the average of all trip durations (based on user selected filter)
    durations.append(df['Trip Duration'].mean())

    return durations


def popular_stations(city_file, time_period, user_filter):
    '''This returns the most popular start and end stations

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (list) Returns the most popular start station in index 0 and the most popular end station in index 1

    Question: What is the most popular start station and most popular end station?
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
    # Getting the most frequent start and end stations
    most_popular_stations = []
    most_popular_stations.append(df['Start Station'].mode()[0])
    most_popular_stations.append(df['End Station'].mode()[0])

    return most_popular_stations

def popular_trip(city_file, time_period, user_filter):
    '''This function returns the most popular trip (Start and End locations)

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (str) Returns the most frequent trip - Start and End stations     

    Question: What is the most popular trip?
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
    # Creating new concatenated Start-End Station column
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']

    # Getting the mode of the new trip column
    most_popular_trip = df['Trip'].mode()[0]

    return most_popular_trip

def users(city_file, time_period, user_filter):
    '''This function returns the counts for each type of user
    
    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (pd.series) Returns each user type and the total number for each type

    Question: What are the counts of each user type?
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
    # Getting the counts for each type of user
    user_type_count = df['User Type'].value_counts()

    return user_type_count


def gender(city_file, time_period, user_filter):
    '''Returns the counts of each gender
    
    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (pd.series) Returns each gender type and the total number for each type

    Question: What are the counts of gender?
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]
        
    df['Gender'] = df['Gender'].fillna('Not Specified')

    # Getting the counts for each gender type
    gender_count = df['Gender'].value_counts()

    return gender_count

def birth_years(city_file, time_period, user_filter):
    ''' This function returns the oldest user, youngest user, and the most popular birth year

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        (list) Returns a list of the oldest user age in index 0, the youngest users age in index 1, and the most popular birth year in index 2

    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    '''

    # Getting current year
    current_year = datetime.date.today().year

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]

    # Removing rows with null values
    df = df.dropna(axis=0)

    # Creating blank age list
    age = []

    # Getting oldest users age
    age.append(current_year - df['Birth Year'].min())

    # Getting youngest users age
    age.append(current_year - df['Birth Year'].max())

    # Getting most common birth year
    age.append(round(df['Birth Year'].mode()[0]))

    return age

def display_data(city_file, time_period, user_filter):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        city_file - the selected city the user wanted to use from get_city() function
        time_period - the month or day the user wanted to filter down to
        user_filter - the selected month or day from user

    Return:
        none
    '''

    # Opens city file
    df = pd.read_csv(city_file)

    # Formatting start time column to proper datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Checks if user wanted to filter by a specific month
    if time_period == 'month':
        
        # Creating a month column
        df['month'] = df['Start Time'].dt.month

        # Filtering down to the month the user chose
        df = df[df['month'] == user_filter]

    #Checks if user wanted to filter by a specific day
    elif time_period == 'day':

        # Creating a day of week column
        df['day'] = df['Start Time'].dt.dayofweek
        
        # Filtering down to the specific day of week
        df = df[df['day'] == user_filter]

    # Creating dicionary to check if input was valid
    valid_value = {'yes' : 'yes', 'no' : 'no'}
    
    # Setting display value to yes
    display = 'yes'

    # Setting counter to 5
    counter = 5

    # If yes - while loop will run till user inputs 'no'
    while display == 'yes':
        try:
            if counter == 5:
                display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')
                display = valid_value[display.lower()]            
            else:
                display = input('\nWould you like to view additional trip data?'
                        'Type \'yes\' or \'no\'.\n')
                display = valid_value[display.lower()]
            
            # Displaying 5 rows of filtered data
            if display == 'yes':
                
                # Checking if index is out of range - if it is it will show what it can and leave the function
                if len(df) < counter:
                    print(df.iloc[counter-5:len(df)])
                    print('No more data to show')
                    display = 'no'
                    break
                # If index is not out of range - it will return the next 5 lines of raw data
                else:
                    print(df.iloc[counter-5:counter])
                    counter += 5
                
            continue
            
        except:
            display = 'yes'
            print('\nNot a valid input. Please type yes or no.\n')

            
        


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    user_month = None
    user_day = None
    no_filter = None

    print('\nCalculating the first statistic...')

    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        
        #TODO: call popular_month function and print the results
        
        most_popular_month = popular_month(city, time_period)

        print('\nThe most popular month is: {}'.format(most_popular_month))
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...Most popular day")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        # If month was a selected filter then it will prompt the user to select which month they want
        if time_period == 'month':
            user_month = get_month()

        # TODO: call popular_day function and print the results
        
        most_popular_day = popular_day(city, user_month)

        print('\nThe most popular day is: {}'.format(most_popular_day))
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...Most popular hour")    



    # What is the most popular hour of day for start time?
    # TODO: call popular_hour function and print the results
    
    
    # Checking which time period was selected and running the popular_hour() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        most_popular_hour = popular_hour(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        user_day = get_day()
        most_popular_hour = popular_hour(city, time_period, user_day)
    else:
        start_time = time.time()
        most_popular_hour = popular_hour(city, time_period, no_filter)

    print('\nThe most popular hour is: {}'.format(most_popular_hour))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...Trip durations")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    # TODO: call trip_duration function and print the results

    # Checking which time period was selected and running the trip_duration() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        durations = trip_duration(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        durations = trip_duration(city, time_period, user_day)
    else:
        start_time = time.time()
        durations = trip_duration(city, time_period, no_filter)

    print('\nThe total trip duration was: {}'.format(durations[0]))
    print('The average trip duration was: {}'.format(durations[1]))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...Most popular stations")
    start_time = time.time()

    # What is the most popular start station and most popular end station?

    # Checking which time period was selected and running the popular_stations() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        most_popular_stations = popular_stations(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        most_popular_stations = popular_stations(city, time_period, user_day)
    else:
        start_time = time.time()
        most_popular_stations = popular_stations(city, time_period, no_filter)

    print('\nThe most popular start station is: {}'.format(most_popular_stations[0]))
    print('The most popular end station is: {}'.format(most_popular_stations[1]))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...Most popular trip")
    start_time = time.time()

    # What is the most popular trip?
    # TODO: call popular_trip function and print the results

    # Checking which time period was selected and running the popular_trip() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        most_popular_trip = popular_trip(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        most_popular_trip = popular_trip(city, time_period, user_day)
    else:
        start_time = time.time()
        most_popular_trip = popular_trip(city, time_period, no_filter)

    print('\nThe most popular trip is: {}'.format(most_popular_trip))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...User type counts")
    start_time = time.time()

    # What are the counts of each user type?
    # TODO: call users function and print the results

    # Checking which time period was selected and running the users() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        user_type_count = users(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        user_type_count = users(city, time_period, user_day)
    else:
        start_time = time.time()
        user_type_count = users(city, time_period, no_filter)

    # Printing blank line for formatting
    print()

    # For loop to iterate through the different user types and counts
    for i in range(len(user_type_count)):
        print('User Type: {}, Count: {}'.format(user_type_count.index[i], user_type_count.iloc[i]))

    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...Gender counts")
    start_time = time.time()

    # What are the counts of gender?
    # TODO: call gender function and print the results

    # Checking which time period was selected and running the gender() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        gender_count = gender(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        gender_count = gender(city, time_period, user_day)
    else:
        start_time = time.time()
        gender_count = gender(city, time_period, no_filter)

    # Printing blank line for formatting
    print()

    # For loop to iterate through the different user types and counts
    for i in range(len(gender_count)):
        print('Gender: {}, Count: {}'.format(gender_count.index[i], gender_count.iloc[i]))

    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...User base ages")
    start_time = time.time()

    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    # TODO: call birth_years function and print the results

    # Checking which time period was selected and running the gender() function using the approprate filter value (ex. month, day, no filter)
    if time_period == 'month':
        start_time = time.time()
        age = birth_years(city, time_period, user_month)
    elif time_period == 'day':
        start_time = time.time()
        age = birth_years(city, time_period, user_day)
    else:
        start_time = time.time()
        age = birth_years(city, time_period, no_filter)

    print('The oldest user is: {} years old'.format(age[0]))
    print('The youngest user is: {} years old'.format(age[1]))
    print('The most popular birth year is: {}'.format(age[2]))
    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    if time_period == 'month':
        display_data(city, time_period, user_month)
    elif time_period == 'day':
        display_data(city, time_period, user_day)
    else:
        display_data(city, time_period, no_filter)
    

    # Restart?

    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
