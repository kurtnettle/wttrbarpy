from datetime import datetime
from functools import lru_cache

from wttrbarpy import emojis, icons
from wttrbarpy.config import Config


def hour12_to_hour24(hour: str) -> str:
    hour = int(hour.replace("00", ""))
    am_or_pm = "PM" if hour >= 12 else "AM"

    if hour > 12:
        hour = hour % 12
    elif hour == 0:
        hour = 12

    return f"{hour}{am_or_pm}"


def is_day(data: dict) -> bool:
    if isinstance(data, dict):
        curr_time = datetime.now().time()
        sunrise = datetime.strptime(data["sunrise"], "%I:%M %p").time()
        sunset = datetime.strptime(data["sunset"], "%I:%M %p").time()
        return curr_time >= sunrise and curr_time <= sunset
    elif isinstance(data, str):
        return int(data) >= 600 and int(data) < 1800


def get_uv_index_lvl(uv_index: int, color_txt=True) -> str:
    # https://en.wikipedia.org/wiki/Ultraviolet_index

    if isinstance(uv_index, str):
        uv_index = int(uv_index)

    text = ""

    if uv_index <= 2:
        lvl = "low"
        color = "green"  # missing 'u' :(
    elif uv_index >= 3 and uv_index <= 5:
        lvl = "moderate"
        color = "yellow"
    elif uv_index >= 6 and uv_index <= 7:
        lvl = "high"
        color = "orange"
    elif uv_index >= 8 and uv_index <= 10:
        lvl = "very high"
        color = "red"
    elif uv_index >= 11:
        lvl = "extreme"
        color = "violet"

    return lvl


def get_clock_icon(hour: str, emoji=False) -> str:
    clock = None

    if hour in ("0", "1200"):
        clock = "0"
    elif hour in ("300", "1500"):
        clock = "3"
    elif hour in ("600", "1800"):
        clock = "6"
    elif hour in ("900", "2100"):
        clock = "9"
    else:
        raise ValueError(f"Invalid hour ({hour}) was passed.")

    if emoji:
        return emojis["clock"][clock]
    else:
        return icons["clock"][clock]


def get_moon_phase_icon(phase: str, emoji: bool = False) -> str:
    # https://www.worldweatheronline.com/weather-api/api/docs/astronomy-api.aspx
    phases = {
        "New Moon": "new",
        "Waxing Crescent": "waxing-crescent",
        "First Quarter": "first-quarter",
        "Waxing Gibbous": "waxing-gibbous",
        "Full Moon": "full",
        "Waning Gibbous": "waning-gibbous",
        "Last Quarter": "last-quarter",
        "Waning Crescent": "waning-crescent",
    }

    if phases.get(phase):
        if emoji:
            return emojis["moon"][phases[phase]]
        else:
            return icons["moon"][phases[phase]]
    else:
        raise ValueError(f"Invalid moon phase ({phase}) was passed.")


@lru_cache(maxsize=10)
def get_wind_icon(wind_dir_degree: int, emoji: bool = False) -> str:
    wind_dir_degree = int(wind_dir_degree)

    wind_icon = ""
    icon = emojis if emoji else icons

    if wind_dir_degree == 0:
        wind_icon = icon["wind_dir"]["up"]
    elif wind_dir_degree > 0 and wind_dir_degree < 90:
        wind_icon = icon["wind_dir"]["up_right"]
    elif wind_dir_degree == 90:
        wind_icon = icon["wind_dir"]["right"]
    elif wind_dir_degree > 90 and wind_dir_degree < 180:
        wind_icon = icon["wind_dir"]["down_right"]
    elif wind_dir_degree == 180:
        wind_icon = icon["wind_dir"]["down"]
    elif wind_dir_degree > 180 and wind_dir_degree < 270:
        wind_icon = icon["wind_dir"]["down_left"]
    elif wind_dir_degree == 270:
        wind_icon = icon["wind_dir"]["left"]
    elif wind_dir_degree > 270 and wind_dir_degree < 360:
        wind_icon = icon["wind_dir"]["up_left"]
    elif wind_dir_degree == 360:
        wind_icon = icon["wind_dir"]["up"]
    else:
        raise ValueError(
            f"Invalid wind direction degree ({wind_dir_degree}) was passed."
        )
    return wind_icon


