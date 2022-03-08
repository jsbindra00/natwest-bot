from pydoc import Doc
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from docutil import DocUtil
from datetime import date

customerNumber = "123"

pin = "123"
password = "123"
TIMEOUT_DURATION = 3
EXPENDITURE_SAVE_LOCATION = r"D:\FILES\Desktop\other\Expenditure analysis\Analysis\2022\Expenditure arrivals"


SEARCH_FROM_DATE = "01/01/2022"
SEARCH_TO_DATE = date.today().strftime("%d/%m/%Y")


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



def PullStatements(browser):
    print("Pulling statements...")
    browser.switch_to.default_content()
    WebDriverWait(browser, TIMEOUT_DURATION).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="ctl00_secframe"]')))

    try:
        # click the statements hub
        [button for button in browser.find_elements_by_css_selector("a") if button.text.lower() == "statements"][0].click()

        # click the download statements button
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_SS1AALDAnchor"]'))).click()

        # choose date span
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_SS6NLAAnchor"]'))).click()



        SEARCH_FROM_DATE_LST = SEARCH_FROM_DATE.split("/")

        # configure DATE ONE
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_FROM_DATE_LST[0] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEA_day"]'))
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_FROM_DATE_LST[1] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEA_month"]/option[2]'))
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_FROM_DATE_LST[2] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEA_year"]/option[1]'))

        SEARCH_TO_DATE_LST = SEARCH_TO_DATE.split("/")

        # configure DATE TWO
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_TO_DATE_LST[0] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEB_day"]'))
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_TO_DATE_LST[1] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEB_month"]/option[1]'))
        browser.execute_script("arguments[0].setAttribute('value'," + SEARCH_TO_DATE_LST[2] + ")", browser.find_element_by_xpath('//*[@id="ctl00_mainContent_SS6DEB_year"]/option[1]'))

        # click download
        browser.find_element_by_xpath('//*[@id="ctl00_mainContent_FinishButton_button"]').click()

        # click export
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_SS7-LWLA_button_button"]'))).click()

    except Exception as e:
        print(e)
 



def launch():

 
    print("Configuring browser options...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    chromeProfileLocation = r"C:\Users\jasbi\AppData\Local\Google\Chrome\User Data\Default"

    options.add_argument("user-data-dir="+chromeProfileLocation)
    options.add_experimental_option("prefs",{"download.default_directory" : EXPENDITURE_SAVE_LOCATION})

    print("Launching browser...")
    browser = webdriver.Chrome(r"D:\FILES\Desktop\other\Expenditure analysis\chromedriver.exe", chrome_options=options)

    print("Redirecting to Natwest...")
    browser.get('https://www.onlinebanking.natwest.com/Default.aspx')
   
    try:
        # all of the inputs are in a <frame> tag. switch the reference frame of the browser to that frame.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//*[@id=\"ctl00_secframe\"]")))

        # type in the customer number into the input tag.
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_LI5TABA_CustomerNumber_edit"]'))).send_keys(customerNumber)

        # progress to the authentification page
        WebDriverWait(browser, TIMEOUT_DURATION).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_mainContent_LI5TABA_LI5-LBB_button_button"]'))).click()

        # bypass the authentification
        BypassAuthentification(browser)

        # now we are onto the online banking central hub.
        PullStatements(browser)
        
    except Exception as e:
        browser.quit()
        print(e)


    while True:
        i = 3
    return True
  

while True:
    try:
        DocUtil.DeleteFolder(EXPENDITURE_SAVE_LOCATION)
    except(Exception):
        pass
    DocUtil.CreateFolderAbsoluteDirectory(EXPENDITURE_SAVE_LOCATION)
  
    if launch():
        break


