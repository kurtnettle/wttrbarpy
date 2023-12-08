from argparse import ArgumentParser
from json import dumps, loads
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen

from wttrbarpy.config import Config, build_config
from wttrbarpy.formats import format_text, format_tooltip


def print_json(data: dict) -> None:
    print(dumps(data, ensure_ascii=False))


def main() -> None:
    parser = ArgumentParser(
        prog="wttrbarpy",
        description="a highly customizable weather module for Waybar",
        allow_abbrev=False,
    )

    parser.add_argument(
        "--ampm",
        action="store_true",
        dest="ampm",
        help="show time in AM/PM format. defaults to False",
    )
    parser.add_argument(
        "--location",
        "-l",
        dest="location",
        type=str,
        default="",
        help="specify a location. defaults to None (i.e your current location)",
    )
    parser.add_argument(
        "--main-indicator",
        dest="main_indicator",
        type=str,
        default="temp_C",
        help="decide which current_conditions key will be shown on waybar. defaults to temp_C",
    )
    parser.add_argument(
        "--custom-indicator",
        dest="custom_indicator",
        type=str,
        default=None,
        help="customize the indicator. example: $temp_C",
    )
    parser.add_argument(
        "--date-format",
        dest="date_format",
        type=str,
        default="%A %b %d",
        help="formats the date next to the days. defaults to %%A-%%b-%%d",
    )
    parser.add_argument(
        "--hide-conditions",
        action="store_true",
        dest="hide_conditions",
        help='hide extra conditions next to each hour description. like "20° Cloudy" instead of "20° Cloudy, Overcast 81%%, Sunshine 13%%". defaults to False',
    )
    parser.add_argument(
        "--hide-wind-details",
        action="store_true",
        dest="hide_wind_details",
        help="removes extra wind details (wind direction and degree). defaults to False",
    )
    parser.add_argument(
        "--max-conditions",
        dest="max_conditions",
        type=int,
        default=0,
        help="limit the number of conditions to show next to each hour description. defaults to 0 (shows all available)",
    )
    parser.add_argument(
        "--fahrenheit",
        "-f",
        action="store_true",
        dest="fahrenheit",
        help="use fahrenheit instead of celsius. defaults to False",
    )
    parser.add_argument(
        "--vertical-view",
        action="store_true",
        dest="vertical_view",
        help="shows the icon on the first line and temperature in a new line (doesn't work for custom-indicator). defaults to False",
    )
    parser.add_argument(
        "--format-type",
        dest="format_type",
        type=int,
        default=2,
        help="specify the global output format type (1 only text,  2 only icon/emoji, 3 text with icon/emoji). defaults to 2",
    )
    parser.add_argument(
        "--hour-text-only",
        action="store_true",
        dest="hour_text_only",
        help="show hour as text only. defaults to False",
    )
    parser.add_argument(
        "--emoji",
        action="store_true",
        dest="emoji",
        help="replace icons with emojis. defaults to False",
    )
    parser.add_argument(
        "--neutral-icon",
        action="store_true",
        dest="neutral_icon",
        help="show neutral icon instead of daytime/nighttime icons. defaults to False",
    )
    parser.add_argument(
        "--plain-text",
        action="store_true",
        dest="plain_text",
        help="shows the plain text removing all pango markup tags and json output. defaults to False",
    )
    parser.add_argument(
        "--show-temp-unit",
        action="store_true",
        dest="show_temp_unit",
        help="show temperature value with unit like 20°C or 20°F. defaults to False",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
        help="show wttrbarpy version.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        dest="debug_mode",
        help="lets not spam wttr.in :)",
    )

    args = parser.parse_args()

    api_url = "https://wttr.in/{}?format=j1".format(args.location)

    if args.debug_mode:
        api_url = "http://0.0.0.0:8000/{}.json?format=j1".format(args.location)

    try:
        with urlopen(api_url, timeout=60) as response:
            resp = response.read()
            data = loads(resp.decode())
    except HTTPError as e:
        output = {"text": "⚠️", "tooltip": str(e)}
        print_json(output)
        return

    config = build_config(data, args)
    output = {
        "text": format_text(config=config),
        "tooltip": format_tooltip(config=config),
    }

    if not config.plain_text:
        print_json(output)
    else:
        print_json(output["tooltip"])


if __name__ == "__main__":
    main()
