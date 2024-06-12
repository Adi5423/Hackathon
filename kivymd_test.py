import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.radiobutton import RadioButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
import json
import requests
import random

class QuestionAnsweringCard(MDCard):
    question = StringProperty()
    options = StringProperty()

class GenAIJournalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Red"
        self.root = BoxLayout(orientation="vertical")
        self.root.add_widget(MDLabel(text="GenAI Journal", font_size=40, halign="center"))
        self.question_card = QuestionAnsweringCard()
        self.root.add_widget(self.question_card)
        self.next_button = MDRaisedButton(text="Next", pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.next_button.bind(on_press=self.next_question)
        self.root.add_widget(self.next_button)
        self.current_question = 0
        self.questions = self.load_questions()
        self.display_question()

    def load_questions(self):
        with open("qna_bank.json", "r") as file:
            return json.load(file)

    def display_question(self):
        question = self.questions[self.current_question]
        self.question_card.question = question["question"]
        self.question_card.options = "\n".join(question["options"])

    def next_question(self, instance):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.show_script_generation()

    def show_script_generation(self):
        self.root.clear_widgets()
        self.root.add_widget(MDLabel(text="Script Generation", font_size=40, halign="center"))
        self.script_text = MDTextField(multiline=True, readonly=True)
        self.root.add_widget(self.script_text)
        self.generate_script_button = MDRaisedButton(text="Generate Script")
        self.generate_script_button.bind(on_press=self.generate_script)
        self.root.add_widget(self.generate_script_button)

    def generate_script(self, instance):
        # Implement script generation logic here
        self.script_text.text = "Generated script will appear here"

    def on_start(self):
        self.root.add_widget(self.next_button)

if __name__ == "__main__":
    GenAIJournalApp().run()