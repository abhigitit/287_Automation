from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import spacy
import time
import csv
import os

data = list


# opens the browser with the given link
def open_browser():
    browser.get('https://web.telegram.org/k/#@Quickchat_Emerson_bot')
    time.sleep(5)


# selects the chat window based on the xpath
def open_chat():
    user_name = 'Emerson AI'
    links = browser.find_elements("xpath", "//a[@href]")
    for link in links:
        if "Emerson AI" in link.get_attribute("innerHTML"):
            link.click()
            break


def read_data(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        d = list(reader)[1:]
    return d


# preprocessing the text for similarity comparision
def preprocess_word(word):
    word = word.lower()
    res = ''
    for s in word:
        if s.isalpha() or s == ' ' or s.isnumeric():
            res += s
    return res


if __name__ == '__main__':
    start_time = time.time()
    load_dotenv()
    fp = webdriver.FirefoxProfile(os.environ.get('FIREFOX_PROFILE_PATH'))
    browser = webdriver.Firefox(executable_path='drivers/geckodriver', firefox_profile=fp)
    open_browser()
    open_chat()
    time.sleep(5)

    data = read_data("data.csv")

    expected_responses = None
    positive_results = 0
    negative_results = 0
    for i in range(len(data)):
        in_message = data[i][0]
        expected_responses = data[i][1].split(",")

        # Input the message into the chat textbox
        message_box = browser.find_element(By.XPATH, "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[8]/div[1]/div[1]")
        message_box.send_keys(in_message)

        # Send the input message
        send_button = browser.find_element(By.XPATH, "//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[5]")
        send_button.click()
        time.sleep(5)

        # Extract the response to the input message
        last_response_xpath = "/html/body/div[1]/div[1]/div[2]/div/div/div[3]/div/div/section/div[last()]/div/div/div/div[1]"
        time.sleep(5)
        response = browser.find_element(By.XPATH, last_response_xpath)
        actual_response = response.text.split('\n')[0]

        # print(actual_response)

        # Perform cosine similarity check
        nlp = spacy.load('en_core_web_sm')

        actual_response = preprocess_word(actual_response)
        actual_out = nlp(actual_response)
        similarity = 0
        for expected_response in expected_responses:
            expected_out = nlp(expected_response)
            simi2 = actual_out.similarity(expected_out)
            similarity = max(similarity, simi2)

        print("Test case %s:" % str(i+1))
        print("Input: %s" % in_message)
        print("Output: %s" % actual_response)
        print("Similarity: %s" % similarity)
        if similarity > 0.40:
            positive_results += 1
            print("Result: PASS")
        else:
            negative_results += 1
            print("Result: FAIL")
        print()

    end_time = time.time()
    print("Total positive results: %d" % positive_results)
    print("Total negative results: %d" % negative_results)
    print("Total time consumed: %d secs" % (end_time - start_time))

    browser.quit()
