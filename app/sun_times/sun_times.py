from typing import Dict, Tuple
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

class SunDisplayer():
    def __init__(self, lat, lon):
        self.coords: Tuple[float] = (lat, lon)
        self.font = ImageFont.truetype(Path(__file__).parent / f'assets/fonts/04B_03__.TTF', size=8)

        self.today: datetime = datetime.today()
        tomorrow = self.today + timedelta(days=1)
        self.todayData: SunData = getSunData(self.coords[0], self.coords[1])
        self.tomorrowData: SunData = getSunData(self.coords[0], self.coords[1], tomorrow)

        self.showSun: bool = True

    def generateImage(self) -> Image.Image:
        image: Image.Image = Image.new('RGBA', (64, 32)) # new PIL image to build on
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(image) # draw object to use for adding text
        
        self._drawText(draw)
        self._drawArcs(draw)
        if self.showSun: self._drawSun(draw)

        return image

    def reloadData(self):
        self.today = datetime.today()
        self.todayData: SunData = getSunData(self.coords[0], self.coords[1])
        tomorrow = self.today + timedelta(days=1)
        self.tomorrowData: SunData = getSunData(self.coords[0], self.coords[1], tomorrow)

    def _drawText(self, draw: ImageDraw.ImageDraw):
        if self.todayData.sunrise < self.today:
            eventLabel: str = "Sunset"
            eventTime: str = self.todayData.sunset.strftime('%H:%M')
            # bottomLabel: str = "Sunrise"
            # bottomText: str = self.tomorrowData.sunrise.strftime('%H:%M')
        else:
            eventLabel: str = "Sunrise"
            eventTime: str = self.todayData.sunrise.strftime('%H:%M')
            # bottomLabel: str = "Sunset"
            # bottomText: str = self.todayData.sunset.strftime('%H:%M')

        draw.text((33, 1), self.today.strftime('%H:%M'), fill=None, font=self.font)
        draw.text((33, 17), eventLabel, fill=None, font=self.font)
        draw.text((33, 24), eventTime, fill=None, font=self.font)
        # draw.text((33, 17), bottomLabel, fill=None, font=self.font)
        # draw.text((33, 24), bottomText, fill=None, font=self.font)

    def _drawArcs(self, draw: ImageDraw.ImageDraw):
        day_arc = self.todayData.day_length / (24*60*60) * 360
        day_arc_offset = (180-day_arc)/2
        draw.arc(((1,1),(30,30)), day_arc_offset-180, -day_arc_offset, fill='#57b9fa', width=2)
        draw.arc(((1,1),(30,30)), -day_arc_offset, day_arc_offset-180, fill='#7a7a7a', width=2)

    def _drawSun(self, draw: ImageDraw.ImageDraw):
        midnight = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
        sun_theta = (self.today - midnight).seconds / (24*60*60) * 2*math.pi
        sun_x = int(16 - 14*math.sin(sun_theta))
        sun_y = int(16 + 14*math.cos(sun_theta))

        draw.point((sun_x,sun_y), fill='#ffe921')
        draw.point((sun_x+1,sun_y), fill=(255, 233, 33, 70))
        draw.point((sun_x-1,sun_y), fill=(255, 233, 33, 70))
        draw.point((sun_x,sun_y+1), fill=(255, 233, 33, 70))
        draw.point((sun_x,sun_y-1), fill=(255, 233, 33, 70))


def getSunData(lat:float, lon:float, date:datetime=datetime.today()) -> SunData:
    url: str = f"https://api.sunrisesunset.io/json?lat={lat:0.6f}&lng={lon:0.6f}&date={date.strftime('%Y-%m-%d')}"
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

