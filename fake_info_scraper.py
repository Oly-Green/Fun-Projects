from bs4 import BeautifulSoup
import requests
import string
import random
import geocoder
import pandas as pd

class Fake:
    def __init__(self):
        self.req = requests.get('https://www.fakeaddressgenerator.com/World_Address/get_us_address1')
        self.soup = BeautifulSoup(self.req.text,'lxml')

        #name
        self.name = self.soup.find('table').find('strong').text.strip().split('\xa0')

        #adress
        self.street = self.soup.find_all('input', class_="no-style")[0]['value']
        self.city = self.soup.find_all('input', class_="no-style")[1]['value']
        self.state = self.soup.find_all('input', class_="no-style")[3]['value']
        self.zipcode = self.soup.find_all('input', class_="no-style")[4]['value']

        #county
        API_KEY = 'nope'
        self.results = geocoder.google(f"{self.city}, {self.state}", key=API_KEY)
        print(self.results)
        self.county = self.results.current_result.county

        #contact info
        self.phone_num = self.soup.find_all('input', class_="no-style")[5]['value']

        email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'hotmail.co.uk', 'hotmail.fr', 'msn.com', 'yahoo.fr', 'wanadoo.fr',
        'orange.fr', 'comcast.net', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.co.in', 'live.com', 'rediffmail.com', 'gmx.de', 'web.de',
        'yandex.ru', 'ymail.com', 'libero.it', 'outlook.com']
        ending_chars = string.ascii_letters + string.digits + '!#$%^&*-_'

        self.domain = random.choice(email_domains)
        self.ending = ''.join([random.choice(ending_chars) for i in range(random.randint(1,5))])
        self.email = f"{''.join(self.name)}{self.ending}@{self.domain}"

        #polling place
        poll_ends = ['YMCA', 'Fairmount', 'Phila', 'Theatre', 'Center', 'Tabernacle', 'Charter', 'Church', 'Cca', 'Room', 'Bldg', 'Apartments', 'Parole',
        'Lobby', 'World', 'Condos', 'Residences', 'Alliance', 'Thomas', 'Restaurant', 'Visitation', 'Inc', 'Mosque', 'Property', 'Museum',
        'Oxford/buchanan', 'Apts-clubhouse', 'Plaza', 'Faith', 'Home', 'Post', 'St', 'Garage-rear', 'Suites', 'Hall', 'Institute', 'Revolution', 'Homes(pha)',
        'Salon', 'Lsh', 'Branch', 'Germantown', 'Cdc', 'Center', 'Homes', 'Tower', 'Monuments', 'Meeting', 'Auditorium', 'Courts', 'Memorial', 'Villas', 'Society',
        'Organization', 'Gym', 'Legion', 'Christ', 'Laboratory', 'Ballroom', 'Clubhouse', 'Events', 'Office', 'Library', 'Bethel', 'Ministries', 'Solomon',
        'Towers', 'Southwest', 'Club', 'School', 'Academy', 'Apts', 'Landing', 'Future', 'Jefferson', 'Tasker', 'Square', 'Assoc', 'Airy', 'Sciences', 'Temple',
        'Association', 'Schoolhouse', 'Asc', '4','366', 'Building', 'Rear', 'Venue', 'Daycare', 'Seminary', 'Shop', 'Place]', 'School', 'Education', 'City',
        'House', 'Court', 'Manor', 'Gardens', 'Center(rear)', 'Housing', 'Place', 'Assembly', 'Ave', 'Medal', 'Cafe', 'Frankford', 'Epiphany', 'Lounge', 'Bride', 'Park', 'Shepherd', 'Nazarene']

        df_names = pd.read_csv('baby-names.csv')
        df_names = list(df_names["name"])

        self.poll_start = ''.join([f'{random.choice(df_names)} ' for i in range(random.randint(1,3))])
        self.poll_end = random.choice(poll_ends)
        self.poll = self.poll_start + self.poll_end

    def make_dict(self):
        return {'Name':self.name, 'Street':self.street, 'City':self.city, 'State':self.state, 'County':self.county, 'ZipCode':self.zipcode,
                'PollingPlace':self.poll, 'PhoneNumber':self.phone_num, 'Email':self.email}

    def __repr__(self):
        return str(self.make_dict())
