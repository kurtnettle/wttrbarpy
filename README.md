<h1 align="center"> wttrbar.py </h1>
<p align="center"> a highly customizable weather module for <a href="https://github.com/Alexays/Waybar/">Waybar</a> inspired by <a href="https://github.com/bjesus/wttrbar">wttrbar</a> using <a href="https://wttr.in/">wttr.in</a>
</p>

## ⚠️ This project has been discontinued.
### I am working on a new weather module which will have multiple sources for fetching the weather data.

## Preview 
<p align="center">
<img src="https://github.com/kurtnettle/wttrbarpy/assets/89929240/d093b739-e707-4646-b432-0c409a585a6a"/>
</p>

## Installation

`pip install git+https://github.com/kurtnettle/wttrbarpy.git`

## Usage

- `--ampm` - show time in AM/PM format. defaults to `False`
- `--custom-indicator` - customize the indicator.
- `--date-format` - formats the date next to the days. see [reference](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). defaults to `%A-%b-%d`
- `--emoji` - replace icons with emojis. defaults to `False`
- `--fahrenheit` - use fahrenheit instead of celsius. defaults to `False`
- `--format-type` - specify the global output format type (1 only text,  2 only icon/emoji, 3 text with icon/emoji). defaults to `2`
- `--hide-conditions` - hide extra conditions next to each hour description, like `20° Cloudy` instead of `20° Cloudy, Overcast 81%, Sunshine 13%`. defaults to `False`
- `--hide-wind-details` - removes extra wind details (wind direction and degree). defaults to `False`

- `--location` - specify a location. defaults to `None` (i.e your current location)
- `--main-indicator` - decide which `current_conditions` key will be shown on Waybar. defaults to `temp_C`
- `--max-conditions` - limit the number of conditions to show next to each hour description. defaults to `0` (shows all available)
- `--neutral-icon` - show neutral icon instead of daytime/nighttime icons. defaults to `False`
- `--plain-text` - shows the plain text removing all Pango markup tags and json output. defaults to `False`
- `--show-temp-unit` - show temperature value with unit like 20°C or 20°F. defaults to `False` 
- `--vertical-view` - shows the icon on the first line and temperature in a new line (doesn't work for custom-indicator). defaults to `False`
- `--hour-text-only` - show hour as text only. defaults to `False`
- `--version` - show wttrbarpy version.

e.g. `wttrbarpy --location Dhaka --max-conditions 2 --format-type 1`


## Waybar configuration

Assuming `wttrbarpy` is in your path, it can be used like:
```json
"custom/weather": {
    "format": "{}",
    "tooltip": true,
    "interval": 3600,
    "exec": "wttrbarpy",
    "return-type": "json"
},
```
