rpi_heating_control

Raspberry pi based heating control. Uses python scripts to pull heating prices from
Nordpool and determine wether to turn off the heating or not.

You can enter PriceLimit (€/MWh) and maximum of skipped (MaxSkipped) hours to Settings.txt.
Gpio pin in same file acts as control for the heating element.

Based on SpotPriceForHeatPumpControl from Arttu Huttunen.

https://github.com/arkahu/SpotPriceForHeatPumpControl