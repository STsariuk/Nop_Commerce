from bs4 import BeautifulSoup

from src.locustfiles.tasksets.base import BaseTaskSet


class GetCategoryPage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def get_category(self, page_url: str):
        with self.client.get(
            url=page_url,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name='/random/category/page'
        ) as response:
            self.validate_response(response)

        soup = BeautifulSoup(response.text, 'html.parser')
        sub_category = soup.find('div', class_='category-grid sub-category-grid')
        if sub_category:
            list_of_url = [a.get('href') for a in sub_category.find_all('a', href=True)]
        else:
            products = soup.select('div.product-item div.picture a')
            list_of_url = [p.get('href') for p in products]
        return list_of_url
