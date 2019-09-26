# Whos_Home
Quick Raspberry Pi project for lighting up status lights based on which devices are visible locally

This was carried out on a Raspberry Pi Zero W - WiFi functionality will obviously be required, but it shouldn't matter whether that's inbuilt, or using an adaptor.

Note before you start that different phones react differently to this - for whatever reason, my Android always responds, but my partner's Android only responds when the screen is unlocked. This seems to be to do with the Android version, but you can get around it to some extent with a longer cooldown timer - that way the screen only has to be unlocked occasionally!



Most of the things you'd want to edit in WiFiPing.py are set as variables near the beginning - the IP addresses of the devices, the time interval, cooldown period, operating hours, etc. Customise as suits you, and drop onto your Pi.

Open */etc/rc.local* on your Pi, and add the following on the line before *exit 0*

*python3 /home/pi/WiFiPing.py &

(Adjust the path depending on where you put the file!)

This will run your script when the Pi boots. The '&' is important here - it means the script will open the script in the background, and not wait for it to finish before carrying on. That's good, as this script won't finish!

If your Pi is set up to support a desktop, you might find it doesn't boot without a monitor plugged in, which is useful. You can get around this by enabling *hdmi_force_hotplug=1* in */boot/config.txt*


**Lights**

Super basic, the script will toggle GPIO2, 3 and 4. Check your pinout diagram and plug in accordingly.
