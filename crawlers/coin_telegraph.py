import time
import logging
from datetime import datetime
from tempfile import mkdtemp
from selenium import webdriver
from typing import List, Any
from bs4 import BeautifulSoup
from crawlers.base import BaseCrawler
from models.documents import ArticleDocument
from selenium.webdriver.common.by import By


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CoinTelegraphCrawler(BaseCrawler):
    date_format = "%Y-%m-%d"
    url = "https://cointelegraph.com/"

    def __init__(self) -> None:
        super().__init__()
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # TODO: it breaks in headless mode. FIX

        # observe crawling behaviour?
        self.driver = webdriver.Chrome(options=options)


    def extract(
        self,
        n_scrolls,
        start_date=datetime.now().strftime(date_format),
        end_date=datetime.now().strftime(date_format),
    ) -> List[Any]:
        """Scrap news from cointelegraph"""

        self.driver.get("https://cointelegraph.com/")
        main_carousel = self.driver.find_element(
            By.XPATH, "//div[@data-testid='carousel-main']"
        )
        first_link = main_carousel.find_element(
            By.XPATH, "//a[@data-testid='main-news-controls__link']"
        )
        first_link.click()

        logger.info(f"Scraping articles from: {self.url}")
        self.__scroll_ntimes(n=n_scrolls)
        articles = []

        # Parse the page source
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Find all the 'article' elements
        article_elements = soup.find_all("article")

        # For each 'article', find the 'h1' element and all 'div' siblings
        for article in article_elements:
            h1_element = article.find("h1")
            title = h1_element.text
            summary = h1_element.find_next_sibling("div").text
            content_div = article.find("div", class_="post__content-wrapper")
            time_element = article.find("time")
            datetime = time_element.get("datetime") if time_element else None
            ps = content_div.find_all("p")
            content = " ".join(p.text for p in ps if "Advertisement" not in p.text)

            articles.append(
                ArticleDocument(
                    source="coin_telepraph",
                    title=title,
                    summary=summary,
                    content=content,
                    published_at=datetime,
                )
            )

        self.driver.close()
        filtered_articles = [
            article
            for article in articles
            if self.date_filter(article.published_at, start_date, end_date)
        ]
        return filtered_articles

    def date_filter(self, date, lower: str, upper: str):
        dt = datetime.strptime(date, self.date_format)
        lower_dt = datetime.strptime(lower, self.date_format)
        upper_dt = datetime.strptime(upper, self.date_format)
        return dt >= lower_dt and dt <= upper_dt

    def save(self, articles) -> None:
        ArticleDocument.bulk_insert(articles)

    def __scroll_ntimes(self, n=3) -> None:
        """Scroll a webpage n times

        Args:
            n (int, optional): Number of page scrolls before stop.
        """

        scrolls = 0
        while True:
            # # Scroll down the page a few times
            self.driver.execute_script("window.scrollBy(0, 2 * window.innerHeight);")

            # Wait to load page
            time.sleep(1.5)

            scrolls += 1
            if scrolls == n:
                break
