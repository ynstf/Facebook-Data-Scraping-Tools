from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup


# take credential
mail = input("email : ")
pswd =input("password : ")
steps = int(input("namber of pages : "))
group_members_url = input("member page of group : ")

# Step 1) Open Firefox in headless mode

options = webdriver.FirefoxOptions()

options.add_argument("--headless")  # Run the browser in headless mode

options.add_argument("--window-size=1920,1080")  # Set the window size

browser = webdriver.Firefox(options=options)

# Step 2) Navigate to Facebook

browser.get("http://www.facebook.com")

# Step 3) Search & Enter the Email or Phone field & Enter Password

username = browser.find_element("id", "email")

password = browser.find_element("id", "pass")

submit = browser.find_element("name", "login")

username.send_keys(mail)

password.send_keys(pswd)

# Step 4) Click Login

submit.click()

# Step 5) Wait for the login process to complete
sleep(5)

# Step 6) Navigate to the group members page

#group_members_url = "https://www.facebook.com/groups/933226904724060/members"#

browser.get(group_members_url)

group_members_url.split('/')[-2]

# Step 7) Scroll down to load all users (as mentioned in the previous response)

# Get scroll height
last_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
n = 0

while True:

    if n >steps:
        break

    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    ###sleep(SCROLL_PAUSE_TIME)
    
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    if new_height != last_height:
        n+=1
        print(f"Processing: {n}", end='\r', flush=True)
    last_height = new_height
    
print(f"Processing: {n}")

# Step 8) Extract user IDs after all users are loaded

html_source = browser.page_source

soup = BeautifulSoup(html_source, 'html.parser')

user_elements = soup.find_all("a", href=lambda href: href and f"/groups/{group_members_url.split('/')[-2]}/user/" in href)

user_ids = [element['href'].split("/")[-2] for element in user_elements]

print(f'you have {len(set(user_ids))} user')


# Specify the path where you want to save the file
file_path = "user_ids.txt"

# Open the file in write mode
i = 0

with open(file_path, 'w') as file:
    # Write each user ID to the file
    for user_id in set(user_ids):
        file.write(f"User ID: {user_id}\n")
        i+=1
        # Print the dynamic count in the command prompt
        print(f"Processing: {i}", end='\r', flush=True)

print(f"Processing: {i}")
print(f"User IDs have been saved to {file_path}")