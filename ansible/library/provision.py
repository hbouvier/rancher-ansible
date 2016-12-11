#!/usr/bin/env python

"""
Example Usage:
"""

import argparse
from dockermachine import DockerMachine

def _machine_present(module, dm):
  is_error = False
  has_changed = False
  meta    = {}

  rc, present, meta = dm.exists(module.params['name'])
  if rc != 0:
    is_error = True
    module.fail_json(
      msg='Error: ' + meta['cmd'] + ' rc=' + str(rc) + ' ' + meta['stderr'],
      cmd=meta['cmd'], out=meta['stdout'], err=meta['stderr'], rc=rc
    )
  elif not present:
    rc, meta = dm.create(module)
    if rc != 0:
      is_error = True
      module.fail_json(
        msg='Error: ' + meta['cmd'] + ' rc=' + str(rc) + ' ' + meta['stderr'],
        cmd=meta['cmd'], out=meta['stdout'], err=meta['stderr'], rc=rc
      )
    has_changed = True
  return is_error, has_changed, meta

def _machine_absent(module, dm):
  is_error = False
  has_changed = False
  meta    = {}

  rc, present, meta = dm.exists(module.params['name'])
  if rc != 0:
    is_error = True
    module.fail_json(
      msg='Error: ' + meta['cmd'] + ' rc=' + str(rc) + ' ' + meta['stderr'],
      cmd=meta['cmd'], out=meta['stdout'], err=meta['stderr'], rc=rc
    )
  elif present:
    rc, meta = dm.rm(module)
    if rc != 0:
      is_error = True
      module.fail_json(
        msg='Error: ' + meta['cmd'] + ' rc=' + str(rc) + ' ' + meta['stderr'],
        cmd=meta['cmd'], out=meta['stdout'], err=meta['stderr'], rc=rc
      )
    has_changed = True
  return is_error, has_changed, meta

def main():
  fields = {
    "name": {"required": True, "type": "str"},
    "driver": {
      "default":"virtualbox",
      "choices":['virtualbox','amazonec2'],
      "required": False,
      "type": "str"
    },
    "state": {
      "default": "present",
      "choices": ['present', 'absent'],
      "type": 'str'
    },
    "virtualbox_boot2docker_url": {"required": False, "type": "str"},
    "virtualbox_memory": {"required": False, "type": "int"},
    "virtualbox_cpu_count": {"required": False, "type": "int"},
    "virtualbox_disk_size": {"required": False, "type": "int"},
    
    # "aws_ssh_keypath": {"required": True, "type": "str"},
    # "aws_access_key" : {"required": True, "type": "str"},
    # "aws_secret_key" : {"required": True, "type": "str"},
    # "aws_region" : {
    #   "default": "us-east-1",
    #   "choices": ['us-east-1', 'us-west-1'],
    #   "type": 'str'
    # },
    # "aws_instance" : {"required": True, "type": "str"},
    # "aws_ami" : {"required": True, "type": "str"},
    # "aws_disk_size_gb" : {"required": True, "type": "int"},
    # "aws_vpc_id" : {"required": True, "type": "str"},
    # "aws_zone" : {
    #   "default": "a",
    #   "choices": ['a', 'b', 'd'],
    #   "type": 'str'
    # },
    # "aws_security_group" : {"required": True, "type": "str"},
    # "aws_use_private_addresss" : {"required": False, "type": "bool"},
    # "aws_tags" : {"required": True, "type": "str"}
  }

  choice_map = {
    "present": _machine_present,
    "absent": _machine_absent,
  }

  dm = DockerMachine()
  module = AnsibleModule(argument_spec=fields)
  is_error, has_changed, result = choice_map.get(module.params['state'])(module, dm)

  if not is_error:
    module.exit_json(changed=has_changed, meta=result)
  else:
    module.fail_json(msg="Error deleting repo", meta=result)

###############################################################################

from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
   main()
