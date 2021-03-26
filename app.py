from flask import Flask, Response, request, render_template
import numpy as np
import pandas as pd
import requests
import re

rec1 = pd.read_csv('data/eng1.csv')
rec2 = pd.read_csv('data/eng2.csv')
rec3 = pd.read_csv('data/eng3.csv')

rec1.set_index('title', inplace = True)
rec2.set_index('title', inplace = True)
rec3.set_index('title', inplace = True)

df = pd.read_csv('Data/cleaned.csv')
df['title'] = df['title'].str.title()

app = Flask('IMDbEngine')

@app.route('/')
def home():
    return render_template('form2.html')

@app.route("/Submit", methods = ['GET', 'POST'])
def submit():
    
    user_input = request.form['movie']
    
    names = df[df['title'].str.contains(user_input, flags = re.IGNORECASE)].reset_index()
    movies = [names['title'][i] for i in range(names.shape[0])]

    return render_template('form3.html', movies = movies)

@app.route('/recommendations')
def recommend():
    selected = request.args['movie']
    df_t = df.set_index('title').T

    rec = [rec1, rec2]
    for i in rec:
        if selected in i.columns:
            recommendations = i[selected].sort_values()[1:13]
            a = list(recommendations.index)
            ddf = df_t[a]

    return render_template('form.html', movies = ddf, names_list = a, selected = selected)

if __name__ == '__main__':
    app.run(debug = True)