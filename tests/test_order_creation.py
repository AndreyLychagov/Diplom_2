import allure
import pytest
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией и валидными ингридиентами")
    def test_create_order_auth_valid_ingredients_success(
            self, api_client, auth_token, valid_ingredients
    ):
        response = api_client.create_order(
            ingredients=valid_ingredients,
            token=auth_token
        )

        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации и с валидными ингридиентами")
    def test_create_order_no_auth_valid_ingredients_success(
            self, api_client, valid_ingredients
    ):
        response = api_client.create_order(
            ingredients=valid_ingredients,
            token=None
        )

        assert_response_status(response, 200)
        assert_success_response(response)
        assert "order" in response.json()

    @allure.title("Создание заказа без ингридиентов")
    @pytest.mark.parametrize("auth_token", [pytest.param(True, id="with_auth"),
                                            pytest.param(None, id="without_auth")])
    def test_create_order_missing_ingredients_fail(
            self, api_client, auth_token, registered_user
    ):
        token = auth_token if isinstance(auth_token, str) else None
        response = api_client.create_order(
            ingredients=[],
            token=token
        )

        assert_response_status(response, 400)
        assert_error_message(response, "Ingredient ids must be provided")

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @pytest.mark.parametrize("auth_token", [pytest.param(True, id="with_auth"),
                                            pytest.param(None, id="without_auth")])
    def test_create_order_invalid_hash_fail(
            self, api_client, auth_token, registered_user
    ):
        token = auth_token if isinstance(auth_token, str) else None
        response = api_client.create_order(
            ingredients=["invalid_hash_1", "invalid_hash_2"],
            token=token
        )

        assert_response_status(response, 500)