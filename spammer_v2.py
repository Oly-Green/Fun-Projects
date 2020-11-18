from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_info_scraper import Fake
from paragraph_scraper_s import *

#initialize browser
browser  = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://defendyourballot.formstack.com/forms/voter_fraud?utm_source=graphic')

#generate fake information
fake = Fake()
print(fake)

# Fill credentials
#name
browser.find_element_by_name("field101315259-first").send_keys(fake.name[0])
browser.find_element_by_name("field101315259-middle").send_keys(fake.name[1])
browser.find_element_by_name("field101315259-last").send_keys(fake.name[2])


#phone number
browser.find_element_by_name("field101315260").send_keys(fake.phone_num)

#adress
browser.find_element_by_name("field101316245-address").send_keys(fake.street)
browser.find_element_by_name("field101316245-city").send_keys(fake.city)
browser.find_element_by_name("field101316245-state").send_keys(fake.state)
browser.find_element_by_name("field101316245-zip").send_keys(fake.zipcode)

#email
browser.find_element_by_name("field101315261").send_keys(fake.email)
browser.find_element_by_name("field101315261_confirm").send_keys(fake.email)

#Place of Incident
browser.find_element_by_name("field101315264").send_keys(fake.state)
browser.find_element_by_name("field101315265").send_keys(fake.county)
browser.find_element_by_name("field101315266").send_keys(fake.poll)

#Incident decription
browser.find_element_by_name("field101315267").send_keys(generate_description())
