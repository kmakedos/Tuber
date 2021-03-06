from flask import Flask, render_template, request
import os
from multiprocessing import Pool
from pytube import YouTube


app = Flask(__name__)
_pool = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/videos', methods=['GET','POST'])
def videos():
    url = request.form.get('url')
    streams = YouTube(url).streams.filter(only_audio=True, subtype='mp4').order_by('abr').first().download('/tmp/Downloaded')
    return render_template('videos.html', data = streams)

@app.route('/downloaded')
def downloaded():
    songlist = []
    for folder,song in os.walk('/tmp/Downloaded/'):
        songlist.append(song)
    return render_template('downloaded.html', data = songlist)

if __name__ == '__main__':
    if not os.path.exists('/tmp/Downloaded'):
        os.mkdir('/tmp/Downloaded')
    app.run(debug=True)
