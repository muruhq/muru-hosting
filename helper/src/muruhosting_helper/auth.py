"""The bearer token every call to the helper must carry."""

from __future__ import annotations

import hmac
from collections.abc import Iterable

REFUSAL = "the call carries no valid bearer token"


def authorised(metadata: Iterable[tuple[str, str | bytes]] | None, token: str) -> bool:
    """Say whether a call's metadata carries the helper's token as a bearer credential."""

    for key, value in metadata or ():
        if key.lower() != "authorization":
            continue

        text = value.decode("latin-1") if isinstance(value, bytes) else value
        scheme, _, presented = text.partition(" ")

        if scheme.lower() == "bearer" and hmac.compare_digest(
            presented.strip().encode(), token.encode()
        ):
            return True

    return False
