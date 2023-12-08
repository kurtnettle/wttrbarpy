from datetime import datetime
from string import Template

from wttrbarpy import emojis, icons
from wttrbarpy.config import Config
from wttrbarpy.utils import (
    gen_brief_report,
    get_clock_icon,
    get_moon_phase_icon,
    get_uv_index_lvl,
    get_weather_icon,
    get_wind_icon,
    hour12_to_hour24,
    is_day,
)


def format_time(time_str: str, ampm: bool = False) -> str:
    x = datetime.strptime(time_str, "%I:%M %p")
    return time_str if ampm else x.strftime("%H:%M")


def format_date(date_str: str, fmt_str) -> str:
    x = datetime.strptime(date_str, "%Y-%m-%d")
    return x.strftime(fmt_str) if fmt_str else date_str


def format_hour_txt(hour: str, config) -> str:
    if config.ampm:
        txt = hour12_to_hour24(hour=hour)
    else:
        txt = hour.replace("00", "").zfill(2)

    if config.format_type == 1 or config.hour_text_only:
        return txt
    elif config.format_type == 2:
        return f"{get_clock_icon(hour,emoji=config.emoji.enabled)}"
    elif config.format_type == 3:
        return f"{get_clock_icon(hour,emoji=config.emoji.enabled)} {txt}"
    else:
        raise ValueError(f"Invalid hour format type ({config.format_type}) was passed.")


def format_temp_txt(temp: str, unit: str, show_temp_unit: bool) -> str:
    """Format a temperature value

    Args:
        temp (str): temperature value
        unit (str): unit of temperature value
        show_temp_unit (bool): include the unit beside the value.

    Raises:
        ValueError: invalid unit is passed

    Returns:
        str: formatted temperature text
    """

    txt = f"{temp}{emojis['degree']}"

    if show_temp_unit:
        if unit == "USCS":
            txt = txt + "F"
        elif unit == "SI":
            txt = txt + "C"
        else:
            raise ValueError(f"Invalid unit ({unit}) was passed.")

    return txt


def format_wind_txt(data: dict, config: Config) -> str:
    if config.unit == "USCS":
        txt = data["windspeedKmph"] + " km/h"
    elif config.unit == "SI":
        txt = data["windspeedMiles"] + " mph"
    else:
        raise ValueError("invalid wind speed unit was passed.")

    if config.format_type != 1:
        txt += f" {get_wind_icon(data['winddirDegree'],config.emoji.enabled)}"

    if not config.hide_wind_details:
        txt += f" ({data['winddirDegree']}{emojis['degree']} {data['winddir16Point']})"

    return txt


def format_location_txt(config: Config) -> str | ValueError:
    degree = emojis["degree"]

    txt = ""
    location_icon = (
        emojis["flag-in-hole"] if config.emoji.enabled else icons["location"]
    )
    emoji = config.emoji.enabled
    data = config.data["nearest_area"][0]

    if not data:
        return "Location: N/A"

    latitude = data.get("latitude", "N/A") + degree
    longitude = data.get("longitude", "N/A") + degree

    if data["areaName"][0]["value"]:
        txt += f'{data["areaName"][0]["value"]}, '
    if data["region"][0]["value"]:
        txt += f'{data["region"][0]["value"]}, '
    if data["country"][0]["value"]:
        txt += f'{data["country"][0]["value"]}'

    if config.format_type == 1:
        txt = "Location: " + txt
        txt += f" (lat: {latitude} lon: {longitude})"

    elif config.format_type == 2:
        txt = location_icon + " " + txt
        if emoji:
            txt += f" ({latitude} {longitude})"
        else:
            txt += f' ({icons["latitude"]} {latitude} {icons["longitude"]} {longitude})'

    elif config.format_type == 3:
        txt = location_icon + " Location: " + txt
        if emoji:
            txt += f" (lat: {latitude} lon: {longitude})"
        else:
            txt += f' ({icons["latitude"]} lat: {latitude} {icons["longitude"]} lon: {longitude})'

    else:
        ValueError(f"Invalid location format type ({config.format_type}) was passed.")

    return txt


def format_day_report_2nd_line(config: Config) -> str:
    txt = ""

    icon = emojis if config.emoji.enabled else icons

    today = config.data["weather"][0]
    astronomy = config.data["weather"][0]["astronomy"][0]

    if config.unit == "USCS":
        max_temp = format_temp_txt(
            temp=today["maxtempF"],
            unit=config.unit,
            show_temp_unit=config.show_temp_unit,
        )
        min_temp = format_temp_txt(
            temp=today["mintempF"],
            unit=config.unit,
            show_temp_unit=config.show_temp_unit,
        )
    else:
        max_temp = format_temp_txt(
            temp=today["maxtempC"],
            unit=config.unit,
            show_temp_unit=config.show_temp_unit,
        )
        min_temp = format_temp_txt(
            temp=today["mintempC"],
            unit=config.unit,
            show_temp_unit=config.show_temp_unit,
        )

    sunrise = format_time(astronomy["sunrise"], ampm=config.ampm)
    sunset = format_time(astronomy["sunset"], ampm=config.ampm)

    if config.format_type == 1:
        txt += f"max: {max_temp} min: {min_temp} "
        txt += f"sunrise: {sunrise} sunset: {sunset}\n"

    elif config.format_type == 2:
        txt += f'{icon["arrow"]["up"]} {max_temp} {icon["arrow"]["down"]} {min_temp} '
        txt += f'{icon["sunrise"]} {sunrise} {icon["sunset"]} {sunset}\n'

    elif config.format_type == 3:
        txt += f'{icon["arrow"]["up"]} max: {max_temp} {icon["arrow"]["down"]} min: {min_temp} '
        txt += (
            f'{icon["sunrise"]} sunrise: {sunrise} {icon["sunset"]} sunset: {sunset}\n'
        )

    else:
        ValueError(
            f"Invalid day report 2nd line format type ({config.format_type}) was passed."
        )

    return txt


