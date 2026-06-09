#!/usr/bin/env python3
import time
import datetime
import sys
import argparse
import logging
from traceback import format_exception

from sun_times import SunDisplayer


def run():
    displayer = SunDisplayer(34.110856, -118.272459)
    last_today_update = time.time()
    out = sys.stdout.buffer

    while True:
        if time.time() - last_today_update > 10:
            displayer.today = datetime.datetime.today()
            last_today_update = time.time()

        if displayer.todayData.date.day != displayer.today.day:
            displayer.reloadData()

        displayer.showSun = int(time.time() * 1.5) % 2 != 0

        image = displayer.generateImage().convert('RGB')
        out.write(image.tobytes('raw', 'RGB'))
        out.flush()
        image.close()

        time.sleep(0.005)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    try:
        run()
    except BrokenPipeError:
        pass
    except Exception as ex:
        if args.debug:
            raise
        logging.error(''.join(format_exception(None, ex, ex.__traceback__)))
