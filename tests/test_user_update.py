import allure
import pytest
from helpers.assertions import assert_response_status, assert_success_response, assert_error_message
from helpers.data import generate_random_email, generate_random_name, generate_random_password


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    @allure.title("Изменение данных с авторизацией")
    @pytest.mark.parametrize("field", ["name", "email", "password"])
    def test_update_user_with_auth_success(self, api_client, auth_token, field, registered_user):
        update_data = {
            "name": generate_random_name(),
            "email": generate_random_email(),
            "password": generate_random_password()
        }

        response = api_client.update_user(
            token=auth_token,
            **{field: update_data[field]}
        )

        assert_response_status(response, 200)
        assert_success_response(response)

        if field == "password":
            login_response = api_client.login_user({
                "email": registered_user["email"],
                "password": update_data["password"]
            })
            assert_response_status(login_response, 200)
            assert_success_response(login_response)
        else:
            assert response.json()["user"][field] == update_data[field]

    @allure.title("Изменение данных без авторизации")
    def test_update_user_without_auth_fail(self, api_client):
        response = api_client.update_user(
            name=generate_random_name(),
            token=None
        )

        assert_response_status(response, 401)
        assert_error_message(response, "You should be authorised")