# charts/tests.py
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger.setLevel(logging.DEBUG)

class NatalChartSeleniumTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #service = Service('path/to/your/edgedriver')
        options = Options()
        # options.add_argument('headless')  # Uncomment for headless testing
        cls.selenium = webdriver.Edge(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  # Comment this line if you want to manually close the browser
        super().tearDownClass()

    def test_display_natal_chart(self):
        # Open the desired page
        self.selenium.get(f'{self.live_server_url}')
        
        # Interactions with the page (e.g., filling out forms) go here
         # Find the input fields and fill them
        name_input = self.selenium.find_element(By.NAME, 'name')
        birth_date_input = self.selenium.find_element(By.NAME, 'birth_date')
        birth_time_input = self.selenium.find_element(By.NAME, 'birth_time')
        location_input = self.selenium.find_element(By.NAME, 'location')

        name_input.send_keys('Michael Marler')
        birth_date_input.send_keys('07-03-1973')
        birth_time_input.send_keys('19:30')
        location_input.send_keys('Salt Lake City, UT')

         # Verify the values were set correctly
        #logger.debug("Name entered: " + name_input('value'))
        #logger.debug("Birth date entered: " + birth_date_input.get_attribute('value'))
        #logger.debug("Birth time entered: " + birth_time_input.get_attribute('value'))
        #logger.debug("Location entered: " + location_input.get_attribute('value'))
        # ...

        # Uncomment the following lines if needed
        #WebDriverWait(self.selenium, 20).until(
        #EC.presence_of_element_located((By.CSS_SELECTOR, "natal-chart-container"))
        #)

        # Debugging: Keep the browser open
        input("Press Enter to quit the test...")  # Pauses here for manual intervention
