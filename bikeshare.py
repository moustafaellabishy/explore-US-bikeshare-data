import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def user_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nWelcome to US bikershare data! \nData is provided to you by Motivate Co. Let\'s explore some of their data!')
    while True : 
        """Making sure city input is valid and if not, Ask user again for a city name"""
        try :
            print()
            city = str(input('You can start by typing the city name you want to investigate (chicago, new york city, washington): ')).lower().strip()
            """making sure different input capitalization or spacing is handled"""
        except :
            """Handling error may be caused by user input"""
            print()
            print('Sorry, your input is invalid, try again by entering one of the listed city names!')
            continue
        if city not in ('chicago', 'new york city', 'washington') :
            print()
            print("Sorry, your input is invalid, try again by entering one of the listed city names and pay attention to spelling please!")    
        else :
            print()
            print("You have choosen {} to investigate, if you want to change your choice please restart the program.".format(city.title()))
            break  
            """input is valid, break the loop and continue with the program"""
    while True :
        """Giving user choice to filter by month or day or both or not at all"""
        try :
            print()
            filter_ = str(input('Type (month) to filter by month or (day) to filter by weekday or (both) to filter by both month & day or (all) to investigate {} data with no time filters: '.format(city)).title()).lower().strip()
            """making sure different input capitalization or spacing is handled"""
        except:
            """Handling error caused by user input""" 
            print()
            print('Sorry, your input is invalid, try again by entering one of the listed filters!')
            continue
        if filter_ not in ('month', 'day', 'both', 'all') :
            print()
            print("Sorry, your input is invalid, try again by entering one of the listed filters, be careful with spelling!")  
            continue
        elif (filter_ == 'all'):
            """path for no filters"""
            print()
            print('You chose to consider all data with no filters, if you want to add filter restart the program.')
            month = 'all'
            day = 'all'
            break
        elif (filter_ == 'month'):
            """path for filter by month"""
            while True :
                try:
                    print()
                    month = str(input('You chose to filter by month, please type one of the following month names (January, February, March, April, May, June): ')).lower().title()
                    day = 'all'
                except:
                    """Handling error caused by user input""" 
                    print()
                    print('Sorry, your input is invalid, try again by entering one of the listed filters!')
                    continue
                if month not in ('January', 'February', 'March', 'April', 'May', 'June'):
                    print()
                    print("Sorry, your input is invalid, try again by entering one of the listed months exactly as written!")
                else:
                    break   
        elif (filter_ == 'day'):
            """path for filter by day"""
            while True:
                try:
                    print()
                    day= str(input('You chose to filter by day, please type one of the following days names (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday):')).lower().title()
                    month = 'all'
                except:
                    """Handling error caused by user input""" 
                    print()
                    print('Sorry, your input is invalid, try again by entering one of the listed filters!')
                    continue
                if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
                    print()
                    print("Sorry, your input is invalid, try again by entering one of the listed days and pay attention to spelling!")
                else:
                    break
        elif (filter_ == 'both'):
            """giving the user the choice to use both day and month filters""" 
            while True:
                try:
                    print()
                    month = str(input('You chose to filter by both month and day, first choose the month (January, February, March, April, May, June): ')).lower().title()
                except:
                    """Handling error caused by user input""" 
                    print()
                    print('Sorry, your input is invalid, try again by entering one of the listed filters!')
                    continue
                if month not in ('January', 'February', 'March', 'April', 'May', 'June'):
                    print()
                    print("Sorry, your input is invalid, try again by entering one of the listed months and pay attention to spelling please!")
                    continue
                else:
                    while True:
                        try:
                            print()
                            day = str(input('Then please type one of the following days names (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ')).lower().title()
                        except:
                            """Handling error caused by user input""" 
                            print()
                            print('Sorry, your input is invalid, try again by entering one of the listed filters!')
                            continue
                        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
                            print()                           
                            print("Sorry, your input is invalid, try again by entering one of the listed days and pay attention to spelling please!")
                        else:
                            break
                break
        break 
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
    """ converting start time & endtime columns to datetime format"""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    """ creating 2 seperate columns one for month and one for day of week"""
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    """ Filtering by month if user chose to filter by month"""
    if month != 'all':
        """ using list indexing to get the month number"""
        all_months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = all_months.index(month.lower()) + 1
        """filtering the data frame by month if user chose to"""
        df = df[df['month'] == month]
    """ Filtering by day if user chose to filter by day """
    if day != 'all':
        """filtering the data frame by day"""
        df = df[df['day_of_week'] == day]
    print("Please remember that all following calculations are done based on filters you have assigned earlier : ({}) as the city, ({}) as the month and ({}) as the day.".format(city,month, day))
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    all_months = ['january', 'february', 'march', 'april', 'may', 'june']
    df['hour'] = df['Start Time'].dt.hour
   
    if (len(pd.unique(df['month'])) == 1) and (len(pd.unique(df['day_of_week'])) == 1)  :
        print('The count of people took a bike during the filtered month and day is: ', df['month'].value_counts()[df['month'].mode()[0]])
        print('No most common month or day because you have filtered by month and day.')
        """checks if data is filtered as both so uniques values count in both columns are 1 each then display only a count of people who took a bike during that day in that month"""
    else:
        if (len(pd.unique(df['month'])) == 1) :
            print('The count of people who took a bike during filtered month is: ', df['month'].value_counts()[df['month'].mode()[0]])
            print('No most common month because you have filtered by month.')
            """checks if data is filtered by month only so uniques values count in month column is 1 then display only a count of people who took a bike during that month"""
        else:               
            print('The most common month of Travel is ', all_months[df['month'].mode()[0] - 1]) 
            """This gets the most common value appearing in month column"""
            print('The count of people who took a bike during this month is: ', df['month'].value_counts()[df['month'].mode()[0]])
            """This index the value count series to get the count of the most common value"""
        
        if (len(pd.unique(df['day_of_week'])) == 1) :
            """Displays the most common day in letters and count it appeared, if data is filtered by day of week so all day of week column has the same value then show only the count"""
            print ('\nThe count of people who took a bike on filtered day is: ', df['day_of_week'].value_counts()[df['day_of_week'].mode()[0]])
            print('No most common day because you have filtered by day.')
        else:
            print('\nThe most common day of Travel is ', df['day_of_week'].mode()[0]) 
            """This gets the most common value appearing in day of week column"""
            print ('The count of people who took a bike on that day: ', df['day_of_week'].value_counts()[df['day_of_week'].mode()[0]])
            """This index the value count series to get the count of the most common appearing value"""
 
    print('\nThe most common hour of Travel is ', df['hour'].mode()[0])   
    """This gets the most common value appearing in hour column"""
    print ('The count of people who took a bike on that hour: ', df['hour'].value_counts()[df['hour'].mode()[0]])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    """display most commonly used start station by indexing mode value and its count"""
    print('\nThe most common start station of Travel is ', df['Start Station'].mode()[0])
    print ('The count of people who took a bike from this start station is: ', df['Start Station'].value_counts()[df['Start Station'].mode()[0]])
    
    """display most commonly used end station by indexing mode value and its count"""
    print('\nThe most common end station of Travel is ', df['End Station'].mode()[0])
    print ('The count of people who returned the bike to this end station is: ', df['End Station'].value_counts()[df['End Station'].mode()[0]])
    
    """ creating a combined column of both start and end columns with (to) string in between and getting mode string in the combination column"""   
    df['Start_End_Station'] = (df['Start Station'] + ' to ' + df['End Station'])
    print('\nThe most common trip is from ', df['Start_End_Station'].mode()[0])
    print ('The count of people who made this trip is: ', df['Start_End_Station'].value_counts()[df['Start_End_Station'].mode()[0]])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip durations."""
    print('\nCalculating total and average Trip Duration...\n')
    start_time = time.time()
    
    """print total duration of trips in seconds."""
    print('The total duration of travel was: ', int(df['Trip Duration'].sum()), 'seconds')
 
    """\nprint average duration of trips in seconds."""
    print('The average duration of travel was: ', int(df['Trip Duration'].mean()), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users. After investigating data I found that user types and gender columns have NaN data which need to be dropped while calulating the user stats"""

    print('\nCalculating User types,gender and birth year count....\n')
    start_time = time.time()
    
    print('Here are User types and count of each:\n',df['User Type'].dropna().value_counts())
    """prints counts of user types."""
    
    if len(df.columns) == 13 :
        """checking number of colums to decide whether it will print gender and birth year info or not, as I have found using column attribute that newyork and chicago has 13 columns while washington has only 11 columns."""
        
        print('\nOur Users gender count was:\n',df['Gender'].dropna().value_counts())
        """print counts of gender."""
        print('\nOur oldest user was born in: ', int(df['Birth Year'].dropna().min()))
        print('\nOur youngest user was born in: ',int(df['Birth Year'].dropna().max()))
        

        print('\nMost common birth year of our users is: ',int(df['Birth Year'].dropna().mode()[0]),' And the count of users who were born in that year is:',df['Birth Year'].value_counts()[df['Birth Year'].mode()[0]])
        """Displays most common year and its count by getting mode index and value count of mode."""
    else :
        print('\nData from Washington city does not have Gender or Birth year info!')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Promt user whether to show raw data or not if yes, shows first 5 rows of data then ask again if user types yes shows another 5 rows and so on until the user type no"""
    i = 0
    f = 5
    """Iteration factor to use in showing 5 rows of the raw data every iteration in the while loop"""
    while True:
        try :
            print()
            rawdata = str(input('Would you like to take a look at part of the raw data. Enter yes or no.\n')).lower().strip()
            """making sure different input capitalization or spacing is handled"""
        except :
            """Handling error may be caused by user input"""
            print()
            print('Sorry, your input is invalid, try again by entering yes or no.\n')
            continue
        if rawdata == 'yes':
                if len(df.columns) == 13 :
                    """checking how money columns and printing only the columns with useful raw data"""
                    pd.set_option('display.max_rows', None)
                    """I learned about this option through this website https://www.shanelynn.ie/ that offers training and practice examples for working with pandas dataframes"""
                    """this set dataframe options to show all columns without hidding any of them"""
                    print(df.iloc[i:f, 1:9])
                    i += 5
                    f += 5
                    print('You can see the next 5 rows by entering yes one more time in the question below.\n')
                    continue
                else:
                     pd.set_option('display.max_columns', None)
                     print(df.iloc[i:f, 1:7])
                     i += 5
                     f += 5
                     print('You can see the next 5 rows by entering yes one more time in the question below.\n')
                     continue
                
        elif rawdata == 'no':
            break
        else:
            print('\nSorry, your input is invalid, try again by entering yes or no.\n')
            continue
        
def main():
    while True:
        city, month, day = user_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        while True:
            try:
                restart = input('\nWould you like to restart the Program? Enter yes or no.\n')
            except :
                """Handling error may be caused by user input"""
                print()
                print('Sorry, your input is invalid, try again by entering yes or no.\n')
                continue
            if restart.lower() == 'no':
                print('-------------------------------------This is the End of our program!-------------------------------------\n')
                print('------------------------------------------------Thank You------------------------------------------------\n')
                break
            elif restart.lower() == 'yes':
                break
            else:
                print('\nSorry, your input is invalid, try again by entering yes or no.\n')
                continue
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
