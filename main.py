import google.generativeai as genai
import PIL.Image
import pathlib
import textwrap
import sys
import json

from IPython.display import display
from IPython.display import Markdown

import os
from dotenv import load_dotenv
from enum import Enum

class TextColor(Enum):
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    WHITE = '\033[39m'

def color_text(color: TextColor, text:str):
    return color + text + TextColor.WHITE.value

class Hemilia:
    def __init__(self):
        load_dotenv()
        self.load_api_key()
        MODEL_NAME_VISION="gemini-pro-vision"
        MODEL_NAME="gemini-1.5-pro-latest"

        self.model_vision = genai.GenerativeModel(model_name=MODEL_NAME_VISION)
        self.model = genai.GenerativeModel(model_name=MODEL_NAME)

        # history = self.process_images()
        # self.save_json("model_base.json", history)
        history = self.load_history_from_file("model_base.json")
        self.start_chat(history=history)
        
    def start_chat(self, history):
        self.add_to_history("Se apresente como Hemília, uma assistente pessoal para informações sobre Hemofilia e Responda de acordo com as informações fornecidas", history=history)
        chat = self.model.start_chat(history=history)
        prompt = input(color_text(TextColor.ORANGE.value, "User: "))
        # print(color_text(TextColor.ORANGE.value, prompt))

        while prompt.upper() != "FIM":
            response = chat.send_message(prompt)
            print(color_text(TextColor.GREEN.value, "Hemília:"))
            print(color_text(TextColor.GREEN.value, response.text))
            prompt = input(color_text(TextColor.ORANGE.value, "User: "))

        print(color_text(TextColor.GREEN.value, "Hemília:"))
        response = chat.send_message(prompt)
        print(color_text(TextColor.GREEN.value, response.text))

    def load_history_from_file(self, file_name):
        with open(file_name) as f:
            data = json.load(f)
            return data

    def save_json(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def process_images(self):
        folder = pathlib.Path("./images/")
        history = []
        for item in folder.glob("*.jpeg"):
            img = PIL.Image.open(item)
            response = self.model_vision.generate_content(img)
            self.add_to_history(response.text, history=history)
        return history
        
    def load_api_key(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def to_markdown(self, text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    def add_to_history(self, text, history):
        action = {}
        action["role"] = "user"
        action["parts"] = [text]
        history.append(action)

def main():
    try:
        start = Hemilia()
    except ValueError as ve:
        return str(ve)

if __name__ == "__main__":
    sys.exit(main())
