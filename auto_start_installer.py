import winreg
import getpass
import json
import time
import subprocess
import os

print("If You change the path this program, Then You MUST REINSTALL this!")

config = json.load(open('./config.json', 'r'))


# 시스템 자동 로그인 셋팅
user_name = getpass.getuser()

reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
reg_handle = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)


key_r = winreg.OpenKey(reg_handle, reg_path, 0, winreg.KEY_READ)
key_w = winreg.OpenKey(reg_handle, reg_path, 0, winreg.KEY_WRITE)
reg_val_list = []
find_reg1 = False
find_reg2 = False
find_reg3 = False

i = 0
while True:
    try:
        val = winreg.EnumValue(key_r, i)
        reg_val_list.append(val)
        i += 1
    except:
        break


for val in reg_val_list:
    if 'AutoAdminLogon'.upper() == val[0].upper():
        find_reg1 = True
        if val[1] != '1':
            try:
                winreg.SetValueEx(key_w, val[0], 0, winreg.REG_SZ, '1')
                print('reg set AutoAdminLogon!')
            except Exception as e:
                print('reg AutoAdminLogon err!', e)
    if 'DefaultUserName'.upper() == val[0].upper():
        find_reg2 = True
        if val[1] != user_name:
            try:
                winreg.SetValueEx(key_w, val[0], 0, winreg.REG_SZ, user_name)
                print('reg set DefaultUserName!')
            except Exception as e:
                print('reg DefaultUserName err!', e)
    if 'DefaultPassword'.upper() == val[0].upper():
        find_reg3 = True
        if val[1] != config['WindowsPassword']:
            try:
                winreg.SetValueEx(key_w, val[0], 0, winreg.REG_SZ, config['WindowsPassword'])
                print('reg set DefaultPassword!')
            except Exception as e:
                print('reg DefaultPassword err!', e)

if not find_reg1:
    winreg.SetValueEx(key_w, 'AutoAdminLogon', 0, '1')
    print('reg create AutoAdminLogon!')
if not find_reg2:
    winreg.SetValueEx(key_w, 'DefaultUserName', 0, user_name)
    print('reg create DefaultUserName!')
if not find_reg3:
    winreg.SetValueEx(key_w, 'DefaultPassword', 0, winreg.REG_SZ, config['WindowsPassword'])
    print('reg create DefaultPassword!')

winreg.CloseKey(key_r)
winreg.CloseKey(key_w)


# T-Rex 작업스케줄러 등록
try:
    res = subprocess.check_output('schtasks.exe /Query', shell=True)
    s = res.decode('EUC-KR')

    if 'LazyMiner' in s:
        res = subprocess.check_output('schtasks.exe /Delete /TN LazyMiner /F', shell=True)
        # s = res.decode('EUC-KR')
        # print(s)
        print('Deleted in schtasks!')

    file_path = os.path.realpath('./') + '\\start.exe'
    file_path = '"{}"'.format(file_path)
    # arg = '/Create /sc ONSTART /tn LazyMiner /tr {} /RL HIGHEST'.format(file_path)
    arg = '/Create /sc ONLOGON /tn LazyMiner /tr {} /RL HIGHEST'.format(file_path)
    res = subprocess.check_output('schtasks.exe {}'.format(arg), shell=True)
    print("Finished...!")
except Exception as e:
    print("Err", e)


time.sleep(3)
