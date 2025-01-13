import pytest


class TestApi:

    @pytest.mark.user
    @pytest.mark.parametrize("email, password, status_code", [
        ("kot@pes.com", "ochko", 200),
        ("kot@pes.com", "ochko", 409),
        ("test@gmail.com", "salma", 200),
        ('dsad', "dsa", 422)
    ])
    def test_register(self, ac, email, password, status_code):
        response = ac.post("/v1/auth/register", json={
            "email": email,
            "password": password,
        })
        assert response.status_code == status_code
        print(response.json())

    @pytest.mark.user
    @pytest.mark.parametrize("email, password, status_code", [
        ("oleg@example.com", "oleg", 200),
        ("oleg@example.com", "test", 401),
        ("koetus@example.com", "solda", 401),
        ("asd", "dsa", 422)
    ])
    def test_login(self, ac, email, password, status_code):
        response = ac.post("/v1/auth/login", json={
            "email": email,
            "password": password,
        })

        assert response.status_code == status_code
        print(response.json())

    @pytest.mark.user
    @pytest.mark.parametrize("token, status_code, message", [
        (
                "valid_token", 200,
                {"message": "Logged out successfully"}
        )
    ])
    def test_logout_scenarios(self, ac, token, status_code, message):
        if token:
            ac.cookies.set("user_access_token", token)

        response = ac.post("/v1/auth/logout", json={})

        assert response.status_code == status_code
        assert response.json() == message

    @pytest.mark.user
    @pytest.mark.parametrize("email, password, status_code_login, status_code_logout", [
        ("oleg@example.com", "oleg", 200, 200)
    ])
    def test_me(self, ac, email, password, status_code_login, status_code_logout):
        login_response = ac.post("/v1/auth/login", json={
            "email": email,
            "password": password,
        })
        print(login_response.json())

        assert login_response.status_code == status_code_login

        token = login_response.cookies.get("user_access_token")

        headers = {"Authorization": "Bearer " + token}
        response = ac.get("/v1/auth/me", headers=headers)
        assert response.status_code == status_code_logout
