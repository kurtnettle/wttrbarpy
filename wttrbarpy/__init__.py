import json
import os

curr_dir = __file__[:-11]  # delete the suffix __init__.py


try:
    with open(f"{curr_dir}/resources/emojis.json", "r") as f:
        emojis = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Failed to open emojis.json")

try:
    with open(f"{curr_dir}/resources/icons.json", "r") as f:
        icons = json.load(f)
except FileNotFoundError as e:
    raise FileNotFoundError("Failed to open icons.json")
