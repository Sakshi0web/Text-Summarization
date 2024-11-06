from tkinter.tix import Form
from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import  add_user, get_user_by_username
import database

from text_summary import summarizer



import os
import sqlite3
import hashlib

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation 
from heapq import nlargest
import fitz 




DATABASE_NAME = 'users.db'

# def initialize_database():
#     conn = sqlite3.connect(DATABASE_NAME)
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL,
#             email TEXT NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, hash_password(password)))
    
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Change this to a strong, random key for session security
app.config['UPLOAD_FOLDER'] = 'summary'
app.config['UPLOAD_FOLDER'] = 'uploads'
database.initialize_database()

@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('home.html')


# @app.route('/analyze', methods=['GET','POST'])
# def analyze():
#     if request.method == 'POST':
#         rawtext = request.form['rawtext']
#         summary, original_txt, len_prig_txt, len_summary = summarizer(rawtext)


#         return render_template('summary.html', summary=summary, original_txt=original_txt, len_prig_txt=len_prig_txt, len_summary=len_summary)

nlp = spacy.load('en_core_web_sm')
text = "This is an example sentence with some stop words."
doc = nlp(text)

filtered_tokens = [token.text for token in doc if token.text.lower() not in STOP_WORDS]

print(filtered_tokens)



# def summarizer(rawdocs):
#     stopwords = list(STOP_WORDS)
#     doc = nlp(rawdocs)
    
#     word_freq = {}
#     for word in doc:
#         if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
#             if word.text not in word_freq.keys():
#                 word_freq[word.text] = 1
#             else:
#                 word_freq[word.text] += 1

#     max_freq = max(word_freq.values())

#     for word in word_freq.keys():
#         word_freq[word] = word_freq[word] / max_freq

#     sent_tokens = [sent for sent in doc.sents]

#     sent_scores = {}
#     for sent in sent_tokens:
#         for word in sent:
#             if word.text in word_freq.keys():
#                 if sent not in sent_scores.keys():
#                     sent_scores[sent] = word_freq[word.text]
#                 else:
#                     sent_scores[sent] += word_freq[word.text]

#     select_len = int(len(sent_tokens) * 0.3)
#     summary = nlargest(select_len, sent_scores, key=sent_scores.get)
#     final_summary = [word.text for word in summary]
#     summary = ' '.join(final_summary)

#     return summary


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    doc = nlp(rawdocs)
    
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    if not word_freq:  # Check if word_freq is empty
        return "No valid words found in the input text."

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary
pass

 
# @app.route('/analyze', methods=['POST'])
# def analyze():
#     if request.method == 'POST':
#         if 'file' in request.files:
#             uploaded_file = request.files['file']
#             if uploaded_file.filename != '':
#                 pdf_text = extract_text_from_pdf(uploaded_file)
#                 summary = summarizer(pdf_text)
#                 return render_template('summary.html', summary=summary)
#         elif 'rawtext' in request.form:
#             rawtext = request.form['rawtext']
#             summary = summarizer(rawtext)
#             return render_template('summary.html', summary=summary)

#     return render_template('home.html')


def summarize_pdf_or_text(input_data):
    if not input_data:
        return "No valid content found."

    # Check if the input_data is a PDF or text
    if isinstance(input_data, str):
        # Input is text
        summary = summarizer(input_data)
    else:
        # Input is a PDF
        pdf_text = extract_text_from_pdf(input_data)
        summary = summarizer(pdf_text)

    return summary

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     if request.method == 'POST':
#         if 'file' in request.files:
#             uploaded_file = request.files['file']
#             if uploaded_file.filename != '':
#                 summary = summarize_pdf_or_text(uploaded_file)
#                 return render_template('summary.html', summary=summary)
#         elif 'rawtext' in request.form:
#             rawtext = request.form['rawtext']
#             summary = summarize_pdf_or_text(rawtext)
#             return render_template('summary.html', summary=summary)

#     return render_template('home.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        rawtext = request.form['rawtext']

        # Check if a file was uploaded and if the textarea has content
        if uploaded_file.filename != '' and rawtext:
            flash('Please choose either a file or enter raw text, not both.', 'danger')
            return redirect(url_for('home'))

        if uploaded_file.filename != '':
            pdf_text = extract_text_from_pdf(uploaded_file)
            summary = summarizer(pdf_text)
            return render_template('summary.html', summary=summary)
        elif rawtext:
            summary = summarizer(rawtext)
            return render_template('summary.html', summary=summary)

    return render_template('home.html')



def extract_text_from_pdf(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pdf_text = ""

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pdf_text += page.get_text()

    return pdf_text



  
# @app.route('/login', methods=['GET','POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     user = database.get_user(username)

#     if user is not None and user[3] == database.hash_password(password):
#         flash('Login successful', 'success')
#         return redirect(url_for('home'))
#     else:
#         flash('Login failed. Check your credentials.', 'danger')
#         return redirect(url_for('home'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()
#         c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#         user = c.fetchone()
#         conn.close()
        
#         if user:
#             session['username'] = username
#             flash('Login successful', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login failed. Please check your username and password.', 'danger')
    
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user is None:
            flash('Username not found. Please check your username.', 'danger')
        elif password != user[3]:  # Check if the entered password matches the one in the database
            flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('Login successful. Welcome back, {}!'.format(username), 'success')
            # You can redirect the user to their profile or any other page here.
            return redirect(url_for('home'))

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and Confirm Password do not match.', 'danger')
        elif get_user_by_username(username):
            flash('Username already exists. Please choose a different username.', 'danger')
        else:
            add_user(username, email, password)
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/textsumm')
def textsumm():
    return render_template('textsummarizations.html')

@app.route('/diff')
def diff():
    return render_template('diff.html')

@app.route('/chatgpt')
def chatgpt():
    return render_template('chatgpt.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('username', None)
    return redirect(url_for('home'))





if __name__ == 'main':
    app.run(debug=True)