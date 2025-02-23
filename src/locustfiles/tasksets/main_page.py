
from bs4 import BeautifulSoup

from src.locustfiles.tasksets.base import BaseTaskSet


class HomePage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def get_main_page(self):
        request_path = '/'
        list_of_categories = []

        with self.client.get(
            url=request_path,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=request_path
        ) as response:
            self.validate_response(response)

        soup = BeautifulSoup(response.text, 'lxml')
        menu = soup.find('ul', class_='top-menu notmobile')
        links = menu.find_all('a', href=True)
        all_menu_links = [item.attrs.get('href') for item in links if item.attrs.get('href') not in ('/computers', '/electronics', '/apparel')]
        return all_menu_links
