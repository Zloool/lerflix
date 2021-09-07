from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver.v2 as uc
from settings import url

def get_tasks(username, password):
    # PROXY = "localhost:8080"
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'")

    driver = uc.Chrome()
    # driver = webdriver.Chrome(r'D:\chromedriver.exe', chrome_options=chrome_options)
    # driver.manage().window().minimize()
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.get(url)
    # assert "Selenium Easy Demo - Simple Form to Automate using Selenium" in driver.title

    eleUserMessage = driver.find_element_by_id("username")
    eleUserMessage.click()
    # sleep(1000)
    eleUserMessage.send_keys(username)
    # sleep(1000)
    eleUserMessage = driver.find_element_by_id("password")
    eleUserMessage.click()
    # sleep(1000)
    eleUserMessage.send_keys(password)
    # sleep(1000)


    eleUserMessage = driver.find_element_by_id("post-ok")
    eleUserMessage.click()

    wait = WebDriverWait(driver, 30)
    # print(dir(By))
    men_menu = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.sharktank-drawer > div > span'), "You are eligible to get tasks."))

    # sleep(2000)
    eleShowMsgBtn=driver.find_element_by_css_selector('.sharktank-drawer > div > button')
    eleShowMsgBtn.click()

    men_menu = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]')))
    men_menu = wait.until(EC.invisibility_of_element((By.XPATH, '//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]')))

    # //*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]
    # eleYourMsg=driver.find_element_by_id("display")
    # assert "Test Python" in eleYourMsg.text

    urgent = driver.find_element_by_xpath('//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[1]/button/span').text
    twentyfour = driver.find_element_by_xpath('//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/button/span').text
    twothree = driver.find_element_by_xpath('//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[3]/button/span').text
    fourseven = driver.find_element_by_xpath('//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[4]/button/span').text
    wplus = driver.find_element_by_xpath('//*[@id="appView"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div[5]/button/span').text


    total = 0 + int(urgent) + int(twentyfour) + int(twothree) + int(fourseven) + int(wplus)
    # print("Total: " + str(total))

    driver.close()
    return total

if __name__ == "__main__":
    print("Test")
    import undetected_chromedriver.v2 as uc
    driver = uc.Chrome()
    with driver:
        driver.get('https://nowsecure.nl')