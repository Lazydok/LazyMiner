import socket
import json
import smtplib
import time
import statistics
import os
import logging
import uptime
import psutil

###################################################CONFIG##############################################################



# miner
miner_ip = '222.97.25.130'
miner_port = 3333


# limits
hashrate_limit = 100000 	#h/s
fan_speed_limit = 50		#percent
gpu_temp_limit = 65			#Celsius
uptime_limit = 180			#seconds
cards_limit = 6

# logging
log_name = 'ethmon.log'


#######################################################################################################################

def get_data(ip, port, password, logger):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    try:
        sock.connect(server_address)
    except Exception as e:
        logger.info('Miner socket ' + str(ip) + ':' + str(port) + ' is closed')
        return []
    request = '{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\",\"psw\":\"' + password + '\"}'
    request = request.encode()
    try:
        sock.sendall(request)
    except Exception as e:
        logger('Sending data was aborted')
        return []
    try:
        data = sock.recv(512)
    except Exception as e:
        logger('Recieveing data was aborted')
        return []
    message = json.loads(data)
    sock.close()
    return message

print(get_data(miner_ip, miner_port, '', ''))
print(psutil.)


def check_connection(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except Exception as e:
        return False
    finally:
        s.close()


def get_pid(procces):
    pids = []
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == procces:
            pids.append(p.pid)
    return pids


def send_email(user, pwd, recipient, subject, body, logger):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        logger.info('Successfully sent the mail')
    except:
        logger.info('Failed to send mail')


def get_avg_hashrate_1m(ip, port, password, logger):
    hashrates = []
    for i in range(0, 5):
        data = get_data(ip, port, password, logger)
        try:
            hashrate = data['result'][2].split(';')[0]
        except Exception as e:
            logger.info('Data is empty or invalid')
            time.sleep(30)
            continue
        hashrates.append(float(hashrate))
        time.sleep(10)
        i += 1
    try:
        return statistics.mean(hashrates)
    except Exception as e:
        return 0


def config_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_name)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger
