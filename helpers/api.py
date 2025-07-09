import requests


class StellarBurgersAPI:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    def create_user(self, user_data):
        url = f"{self.BASE_URL}/auth/register"
        return requests.post(url, json=user_data)

    def login_user(self, credentials):
        url = f"{self.BASE_URL}/auth/login"
        return requests.post(url, json=credentials)

    def update_user(self, token, name=None, email=None, password=None):
        url = f"{self.BASE_URL}/auth/user"
        headers = {"Authorization": token}
        payload = {}
        if name: payload["name"] = name
        if email: payload["email"] = email
        if password: payload["password"] = password
        return requests.patch(url, json=payload, headers=headers)

    def create_order(self, ingredients, token=None):
        url = f"{self.BASE_URL}/orders"
        headers = {"Authorization": token} if token else {}
        payload = {"ingredients": ingredients}
        return requests.post(url, json=payload, headers=headers)

    def get_user_orders(self, token):
        url = f"{self.BASE_URL}/orders"
        headers = {"Authorization": token}
        return requests.get(url, headers=headers)

    def get_ingredients(self):
        url = f"{self.BASE_URL}/ingredients"
        return requests.get(url)