# SPDX-License-Identifier: Apache-2.0

"""Common utilities."""
import json
import os
from pathlib import Path


def load_json(filepath: os.PathLike) -> dict:
    """Load from JSON file."""
    return json.loads(Path(filepath).read_bytes())
