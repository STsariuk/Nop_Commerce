from bs4 import BeautifulSoup

from src.locustfiles.tasksets.base import BaseTaskSet


class ProductPage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def product(self, product_url: str):
        with self.client.get(
            url=product_url,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=product_url
        ) as response:
            self.validate_response(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        verification_token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
        product_id = soup.find('div', attrs={'data-productid': True}).get('data-productid')
        product_data = {
            'request_verification_token': verification_token,
            'product_id': product_id
        }
        return product_data
