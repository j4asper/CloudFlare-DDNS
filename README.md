# CloudFlare Dynamic DNS
### Using your domain as your dynamic dns.

This is primarily created to run on linux on a raspberry pi or something else at home.

### Installation
Clone the repo:
```git clone https://github.com/j4asper/ddns.git```

Then cd into the directory:
```cd ddns```

Now edit the config.yaml file to fit your needs:
You can use the text editor of choice, i use nano.
```nano config.yaml```

Your global api key can be found here: https://dash.cloudflare.com/profile/api-tokens

Save the file, and download the requirements from the requirements.txt file:
```pip3 install -r requirements.txt``` or ```python3 -m pip install -r requirements.txt```

If you are hosting this on a home server or raspberry pi, you should create a systemd service. This makes the script start on bootup.