def get_weather_icon(code: int, icon_type: str, is_emoji: bool = False):
    code = int(code)

    if code == 113:  # clear/sunny
        icon = icons["clear"][icon_type]
        if icon_type == "day":
            emoji = emojis["sun"]
        else:
            emoji = emojis["moon"]["crescent"]
    elif code == 116:  # partly cloudy
        icon = icons["cloudy"][icon_type]
        if icon_type == "day":
            emoji = emojis["sun-behind-cloud"]
        else:
            emoji = emojis["cloud"]
    elif code == 119:  # cloudy
        icon = icons["cloudy"][icon_type]
        emoji = emojis["cloud"]
    elif code == 122:  # overcast
        if icon_type == "day":
            icon = icons["overcast"]["day"]
            emoji = emojis["sun-behind-large-cloud"]
        else:
            icon = icons["cloudy"]["night"]
            emoji = emojis["cloud"]
    elif code == 143:  # mist
        icon = icons["fog"][icon_type]
        emoji = emojis["fog"]
    elif code == 176:  # patchy rain nearby
        icon = icons["rain"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 179:  # patchy snow nearby
        icon = icons["snow"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 182:  # patchy sleet nearby
        icon = icons["sleet"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 185:  # patchy freezing drizzle nearby
        icon = icons["rain-wind"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 200:  # thundery outbreaks in nearby
        icon = icons["lightning"][icon_type]
        emoji = emojis["lightning-cloud"]
    elif code == 227:  # blowing snow
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 230:  # blizzard
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 248:  # fog
        icon = icons["fog"][icon_type]
        emoji = emojis["fog"]
    elif code == 260:  # freezing fog
        icon = icons["fog"][icon_type]
        emoji = emojis["fog"]
    elif code == 263:  # patchy light drizzle
        icon = icons["rain"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 266:  # light drizzle
        icon = icons["rain"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 281:  # freezing drizzle
        icon = icons["rain-wind"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 284:  # heavy freezing drizzle
        icon = icons["rain-mix"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 293:  # patchy light rain
        icon = icons["rain"][icon_type]
        if icon_type == "day":
            emoji = emojis["sun-behind-rain-cloud"]
        elif icon_type == "night":
            emoji = emojis["rain-cloud"]
    elif code == 296:  # light rain
        icon = icons["rain"][icon_type]
        if icon_type == "day":
            emoji = emojis["sun-behind-rain-cloud"]
        elif icon_type == "night":
            emoji = emojis["rain-cloud"]
    elif code == 299:  # moderate rain at times
        icon = icons["rain-wind"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 302:  # moderate rain
        icon = icons["rain-wind"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 305:  # heavy rain at times
        icon = icons["rain-mix"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 308:  # heavy rain
        icon = icons["rain-mix"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 311:  # light freezing rain
        icon = icons["rain"]["neutral"]
        emoji = emojis["rain-cloud"]
    elif code == 314:  # moderate or heavy freezing rain
        icon = icons["rain-mix"]["neutral"]
        emoji = emojis["rain-cloud"]
    elif code == 317:  # light sleet
        icon = icons["sleet"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 320:  # moderate or heavy sleet
        icon = icons["sleet"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 323:  # patchy light snow
        icon = icons["snow"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 326:  # light snow
        icon = icons["snow"][icon_type]  # Hey there, archeologist!
        emoji = emojis["snow-cloud"]  # Just to know, I haven't manually type all these
    elif code == 329:  # patchy moderate snow
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 332:  # moderate snow
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 335:  # patchy heavy snow
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 338:  # heavy snow
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 350:  # ice pellets
        icon = icons["snowflake"]["neutral"]
        emoji = emojis["snowflake"]
    elif code == 353:  # light rain shower
        icon = icons["showers"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 356:  # moderate or heavy rain shower
        icon = icons["showers"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 359:  # torrential rain shower
        icon = icons["rain-mix"][icon_type]
        emoji = emojis["rain-cloud"]
    elif code == 362:  # light sleet showers
        icon = icons["sleet"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 365:  # moderate or heavy sleet showers
        icon = icons["sleet-storm"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 368:  # light snow showers
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 371:  # moderate or heavy snow showers
        icon = icons["snow-wind"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 374:  # light showers of ice pellets
        icon = icons["snowflake"]["neutral"]
        emoji = emojis["snowflake"]
    elif code == 377:  # moderate or heavy showers of ice pellets
        icon = icons["snowflake"]["neutral"]
        emoji = emojis["snowflake"]
    elif code == 386:  # patchy light rain in area with thunder
        icon = icons["lightning"][icon_type]
        emoji = emojis["lightning-cloud"]
    elif code == 389:  # moderate or heavy rain in area with thunder
        icon = icons["thunderstorm"][icon_type]
        emoji = emojis["lightning-rain-cloud"]
    elif code == 392:  # patchy light snow in area with thunder
        icon = icons["snow-thunderstorm"][icon_type]
        emoji = emojis["snow-cloud"]
    elif code == 395:  # moderate or heavy snow in area with thunder
        icon = icons["snow-thunderstorm"][icon_type]
        emoji = emojis["snow-cloud"]
    else:
        raise ValueError(f"Invalid weather code ({code}) was passed.")

    return emoji if is_emoji else icon


def gen_brief_report(data: dict, config: Config, hr_txt: str = None):
    if config.unit == "USCS":
        temp = data.get("tempF", data.get("temp_F", "N/A"))
        feel_like = data.get("FeelsLikeF", "N/A")
        wind_speed = data.get("windspeedKmph", "N/A")
    elif config.unit == "SI":
        temp = data.get("tempC", data.get("temp_C", "N/A"))
        feel_like = data.get("FeelsLikeC", "N/A")
        wind_speed = data.get("windspeedMiles", "N/A")
    else:
        raise ValueError(f"Invalid unit ({config.unit}) was passed.")

    if config.neutral_icon:
        icon_type = "neutral"
    else:
        icon_type = "day" if is_day(hr_txt) else "night"

    return {
        "temp": temp,
        "icon": get_weather_icon(
            data["weatherCode"], icon_type=icon_type, is_emoji=config.emoji.enabled
        ),
        "feels_like": feel_like,
        "wind_speed": wind_speed,
        "desc": data["weatherDesc"][0]["value"],
    }
