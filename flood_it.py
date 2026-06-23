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
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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


# pprint(get_board())

def click_colour():
    pass

# Set up initial grid data dimensions (10x10)

# data = get_board()

colors = get_board()

# np.array([['rgb(0, 187, 0)', 'red'],
                   # ['cyan', 'rgb(255, 204, 102)']])

# Convert 'rgb(r, g, b)' strings to normalized (0-1) tuples for Matplotlib
def parse_rgb(c):
    if c.startswith('rgb'):
        vals = eval(c.replace('rgb', ''))
        return [v/255 for v in vals]
    return c

# Convert array for plotting
plot_data = np.vectorize(parse_rgb, otypes=[object])(colors)

# Create the visualization
fig, ax = plt.subplots(figsize=(10, 10))
for (i, j), color in np.ndenumerate(plot_data):
    print((i, j), color)
    ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))

# Formatting
ax.set_xlim(0, columns)
ax.set_ylim(0, columns)
ax.set_xticks([0.5, 1.5])
ax.set_yticks([0.5, 1.5])
ax.set_xticklabels(['0', '1'])
ax.set_yticklabels(['0', '1'])
# ax.set_aspect('equal')

plt.tight_layout()

plt.title("Matplotlib Color Grid")
plt.show()