def format_chances(hour: dict, max_chances: int) -> str:
    txt = ""
    max_chances = int(max_chances)
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind",
    }

    ttxt = {}
    for chance in chances:
        if int(hour[chance]) > 0:
            ttxt[chances.get(chance)] = int(hour[chance])

    ttxt = sorted(ttxt.items(), key=lambda x: x[1], reverse=True)  # sort by % in desc

    for idx, i in enumerate(ttxt, start=1):
        if idx > max_chances and max_chances > 0:
            break

        txt += f"{i[0]} {i[1]}%"

        if idx < len(ttxt) and not (max_chances > 0 and idx > max_chances - 1):
            txt += ", "

    return txt


def format_days_report(config: Config):
    txt = ""

    days = config.data["weather"]
    for i, day in enumerate(days):
        tmp = ""
        if i == 0:
            tmp += f"Today, "
        elif i == 1:
            tmp += f"Tomorrow, "
        elif i == 2:
            tmp += f"Day after tomorrow, "

        tmp += f'{format_date(day["date"],fmt_str=config.date_format)}'

        if not config.plain_text:
            tmp = "<b>" + tmp + "</b>"

        tmp += "\n"

        tmp += format_day_report_2nd_line(config=config)

        curr_hour = datetime.now().strftime("%H")
        for hour in day["hourly"]:
            hr_txt = format_hour_txt(hour=hour["time"], config=config)
            if i == 0:
                if int(hour["time"].replace("00", "")) < int(curr_hour):
                    continue

            report = gen_brief_report(
                data=hour,
                hr_txt=hour["time"],
                config=config,
            )
            temp = format_temp_txt(
                temp=report["temp"],
                unit=config.unit,
                show_temp_unit=config.show_temp_unit,
            )
            if config.format_type != 1:
                if config.emoji.enabled:
                    tmp += f"{hr_txt}  {report['icon']}  {temp} {report['desc']}"
                else:
                    tmp += f"{hr_txt} {report['icon']}  {temp} {report['desc']}"
            else:
                tmp += f"{hr_txt} {temp} {report['desc']}"

            if not config.hide_conditions:
                tmp += ", " + format_chances(hour, max_chances=config.max_conditions)
            tmp += "\n"

        txt += tmp + "\n"

    return txt


def format_tooltip(config: Config) -> str:
    nearest_area = config.data["nearest_area"][0]
    current_condition = config.data["current_condition"][0]
    report = gen_brief_report(
        data=current_condition,
        config=config,
        hr_txt=config.data["weather"][0]["astronomy"][0],
    )

    txt = ""
    if not config.plain_text:
        txt += f"<b>{report['desc']}</b> "
    else:
        txt += f"{report['desc']}, "

    txt += f"{format_temp_txt(temp=report['temp'],unit=config.unit,show_temp_unit=config.show_temp_unit)}\n"
    txt += f"Feels Like: {format_temp_txt(temp=report['feels_like'],unit=config.unit,show_temp_unit=config.show_temp_unit)}\n"
    txt += f"Humidity: {current_condition['humidity']}%\n"
    txt += f"Wind: {format_wind_txt(data=current_condition,config=config)}\n"
    
    today_astronomy = config.data["weather"][0]["astronomy"][0]
    if not is_day(today_astronomy):
        moon_phase_icon=get_moon_phase_icon(phase=today_astronomy['moon_phase'],emoji=config.emoji.enabled)
        txt += f"Moon Phase: {moon_phase_icon} ({today_astronomy['moon_phase']})\n"
    
    txt += f"UV Index: {current_condition['uvIndex']} ({get_uv_index_lvl(current_condition['uvIndex'])}) \n"

    txt += format_location_txt(config)
    txt += "\n\n"
    txt += format_days_report(config)

    return txt.strip()


def format_text(config: Config):
    current_condition = config.data["current_condition"][0]
    temp_keys = ["FeelsLikeC", "FeelsLikeF", "temp_C", "temp_F", "tempF", "tempC"]

    if config.neutral_icon:
        icon_type = "neutral"
    else:
        today_astronomy = config.data["weather"][0]["astronomy"][0]
        if is_day(today_astronomy):
            icon_type = "day"
        else:
            icon_type = "night"

    weather_icon = get_weather_icon(
        code=current_condition["weatherCode"],
        icon_type=icon_type,
        is_emoji=config.emoji.enabled,
    )

    text = "N/A"
    if config.custom_indicator:
        text = Template(config.custom_indicator)
        try:
            text = text.substitute(current_condition, icon=weather_icon)
        except Exception as e:
            raise KeyError(f"Invalid placeholder: {e}") from e

    else:
        if config.main_indicator in temp_keys:
            if config.main_indicator == "temp_C" and config.unit == "USCS":
                config.main_indicator = "temp_F"

            text = format_temp_txt(
                current_condition[config.main_indicator],
                unit=config.unit,
                show_temp_unit=config.show_temp_unit,
            )
        else:
            text = current_condition[config.main_indicator]

    if config.custom_indicator:
        return text

    if config.vertical_view:
        return f"{weather_icon}\n{text}"
    else:
        return f"{weather_icon} {text}"
