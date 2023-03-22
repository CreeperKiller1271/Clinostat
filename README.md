# Setup
<ol>
<li>The pi must first be conected to the internet.</li>
  <ul>
  <li>Type the following command into the command prompt: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf</li>
  <li>Enter the code from the dopout bellow into the file.</li>
<pre>
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
      }</pre>
  <li>After entering the code use cntrl+o to save and cntrl+x to exit.</li>
  </ul>
<li>Go to the setting menue in the pi and enable I2C, optionally SSH can be enabled for off device editing.</li>
<li>Reboot the system using the "sudo reboot" command.</li>
<li>Next open a command prompt and run all the commands individually, this will intall all software and the needed pluggins.</li>
<li>Finally the respository can be pulled either using a git client or taking the files from a usb drive.</li>
</ol>
