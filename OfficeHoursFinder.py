import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime as dt

def get_office_hours():
    '''Scrape office hours chart from sylabus website into DataFrame'''
    ds_class = input('What is your DS class code (2000 or 2500)? ')
    res = requests.get(f"https://www.ccs.neu.edu/home/rachlin/python/ds{ds_class}/index.html")
    soup = bs(res.content,'lxml')
    table = soup.find_all('table')[1]
    df = pd.read_html(str(table))
    df = pd.DataFrame(df[0])

    #Scrape the zoom links and add them to the df
    links = table.find_all('a')
    links_f = [str(link).strip(' zoom</a>"')[6:] for link in links]

    df['Zoom Links'] = links_f
    del df['Zoom'] #Old hyperlink text

    return df

def office_hours_to_datetime(df):
    '''Convert all the office hour strings from scrapped DataFrame into datetime objects'''

    hour_list = []
    default_dt = dt.datetime.now().isoformat(timespec='hours').split('T')[0]

    for hours in df['Office Hours']:

        #Different hours for each day
        if ',' in hours:
            hours = hours.split(',')
            hours = [hour.strip(' ').split(' ') for hour in hours]


        #Same hours for all days
        else:
            hours = hours.split(' ')
            hours = [hour.split('/') for hour in hours]
            if len(hours[0]) > 1:
                hours = [[hours[0][0], hours[1][0]], [hours[0][1], hours[1][0]]]
            else:
                hours = [[hours[0][0], hours[1][0]]]

        for i in range(len(hours)):
            hours[i][1] = hours[i][1].split('-')

            for x in range(len(hours[i][1])):
                raw_hour = hours[i][1][x]
                f_hour = hours[i][1][x]

                if raw_hour.endswith('a') or raw_hour.endswith('p'):
                    f_hour = hours[i][1][x][:-1]

                if any([char.isalpha() for char in f_hour]):
                    hours[i][1][x] = None
                    break

                time_string = f'{default_dt}T{f_hour}'

                if len(f_hour) == 1 or (':' in f_hour and len(f_hour.split(':')[0]) == 1):
                    time_string = f'{default_dt}T0{f_hour}'

                hours[i][1][x] = dt.datetime.fromisoformat(time_string)

                if raw_hour.endswith('p') and not f_hour.startswith('12'):
                    hours[i][1][x] = hours[i][1][x] + dt.timedelta(hours=12)

        hour_list.append(hours)

    df['Hours'] = hour_list

    return df

def str_to_dt(string):
    '''This funciton is for the user input time string which is going to be in a slightly different format than the strings on the website'''
    default_dt = dt.datetime.now().isoformat(timespec='hours').split('T')[0]
    raw_hour = string
    f_hour = string

    if raw_hour.endswith('a') or raw_hour.endswith('p'):
        f_hour = string[:-1]

    time_string = f'{default_dt}T{f_hour}'

    if len(f_hour) == 1 or (':' in f_hour and len(f_hour.split(':')[0]) == 1):
        time_string = f'{default_dt}T0{f_hour}'

    string = dt.datetime.fromisoformat(time_string)

    if raw_hour.endswith('p') and not f_hour.startswith('12'):
        string = string + dt.timedelta(hours=12)

    return string

def get_user_input():
    now_other = input('Do you want to check for office hours now or some other time (Now/Other)? ')
    if now_other == 'Now':
        current_time = dt.datetime.now()

        week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day = week_days[current_time.weekday()]

    elif now_other == 'Other':

        day = input('What day of the week is it (first 3 letters) (eg. Thu)? ')
        time = input("What time is it (in 24h system) (hh:mm) (eg. 15:00)? ")
        current_time = str_to_dt(time)

    return(day, current_time)

def return_office_hours(df, day, current_time):
    '''Actual calculations to figure out if the current time or other user inputted time lines up witht he office hours'''

    right_now = []
    next_hour = []
    no_days = []

    for x in range(len(df['Hours'])):
        for sublist in df['Hours'][x]:
            if day in sublist:

                if current_time >= sublist[1][0] and current_time < sublist[1][1]:
                    right_now.append((sublist, x))

                elif current_time >= sublist[1][0] - dt.timedelta(hours=1) and current_time < sublist[1][0]:
                    next_hour.append((sublist, x))

                else:
                    no_days.append((sublist, x))

    if len(right_now) > 0:
        print('\nOffice hours right now:\n')
        for sublist,x in right_now:
            print(df.loc[x, ['Name', 'Office Hours']].to_string())
            print(df['Zoom Links'][x], '\n')

    if len(next_hour) > 0:
        print('\nOffice hours in the next hour:\n')
        for sublist,x in next_hour:
            print(df.loc[x, ['Name', 'Office Hours']].to_string())
            print(df['Zoom Links'][x], '\n')

    #Extra section incase the user wanted to check more than an hour into the future
    if len(right_now) + len(next_hour) == 0:
        new_range = []
        print('There are no office hours now or in the next hour.')
        hour_range = int(input('How many hours would you like to expand the search range by (int)? '))

        for sublist,x in no_days:

            if current_time >= sublist[1][0] - dt.timedelta(hours=hour_range) and current_time < sublist[1][0]:
                new_range.append((sublist, x))

        if len(new_range) > 0:
            print(f'\nHere are the office hours in the next {hour_range} hours:\n')

            for sublist,x in new_range:
                print(df.loc[x, ['Name', 'Office Hours']].to_string())
                print(df['Zoom Links'][x], '\n')

        else:
            print(f'There are no office hours in the next {hour_range} hours.')

def main():
    df = get_office_hours()
    df = office_hours_to_datetime(df)
    day, current_time = get_user_input()
    return_office_hours(df, day, current_time)

if __name__ == '__main__':
    main()
