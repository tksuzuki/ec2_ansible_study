#!/usr/bin/env python
# coding: utf-8

import sys
import json
import subprocess

p = subprocess.Popen(['aws', 'ec2', 'describe-instances'], shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
j = json.loads('\n'.join(p.stdout.readlines()))
fp = open("/etc/hosts", "a")
for r in j.get('Reservations'):
    for i in r.get('Instances'):
        for tag in i.get('Tags'):
            if tag["Key"] == "Name":
                fp.write("%s %s\n" % (i.get('PrivateIpAddress'), tag["Value"]))
                break

fp.close()
