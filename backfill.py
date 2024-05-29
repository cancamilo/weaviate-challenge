import json
import asyncio
import logging
import pandas as pd
from typing import Any
from datetime import datetime, timedelta
from crawlers import CoinTelegraphCrawler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

date_format="%Y-%m-%d"
coin_crawler = CoinTelegraphCrawler()


def backfill():
    """ Extract past articles by scrolling multiple times 
    """
    start_dt = datetime.now() - timedelta(days=200)
    end_dt = datetime.now()
    ct_articles = coin_crawler.extract(
        n_scrolls=100, 
        start_date=start_dt.strftime(date_format),
        end_date=end_dt.strftime(date_format)
    )
    save_as_df(ct_articles)
    return ct_articles

def daily():
    """ Extract articles for the current date only
    """
    ct_articles = coin_crawler.extract(n_scrolls=10)
    save_as_df(ct_articles)
    return ct_articles

def save_as_df(articles):
    df = pd.DataFrame.from_records([article.model_dump() for article in articles])
    df.to_csv("data/articles_1.csv", index=False)

if __name__ == "__main__":
    try:
        backfill()
    except Exception as e:
        print("Unable to extract articles", e)

