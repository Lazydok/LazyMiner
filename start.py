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
            time.sleep(60)
            url = "http://127.0.0.1:4067/summary"
            response = urllib.request.urlopen(url)
            status = json.loads(response.read())
            param = {
                'email': email,
                'uuid': uuid,
                'worker_nm': worker_name,
                'data': status
            }

            param = json.dumps(param)
            res = requests.request('POST', url='http://stick.coffee:8288/api/lazy-miner/log', data=param)
            data = json.loads((res.text).encode('utf-8'))
            turnoff_flag = False
            if data['message']['status'] == 'tryReboot':
                turnoff_flag = True
            elif data['setting']['auto_turnoff']:
                lm_rate = data['setting']['turnoff_limit_rate']
                rate = status['hashrate'] / status['hashrate_day'] * 100
                if lm_rate > rate:
                    turnoff_flag = True

            if turnoff_flag:
                param = {
                    'uuid': uuid,
                    'farm': farm_hash
                }

                param = json.dumps(param)
                res = requests.request('POST', url='http://stick.coffee:8288/api/lazy-miner/worker/turnoff-ok', data=param)
                data = json.loads((res.text).encode('utf-8'))
                print(data)
                os.system("shutdown -t 0 -r -f")
        except Exception as e:
            print(e)
            pass

except Exception as e:
    print(e)
    print('오류로 인한 종료중...')
    time.sleep(10)