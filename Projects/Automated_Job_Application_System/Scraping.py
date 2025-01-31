from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Set up WebDriver
driver = webdriver.Chrome()

# Open Naukri.com
driver.get("https://www.naukri.com/")
time.sleep(3)

# Search for Jobs
search_box = driver.find_element(By.ID, "qsb-keyword-sugg")  # Job Role Input
search_box.send_keys("Data Scientist")  # Change this to your preferred job role
time.sleep(1)

location_box = driver.find_element(By.ID, "qsb-location-sugg")  # Location Input
location_box.send_keys("Bangalore")  # Change this to your preferred location
time.sleep(1)

search_box.send_keys(Keys.RETURN)  # Press Enter to search
time.sleep(5)

# Extract Job Listings
jobs = driver.find_elements(By.CSS_SELECTOR, ".jobTuple.bgWhite")

job_data = []
for job in jobs[:10]:  # Scrape first 10 jobs
    try:
        title = job.find_element(By.CSS_SELECTOR, "a.title.fw500.ellipsis").text
        company = job.find_element(By.CSS_SELECTOR, "a.subTitle.ellipsis.fleft").text
        experience = job.find_element(By.CSS_SELECTOR, ".ellipsis.fleft.expwdth").text
        location = job.find_element(By.CSS_SELECTOR, ".ellipsis.fleft.locWdth").text
        job_link = job.find_element(By.CSS_SELECTOR, "a.title.fw500.ellipsis").get_attribute("href")
        
        job_data.append([title, company, experience, location, job_link])
    except Exception as e:
        print("Error:", e)

# Close the browser
driver.quit()

# Save Data to CSV
df = pd.DataFrame(job_data, columns=["Job Title", "Company", "Experience", "Location", "Apply Link"])
df.to_csv("naukri_jobs.csv", index=False)

print("Job data saved to naukri_jobs.csv")
