#!/usr/bin/env python

"""
Example Usage:
"""

import argparse
from dockermachine import DockerMachine

try:
    import json
except ImportError:
    import simplejson as json

def main():
  fields = {
    "name": {"required": True, "type": "str"}
  }

  dm = DockerMachine()
  module = AnsibleModule(argument_spec=fields)
  rc, config, meta = dm.inspect('{"name":"{{.Driver.MachineName}}","ip":"{{.Driver.IPAddress}}","tls":"{{.HostOptions.EngineOptions.TlsVerify}}","key_path":"{{.HostOptions.AuthOptions.ClientKeyPath}}","cert_path":"{{.HostOptions.AuthOptions.ClientCertPath}}","cacert_path":"{{.HostOptions.AuthOptions.CaCertPath}}","docker_host":"tcp://{{.Driver.IPAddress}}:2376"}', module.params['name'])
  if rc == 0 and len(config) == 1:
    object = json.loads(config[0])

    module.exit_json(changed=False, config=object, meta=meta)
  else:
    module.fail_json(msg="Cannot find VM " + module.params['name'], meta=meta)

###############################################################################

from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
   main()
