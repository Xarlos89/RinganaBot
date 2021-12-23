from bs4 import BeautifulSoup
from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
from secret import *
import requests
import time
import random


driver = webdriver.Chrome() #Initialize a browser window
matchcodes = [] # A list of matchcodes, called with grab_matchcodes_customer()

def login():
	driver.get(COM_url)
	time.sleep(2)
	CookieButton = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[2]/div[1]/button[2]")
	CookieButton.click()
	time.sleep(2)
	#Enter Username
	driver.get(COM_url + '/anmeldung/')
	time.sleep(1)
	login = driver.find_elements_by_xpath('//*[@id="post-5273"]/div/section/div/div[1]/form/label[1]/input')
	print("Logging in...")
	login[0].send_keys(username) 
	#Enter Password
	clickbutton1 = driver.find_element_by_xpath('//*[@id="loginButton"]')
	clickbutton1.click()
	time.sleep(1)
	user = driver.find_element_by_xpath('//*[@id="post-5273"]/div/section/div/div[1]/form/label[2]/input') 
	user.send_keys(password) 
	#Click log-in button
	LOG = driver.find_elements_by_xpath('//*[@id="loginButton"]') 
	LOG[0].click() 
	print("Login Successful") 
	time.sleep(3) # Logs into PRODUCTION site
def login_to_test():
	driver.get(TEST_url)
	time.sleep(2)
	CookieButton = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div[2]/div[1]/button[2]")
	CookieButton.click()
	time.sleep(2)
	#Enter Username
	driver.get(TEST_url + '/anmeldung/')
	time.sleep(1)
	login = driver.find_elements_by_xpath('//*[@id="post-5273"]/div/section/div/div[1]/form/label[1]/input')
	print("Logging in...")
	login[0].send_keys(username) 
	#Enter Password
	clickbutton1 = driver.find_element_by_xpath('//*[@id="loginButton"]')
	clickbutton1.click()
	time.sleep(1)
	user = driver.find_element_by_xpath('//*[@id="post-5273"]/div/section/div/div[1]/form/label[2]/input') 
	user.send_keys(testing_password) 
	#Click log-in button
	LOG = driver.find_elements_by_xpath('//*[@id="loginButton"]') 
	LOG[0].click() 
	print("Login Successful") 
	time.sleep(5) # Logs into TESTING site.

def check_exists_by_xpath(xpath): #Checks if x-path element exists, returns boolean
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def grab_matchcodes_customer():
	r = requests.get(all_products)
	data = r.json()
	numberOfProducts = len(data)
	for x in range(0,numberOfProducts):
		matchcodes.append(data[x]["matchcode"])# Grabs all currentproduct matchcodes

def TEST_Cart_Add_ranItem():
	driver.get(TEST_url + '/shopping-cart/')
	grab_matchcodes_customer()
	time.sleep(3)
	try: # try opening the personal shopping cart. 
		personal_cart = driver.find_element_by_xpath('//*[@id="post-5268"]/span/div/div[2]/div[1]/div/div/div')
		personal_cart.click()
		time.sleep(.5)
		for i in range(0,len(matchcodes)):
			try: #Try adding to cart via the matchcode
				product = random.randint(0,len(matchcodes))
				matchcode_text_box = driver.find_element_by_xpath('//*[@id="vs3__combobox"]/div[1]/input')
				print('Adding ' + matchcodes[product] + ' to the cart.')
				matchcode_text_box.click()
				matchcode_text_box.send_keys(matchcodes[product])
				time.sleep(2)
				matchcode_text_box.send_keys(Keys.ENTER)
				time.sleep(2)
				try: # Remove item from shopping cart. 
					remove_item = driver.find_element_by_xpath('//*[@id="post-5268"]/span/div/div[3]/div/div[2]/table/tbody/tr[1]/td[6]/div/button/span')
					print('Removing item.')
					remove_item.click()
					time.sleep(2)
				except:
					print('Cannot remove ' + matchcodes[product] + ' from Sopping Cart, clearing error code.') ### Shit fails here for some reason when there is error adding to cart. 
					driver.refresh()
					time.sleep(4)
					personal_cart.click()


			except:
				print('Cannot add ' + matchcodes[product] + ' to the shopping cart.')
	except:
		print('Error opening Personal Shopping Cart') # TO-DO: Fix Crash bug when product is unavailible


