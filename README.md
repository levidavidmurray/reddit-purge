# Reddit History Purger
Python script making use of reddit's API to delete all comments or posts from your reddit account

## Prerequisites
Ensure you have the python requests module
```shell
pip3 install requests
```

Ensure you have a valid reddit app for API usage tied to your account.

1. Go to https://www.reddit.com/prefs/apps/ and click "Create an app"
2. Name can be whatever you want (e.g. *purge-history*)
3. Select the *script* radio button
4. *description* and *about url* can be left blank
5. For *redirect uri* enter: *http://www.example.com/unused/redirect/uri*

Make note of app ID under **personal use script** (e.g. *fIdR-MDfo6Zcpx*)

Make note of **secret** (e.g. *fJxo0ALVNc_bT1P2A3ro3eXVBdI*)

## Usage
```shell 
# Command Line

git clone https://github.com/levidavidmurray/reddit-purge.git
cd reddit-purge
```
Open account.ini and enter your reddit username and password, as well as the app ID and secret that you made note
of earlier. **Do not use quotes for account values**

```ini
# account.ini

[ACCOUNT]
username = LeviMurray
password = hunter2
app_id = fIdR-MDfo6Zcpx
secret = fJxo0ALVNc_bT1P2A3ro3eXVBdI
```

Verify your values are correct, and save the file.

```shell
# Command Line

./reddit_purge.py
```

You'll be quickly prompted with inputting whether you want to delete all of your comments and posts, only your comments,
or only your posts. Select your option, press enter, and let the script do the rest!
