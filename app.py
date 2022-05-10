from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.j1l8r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.mureca

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/music", methods=["POST"])
def music_post():
    title_receive = request.form['title_give']
    url_receive = request.form['url_give']
    artist_receive = request.form['artist_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    image = soup.select_one('meta[property="og:image"]')['content']


    doc = {
        'title':title_receive,
        'image':image,
        'artist':artist_receive
    }
    db.musics.insert_one(doc)

    return jsonify({'msg':'등록 완료!'})

@app.route("/music", methods=["GET"])
def music_get():
    music_list = list(db.musics.find({}, {'_id': False}))
    return jsonify({'musics':music_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)