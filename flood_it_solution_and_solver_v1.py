from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from scipy.ndimage import label
from pprint import pprint
from PIL import Image
from datetime import datetime

import ast
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

columns = 6 #2 # 6 8 10

# Initialize Chrome Options
chrome_options = Options()

# Add the experimental option to detach the browser
chrome_options.add_experimental_option("detach", True)

# Pass options into your driver initialization
driver = webdriver.Chrome(options=chrome_options)

driver.get(f'https://unixpapa.com/floodit/?sz={columns}&nc=5')# ("https://unixpapa.com/floodit/?sz=10&nc=6")

def get_board():

    board_matrix = driver.find_element(By.XPATH, "//div[@id='game']").get_attribute("innerHTML").split('background-color')
    board_matrix = [string[:string.find('position')].strip(':').strip('; ') for string in board_matrix][1:]
    return np.array(board_matrix).reshape(-1, columns).T#, axis=1)

def click_colour(pixel):
    pass

def current_posession(grid):
    color = grid[0, 0]

    # Create a binary mask where the color matches
    mask = (grid == color).astype(int)

    # Label connected components (islands)
    labeled_array, num_features = label(mask)

    color_islands = []
    for i in range(1, num_features + 1):
        # Isolate each specific island
        island_mask = (labeled_array == i).astype(int)
        color_islands.append(island_mask)

    return color_islands[0]


def parse_rgb(color_str):

        # Handle 'rgb(r, g, b)' strings
    if color_str.startswith('rgb'):
        # Strip 'rgb(' and ')' then split by comma
        return tuple(map(int, color_str[4:-1].split(',')))
    return color_str

def create_frame(matrix):
    size = 10**2
    img = Image.new("RGB", (columns, columns))
    for y, row in enumerate(matrix):
        for x, color in enumerate(row):
            img.putpixel((x, y), Image.new("RGB", (1, 1), color).getpixel((0, 0)))

    return img

def step(game_board = get_board()):

    coords = np.argwhere(current_posession(game_board) == 1)
    # print(coords)
    parsed = [[parse_rgb(c) for c in row] for row in game_board]
    palette = list(np.unique(game_board))

    x = 0

    for i in range(len(palette)):
        if game_board[0, 0] in palette[i]:
            x = i
            break

    palette.pop(x)

    choices = {}

    for color in palette:

        new_board = game_board.copy()

        for coord in coords:
            new_board[tuple(coord)] = color
        tally = np.sum(new_board == color)
        # print(tally)
        if int(tally) >= int(columns*columns):
            choices[color] = new_board
            global stop
            stop = False
            return choices
        elif len(coords) < int(tally):
            choices[color] = new_board

    return choices

stop = True
steps_dict = step()

while stop:
    next_steps = {}
    for i in steps_dict:
        change = step(steps_dict[i])
        # print(stop??)
        for x in change:
            next_steps[f' {i} | {x}'] = change[x]
            if not stop: break
        if not stop: break

    del steps_dict
    steps_dict = next_steps.copy()

print('\n')

solution = list(steps_dict.keys())[-1]

print(solution.split('|'))

for i in solution.split('|'):
    i = i.strip()
    element = driver.find_element(By.XPATH, f"//*[contains(@style, 'background-color: {i}')]")
    element.click()

print('done')






