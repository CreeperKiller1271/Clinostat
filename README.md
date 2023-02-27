# Setup
1. the pi must first be conected to the internet.
  a. Type the following command into the command prompt: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
  b. Enter the code from the dopout bellow into the file.
  <details>
  <summary>My top THINGS-TO-RANK</summary>

  network={
      ssid="network name"
      priority=1
      proto=RSN
      key_mgmt=WPA-EAP
      pairwise=CCMP
      auth_alg=OPEN
      eap=PEAP
      identity="username"
      password="password"
      phase1="peaplabel=0"
      phase2="auth=MSCHAPV2"
      }
  
  </details>
  c. After entering the code use cntrl+o to save and cntrl+x to exit.
2. Go to the setting menue in the pi and enable I2C, optionally SSH can be enabled for off device editing.
3. Reboot the system using the "sudo reboot" command
3. Next open a command prompt and run all the commands individually, this will intall all software and the needed pluggins.
4. Finally the respository can be pulled either using a git client or taking the files from a usb drive.
