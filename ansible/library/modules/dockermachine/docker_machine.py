#!/usr/bin/env python

"""
Example Usage:
"""

import os
import argparse
from subprocess import Popen, PIPE

class DockerMachine(object):
  def __init__(self):
    self.machine_storage_path = os.environ.get('MACHINE_STORAGE_PATH', os.environ['HOME'] + '/.docker/machine')

  def list(self, *machine_names):
    rc, meta = self._exec(["ls", "-q"] + list(machine_names))
    return rc, meta['stdout'].splitlines(), meta

  def inspect(self, format, machine_name):
    rc, meta = self._exec(["inspect", "-f", format, machine_name])
    return rc, meta['stdout'].splitlines(), meta

  def exists(self, machine_name):
    rc, machines, meta = self.list(machine_name)
    return rc != 0, machine_name in meta['stdout'], meta

  def create(self, module):
    params = module.params
    command = [
      'create', 
      '--driver', params['driver']
    ]
    if params['driver'] == 'virtualbox':
      command.extend([
        '--virtualbox-boot2docker-url', params['virtualbox_boot2docker_url'],
        '--virtualbox-memory', params['virtualbox_memory'],
        '--virtualbox-cpu-count', params['virtualbox_cpu_count'],
        '--virtualbox-disk-size', params['virtualbox_disk_size']
      ])
    elif params['driver'] == 'amazonec2':
      command.extend([
          '--amazonec2-ssh-keypath', params['aws_ssh_keypath'],
          '--amazonec2-access-key', params['aws_access_key'],
          '--amazonec2-secret-key', params['aws_secret_key'], 
          '--amazonec2-region', params['aws_region'],
          '--amazonec2-instance-type', params['aws_instance'],
          '--amazonec2-ami', params['aws_ami'],
          '--amazonec2-ssh-keypath', params['aws_ssh_key'],
          '--amazonec2-root-size', params['aws_disk_size_gb'],
          '--amazonec2-vpc-id', params['aws_vpc_id'],
          '--amazonec2-zone', params['aws_zone'],
          '--amazonec2-security-group', params['aws_security_group']
      ])
      if params['aws_use_private_addresss']:
        command.extend([
          '--amazonec2-use-private-address'
        ])
      if params['aws_tags']:
        command.extend([
          '--amazonec2-tags', params['aws_tags']
        ])
    elif params['driver'] == 'digitalocean':
      command.extend([
          '--digitalocean-access-token', params['digitalocean_access_token']
      ])
      if params['digitalocean_image']:
          command.extend([
              '--digitalocean-image', params['digitalocean_image']
          ])
      if params['digitalocean_region']:
          command.extend([
              '--digitalocean-region', params['digitalocean_region']
          ])
      if params['digitalocean_size']:
          command.extend([
              '--digitalocean-size', params['digitalocean_size']
          ])
    command.append(params['name'])
    rc, meta = self._exec(command)
    return rc, meta

  def rm(self, module):
    rc, found, meta = self.exists(module.params['name'])
    if rc == 0 and found == True:
      rc, meta = self._exec(["rm", "-f", module.params['name']])
    return rc, meta

  def regenerate_certs(self, module):
    regenerated = False
    rc, found, meta = self.exists(module.params['name'])
    if rc == 0 and found == True:
      rc, meta = self._exec(["regenerate-certs", "-f", module.params['name']])
      if rc == 0:
        regenerated = True
      else:
        module.fail_json(
          msg='Error: ' + command + ' rc=' + str(rc) + ' ' + stderr,
          cmd=command, out=stdout, err=stderr, rc=rc
        )
    return rc, meta, regenerated

  #############################################################################

  def _exec(self, args):
    args = map(str, args)
    try:
      command = ' '.join(["docker-machine", "-s", self.machine_storage_path] + args)
      popen = Popen(["docker-machine", "-s", self.machine_storage_path] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
      stdout, stderr = popen.communicate()
      rc = popen.returncode
    except:
      rc = -1
      command = ' '.join(map(str, args))
      stdout = ''
      stderr = ''
    msg =  "cmd='" + command + "'"
    if rc != 0:
      msg = "ERROR: rc=" + str(rc) + ", " + msg
    meta = {
      "rc" : rc,
      "cmd" : command,
      "stdout" : stdout,
      "stderr" : stderr,
      "msg" : msg
    }
    return rc, meta



try:
    import json
except ImportError:
    import simplejson as json


def main():
  dm = DockerMachine()
  rc, config, meta = dm.inspect('{"name":"{{.Driver.MachineName}}","ip":"{{.Driver.IPAddress}}","tls_verify":"{{.HostOptions.EngineOptions.TlsVerify}}","key_path":"{{.HostOptions.AuthOptions.ClientKeyPath}}","cert_path":"{{.HostOptions.AuthOptions.ClientCertPath}}","cacert_path":"{{.HostOptions.AuthOptions.CaCertPath}}","docker_host":"tcp://{{.Driver.IPAddress}}:2376"}', "rancher")
  if len(config) == 0:
    print "oops"

  print config[0]
  object = json.loads(config[0])
  print object

if __name__ == '__main__':
    main()
