from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import csv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def try_click(driver, xpath):
    """

    :param driver: by default
    :param xpath: xpath that we need to click
    :return: False if we fail to click the element in 5 times, otherwise if we can then True
    """
    i = 0
    while i < 5:
        try:
            driver.find_element(By.XPATH, xpath).click()
            i = 6
        except:
            time.sleep(1)
            i = i + 1
    if i == 5:
        return False
    return True


def check_exists_by_xpath(driver, xpath):
    """

    :param driver:
    :param xpath: xpath if we want to find
    :return: return False if we could not find, return True otherwise
    """
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

opt = Options()
""""""
opt.add_argument("--disable-infobars")      # disable the info bars
opt.add_argument("start-maximized")         # used to maximize the window of Chrome
opt.add_argument("--disable-extensions")    # disable extensions such as Translations
opt.add_argument("--lang=ja")               # set language as Japanese by default
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
  })    # Pass the argument 1 to allow and 2 to block. In this case, we set all 1 by default for the sake of testing
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)


def login(file):
    i = 0
    file = open(file, "r")
    reader = csv.reader(file)
    next(reader)    # skip the header of the csv file
    for line in reader:
        if i != 0:
            driver.execute_script("window.open('about:blank', 'tab" + str(i) + "');")
            driver.switch_to.window("tab" + str(i))
        i = i + 1
        driver.get("https://phase2.remote-oasis.jp/login")
        x = check_exists_by_xpath(driver, "//input[@name='email']")
        while x == False:
            time.sleep(1)
            x = check_exists_by_xpath(driver, "//input[@name='email']")
        driver.find_element(By.XPATH, "//input[@name='email']").send_keys(line[0])  # email
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(line[1])   # password
        if not try_click(driver, "//button[@class='btn btn-primary login-button']"):    # log-in button
            print ("User " + str(i) + " cannot click login-button")
            continue
        if not try_click(driver, "//div[text()='"+line[2]+"']"):        # space
            print ("User " + str(i) + " cannot choose space with the name " + line[2])
            continue
        if not try_click(driver, "//button[@class='MuiButtonBase-root MuiButton-root MuiButton-contained workplace_sso-btn_submit']"):      # enter space
            print("User " + str(i) + " cannot click MuiButtonBase")
            continue
        if not try_click(driver, "//div[text()='"+line[3]+"']"):        # floor
            print ("User " + str(i) + " cannot choose floor with the name " + line[3])
            continue
        if not try_click(driver, "//button[@class='btn btn-primary login-button-floors']"):     # join floor
            print("User " + str(i) + " cannot click login-button-floor")
            continue
        if not try_click(driver, "//div[@id='re-" + line[4]+ "']"):     # join unit
            print("User " + str(i) + " cannot click unit")
            continue
        if not bool(line[5]):                                           # join unit
            print ("User " + str(i) + " does not join the meeting")
            continue
        time.sleep(1)
        driver.find_element(By.XPATH,"//div[@id='re-" + line[4]+ "']").click()


file = "C:\\Users\\HungNV11\\PycharmProjects\\BotAutoLogin_Oasis\\Data_botauto_login.csv"   # address of the csv file
login(file)
while True:
    time.sleep(1)








