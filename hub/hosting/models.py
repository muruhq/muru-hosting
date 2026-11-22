"""The sites the hub manages, and the deploys it has made to them."""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

# A site's name becomes part of a hostname and of a Kubernetes namespace, so
# it is a DNS label.

site_name = RegexValidator(
    r"^[a-z0-9]([a-z0-9-]{0,38}[a-z0-9])?$",
    "Use lower case letters, digits and hyphens, starting and ending with a letter or digit.",
)

# The one application a site's daemon holds (whether a site may hold
# several is an open question of the specification).

APP = "site"


class Site(models.Model):
    """A hosted site: one Muru daemon with the releases of one owner's application."""

    class Kind(models.TextChoices):
        """Where a site runs (specification section 15.1)."""

        LOCAL = "local", "On this machine"
        KUBERNETES = "kubernetes", "In Kubernetes"

    class State(models.TextChoices):
        """How far the site has got."""

        CREATING = "creating", "Being created"
        READY = "ready", "Ready"
        FAILED = "failed", "Failed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sites",
        help_text="The account the site counts against.",
    )
    name = models.CharField(max_length=40, validators=[site_name])
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.LOCAL)
    state = models.CharField(max_length=16, choices=State.choices, default=State.CREATING)
    state_message = models.TextField(
        blank=True, help_text="Why the site failed, or what is being done to it."
    )
    url = models.URLField(blank=True, help_text="Where the site answers.")
    helper_address = models.CharField(
        max_length=255, blank=True, help_text="The site helper's address, as HOST:PORT."
    )
    helper_token = models.CharField(
        max_length=255, blank=True, help_text="The bearer token the helper asks of the hub."
    )
    site_dir = models.CharField(
        max_length=1024,
        blank=True,
        help_text="The site's directory as its daemon reads it, which holds its sources and data.",
    )
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


class Deploy(models.Model):
    """One deploy of a source to a site, and the Muru release it made.

    Muru's releases carry no commit or other word of where their code came
    from (muruhq/muru#866; #36 here), so the hub keeps that here. A deploy
    also records how far its job has got, so that a job run again goes on
    from there.
    """

    class State(models.TextChoices):
        """How far the deploy has got."""

        QUEUED = "queued", "Queued"
        UPLOADING = "uploading", "Uploading the source"
        DEPLOYING = "deploying", "Starting the release"
        SERVING = "serving", "Serving"
        FAILED = "failed", "Failed"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="deploys")
    source_name = models.CharField(
        max_length=100, help_text="The source's directory at the site, named for what it holds."
    )
    archive = models.CharField(
        max_length=255, help_text="The source archive's file in the hub's data directory."
    )
    sha256 = models.CharField(max_length=64)
    commit = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=255, blank=True)
    source_path = models.CharField(
        max_length=1024,
        blank=True,
        help_text="The source's directory as the site's daemon reads it.",
    )
    env = models.JSONField(
        default=dict, blank=True, help_text="Environment variables the hub gives the release."
    )
    release = models.CharField(max_length=32, blank=True, help_text="The Muru release, such as r2.")
    state = models.CharField(max_length=16, choices=State.choices, default=State.QUEUED)
    message = models.TextField(blank=True)
    trace_headers = models.JSONField(
        default=dict, blank=True, help_text="The trace the deploy was asked for in."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-id")

    def __str__(self) -> str:
        return f"{self.site.slug} {self.release or self.source_name}"


class AuditEntry(models.Model):
    """One action taken on a site: who took it, what it was and how it ended.

    The hub's record is the only one that names the person, since Muru's
    events name the helper's user (specification section 5.7). This is the
    start of that log: which rule admitted the person and the call's full
    arguments are still to be recorded.
    """

    class Via(models.TextChoices):
        """The way an action came."""

        PAGE = "page", "A page"
        COMMAND = "command", "A management command"

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="audit_entries")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Who took the action; nobody for one taken on the hub's own machine.",
    )
    via = models.CharField(max_length=16, choices=Via.choices)
    action = models.CharField(max_length=32, help_text="The action, such as roll-back.")
    detail = models.CharField(max_length=255, blank=True, help_text="What it was taken on.")
    succeeded = models.BooleanField(default=True)
    message = models.TextField(blank=True, help_text="What came of it, or why it failed.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-id")
        verbose_name_plural = "audit entries"

    def __str__(self) -> str:
        return f"{self.site.slug} {self.action}"
