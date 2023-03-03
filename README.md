# clawclan
claw clan machines
Claw clan website im working on

First, run this `sudo apt install ffmpeg python3-serial python3-dev libgnutls28-dev espeak python3-smbus python3-pip git` to install the libraries. 

Next, run `git clone https://github.com/byronbonkers/clawclan.git ~/clawclan` to clone the git repo.

Then, run `sudo python3 -m pip install -r ~/clawclan/requirements.txt`

Open the new clawclan directory `cd clawclan`

Then just make it run at start up by doing `crontab -e` and paste this in at the bottom:

`@reboot /bin/bash /home/pi/clawclan/start_machine`
