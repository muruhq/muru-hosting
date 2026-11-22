"""Which sites a person sees."""

from django.test import Client
from wrapture import Tape

from hub.accounts.models import User
from hub.hosting import services
from hub.hosting.models import Site


def test_a_member_sees_only_the_sites_they_own(member: User, admin: User) -> None:
    mine = Site.objects.create(owner=member, name="blog")
    Site.objects.create(owner=admin, name="status")

    assert list(services.sites_visible_to(member)) == [mine]


def test_a_platform_admin_sees_every_site(member: User, admin: User) -> None:
    Site.objects.create(owner=member, name="blog")
    Site.objects.create(owner=admin, name="status")

    assert [site.slug for site in services.sites_visible_to(admin)] == ["alice/blog", "root/status"]


def test_the_home_page_lists_the_sites_through_the_service(
    client: Client, member: User, tape: Tape
) -> None:
    Site.objects.create(owner=member, name="blog")
    client.force_login(member)

    response = client.get("/")

    assert '<a href="/sites/alice/blog/">blog</a>' in response.text
    tape.where(label="sites.visible_to").assert_once()


def test_the_home_page_says_when_there_are_no_sites(client: Client, member: User) -> None:
    client.force_login(member)

    assert "You have no sites." in client.get("/").text
