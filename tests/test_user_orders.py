import allure
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message


@allure.feature("Получение заказов конкретного пользователя")
class TestUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_auth_user_success(self, api_client, auth_token, valid_ingredients):
        api_client.create_order(
            ingredients=valid_ingredients,
            token=auth_token
        )

        response = api_client.get_user_orders(token=auth_token)

        assert_response_status(response, 200)
        assert_success_response(response)
        assert len(response.json()["orders"]) > 0

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauth_user_fail(self, api_client):
        response = api_client.get_user_orders(token=None)

        assert_response_status(response, 401)
        assert_error_message(response, "You should be authorised")