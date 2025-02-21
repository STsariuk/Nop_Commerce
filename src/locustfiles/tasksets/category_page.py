from bs4 import BeautifulSoup

from src.locustfiles.tasksets.base import BaseTaskSet
from src.locustfiles.tasksets.main_page import HomePage


class GetCategoryPage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def get_category(self, page_url: str):
        with self.client.get(
            url=page_url,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=page_url
        ) as response:
            self.validate_response(response)

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select('div.product-item div.picture a')
        products_links = [p.get('href') for p in products]
        return products_links
