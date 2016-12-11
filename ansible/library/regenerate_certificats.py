#!/usr/bin/env python

"""
Example Usage:
$ MACHINE_STORAGE_PATH=~/.docker/machine/machines ansible -i library/docker-machine-provision.py ???
$ python modules/dockermachine/inventory.py | jq
"""

import argparse
from dockermachine import DockerMachine

def main():
  fields = {
    "name": {"required": True, "type": "str"},
    "driver": {
      "default":"virtualbox",
      "choices":['virtualbox','amazonec2'],
      "required": False,
      "type": "str"
    }
  }

  dm = DockerMachine()
  module = AnsibleModule(argument_spec=fields)

  rc, meta, regenerated = dm.regenerate_certs(module)

  if rc == 0:
    module.exit_json(changed=regenerated, meta=meta)
  else:
    module.fail_json(msg="Error deleting repo", meta=meta)

###############################################################################

from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
   main()
