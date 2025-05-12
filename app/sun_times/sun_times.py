from typing import Dict, Tuple, Callable
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timedelta
import math
import logging

import requests
from PIL import Image, ImageDraw, ImageFont

@dataclass
class SunData():
    date: datetime
    sunrise: datetime
    sunset: datetime
    first_light: datetime
    last_light: datetime
    dawn: datetime
    dusk: datetime
    golden_hour: datetime
    day_length: int

    def __post_init__(self):
        td: timedelta = self.dusk - self.dawn
        self.light_length: int = td.seconds

class SunDisplayer():
    def __init__(self, lat, lon, now:datetime=datetime.today()):
        self.coords: Tuple[float] = (lat, lon)
        self.font = ImageFont.truetype(Path(__file__).parent / f'assets/fonts/04B_03__.TTF', size=8)

        self.today: datetime = now
        tomorrow = self.today + timedelta(days=1)
        self.todayData: SunData = getSunData(self.coords[0], self.coords[1], self.today)
        self.tomorrowData: SunData = getSunData(self.coords[0], self.coords[1], tomorrow)

        self.showSun: bool = True

    def generateImage(self) -> Image.Image:
        image: Image.Image = Image.new('RGBA', (64, 32)) # new PIL image to build on
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(image) # draw object to use for adding text

        self._drawText(draw)
        self._drawArcs(draw)
        self._drawRainbow(draw)

        if self.showSun: self._drawSun(draw)

        return image

    def reloadData(self):
        self.today = datetime.today()
        self.todayData: SunData = getSunData(self.coords[0], self.coords[1], self.today)
        tomorrow = self.today + timedelta(days=1)
        self.tomorrowData: SunData = getSunData(self.coords[0], self.coords[1], tomorrow)

    def _drawRainbow(self, draw: ImageDraw.ImageDraw):
        rainbow_colors = [
            "#FF0000",  # Red
            "#FF7F00",  # Orange
            "#FFFF00",  # Yellow
            "#00FF00",  # Green
            "#0000FF",  # Blue
            "#4B0082",  # Indigo
            "#EE82EE"   # Violet
        ]
        x = 33
        for color in rainbow_colors:
            draw.point((x, 15), fill=color)
            draw.point((x, 16), fill=color)
            # draw.point((x, 12), fill=color)
            x += 4

    def _drawText(self, draw: ImageDraw.ImageDraw):
        # -- pick the correct day to pull data from
        # - if it's after today's sunrise and before today's dusk
        if self.todayData.sunrise < self.today and self.todayData.dusk > self.today:
            topLabel: str = "Sunset"
            topTime: str = self.todayData.sunset.strftime('%H:%M')
            bottomLabel: str = "Dusk"
            bottomText: str = self.todayData.dusk.strftime('%H:%M')
        # - if it's after today's sunrise and after today's dusk
        elif self.todayData.sunrise < self.today and self.todayData.dusk < self.today:
            topLabel: str = "Dawn"
            topTime: str = self.tomorrowData.dawn.strftime('%H:%M')
            bottomLabel: str = "Sunrise"
            bottomText: str = self.tomorrowData.sunrise.strftime('%H:%M')
        # - if it's before today's sunrise and before today's dusk
        else:
            topLabel: str = "Dawn"
            topTime: str = self.todayData.dawn.strftime('%H:%M')
            bottomLabel: str = "Sunrise"
            bottomText: str = self.todayData.sunrise.strftime('%H:%M')

        draw.text((6, 13), self.today.strftime('%H:%M'), fill=None, font=self.font)
        draw.text((33, 1), topLabel, fill=None, font=self.font)
        draw.text((33, 8), topTime, fill=None, font=self.font)
        draw.text((33, 17), bottomLabel, fill=None, font=self.font)
        draw.text((33, 24), bottomText, fill=None, font=self.font)

    def _drawArcs(self, draw: ImageDraw.ImageDraw):
        arc_w: int = 2
        arc_point: Callable[[datetime], float] = lambda dt: (dt.hour + dt.minute/60) / 24 * 360 + 90
        draw.arc(((1,1),(30,30)), arc_point(self.todayData.sunset), arc_point(self.todayData.sunrise), fill='#7a7a7a', width=arc_w) # night arc
        draw.arc(((1,1),(30,30)), arc_point(self.todayData.dawn), arc_point(self.todayData.dusk), fill='#07446e', width=arc_w) # light arc
        draw.arc(((1,1),(30,30)), arc_point(self.todayData.sunrise), arc_point(self.todayData.sunset), fill='#87cfff', width=arc_w) # day arc

    def _drawSun(self, draw: ImageDraw.ImageDraw):
        midnight = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        sun_theta = (self.today - midnight).seconds / (24*60*60) * 2*math.pi
        sun_r: float = 14
        sun_x = int(16 - sun_r*math.sin(sun_theta))
        sun_y = int(16 + sun_r*math.cos(sun_theta))

        draw.point((sun_x,sun_y), fill='#ffe921')
        draw.point((sun_x+1,sun_y), fill=(255, 233, 33, 70))
        draw.point((sun_x-1,sun_y), fill=(255, 233, 33, 70))
        draw.point((sun_x,sun_y+1), fill=(255, 233, 33, 70))
        draw.point((sun_x,sun_y-1), fill=(255, 233, 33, 70))


def getSunData(lat:float, lon:float, date:datetime=datetime.today()) -> SunData:
    url: str = f"https://api.sunrisesunset.io/json?lat={lat:0.6f}&lng={lon:0.6f}&date={date.strftime('%Y-%m-%d')}"
    logging.debug(url)
    r = requests.get(url)
    if r.status_code != 200: return None
    if r.headers['content-type'] != "application/json": return None
    results: Dict[str, str] = r.json().get('results')

    data_date: datetime = datetime.strptime(results['date'], "%Y-%m-%d")
    day_len: int = int(results['day_length'].split(':')[0]) * 3600 + int(results['day_length'].split(':')[1]) * 60 + int(results['day_length'].split(':')[2])

    data = SunData(
        date=data_date,
        sunrise=datetime.strptime(f"{results['date']} {results['sunrise']}", "%Y-%m-%d %I:%M:%S %p"),
        sunset=datetime.strptime(f"{results['date']} {results['sunset']}", "%Y-%m-%d %I:%M:%S %p"),
        first_light=datetime.strptime(f"{results['date']} {results['first_light']}", "%Y-%m-%d %I:%M:%S %p"),
        last_light=datetime.strptime(f"{results['date']} {results['last_light']}", "%Y-%m-%d %I:%M:%S %p"),
        dawn=datetime.strptime(f"{results['date']} {results['dawn']}", "%Y-%m-%d %I:%M:%S %p"),
        dusk=datetime.strptime(f"{results['date']} {results['dusk']}", "%Y-%m-%d %I:%M:%S %p"),
        golden_hour=datetime.strptime(f"{results['date']} {results['golden_hour']}", "%Y-%m-%d %I:%M:%S %p"),
        day_length=day_len,)
    return data

