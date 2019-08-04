# IITG-AutoLogin

## What does it do?

As the name suggests, it will log in with your username and password to agnigarh.iitg.ac.in, so this means no more browser tabs :)

## Requirements

- Python 3

That's it. *ZERO* external deps. *yay*

## Usage

python login.py [-h] [-u USER] [-p PW] [-l] [-o FILE]

Auto-login into IITG web interface

optional arguments:
  -h, --help            		    show this help message and exit
  -u USER, --user USER, --username USER     Provide signin username
  -p PW, --pass PW, --password PW	    Provide signin password
  -l, --log, --logging  		    Enable logs
  -o FILE, --out FILE, --outfile FILE	    Specify outfile for logs

If any of the username or password are missing in arguments, those will be asked on runtime.



## Bonus

You can run this with "pythonw" interpreter instead of the normal "python" interpreter, to run the script in background.
Use -

```bash
pythonw login.py -u USERNAME -p PASSWORD
```

Make sure you specify username and password as command line arguments.

I have also included certificate chain for *.iitg.ac.in . So if someone is getting ssl errors, he/she can edit login.py to include these certs.
