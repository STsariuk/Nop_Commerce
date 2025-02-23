from locust import task
import logging
from random import choice

from src.locustfiles.tasksets.main_page import HomePage
from src.locustfiles.tasksets.category_page import GetCategoryPage
from src.locustfiles.tasksets.product_page import ProductPage
from src.locustfiles.tasksets.add_to_cart import MakePurchase
from src.locustfiles.tasksets.cart_page import CartPage


class UserPurchase(CartPage, HomePage, GetCategoryPage, ProductPage, MakePurchase):

    def __init__(self, parent):
        super().__init__(parent)
        self.random_menu_item = None
        self.random_product = None
        self.product_data = None

    @task
    def new(self):
        menu_items = self.get_main_page()
        if len(menu_items) == 0:
            self.interrupt()
        self.random_menu_item = choice(menu_items)

    @task
    def open_menu_item(self):
        category = self.get_category(page_url=self.random_menu_item)
        self.random_product = choice(category)
        # self.random_product = '/nikon-d5500-dslr'
        # self.random_product = '/portable-sound-speakers'
        # self.random_product = '/nike-floral-roshe-customized-running-shoes'

    @task
    def get_product(self):
        logging.info(f'PRODUCT_URL {self.random_product}')
        self.product_data = self.product(product_url=self.random_product)

    @task
    def add_product_to_cart(self):
        product_id = choice(self.product_data.get("product_ids"))
        qty = choice(range(1, 5))
        body = {
            f'addtocart_{product_id}.EnteredQuantity': qty,
            'CountryId': 0,
            'StateProvinceId': 0,
            'ZipPostalCode': '',
            '__RequestVerificationToken': self.product_data.get('request_verification_token')
        }
        if len(self.product_data.get('product_attributes')) > 0:
            for attribute in self.product_data.get('product_attributes'):
                body[f'product_attribute_{attribute.get("attribute_id")}'] = choice(attribute.get('attr_options'))
        self.add(product_id=product_id,
                 quantity=qty,
                 payload=body)

    @task
    def open_cart(self):
        self.get_cart_page()
