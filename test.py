from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time


# Path to geckodriver
geckodriver_path = r"C:\Tools\geckodriver\geckodriver.exe"

options = Options()
options.headless = True

# Initialize the WebDriver with the correct Service
service = Service(executable_path=geckodriver_path)
# Initialize the WebDriver (ensure geckodriver is in your PATH or provide the path to it)
driver = webdriver.Firefox(service=service, options=options)

# URL to open
start_url = 'https://www.grailed.com/shop/8-r3aVtP4Q'

# Open the URL
driver.get(start_url)

timeout=30

#loading the page so that 'feed-item's can be seen
try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='feed-item']"))
    )

except TimeoutException:
    print("Timed out, page was not able to be loaded")
    driver.quit()


# how many results show up
results = driver.find_elements(By.XPATH, '//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
print("Initial number of results:", len(results))

listing_number_elements = driver.find_elements(By.XPATH, '//span[@class="Body-module__body___FYqu- Text CustomStats-module__customStats___PGk9q"]')

if listing_number_elements:
    listing_number_text = listing_number_elements[0].text
    # converting string into integer
    total_listings = int(listing_number_text.replace(',', '').split()[0])
    print("Total number of listings:", total_listings)
else:
    print("failed to grab total listing number")

print(int(total_listings/200))

# Number of Scrolls, add one in case the function rounds down
#ScrollNumber=round(listing_number_element/40)+1
ScrollNumber=3

Results = []

# Start the scroll
for i in range(0,ScrollNumber):
    results = driver.find_elements(By.XPATH, '//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
    Results=Results+results
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    print("scraped so far: " + str(len(Results)))
    time.sleep(2)

#start scraping here

ListingName = []
Price = []
NewPrice = []
OldPrice = []
Size = []
Time = []
LastBump = []
Link = []

for result in results:
    listing_name = result.find_element(By.XPATH, './/p[@class="ListingMetadata-module__title___Rsj55"]').text
    ListingName.append(listing_name)

    try:
        price = result.find_element(By.XPATH, './/span[@class="Money-module__root___jRyq5"]').text
        new_price = ""
        old_price = ""
        Price.append(price)
        NewPrice.append(new_price)
        OldPrice.append(old_price)
    except NoSuchElementException:
        price = ""
        new_price = result.find_element(By.XPATH, './/span[@class="Money-module__root___jRyq5 Price-module__onSale___1pIHp"]').text
        old_price = result.find_element(By.XPATH, './/span[@class="Money-module__root___jRyq5 Price-module__original___I3r3D"]').text
        Price.append(price)
        NewPrice.append(new_price)
        OldPrice.append(old_price)

    size = result.find_element(By.XPATH, './/p[@class="ListingMetadata-module__size___e9naE"]').text
    Size.append(size)

    try:
        time = result.find_element(By.XPATH, './/span[@class="ListingAge-module__strikeThrough___LoORR"]').text
    except NoSuchElementException:
        time = ""
    Time.append(time)

    try:
        last_bump = result.find_element(By.XPATH, './/span[@class="ListingAge-module__dateAgo___xmM8y"]').text
        LastBump.append(last_bump)
    except NoSuchElementException:
        last_bump = ""
        LastBump.append(last_bump)

    link = result.find_element(By.XPATH, './/a[@class="listing-item-link"]').get_attribute('href')
    Link.append(link)

ItemDataFrame = pd.DataFrame(zip(ListingName, Price, NewPrice, OldPrice, Size, Time, LastBump, Link), columns = ['Name', 'Price', 'NewPrice', 'OldPrice', 'Size', 'Time', 'LastBump', 'Link'])

html = ItemDataFrame.to_html()
with open('dataframe.html', 'w', encoding='utf-8') as f:
    f.write(html)