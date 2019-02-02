#!/usr/bin/python3

import sys
import json
import configparser

import requests
import requests.auth


base_url = 'https://oauth.reddit.com'
del_url = '{0}/api/del'.format(base_url)

def main():
  account = get_credentials()
  token = get_token(account)
  delete_comments(account['username'], token)

def get_credentials():
  config = configparser.ConfigParser()
  config.read('account.ini')
  account = config['ACCOUNT']

  for key in account:
    if not account[key]:
      print('Please verify account.ini values')
      sys.exit()
      
  
  return account

def delete_comments(username, token):
  authorization = 'bearer {0}'.format(token)
  user_agent = 'ChangeMeClient/0.1 by {0}'.format(username)

  comments_url = '{0}/user/{1}/comments'.format(base_url, username)
  headers = {"Authorization": authorization, "User-Agent": user_agent}

  comments_exist = True

  while True:
    response = requests.get(comments_url, headers=headers, params={'limit': '100'})
    response = response.json()
    comments = response['data']['children']

    c_len = len(comments)

    if c_len == 0:
      print('Your comments are purged!')
      break

    print('{0}/100 comments found'.format(c_len))

    i = 1

    for comment in comments:
      comment_id = comment['data']['name']
      params = {'id': comment_id}
      del_res = requests.post(del_url, headers=headers, params=params)
      print('Comment \'{0}\' deleted ({1}/{2})'.format(comment_id, i, c_len))
      i = i + 1


def get_token(account):
  username = account['username']
  password = account['password']
  app_id = account['app_id']
  secret = account['secret']

  client_auth = requests.auth.HTTPBasicAuth(app_id, secret)
  post_data = {"grant_type": "password", "username": username, "password": password}
  headers = {"User-Agent": "ChangeMeClient/0.1 by {0}".format(username)}
  response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

  response = response.json()

  if response['error']:
    if response['error'] == 'invalid_grant':
      print('Verify username and password in account.ini')
      sys.exit()
    else:
      print('Verify app_id and secret in account.ini')
      sys.exit()

  token = response.json()['access_token']

  return token


main()