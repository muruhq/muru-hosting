"""The hub's actions on sites.

Pages, and later the Actions API and the MCP server, all act through this
module, so that who may do what is decided in one place (specification
sections 5.4 and 10.1) and every action is traced the same way (section
14.2).
"""

import wrapture
from django.db.models import QuerySet

from hub.accounts.models import User
from hub.hosting.models import Site


@wrapture.observed(label="sites.visible_to")
def sites_visible_to(user: User) -> QuerySet[Site]:
    """List the sites a person may see: every site for a platform admin, else their own."""

    sites = Site.objects.select_related("owner")

    if user.is_platform_admin:
        return sites

    return sites.filter(owner=user)
