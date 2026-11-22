"""Marking the hub's own code for tracing (specification section 14.2)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import wrapture


def observed[**P, R](**options: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Mark a function or method as an operation to trace, keeping its signature for the type check.

    This is `wrapture.observed` with its options. wrapture's own annotation
    gives a decorated method a signature that takes no arguments
    (GrahamDumpleton/wrapture#6), so the hub's code is marked through
    this instead.
    """

    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        return cast("Callable[P, R]", wrapture.observed(function, **options))

    return decorate
