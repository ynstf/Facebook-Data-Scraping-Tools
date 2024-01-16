from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# take credential
mail = input("email : ")
pswd =input("password : ")
steps = int(input("namber of see more comments : "))
post_url = input("post page url : ")

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

browser.get(post_url)

# Step 7) Scroll down to load all users (as mentioned in the previous response)
steps = 10
SCROLL_PAUSE_TIME = 4   # You can adjust this value based on your needs

# Get scroll height
last_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
n = 0
sleep(4)
while True:
    sleep(SCROLL_PAUSE_TIME)
    
    if n >steps:
        break
    
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    n+=1
    print(f"Processing: {n}", end='\r', flush=True)
    
    try:
        show_more_button = WebDriverWait(browser, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "عرض مزيد من التعليقات")]'))
        )
    except:
        try:
            show_more_button = WebDriverWait(browser, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "View more comments")]'))
        )
        except:
            print("Show more button not found. Exiting loop.")

    # Click the button to reveal more comments
    show_more_button.click()
        
print(f"Processing: {n}")

# Step 8) Extract user IDs after all users are loaded

html_source_comments = browser.page_source

soup_comments = BeautifulSoup(html_source_comments, 'html.parser')

comment_user_elements = soup_comments.find_all('a',{"class":"x1i10hfl"})

all_id=[]
for i in comment_user_elements:
    url = i["href"]
    if "https://www.facebook.com/" in url:
        if "?comment_id=" in url.split("https://www.facebook.com/")[1]:
            ID = url.split("https://www.facebook.com/")[1].split("?comment_id=")[0]
            all_id.append(ID)
        if "comment_id=" in url.split("https://www.facebook.com/")[1]:
            #print(url.split("https://www.facebook.com/")[1].split("comment_id=")[0])
            if "profile.php?id=" in url.split("https://www.facebook.com/")[1].split("comment_id=")[0]:
                ID = url.split("https://www.facebook.com/")[1].split("&comment_id=")[0].split('profile.php?id=')[1]
                all_id.append(ID)
    
print(f'you have {len(set(all_id))} user')


# Specify the path where you want to save the file

file_path = "user_ids.txt"

# Open the file in write mode

i = 0

with open(file_path, 'w') as file:

    # Write each user ID to the file

    for user_id in set(all_id):

        file.write(f"User ID: {user_id}\n")

        i+=1

        # Print the dynamic count in the command prompt

        print(f"Processing: {i}", end='\r', flush=True)

print(f"Processing: {i}")

print(f"User IDs have been saved to {file_path}")