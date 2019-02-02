#!/usr/bin/python3
import sys
import json
import configparser

import requests
import requests.auth

base_url = 'https://oauth.reddit.com'
delete_url = '{0}/api/del'.format(base_url)

delete_map = {
  '7': 'BOTH',
  '8': 'COMMENTS',
  '9': 'POSTS'
}

def main():
  print('[Reddit Purger]')
  print('WARNING There\'s no going back\n')
      
  del_code = get_delete_code() # user input to specify what to delete
  account = get_credentials() # account credentials set in account.ini
  token = get_token(account) # access token returned by the reddit API
  delete(account['username'], token, delete_map[del_code]) # delete specified content

def get_delete_code():
  print('What do you wish to delete?')
  print('0 - Exit')
  print('7 - Comments and Posts')
  print('8 - Comments Only')
  print('9 - Posts Only')

  del_code = input('\nSelect: ')

  if del_code == '0':
    print('\nExiting...')
    sys.exit()

  if del_code not in delete_map:
    print('\nInvalid entry. Exiting...')
    sys.exit()

  # Double check that user intended chosen option before continuing
  verify_intentions(del_code) 

  return del_code

def verify_intentions(del_code):
  warning_map = {
    '7': 'COMMENTS AND POSTS',
    '8': 'COMMENTS',
    '9': 'POSTS'
  }

  intention = input('\nARE YOU SURE YOU WANT TO DELETE ALL {0} [Y/n] '.format(warning_map[del_code]))

  if intention.lower() != 'y':
    print('Exiting...')
    sys.exit()

def get_credentials():
  config = configparser.ConfigParser()
  config.read('account.ini')
  account = config['ACCOUNT']

  for key in account:
    if not account[key]: # config value in account.ini was left empty
      print('Please verify account.ini values')
      sys.exit()
      
  return account

def get_token(account):
  username = account['username']
  password = account['password']
  app_id = account['app_id']
  secret = account['secret']

  # Request sent to reddit API to retrieve access token for account API usage
  client_auth = requests.auth.HTTPBasicAuth(app_id, secret)
  post_data = {"grant_type": "password", "username": username, "password": password}
  headers = {"User-Agent": "ChangeMeClient/0.1 by {0}".format(username)}
  response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

  response = response.json()

  if 'error' in response:
    if response['error'] == 'invalid_grant': # Username and password do not work
      print('Verify username and password in account.ini')
      sys.exit()
    else: # app_id or secret are not recognized
      print('Verify app_id and secret in account.ini')
      sys.exit()

  # access token used to make API calls for this specific user
  token = response['access_token']

  return token


def delete(username, token, del_method):
  authorization = 'bearer {0}'.format(token) # Access token
  user_agent = 'ChangeMeClient/0.1 by {0}'.format(username)
  headers = {"Authorization": authorization, "User-Agent": user_agent}

  # Deleting comments and posts
  if del_method == 'BOTH':
    print('Deleting all comments and posts for {0}'.format(username))
    to_delete = ['comments', 'submitted']

    for content in to_delete:
      delete_content(content, username, headers)

  # Deleting only comments
  if del_method == 'COMMENTS':
    print('Deleting all comments for {0}'.format(username))
    delete_content('comments', username, headers)

  # Deleting only posts
  if del_method == 'POSTS':
      print('Deleting all posts for {0}'.format(username))
      delete_content('submitted', username, headers)

def delete_content(content_type, username, headers):
  print_type = content_type # either 'comments' or 'submitted'

  # This is just for printing purposes
  if content_type == 'submitted':
    print_type = 'posts'

  # URL to user's comments or posts (eg. https://www.reddit.com/user/LeviMurray/comments)
  content_url = '{0}/user/{1}/{2}'.format(base_url, username, content_type)

  # Loops until content_url returns 0 content objects
  while True:
    # reddit API limits requests to 100, not sure if there's a way around it
    response = requests.get(content_url, headers=headers, params={'limit': '100'})
    # TODO Find a way to request more than 100 content objects from reddit API
    response = response.json()
    content = response['data']['children'] # Array of content objects

    # Number of content objects out of 100 returned
    content_length = len(content)

    # if content_length is 0, then there are no comments/posts,
    # and we can exit our deletion loop
    if content_length == 0:
      print('Your {0} are purged!'.format(print_type))
      break

    print('{0}/100 {1} found'.format(content_length, print_type))

    # i is for printing purposes only--showing what content object
    # out of content_length we are currently deleting
    i = 1

    # API request loop to hit the delete content endpoint for every comment or post
    for item in content:
      # Content identifier the delete endpoint needs to delete the comment/post
      content_id = item['data']['name']
      params = {'id': content_id}
      requests.post(delete_url, headers=headers, params=params) # API request
      
      if content_type == 'comments':
        print('Comment \'{0}\' deleted ({1}/{2})'.format(content_id, i, content_length))
      else:
        print('Post \'{0}\' deleted ({1}/{2})'.format(content_id, i, content_length))
        
      i = i + 1

main()