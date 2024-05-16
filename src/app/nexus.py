# SPDX-License-Identifier: Apache-2.0

"""Nexus related functions."""

import logging

from entity_management.nexus import file_as_dict, load_by_id

from app.schemas import NexusConfig
from app.utils import load_json

L = logging.getLogger(__name__)


def get_resource_json_ld(resource_id: str, nexus_config: NexusConfig, nexus_token: str) -> dict:
    """Get Nexus resource as a json-ld dictionary.

    Args:
        resource_id: The resource id.
        nexus_config: The NexusConfig containing the Nexus endpoint and bucket.
        nexus_token: The Nexus authentication token.

    Returns:
        The json-ld dictionary of the Nexus resource.
    """
    return load_by_id(
        resource_id=resource_id,
        cross_bucket=True,
        base=nexus_config.endpoint,
        org=nexus_config.org,
        proj=nexus_config.project,
        token=nexus_token,
    )


def load_json_distribution_file(resource: dict, nexus_token: str) -> dict:
    """Load json file from the resource's distribution.

    Args:
        resource: A json-ld dictionary of the Nexus resource.
        nexus_token: Nexus authentication token.

    Returns:
        The loaded json file data.
    """
    try:
        distribution = resource["distribution"]
    except KeyError as e:
        raise RuntimeError(f"No distribution found in {resource['@id']}") from e

    try:
        gpfs_location = distribution["atLocation"]["location"].removeprefix("file://")
        return load_json(gpfs_location)
    except KeyError:
        L.info(
            "No gpfs atLocation found for %s. Resource will be downloaded from Nexus.",
            resource["@id"],
        )
    except PermissionError:
        L.info(
            "No permission to access gpfs location %s. Resource will be downloaded from Nexus.",
            gpfs_location,
        )
    except FileNotFoundError:
        L.info(
            "File path %s was not found. Resource will be downloaded from Nexus.",
            gpfs_location,
        )

    json_data = file_as_dict(distribution["contentUrl"], token=nexus_token)

    return json_data
