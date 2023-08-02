# RPi Fan Control

A python utility to control a variable speed fan on a Raspberry Pi

This is specifically for the ICE Tower cooler from 52Pi as documented [here](https://wiki.52pi.com/index.php?title=EP-0163). GPIO configuration for other PWM cooling fans may differ.

## Features

- Can be run as a normal user, e.g., via a user's crontab:
  - `@reboot ~/.local/bin/rpi-fancontrol`
- Applies a slope function to determine fan speed:
  - slope = (Speed_max / (TempUpperThreshold - TempLowerThreshold))
  - speed = (slope x (CurrentTemp - TempLowerThreshold))
- Applies a 2°C hysteresis to prevent rapid changes of fan speed
  - Temperature must move 2°C or more in either direction to adjust fan speed