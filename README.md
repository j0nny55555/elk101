ELK101
============================

This repo holds all of the bits that I will present as a part of talk titled "ELK101" at SecKC on Tuesday the 17th of April.

To use this, you will need a running ELK installation.
Please refer to https://github.com/apolloclark/elk for a good easy ELK to spin up.

The tools I've wrote or wrote with peers were written with intent to move specific data. You will need to modify them to suite your needs.

CSV:
============================
csvtoelk.py - There are several modules you will need to run this:
Python module install list:
```bash
python -m pip install --upgrade pip
python -m pip install urllib3
python -m pip install elasticsearch
python -m pip install dateutil
python -m pip install python-dateutil
python -m pip install pytz
```
The data folder is where you put your folder groups, then import via:
```bash
python csvtoelk.py indexname data/foldername
```

Syslog:
============================
You will need to modify your ELK installation to forward tcp/udp port 5000.
Then move the syslogpipeline.conf to the /etc/logstash/conf.d/ folder
On the host you want to send logs from:
```bash
sudo vim /etc/rsyslog.d/50-default.conf
```
Then add a line like this:
```bash
*.* @syslogserverhostname:5000
```

Thank you:
============================
Thank you to all that have published helpful bits, I will attempt to record
all of it here:

Tools and parts:
============================

Vim in PowerShell:
http://www.expatpaul.eu/2014/04/vim-in-powershell/

Vagrant:
https://www.vagrantup.com/

VirtualBox:
https://www.virtualbox.org/

ELK Vagrant Box:
https://github.com/apolloclark/elk


Log Manipulation:
=============================

Prompt Syslog to Forward on its Own:
https://www.randomhacks.co.uk/how-to-configure-an-ubuntu-server-to-log-to-a-remote-syslog-server/

Getting Rsyslog to Capture another Hosts logs and store them:
http://yallalabs.com/linux/how-to-setup-a-centralized-log-server-using-rsyslog-on-ubuntu-16-04-lts/

Collecting and sending Syslog with additional Effects:
https://www.digitalocean.com/community/tutorials/how-to-centralize-logs-with-rsyslog-logstash-and-elasticsearch-on-ubuntu-14-04

Script building:
=============================

Python:
https://www.python.org/downloads/release/python-2714/

XML Parsing in Python:
https://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python

Sample Data:
=============================

Weather and other CSVs:
http://data.gov

