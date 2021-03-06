#! /usr/bin/env python3

from bot import Bot
from db import DB
from cian import Cian
from config import CIAN_URLS
from distance import Distance
import re

if __name__ == '__main__':
    for url in CIAN_URLS:
        cian = Cian(url)
        ads = cian.get_ads()
        db = DB()
        for ad in ads:
            _, created = db.get_or_create(ad)
            if created:
                walk = Distance.calc(ad.address)
                matches = re.search('([0-9.]+)', ad.price)
                priceForMonth = matches.group()
                restOfPrice = matches.group() + ad.price[matches.end():]
                message = '%s, %s, %s, %s\n%s' % (
                    '<b>%s от офиса</b> ' % walk['text'] if walk['value'] else ' ',
                    ad.address,
                    '<b>%s</b>' % priceForMonth,
                    restOfPrice,
                    ad.url
                )
                Bot.notify(message)
        db.conn.close()
