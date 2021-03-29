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

### Installing packages
Save the file, and download the requirements from the requirements.txt file:  
Sudo is only needed if you plan on creating a service later.  
```sudo pip3 install -r requirements.txt``` or ```sudo python3 -m pip install -r requirements.txt```

### Creating a service
If you are hosting this on a home server or raspberry pi, you should create a systemd service. This makes the script start on bootup.

Create the service file:  
```sudo nano /lib/systemd/system/ddns.service```  
You can change "ddns" out with another service name if you want to.

Copy and paste this into the file:  
```
[Unit]
Description=Dynamic DNS via CloudFlare
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/<YourUsername>/ddns/ddns.py
Restart=on-failure
WorkingDirectory=/home/<YourUsername>/ddns

[Install]
WantedBy=multi-user.target
```  
Replace <YourUsername> with your username, or replace the whole path if you installed the script elsewhere.

Now save the file, and reload the daemon:  
```sudo systemctl daemon-reload```

Then enable the newly created service:  
```sudo systemctl enable ddns```

And then you can start the service:  
```sudo systemctl start ddns```

You can see the status of the script by using the systemctl status command:  
```sudo systemdtl status ddns```
