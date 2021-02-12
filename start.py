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
import requests

try:
    path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("/", "\\")
    config = json.load(open('{}/config.json'.format(path), 'r'))
    wallet_address = config['WalletAdress']
    pool_domain = config['PoolDomain']
    worker_name = config['WorkerName']
    farm_hash = config['Farm']
    email = config['E-Mail']
    uuid = ':'.join(re.findall('..', '%012x' % uuid.getnode()))


    def run_miner():

        # file_path = os.path.realpath('./') + '\\'
        order = "{}/t-rex.exe -a ethash -o stratum+tcp://{} -u {} -p x -w {}\npause".format(
            path, pool_domain, wallet_address, worker_name)
        p = subprocess.run(order, shell=True, check=True)


    t = threading.Thread(target=run_miner, args=())
    t.start()

    while True:
        try:
            url = "http://127.0.0.1:4067/summary"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            param = {
                'email': email,
                'uuid': uuid,
                'worker_name': worker_name,
                'data': data
            }

            param = json.dumps(param)
            res = requests.request('POST', url='http://jikding.net/api/lazy-miner/log', data=param)
            data = json.loads((res.text).encode('utf-8'))
            print(data)
            if data['status'] == 'tryReboot':
                param = {
                    'uuid': uuid,
                    'farm': farm_hash
                }

                param = json.dumps(param)
                res = requests.request('POST', url='http://jikding.net/api/lazy-miner/worker/turnoff-ok', data=param)
                data = json.loads((res.text).encode('utf-8'))
                print(data)
                os.system("shutdown -t 0 -r -f")
            time.sleep(60)
        except:
            time.sleep(60)

except Exception as e:
    print(e)
    print('오류로 인한 종료중...')
    time.sleep(10)