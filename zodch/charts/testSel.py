
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Setup the Chrome WebDriver
browser = webdriver.Chrome()

# Open the natal.html page
browser.get('http://localhost:8000/natal.html')

# Fill in the birth date, time, and place
browser.find_element_by_id('birth_date').send_keys('2000-01-01')
browser.find_element_by_id('birth_time').send_keys('12:00')
browser.find_element_by_id('birth_place').send_keys('New York, NY')

# Submit the form to render the natal chart
browser.find_element_by_id('submit_button').click()

# Wait for the chart to be rendered
time.sleep(5)

# Close the browser
browser.quit()
