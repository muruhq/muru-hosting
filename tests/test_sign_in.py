"""Signing in with local accounts, and what a hub set to GitHub says."""

import importlib
from collections.abc import Iterator

import pytest
from django.test import Client
from django.urls import clear_url_caches
from pytest_django.fixtures import Settings

import hub.urls
from hub.accounts.models import User

NOTICE = "This hub uses local accounts"


@pytest.mark.django_db
def test_a_page_sends_someone_not_signed_in_to_the_sign_in_page(client: Client) -> None:
    response = client.get("/")

    assert response.status_code == 302
    assert response["Location"] == "/sign-in/?next=/"


def test_a_local_account_signs_in_and_out(client: Client, member: User) -> None:
    response = client.post(
        "/sign-in/", {"username": "alice", "password": "correct horse", "next": "/"}
    )

    assert response.status_code == 302
    assert response["Location"] == "/"
    assert client.get("/").status_code == 200

    client.post("/sign-out/")

    assert client.get("/").status_code == 302


def test_a_wrong_password_is_refused(client: Client, member: User) -> None:
    response = client.post("/sign-in/", {"username": "alice", "password": "wrong"})

    assert response.status_code == 200
    assert "do not match an account" in response.text


def test_every_page_says_the_hub_uses_local_accounts(client: Client, member: User) -> None:
    assert NOTICE in client.get("/sign-in/").text

    client.force_login(member)

    assert NOTICE in client.get("/").text


@pytest.mark.django_db
def test_the_admin_site_is_on_with_local_sign_in(client: Client) -> None:
    assert client.get("/admin/login/").status_code == 200


@pytest.fixture
def development_run(settings: Settings) -> Iterator[None]:
    """Turn Django's debug mode on, with the hub's URLs made again to match."""

    settings.DEBUG = True
    importlib.reload(hub.urls)
    clear_url_caches()

    yield None

    settings.DEBUG = False
    importlib.reload(hub.urls)
    clear_url_caches()


def test_a_development_run_serves_the_stylesheet_to_someone_not_signed_in(
    client: Client, development_run: None
) -> None:
    response = client.get("/static/hub/hub.css")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/css")


@pytest.fixture
def github_sign_in(settings: Settings) -> Iterator[None]:
    """Set the hub to sign people in with GitHub, with its URLs made again to match."""

    settings.HUB_SIGN_IN = "github"
    settings.HUB_ADMIN_SITE = False
    importlib.reload(hub.urls)
    clear_url_caches()

    yield None

    settings.HUB_SIGN_IN = "local"
    settings.HUB_ADMIN_SITE = True
    importlib.reload(hub.urls)
    clear_url_caches()


@pytest.mark.django_db
def test_github_sign_in_without_an_app_says_nobody_can_sign_in(
    client: Client, github_sign_in: None
) -> None:
    response = client.get("/sign-in/")

    assert response.status_code == 503
    assert "no GitHub App configured" in response.text
    assert NOTICE not in response.text


def test_github_sign_in_takes_no_password(
    client: Client, member: User, github_sign_in: None
) -> None:
    response = client.post("/sign-in/", {"username": "alice", "password": "correct horse"})

    assert response.status_code == 503
    assert client.get("/").status_code == 302


@pytest.mark.django_db
def test_the_admin_site_is_off_with_github_sign_in(client: Client, github_sign_in: None) -> None:
    assert client.get("/admin/login/").status_code == 404
