from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
data = list


def open_browser():
    chrome_browser.get('https://web.telegram.org/k/#@Quickchat_Emerson_bot')
    time.sleep(32)


def open_chat():
    user_name = 'Emerson AI'
    links = chrome_browser.find_elements("xpath", "//a[@href]")
    for link in links:
        if "Emerson AI" in link.get_attribute("innerHTML"):
            link.click()
            break


# time.sleep(1)
def read_data(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        d = list(reader)[1:]
    return d


if __name__ == '__main__':
    chrome_browser = webdriver.Chrome(executable_path='/Users/abhitejamandava/Downloads/chromedriver')
    open_browser()
    open_chat()
    time.sleep(8)
    data = read_data("data.csv")
    print(data)

    for i in range(len(data)):
        in_message = data[i][0]
        out_messages = data[i][1]
        out_messages = out_messages.split(",")
        message_box = chrome_browser.find_element("xpath",
                                                  "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[8]/div[1]/div[1]")
        message_box.send_keys(in_message)
        message_box = chrome_browser.find_element("xpath",
                                                  "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[5]")

        message_box.click()
        time.sleep(8)
        ids = chrome_browser.find_element("xpath",
                                          "//div[@class='message spoilers-container']").text
        output = ids
        print(output[-1])
        time.sleep(2)








