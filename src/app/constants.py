# SPDX-License-Identifier: Apache-2.0

"""Common constants."""
import os

ORIGINS = [
    "http://localhost:3000",
    "https://bbp.epfl.ch",
    "https://sonata.sbo.kcp.bbp.epfl.ch",
    "https://core-web-app-dev.sbo.kcp.bbp.epfl.ch",
    "https://bbpteam.epfl.ch",
]

PROJECT_PATH = os.environ.get("PROJECT_PATH")
COMMIT_SHA = os.environ.get("COMMIT_SHA")
DEBUG = os.environ.get("DEBUG", "").lower() == "true"
LOGGING_CONFIG = os.environ.get("LOGGING_CONFIG", "logging.yaml")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")


NEXUS_ENDPOINT = "https://bbp.epfl.ch/nexus/v1"
NEXUS_BUCKET = "bbp/mmb-point-neuron-framework-model"
