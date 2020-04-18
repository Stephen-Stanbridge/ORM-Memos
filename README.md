# ORM-Memos
Console application for communication between users through memos.


# Prerequisites
```
python3
SQLAlchemy
psycopg2-binary
postgresql
argparse
prettytable
prompt-toolkit
pytest
```


# Installation

Optional: Create virtual environment.
1. Install prerequisites
2. In SQL directory create setup_db.py file, create engine for SQLAlchemy and bind Session to it.
3. In Models directory add below line to models.py and run it. DB will be created.
> Base.metadata.create_all(engine)
4. Use python3 app.py USERNAME PASSWORD to create or login to account.


# Tests
In main directory of application run pytest or pytest-3 depending on version of Python installed on your machine.



# How does it work and look like?

First of all user have to register account. Username for each user has to be unique, can only contain 
letters and '_' character.
First letter of username will always be capitalized and saved to db.
After registration user is logged in to dashboard where commands can be listed through 'help' command.

<img src="https://imgur.com/zaNDNiF.png" />

There are basically four types of commands:<br>
memo - Allows for creating memos with title and content, getting list of all created memos, getting single memo by id
and sending them.

<img src="https://imgur.com/JQzkxHz.png" />
<p><img src="https://imgur.com/53IWeQB.png" />  <img src="https://imgur.com/0vTJFDi.png" /></p>
<p><img src="https://imgur.com/DUgMrbf.png" />  <img src="https://imgur.com/pi90zz9.png" /></p>


inbox - Allows for getting and deleting memos in users' inbox.
<img src="https://imgur.com/0P9vQMe.png" />
<p><img src="https://imgur.com/vX8fQCB.png" />  <img src="https://imgur.com/ygU7yHS.png" /></p>


users - Allows for getting list of all users or searching them by id/username.
<img src="https://imgur.com/b4jbEqI.png" />
<p><img src="https://imgur.com/1SOZksX.png" />  <img src="https://imgur.com/AaENVSN.png" />  <img src="https://imgur.com/KKkLuSm.png" /></p>


user - Allows for account management - deleting account along with created memos and inbox and changing password.
<img src="https://imgur.com/yGGVN37.png" />


# Author
<a href="https://www.linkedin.com/in/stephen-stanbridge-26bbb416a/"> Stephen Stanbridge</a>
