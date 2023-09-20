from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_collection(self):
        # print('collection')
        collection_id = randint(2, 6)
        self.client.get(
            f"/store/products/?collection_id={collection_id}", name='store/products')

    @task(4)
    def view_product(self):
        # print('view Product Details')
        product_id = randint(1, 1000)
        self.client.get(
            f"/store/products/{product_id}", name='store/products/:id')

    @task(1)
    def add_to_cart(self):
        # print('add to cart')
        product_id = randint(1, 10)
        self.client.post(f'/store/carts/{self.cart_id}/items/', name='store/carts/items', json={
            'product_id': product_id,
            'quantity': 1
        })

    def on_start(self):
        # print('client browse')
        resposne = self.client.post('/store/carts/')
        result = resposne.json()
        self.cart_id = result['id']
