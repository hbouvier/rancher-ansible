#!/usr/bin/env python

"""
Example Usage:
"""

import argparse
from dockermachine import DockerMachine
import requests

try:
    import json
except ImportError:
    import simplejson as json

def get_token(api_url, environment):
  headers = {
    "Accept":       "application/json",
    "Content-Type": "application/json"
  }

  url  = "{}/v1/projects" . format(api_url)
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    payload = response.json()
    project = filter(lambda data: data['name'] == environment, payload['data'])[0]
    project_id = project['id']

    url  = "{}/v1/projects/{}/registrationTokens" . format(api_url, project_id)
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
      payload = response.json()
      token_id = payload['id']

      url = "{}/v1/projects/{}/registrationToken/{}" . format(api_url, project_id, token_id)
      token = None
      while token == None:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
          payload = response.json()
          token = payload['token']
          if token == None:
            continue
          docker_command = payload['command']
          meta={
            "environment" : environment,
            "url": url,
            "api_url": api_url,
            "project_id": project_id,
            "token_id": token_id,
            "token": token,
            "docker_command" : docker_command,
            "payload": payload
          }
          return 0, token, meta 
        else:
          break
  return -1, "API ERROR: environment=" +  environment, {}


def main():
  fields = {
    "rancher_environment": {"required": True, "type": "str"},
    "api_url": {"required": True, "type": "str"},
    "action": {"required": True, "type": "str"}
  }
  module = AnsibleModule(argument_spec=fields)


  api_url = module.params['api_url']
  environment = module.params['rancher_environment']
  if module.params['action'] == 'token':
    rc, token, meta = get_token(api_url, environment)
    if rc == 0:
      module.exit_json(changed=False, token=token, meta=meta)
    else:
      module.fail_json(msg=token)

###############################################################################

from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
   main()


# PID=`curl -s -X GET -H "Accept: application/json" http://192.168.99.100:8080/v1/projects | jq -r '.data[0].id'`
# TID=`curl -s -X POST -H "Accept: application/json" -H "Content-Type: application/json" http://192.168.99.100:8080/v1/projects/$PID/registrationTokens | jq -r '.id'`
# touch token.json
# while [ `jq -r .command token.json | wc -c` -lt 10 ]; do
#     curl -s -X GET -H "Accept: application/json" http://192.168.99.100:8080/v1/projects/$PID/registrationToken/$TID > token.json
#     sleep 1
# done
# CMD=`jq -r .command token.json`
# eval $CMD
