import nltk
from nltk.stem import WordNetLemmatizer
import tkinter
from tkinter import *
import threading
import tkinter as tk
import webbrowser
import time
import datetime
import pickle
import numpy as np
from tkinter import *
from tkinter import messagebox
import login
import sys
import json
import random
import pyttsx3
import login
lemmatizer = WordNetLemmatizer()
sys.path.append('D:/project/flask/chatbotgui/login.py')
from tensorflow.keras.models import load_model

model = load_model('chatbot_model.h5')


intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

engine = pyttsx3.init()  # initialize the engine

def speak(text):
    engine.say(text)
    engine.runAndWait()

def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Chatmaster: " + res + '\n\n')

        # make the bot speak the response
        speak(res)

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

    if msg:
        if "http://" in res or "https://" in res:
            link_start = res.find("http")
            if link_start == -2:
                link_start = res.find("https")
            link_end = res.find(" ", link_start)
            if link_end == -1:
                link_end = len(res)
            link = res[link_start:link_end]

            ChatLog.configure(state="normal")
            #ChatLog.insert(tk.END, "You: {}\n".format(res))
            #ChatLog.tag_add("link", "1.0 + {}c".format(len("You: ")), "1.0 + {}c".format(len("You: ") + len(link)))
            ChatLog.tag_add("link", "end-{}c".format(len(link) + 2), "end-2c")
            ChatLog.tag_config("link", foreground="blue", underline=True)
            ChatLog.tag_bind("link", "<Button-1>", lambda event, url=link: open_link(url))
            ChatLog.configure(state="normal")
    ChatLog.yview(END)

def shut_down():
    p1 = Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    base.destroy()

if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init()  # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 10)


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


# TO LINK ENTER BUTTON
def enter_function(event):
    send()

def send_message(text=None):
    message = EntryBox.get("1.0", tk.END).strip()
    if message:
        if "http://" in message or "https://" in message:
            link_start = message.find("http://")
            if link_start == -1:
                link_start = message.find("https://")
            link_end = message.find(" ", link_start)
            if link_end == -1:
                link_end = len(message)
            link = message[link_start:link_end]

            EntryBox.configure(state="normal")
            EntryBox.insert(tk.END, "You: {}\n".format(message))
            EntryBox.tag_add("link", "1.0 + {}c".format(len("You: ")), "1.0 + {}c".format(len("You: ") + len(link)))
            EntryBox.tag_config("link", foreground="blue", underline=True)
            EntryBox.tag_bind("link", "<Button-1>", lambda event, url=link: open_link(url))
            EntryBox.configure(state="disabled")
        else:
            add_message("You", message)
    EntryBox.delete("1.0", tk.END)

    if text:
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + text + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))
        ChatLog.tag_configure('bot', foreground="#fedcba", font=("Verdana", 12))
        res = chatbot_response(text)
        ChatLog.insert(END, "Bot: " + res + '\n\n', 'bot')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Chatmaster: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

        # use speech recognition if msg equals "speak"
        if msg.lower() == "speak":
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, phrase_time_limit=5)
                spoken_text = r.recognize_google(audio)
                add_message("You", spoken_text)
                res = chatbot_response(spoken_text)
                add_message("Chatmaster", res)
            except sr.UnknownValueError:
                add_message("Chatmaster", "Sorry, I could not understand what you said.")
            except sr.RequestError as e:
                add_message("Chatmaster", "Sorry, there was an error processing your request. {}".format(e))

def repeatL():
    while True:
        start_speech_recognition()

def add_message(sender, message):
    EntryBox.configure(state="normal")
    EntryBox.insert(tk.END, "{}: {}\n".format(sender, message))
    EntryBox.configure(state="disabled")
    EntryBox.see(tk.END)

def open_link(url):
    webbrowser.open(url)


# Create Chat window
base = Tk()
base.title("SIGCE Chatbot")
img = PhotoImage(file="robo.GIF")
photo = Label(base, image=img)
photo.pack(pady=2)

base.geometry("450x550")
base.resizable(width=FALSE, height=FALSE)

# Bind Enter key to send message
base.bind('<Return>', enter_function)

# Create Chat log window
ChatLog = Text(base, bd=0, bg="light cyan", height="8", width="50", font="Arial", relief=FLAT)

ChatLog.configure(insertbackground='white', fg='white')
ChatLog.bind('<Key>', lambda e: 'break')


# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=1, bg="#25cdf7", activebackground="#3c9d9b", fg='#ffffff',
                    command=send_message)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")

# Place all components on the screen
scrollbar.place(x=426, y=10, height=386)
ChatLog.place(x=6, y=75, height=335, width=420)
EntryBox.place(x=6, y=420, height=70, width=420)
SendButton.place(x=160, y=495, height=50)

def enter_function(event):
    send_message()

t=threading.Thread(target=send)
t.start()

base.bind("event", enter_function)
base.mainloop()

