import subprocess
import time
import RPi.GPIO as GPIO  # Gives access to the digital inputs/outputs on the Pi


#### KEY VARIABLES ###
# Operation times (Hours between which the lights are enabled)
start = 6
end = 22

# IP Addresses - you'll want to set your devices to a static IP on your router.
ipA = "192.168.1.100"
ipL = "192.168.1.101"

# How many failed pings before a device is shown as disconnected. Recommend >1, pings aren't always reliable!
cooldown = 15

# How long between pings, in seconds
interval = 60


#### FUNCTIONS ###
def ping(IP):
    result = subprocess.call(["ping", IP, "-c1", "-W2", "-q"])
    if result == 0:
        return True
    else:
        return False


def led(pin, state):
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)


def reset():
    led(2, False)
    led(3, False)
    led(4, False)
    return 0, 0


def in_between(now):  # Returns True if in hours of operation
    if start <= end:
        return start <= now.tm_hour < end
    else:
        return start <= now.tm_hour or now.tm_hour < end


def wait(duration): time.sleep(duration)


def flash():
    for _ in range(0, 6):
        led(3, True)
        wait(1)
        led(3, False)
        wait(1)


### SETUP ###
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
countA, countL = reset()

for x in range(0, 6):  # Flash the Ampersand to show it's booting
    led(3, True)
    wait(1)
    led(3, False)
    wait(1)

### MAIN LOOP ###
while True:
    if in_between(time.localtime()):  # Check current time is between the functional hours
        if ping(ipA):
            countA = cooldown  # Ping successful, reset count
        elif countA > 0:
            countA -= 1  # Ping unsuccessful, decrement count

        if ping(ipL):
            countL = cooldown
        elif countL > 0:
            countL -= 1

        # Light 'A' if counter not expired
        led(4, countA > 0)

        # Light 'L' if counter not expired
        led(2, countL > 0)

        # Light '&' if both
        led(3, countA > 0 and countL > 0)

    else:
        countA, countL = reset()

    wait(interval)
