"""Generated gRPC stubs for Muru's admin API and the site helper's own service.

`muruhosting_stubs.muru.admin.v1` holds `muru.admin.v1`, from the `.proto`
file of the Muru release that `MURU_VERSION` names, and
`muruhosting_stubs.muruhosting.site.v1` the helper's Sources service. The
modules sit beneath this package, not at the top level, so that they never
meet Muru's own `muru` package in a worker.
"""

from pathlib import Path

MURU_VERSION: str = (Path(__file__).parent / "MURU_VERSION").read_text().strip()
"""The Muru release the admin API's stubs were generated from."""
