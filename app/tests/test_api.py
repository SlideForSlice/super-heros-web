from wsgiref.validate import header_re

import pytest
from sqlalchemy.sql.functions import current_user

from app.users.dependencies import get_current_user


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
    def test_logout(self, ac, token, status_code, message):
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
        print(response)
        assert response.status_code == status_code_logout

    @pytest.mark.article
    def test_get_all_articles(self, ac):
        response = ac.get("/v1/article/all")

        assert response.status_code == 200
        print(response.json())

    @pytest.mark.article
    @pytest.mark.parametrize("article_name, status_code", [
        ("Spider-Man", 200),
        ("supPapi", 404)
    ])
    def test_get_article_by_name(self, ac, article_name, status_code):
        response = ac.get(f"/v1/article/{article_name}")
        assert response.status_code == status_code
        print(response.json())

    @pytest.mark.article
    @pytest.mark.parametrize("article_id, status_code", [
        (1, 200),
        (2, 200),
        (54, 404)
    ])
    def test_share_article_by_id(self, ac, article_id, status_code):
        response = ac.get(f"/v1/article/share/{article_id}")
        assert response.status_code == status_code
        print(response.json())

    @pytest.mark.article
    @pytest.mark.parametrize("article_id, status_code", [
        (1, 200),
        (2, 200),
        (54, 404)
    ])
    def test_get_author_by_id(self, ac, article_id, status_code):
        response = ac.get(f"/v1/article/author/{article_id}")
        assert response.status_code == status_code
        print(response.json())

    @pytest.mark.skip
    @pytest.mark.article
    @pytest.mark.parametrize("name_of_hero, description, powers, solo, email, password, status_code", [
        ("Chon-Huk", "Asian man", "super-mind", True, "oleg@example.com", "oleg", 200),
        ("Chon-Huk", "Asian man", "super-mind", True, "oleg@example.com", "oleg", 409)
    ])
    def test_create_article(self, ac, name_of_hero, description, powers, solo, email, password, status_code):
        login_response = ac.post("/v1/auth/login", json={
            "email": email,
            "password": password,
        })
        print(login_response.json())
        assert login_response.status_code == 200

        token = login_response.cookies.get("user_access_token")
        headers = {"Authorization": "Bearer " + token}
        create_article_response = ac.post("/v1/article/create",
                           params={
                               "name_of_hero": name_of_hero,
                               "description": description,
                               "powers": powers,
                               "solo": solo
                           }, headers=headers)
        print(create_article_response.json())
        assert create_article_response.status_code == status_code

    @pytest.mark.article
    @pytest.mark.parametrize("article_id, new_desc , status_code", [
        (1, "new_desc", 200),
        (1, "new_desc_2", 200),
        (1, "new_desc_3", 200),
        (54, "new_desc", 409)
    ])
    def test_edit_article_desc_by_id(self, ac, article_id, new_desc, status_code):
        params = {"new_description": new_desc}
        response = ac.patch(f"/v1/article/edit_article/{article_id}", params=params)
        print(response.json())
        assert response.status_code == status_code

