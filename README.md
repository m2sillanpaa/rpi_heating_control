rpi_heating_control

Raspberry pi based heating control. Uses python scripts to pull heating prices from
Nordpool and determine wether to turn off the heating or not.

You can enter PriceLimit (€/MWh) and maximum of skipped (MaxSkipped) hours to Settings.txt.
Gpio pin in same file acts as control for the heating element.

Run:
crontab -e

Add:
0 * * * * python3 /home/pi/rpi_heating_control/TimerHeatPumpControl.py

This causes the output adjust to be run every hour.

5 0 * * * python3 /home/pi/rpi_heating_control/SpotPriceGet.py

This causes the prices for next day to be aquired 5 past 00:05. This is because output assumes finnish time and the price timestamp is in swedish timezone (so 00:00 we set the control for 23:00-00:00. So after that we need to get the output values for 00:00->01:00.).


Based on SpotPriceForHeatPumpControl from Arttu Huttunen.

https://github.com/arkahu/SpotPriceForHeatPumpControl