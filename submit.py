import os
from bottle import run, template, get, post, request, static_file, route,  jinja2_view
import requests
from github import Github
import ConfigParser

# we may delete some imports; later time work 

# Secret, don't share the file config. 
Config = ConfigParser.ConfigParser()
Config.read("config")
GITHUB_TOKEN=Config.get ("config", "GITHUB_TOKEN")
GITHUB_USERNAME=Config.get ("config", "GITHUB_USERNAME")
USERNAME=Config.get ("config", "USERNAME")
PASSWORD=Config.get ("config", "PASSWORD")
GITHUB_REPO=Config.get ("config", "GITHUB_REPO")

# references/credits
#https://realpython.com/blog/python/developing-with-bottle-part-2-plot-ly-api/ 
#https://github.com/PyGithub/PyGithub/issues/132
#https://wiki.python.org/moin/ConfigParserExamples


newline="\n"
two_newline="\n \n"
tab="\t"

@get('/user_request')
def form():
    return template('user_req.html',)

@post('/user_request')
def submit():
    username = request.forms.get('username')
    project = request.forms.get('project')
    pi = request.forms.get('pi')
    ssh_public_key = request.forms.get('ssh_public_key')

#for auth with userid/password
#    g = Github("myusername", "mypassword")

#token auth; create token on github.com
    g = Github(GITHUB_TOKEN)
    repo = g.get_user(GITHUB_USERNAME).get_repo(GITHUB_REPO)  

#from API
# Repository.py:    def create_issue(self, title, body=github.GithubObject.NotSet, assignee=github.GithubObject.NotSet, milestone=github.GithubObject.NotSet, labels=github.GithubObject.NotSet):

    title=username
    body="PI is: "+pi+ two_newline + "Project is: " +project + two_newline + "SSH public key is: \n" +ssh_public_key

    response = repo.create_issue(title,body)

    if response:
        return template(
            '''<h1>Congrats!</h1>
            <div>
              You will get an email once account is approved/created <a href="{{response}}"</a>
            </div>
            ''',
            response=response
        )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)

