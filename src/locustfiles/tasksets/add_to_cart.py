import json
import logging

from src.locustfiles.tasksets.base import BaseTaskSet


class MakePurchase(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def add(self, product_id: str, quantity: int, payload: dict):
        request_path = '/addproducttocart/details/{product_id}/{quantity}'
        with self.client.post(
            url=request_path.format(product_id=product_id, quantity=quantity),
            data=payload,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=request_path
        ) as response:
            self.validate_response(response)
        try:
            response_data = response.json()
            if response_data.get('success') is True:
                logging.info('The product has been added to your shopping cart.')
            else:
                response.failure('Product not added!')
        except ValueError:
            logging.error('Failed to parse response as JSON.')
        return
