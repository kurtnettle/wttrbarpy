from argparse import Namespace
from dataclasses import dataclass


@dataclass
class Emoji:
    enabled: bool


@dataclass
class Config:
    data: dict
    unit: str
    ampm: bool
    main_indicator: str
    custom_indicator: str
    format_type: int
    hour_text_only: bool
    plain_text: bool
    hide_wind_details: bool
    hide_conditions: bool
    show_temp_unit: bool
    max_conditions: int
    vertical_view: bool
    date_format: str
    emoji: Emoji
    neutral_icon: bool


def build_config(data: dict, args: Namespace) -> Config:
    return Config(
        data=data,
        unit="USCS" if args.fahrenheit or (args.main_indicator == "temp_F") else "SI",
        ampm=args.ampm,
        main_indicator=args.main_indicator,
        custom_indicator=args.custom_indicator,
        format_type=args.format_type,
        hour_text_only=args.hour_text_only,
        plain_text=args.plain_text,
        hide_wind_details=args.hide_wind_details,
        hide_conditions=args.hide_conditions,
        show_temp_unit=args.show_temp_unit,
        max_conditions=args.max_conditions,
        vertical_view=args.vertical_view,
        date_format=args.date_format,
        emoji=Emoji(enabled=args.emoji),
        neutral_icon=args.neutral_icon,
    )
