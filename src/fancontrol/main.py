#!/usr/bin/env python3

import time

from .gpio import GPIO


class RPiFanControl:
    FAN_PIN = 8
    PWM_START_FREQ = 50
    TEMPERATURE_SYS_NODE = "/sys/class/thermal/thermal_zone0/temp"
    TEMPERATURE_MULTIPLIER = 1000
    TEMP_UPPER = 60
    TEMP_LOWER = 33
    # hysteresis: don't change the fan speed unless the temperature
    # moves at least this much
    TEMP_HYST = 2

    FAN_SPEED_SLOPE = 100 / (TEMP_UPPER - TEMP_LOWER)

    def __init__(self):
        self._saved_temp = -1
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.FAN_PIN, GPIO.OUT)
        p = GPIO.PWM(self.FAN_PIN, self.PWM_START_FREQ)
        p.start(0)
        self._pwm = p

    def temp_changed(self, current_temp):
        # calculate if change is outside hysteresis
        # https://github.com/JFtechOfficial/Raspberry-Pi-PWM-fan/blob/07c951c2bdc52cf43cf8999d94b686bda48311bb/fan.py#L58C23-L58C23
        changed = False
        if self._saved_temp < 0:
            self._saved_temp = current_temp
            changed = True
        else:
            delta = abs(current_temp - self._saved_temp)
            if delta > self.TEMP_HYST:
                self._saved_temp = current_temp
                changed = True

        return changed

    def update(self):
        cpu_temp = self.get_temp()
        # duty cycle is explained here:
        # https://youngkin.github.io/post/pulsewidthmodulationraspberrypi/#terminology
        # can be 0 - 100
        print(f"cpu temp: {cpu_temp:.2f}C")
        if self.temp_changed(cpu_temp):
            cpu_temp = max(cpu_temp, self.TEMP_LOWER)
            speed = int(self.FAN_SPEED_SLOPE * (cpu_temp - self.TEMP_LOWER))

            # bracket speed to an upper bound of 100
            speed = min(speed, 100)

            # round speed to a multiple of 25 using integer divsion
            # speed = speed // 25
            # speed = speed * 25

            print(f"fan set to {speed}%")
            self._pwm.ChangeDutyCycle(speed)

    def get_temp(self) -> float:
        # https://gist.github.com/rogerlin0330/b935f1ac9db7f33db5defd716f3ecb5b#file-fan_speed-py-L25
        with open(self.TEMPERATURE_SYS_NODE, "r") as f:
            _temp_str = f.read()
            cpu_temp = int(_temp_str) / self.TEMPERATURE_MULTIPLIER
            return cpu_temp

    def __del__(self):
        if hasattr(self, "_pwm"):
            self._pwm.stop()
        GPIO.cleanup()


def main():
    f = RPiFanControl()
    while True:
        f.update()
        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard iterrupt. Quitting.")
        exit(0)
