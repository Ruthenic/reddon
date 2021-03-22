import praw
import socket
import os
import colored
from colored import stylize
import requests
def clearscreen(): 
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear') 
clearscreen()
with open('creds.txt') as f:
    creds=f.readlines()
    print(creds)
reddit = praw.Reddit(
    client_id=creds[0].strip(),
    client_secret=creds[1].strip(),
    user_agent=creds[2].strip()
)
subbedsubs = []
if os.path.exists('savedsubs.txt'):
    with open('savedsubs.txt') as f:
        for i in f:
            subbedsubs.append(i.strip())
hostname = socket.gethostname()
username = os.getlogin()
sub = 'all'
oldsub = []
subm = ''
def clearscreen(): 
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear') 
def parseinput(imp):
    imp = imp.replace('r/', '')
    return imp.split(' ')
def savesubs(subs):
    with open('savedsubs.txt', 'w+') as f:
        for i in subs:
            f.write(i+'\n')
def commandrun(inp,sub,oldsub,subm,subbedsubs):
    #ew
    #global sub
    #global oldsub
    #global subm
    if inp[0] == 'lsp':
        postid=inp[1]
        cusamo = False
        for i in inp:
            if i.startswith('--amount=') or i.startswith('-a='):
                lsamount = int(i.replace('--amount=', '').replace('-a=', ''))
                cusamo = True
        if cusamo == False: 
            lsamount = 10
        submission=reddit.submission(id=postid) #dom
        submission.comments.replace_more(limit=None)
        submission.comment_limit = lsamount
        for topcom in submission.comments:
            try:
                print(topcom.body + ' - ' + topcom.author.name)
            except:
                break
    elif inp[0] == 'ls':
        cussub = False
        cusamo = False
        for i in inp:
            if i.startswith('--subreddit=') or i.startswith('-s='):
                temsub = reddit.subreddit(i.replace('--subreddit=', '').replace('-s=', ''))
                cussub = True
            if i.startswith('--amount=') or i.startswith('-a='):
                lsamount = int(i.replace('--amount=', '').replace('-a=', ''))
                cusamo = True
        if cussub == False: 
            temsub = reddit.subreddit(sub)
        if cusamo == False: 
            lsamount = 10
        for submission in temsub.hot(limit=lsamount):
            print(submission.title, end='')
            print(stylize(' [' + submission.url + ']', colored.fg('cyan')), end='')
            print(stylize(' [' + submission.id + ']', colored.fg('red_3a')), end='')
            print(stylize(' [{}]'.format(submission.upvote_ratio), colored.fg('dark_red_1')))
    elif inp[0] == 'clear':
        clearscreen()
    elif inp[0] == 'cd':
        if inp[1] == '..':
            sub = oldsub.pop()
        else:
            oldsub.append(sub)
            sub = inp[1]
        #print(str(sub))
    elif inp[0] == 'exit':
        savesubs(subbedsubs)
        print('Thanks for using Reddon!')
        exit()
    elif inp[0] == 'history':
        for i in oldsub: print(i)
    elif inp[0] == 'img':
        if os.name == 'posix':
            postid=inp[1]
            submission=reddit.submission(id=postid) #dom
            with open('tmp', 'wb') as f:
                img = requests.get(submission.url).content
                f.write(img)
            os.system('xdg-open tmp')
            os.remove('tmp')
        else:
            print('Command only works on Linux!')
    elif inp[0].startswith('#'):
        pass
    elif inp[0] == 'sub' or inp[0] == 'follow':
        if inp[1] != '.':
            subbedsubs.append(inp[1])
        else:
            subbedsubs.append(sub)
    elif inp[0] == 'lsf':
        cusamo = False
        for i in inp:
            if i.startswith('--amount=') or i.startswith('-a='):
                lsamount = int(i.replace('--amount=', '').replace('-a=', ''))
                cusamo = True
        if cusamo == False:
            lsamount = 5
        for s in subbedsubs:
            print(s)
            temsub = reddit.subreddit(s)
            for submission in temsub.hot(limit=lsamount):
                print(submission.title, end='')
                print(stylize(' [' + submission.url + ']', colored.fg('cyan')), end='')
                print(stylize(' [' + submission.id + ']', colored.fg('red_3a')), end='')
                print(stylize(' [{}]'.format(submission.upvote_ratio), colored.fg('dark_red_1')))
    elif inp[0] == 'interpret':
        #debug command
        while True:
            grhgghqahugsoauigigifjioifajoijfaojosjiojigrijoojiafofoajfojifaiojf = input('>>> ') #i swear to god if anyone names a variable this
            try:
                exec(grhgghqahugsoauigigifjioifajoijfaojosjiojigrijoojiafofoajfojifaiojf)
            except Exception as e:
                print(str(e))
    else:
        print('Not a command!')
    return sub,oldsub,subm,subbedsubs
print('Welcome to Reddon!')
while True:
    print(stylize(username + '@' + hostname + ' ' + 'r/' + str(sub) + '/' + str(subm) + '> ', colored.fg('light_green')), end='')
    try:
        command = input()
    except KeyboardInterrupt:
        savesubs(subbedsubs)
        exit()
    sub,oldsub,subm,subbedsubs = commandrun(parseinput(command),sub,oldsub,subm,subbedsubs)
