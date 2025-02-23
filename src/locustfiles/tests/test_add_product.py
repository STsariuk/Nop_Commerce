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
        self.menu_items = None

    @task
    def new(self):
        self.menu_items = self.get_main_page()
        if len(self.menu_items) == 0:
            self.interrupt()
        self.random_menu_item = choice(self.menu_items)

    @task
    def open_menu_item(self):
        category = self.get_category(page_url=self.random_menu_item)
        try:
            self.random_product = choice(category)
        except IndexError:
            self.interrupt()

    @task
    def get_product(self):
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
        if len(self.product_data.get('required_name_attributes')) > 0:
            for attribute in self.product_data.get('required_name_attributes'):
                if 'Email' in attribute:
                    body[attribute] = 'Example@email.com'
                else:
                    body[attribute] = 'Patric'
                    body = {k: v for k, v in body.items() if v not in ('', 0)}
        self.add(product_id=product_id,
                 quantity=qty,
                 payload=body)

    @task
    def open_cart(self):
        self.get_cart_page()

    @task
    def stop(self):
        self.interrupt()
