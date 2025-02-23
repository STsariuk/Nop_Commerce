import logging

from bs4 import BeautifulSoup

from src.locustfiles.tasksets.base import BaseTaskSet


class CartPage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def get_cart_page(self):
        request_path = '/cart'
        with self.client.get(
            url=request_path,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=request_path
        ) as response:
            self.validate_response(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        empty_cart_message = soup.find(string='Your Shopping Cart is empty!')
        if empty_cart_message:
            logging.error("The shopping cart is empty.")
        else:
            logging.info("The shopping cart has items.")
        return
