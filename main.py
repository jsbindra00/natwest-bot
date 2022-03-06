from tkinter import E
from docutil import DocUtil
import os
import subprocess
from time import sleep
from InputExecutor import InputExecutor, EMULATORARGS
import sys
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

customerNumber = "12345"

pin = "12345"
password = "12345"
TIMEOUT_DURATION = 3




def PullAuthentificationCharacters(browser):
    requiredIndices = []
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label.wizardLabelRememberMeWide')))

    indicesLabels = browser.find_elements_by_css_selector("label.wizardLabelRememberMeWide")

    # the first six labels are the required indices
    for lab in indicesLabels[:6]:
        index = int(re.sub("[^0-9]", "", lab.text))
        requiredIndices.append(index)
    return requiredIndices



def BypassAuthentification(browser):
    print("Bypassing authentification...")

    requiredIndices = PullAuthentificationCharacters(browser)
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
    
    inputFields = browser.find_elements_by_xpath("//input[@type='password']")

    enterInfoFrom = [pin, password]

    for i in range(0,6):
  

        infoIndex = int(i / 3)
        currentInfo = enterInfoFrom[infoIndex]
        enterCharacter = currentInfo[requiredIndices[i] - 1]
        print(str(enterCharacter))
        inputFields[i].send_keys(str(enterCharacter))

    sleep(2)
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_mainContent_next_text_button_button"]'))).click()

    



def ProcessCard(browser, cardLink):
    # navigate to the card.
    cardLink.click()

    # click export 
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ctl00_mainContent_VT2ITCHF"))).click()

    # click export to csv
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_mainContent_VTSDDDA"]/option[1]'))).click()

    # click download
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_mainContent_SS7-LWLA_button_button"]'))).click()

    # wait for download to initiate
    sleep(1)




    
def PullAllCards(browser):

    # wait until all cards on central hub have loaded.
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.cardContent')))

    # pull the links to the transaction page to each card
    numCards = len([card for card in browser.find_elements_by_css_selector("div.cardContent a") if card.text.lower() == "view transactions"])
    print("Found " + str(numCards) + " cards...")

    # iterate through each card.
    for i in range(0, numCards):
        # wait for the link to be clickable.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.cardContent a")))
        # process the card
        ProcessCard(browser, [card for card in browser.find_elements_by_css_selector("div.cardContent a") if card.text.lower() == "view transactions"][i])

        # come back to the central hub.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_menu__fffd5cd41206055f_AS1MNUAnchor"]'))).click()


        

    







def launch():
    # launch browser

 
    print("Configuring browser options...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-data-dir=C:\\Users\\jasbi\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    options.add_experimental_option("prefs",{"download.default_directory" : r"D:\FILES\Desktop\Expenditure analysis\Expenditure Updater Script"})

    print("Launching browser...")
    browser = webdriver.Chrome(r"D:\FILES\Desktop\Expenditure analysis\chromedriver.exe", chrome_options=options)

    print("Redirecting to Natwest...")
    browser.get('https://www.onlinebanking.natwest.com/Default.aspx')
   

    try:
        # all of the inputs are in a <frame> tag. switch the reference frame of the browser to that frame.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//*[@id=\"ctl00_secframe\"]")))

        try:
            pass
            # accept the cookies popup.
            # WebDriverWait(browser, TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'))).click()
        except(Exception):
            pass
        

        # type in the customer number into the input tag.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_LI5TABA_CustomerNumber_edit"]'))).send_keys(customerNumber)

        # progress to the authentification page
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_LI5TABA_LI5-LBB_button_button"]'))).click()

        # bypass the authentification
        BypassAuthentification(browser)

        # now we are onto the online banking central hub.
        # find all <a> tags with text "view transactions"
        PullAllCards(browser)

        
        
    except Exception as e:
        print(e)



    while True:
        continue

    

launch()












# # navigate to authentification
# # need a way to pull the required characters.
#     # save the html
#     # run html through authenticator script
#         # returns the 6 required characters.



# def PullRequiredPinDigits():
#     pass

# def PullRequiredPasswordCharacters():
#     pass

# requiredPinDigits = []
# requiredPasswordCharacters = []


# logFile = r"D:\FILES\Desktop\Expenditure analysis\Expenditure Updater Script\filesaver.txt"
# inputexecutor = InputExecutor()
# inputexecutor.execute(logFile)

