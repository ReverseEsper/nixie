from flask import Flask,request,json
from flask_cors import CORS

from pprint import pprint as pp
import git
import logging

from subprocess import call

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/githubIssue',methods=['POST'])
def githubIssue():
    data = request.json
    ##pp (data)
    print ("Wydaje mi się, ze jest coś do pociągnięcia")
    g = git.cmd.Git("/home/pi/git/nixie")
    g.pull()
    # Check if webhook was modified
    if "commits" in data:
        for commit in data["commits"]:
            if commit['modified']:
                print(f"Modified File: {commit['modified']}")
                if 'nixie.py' in commit['modified']:
                    logging.info('Nixie refreshed, has to restart service')
                    call(["systemctl", "restart", "nixie_clock.service"])
                    logging.info('Service Restarted. Actaully that should not show...')
                                
        
    return 'Webhooks with Python'


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0",port=8081)
