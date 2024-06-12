import tkinter as tk
import json
from groq import Groq
from gtts import gTTS
import io
import os
import random
import matplotlib.pyplot as plt
import pandas as pd

# API key (replace with yours)
api_key = "YOUR_API_KEY"

# Question bank
with open("qna_bank.json", "r") as file:
    question_bank = json.load(file)

# Initialize questions and responses
current_question_index = 0
responses = []

# Function to choose a random question
def choose_question():
    global current_question_index
    current_question_index = random.randint(0, len(question_bank) - 1)
    return question_bank[current_question_index]

# Function to store responses
def store_responses(user_response, free_text):
    responses.append((question_bank[current_question_index]["question"], user_response, free_text))

# Function to generate script
def generate_script(qna_pairs):
    qna_pairs_string = json.dumps(qna_pairs)
    query = f"""
    below are the few details which bot collected from user's that day's activity, so please create good 30-60 seconds script , it should only contains text which user can directly read & speak. Or with bot can directly convert from text to speech. Don't add anything except script in output. User is going to do voice over with this, so use I instead of You.

    {qna_pairs_string}

    """

    chat_completion = Groq(api_key=api_key).chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama3-8b-8192",
    )

    script = chat_completion.choices[0].message.content.split('"')[1]
    return script

# Function to generate audio
def generate_audio(script):
    tts = gTTS(text=script, lang="en", slow=False)
    tts.save("day1.mp3")

# Function to calculate Ikigai score
def calculate_ikigai_score(passion, mission, profession, vocation):
    return passion + mission + profession + vocation

# Function to display Ikigai score and pie chart
def display_ikigai_score(score):
    data = pd.DataFrame({"Category": ["Passion", "Mission", "Profession", "Vocation"], "Score": [passion, mission, profession, vocation]})

    fig, ax = plt.subplots()
    ax.pie(data["Score"], labels=data["Category"], autopct="%1.1f%%")
    ax.axis("equal")

    fig.savefig("ikigai_pie.png")
    img = tk.PhotoImage(file="ikigai_pie.png")
    ikigai_label.config(image=img)
    ikigai_score_label.config(text=f"Ikigai Score: {score}")

# Main application window
root = tk.Tk()
root.title("GenAI Journal")
root.geometry("800x600")

# Section selection frame
section_frame = tk.Frame(root, padx=10, pady=10)
section_frame.pack(fill=tk.X)

section_var = tk.StringVar()
section_var.set("Intro")

intro_radio = tk.Radiobutton(section_frame, text="Intro", variable=section_var, value="Intro")
qa_radio = tk.Radiobutton(section_frame, text="Question-Answering", variable=section_var, value="QA")
script_radio = tk.Radiobutton(section_frame, text="Script Generation", variable=section_var, value="Script")
audio_radio = tk.Radiobutton(section_frame, text="Convert Script to Audio", variable=
