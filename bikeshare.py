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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    while city not in ['chicago','new york city', 'washington']:
        city =input('\nPlease type in a valid city name (Chicago, New York City or Washington):\n').lower()
        
    # TO DO: get user input for month (all, january, february, ... , june)

    month=''
    months=['all','january','february','march','april','may','june']
    
    #Check if month input is valid and part of the list months
    while month not in months:
        month=input('\nPlease enter "all" or a valid month, you want to look at (January - June):\n').lower()

    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    days=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    #Check if input is valid and part of the list days
    while day not in days:
        day=input('\nPlease enter "all" or a day, you want to look at (ex. Monday):\n').lower()

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
    #import csv of specified city
    df = pd.read_csv(city.replace(' ','_') + '.csv')
    
    #convert dates to datetime format 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #convert birth year to numeric format, when new york city or washington is selected
    if city in ['chicago','new york city']:
        df['Birth Year'] =pd.to_numeric(df['Birth Year'])
    
    #Add columns for month of start time and day of start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek +1
    
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
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]
    
    print(df.head())
    
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('The Most Common Month is:', months[popular_month - 1].title(), 'counts: ', df['month'].value_counts()[popular_month])
    
    # TO DO: display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        print('The Most Common Day is:', days[popular_day - 1].title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:', pop_start_station)

    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:', pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    pop_trip = df['Trip'].mode()[0]
    print(f'\nMost Freuquent Combination of Start and End Station: {pop_trip}\n')
     
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Traveltime']=df['End Time']-df['Start Time']
    sum_travel_time=df['Traveltime'].sum()
    print(f'Customers travelled in sum for {sum_travel_time}.\n')

    # TO DO: display mean travel time
    mean_travel_time=df['Traveltime'].mean()                 
    print(f'Customers travelled on average for {pd.Timedelta(mean_travel_time,min)}.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\nType of Users:\n')
    print(df.groupby(['User Type'])['User Type'].count())
    
    # TO DO: Display counts of gender
    if city in ('chicago','new york city'):
        print('\nGender of Users:\n')
        print(df.groupby(['Gender'])['Gender'].count())
        
        # TO DO: Display earliest, most recent, and most common year of birth
        print('\nBirth Year of Users:\n')
        most_recent_byear = df['Birth Year'].max()
        earliest_byear = df['Birth Year'].min()
        most_common_byear = df['Birth Year'].dropna().mode()[0]
    
        print('Most recent Birth Year: {}'.format(int(most_recent_byear)))
        print('Earliest Birth Year: {}'.format(int(earliest_byear)))
        print('Most common Birth Year: {}\n'.format(int(most_common_byear)))
    else:
        print('\nGender and Birth year statistics are not available for this city. \n')
        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_data(df):
    """Displays 5 lines of raw data, as long as user continues to enter yes."""
    
    raw_data = input('\nDo you want to have a look at some data in detail? (Yes/No)\n').lower()
    #Number of lines in the dataset
    max_line=df.shape[0]
    #Specifies the number of last row to show
    line_index=5
    
    if raw_data =='yes':
        while raw_data=='yes' and line_index <= max_line:
            #prints 5 rows of data up to the current line_index
            for i in range(5):
                #prints one row of data as a dictionary
                print(df.iloc[line_index-5+i].to_dict(),'\n')

            raw_data = input('\n Do you want to see further 5 rows?(Yes/No)\n').lower() 
            line_index += 5
            
        
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Statistics for \nCity: {}\nMonth: {}\nDay of Week: {}\nwill now be calculated.\n'.format(city.title(),month.title(),day.title()))
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
