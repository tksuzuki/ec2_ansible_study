#!/usr/bin/env python
# coding: utf-8

import sys
import json
import subprocess
import os.path

p = subprocess.Popen(['aws', 'ec2', 'describe-instances'], shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
j = json.loads('\n'.join(p.stdout.readlines()))
#print(j)
fp = open("/home/ansible/hosts/inventory", "w")
for r in j.get('Reservations'):
    for i in r.get('Instances'):
        print(i)
        for tag in i.get('Tags'):
            print(tag)
            if tag["Key"] == "Name":
                #fp.write("%s %s\n" % (i.get('PrivateIpAddress'), tag["Value"]))
                #fp.write("%s\n%s\n" % (tag["Value"], i.get('PrivateIpAddress')))
                fp.write("[%s]\n%s\n\n" % (tag["Value"], i.get('PrivateIpAddress')))
                break
            
fp.close()
