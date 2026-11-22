"""The sites the hub manages."""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

# A site's name becomes part of a hostname and of a Kubernetes namespace, so
# it is a DNS label.

site_name = RegexValidator(
    r"^[a-z0-9]([a-z0-9-]{0,38}[a-z0-9])?$",
    "Use lower case letters, digits and hyphens, starting and ending with a letter or digit.",
)


class Site(models.Model):
    """A hosted site: one Muru daemon with the releases of one owner's application."""

    class Kind(models.TextChoices):
        """Where a site runs (specification section 15.1)."""

        LOCAL = "local", "On this machine"
        KUBERNETES = "kubernetes", "In Kubernetes"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sites",
        help_text="The account the site counts against.",
    )
    name = models.CharField(max_length=40, validators=[site_name])
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.LOCAL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("owner__username", "name")
        constraints = (
            models.UniqueConstraint(fields=("owner", "name"), name="site_unique_per_owner"),
        )

    def __str__(self) -> str:
        return self.slug

    @property
    def slug(self) -> str:
        """The site as people name it, OWNER/NAME."""

        return f"{self.owner.username}/{self.name}"
