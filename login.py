import argparse
import getpass
import logging
import urllib.request
import urllib.parse
import re
import time
def openurl(url, data=None):
    try:
        headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
        if data is not None:
            data = urllib.parse.urlencode(data)
            data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(url, data=data)#headers=headers, 
        html = urllib.request.urlopen(req, timeout=10).read()
        return html.decode('utf-8')
    except:
        logging.warning("Network unreachable")
        return None
def login(username, password):
    # login
    logging.info("Sending login get")
    loginreq = openurl("https://agnigarh.iitg.ac.in:1442/login?1")
    if loginreq is None:
        return None
    # get magic
    magic = re.search(r'name="magic" value="(.+)"', loginreq)
    if magic:
        magic = magic.group(1)
        logging.info(f"Got magic = {magic}")
    else:
        logging.warning("Got no magic. Abort login")
        return None
    payload = {'4Tredir': 'https://agnigarh.iitg.ac.in/login?1', 'magic': magic, 'username': username, 'password': password}
    r = openurl("https://agnigarh.iitg.ac.in:1442/", data=payload)
    if r is None:
        return None
    logging.info("Sending login post")
    ka = re.search(r'https://agnigarh.iitg.ac.in:1442/keepalive\?(.+)"', r)
    if ka:
        ka = ka.group()[:-1]
        logging.info(f"Got keepalive = {ka}")
        return ka
    else:
        logging.warning("Didn't get keepalive")
        return None

def keepalive(kaurl):
    # keepalive
    logging.debug(f"Sending keepalive to {kaurl}")
    karet = openurl(kaurl)
    if karet is None:
        return None
    # print(karet)
    if kaurl.replace("keepalive", "logout") in karet:
        # success
        logging.info("Keepalive success")
        return kaurl
    else:
        # failure
        logging.warning("Keepalive failure")
        return None
def main(username, password, logs, file):
    if username is None:
      username = str(input("Username: "))
    if password is None:
       password = getpass.getpass()
    if logs == True and file is None:
        logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO, format='[%(levelname)s](%(asctime)s)\t%(message)s')
    elif logs == True:
       logging.basicConfig(filename="./"+file, filemode='w',datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO, format='[%(levelname)s](%(asctime)s) %(message)s')
    else:
       logging.disable()
    logging.info("Started logging")
    keepalive_url = login(username, password)

    while True:
        # if already loggedin
        if keepalive_url is not None:
            keepalive_url = keepalive(keepalive_url)
        # if not logged in
        if keepalive_url is None:
            keepalive_url = login(username, password)
        if keepalive_url is None:
            logging.error("Could not log in. Trying back in 5 sec")
            time.sleep(5)
        else:
            logging.info("Sleeping for 90 sec")
            time.sleep(90)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto-login into IITG web interface', allow_abbrev=False)
    parser.add_argument('-u','--user', '--username', type=str, help='Provide signin username', dest="user")
    parser.add_argument('-p','--pass', '--password', type=str, help='Provide signin password', dest="pw")
    parser.add_argument('-l', '--log', '--logging', help="Enable logs", dest="l", action='store_true')
    parser.add_argument('-o', '--out', '--outfile', type=str, help="Specify outfile for logs", dest="file")
    args = parser.parse_args()
    main(args.user, args.pw, args.l, args.file)
