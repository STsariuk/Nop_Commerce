import logging

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
        product_attributes = []
        required_name_attributes = []
        attributes = soup.find_all('dt', id=lambda x: x and x.startswith('product_attribute_label_'))
        if attributes:
            for attribute in attributes:
                attribute_id = attribute['id'].split('_')[-1]
                input_element = soup.find('dd', id=f'product_attribute_input_{attribute_id}')

                if input_element:
                    select = input_element.find('select')
                    if select:
                        options = [option.get('value') for option in select.find_all('option') if option.get('value') != '0']
                        product_attributes.append({
                            'attribute_id': attribute_id,
                            'attr_options': options
                        })

                    else:
                        ul = input_element.find('ul')
                        if ul:
                            item_values = [item.get('data-attr-value') for item in ul.find_all('li')]
                            product_attributes.append({
                                'attribute_id': attribute_id,
                                'attr_options': item_values
                            })
        else:
            giftcard_div = soup.find('div', class_='giftcard')
            if giftcard_div:
                div_elements = giftcard_div.find_all('div')
                for div in div_elements:
                    if div.find('span', class_='required'):
                        input_element = div.find(['input', 'textarea'])
                        if input_element and input_element.has_attr('name'):
                            required_name_attributes.append(input_element['name'])
        available_products = soup.find_all('button', class_='add-to-cart-button')
        product_ids = [product.get('data-productid') for product in available_products]
        verification_token = soup.find('input', {'name': '__RequestVerificationToken'}).get('value')
        product_data = {
            'request_verification_token': verification_token,
            'product_ids': product_ids,
            'product_attributes': product_attributes,
            'required_name_attributes': required_name_attributes
        }
        return product_data
