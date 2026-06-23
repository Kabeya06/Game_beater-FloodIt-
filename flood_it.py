#
# from kivy.app import App
# from kivy.core.window import Window
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.spinner import Spinner
# from kivy.uix.button import Button
# from kivy.uix.label import Label

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


from pprint import pprint
import numpy as np
import json

columns = 10 #2 # 4 6 8 10

# Initialize Chrome Options
chrome_options = Options()

# Add the experimental option to detach the browser
chrome_options.add_experimental_option("detach", True)

# Pass options into your driver initialization
driver = webdriver.Chrome(options=chrome_options)

driver.get(f'https://unixpapa.com/floodit/?sz={columns}&nc=6')# ("https://unixpapa.com/floodit/?sz=10&nc=6")

def get_board():

    board_matrix = driver.find_element(By.XPATH, "//div[@id='game']").get_attribute("innerHTML").split('background-color')
    board_matrix = [string[:string.find('position')].strip(':').strip('; ') for string in board_matrix][1:]
    return np.array(board_matrix).reshape(-1, columns).T



pprint(get_board())
