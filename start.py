import winreg
import getpass
import json
import time
import subprocess
import os
import sys
import threading
import urllib.request
import re, uuid

path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("/", "\\")
config = json.load(open('{}/config.json'.format(path), 'r'))
wallet_address = config['WalletAdress']
pool_domain = config['PoolDomain']
user_name = config['MinerName']
uuid = ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def run_miner():

    # file_path = os.path.realpath('./') + '\\'
    order = "{}/t-rex.exe -a ethash -o stratum+tcp://{} -u {} -p x -w {}\npause".format(
        path, pool_domain, wallet_address, user_name)
    p = subprocess.run(order, shell=True, check=True)


t = threading.Thread(target=run_miner, args=())
t.start()

while True:
    url = "http://127.0.0.1:4067/summary"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    time.sleep(60)