from unittest.mock import patch

from app import nexus as test_module
from app.constants import NEXUS_ENDPOINT, NEXUS_BUCKET

import pytest


def test_get_resource_id(nexus_config):
    with patch("app.nexus.load_by_url", side_effect=lambda url, token: (url, token)):
        res = test_module.get_resource_json_ld("my-resource", nexus_config, nexus_token="foo")

        expected_url = f"{NEXUS_ENDPOINT}/resolvers/{NEXUS_BUCKET}/_/my-resource"

        assert res[0] == expected_url
        assert res[1] == "foo"


def test_load_json_file__raise_if_no_distribution():
    mock_json = {
        "@id": "my-resource",
    }
    with pytest.raises(RuntimeError, match="No distribution found in my-resource"):
        test_module.load_json_distribution_file(mock_json, None)


def test_load_json_file__use_atLocation_if_available():
    mock_json = {
        "@id": "my-resource",
        "distribution": {"atLocation": {"location": "file://path"}, "contentUrl": "my-url"},
    }
    with patch("app.nexus.load_json", side_effect=lambda x: x):
        res = test_module.load_json_distribution_file(mock_json, None)
        assert res == "path"


def test_load_json_file__use_contentUrl_if_no_atLocation():
    mock_json = {
        "@id": "my-resource",
        "distribution": {"contentUrl": "my-url"},
    }
    with patch("app.nexus.file_as_dict", side_effect=lambda x, token: x):
        res = test_module.load_json_distribution_file(mock_json, None)
        assert res == "my-url"


def test_load_json_file__use_contentUrl_if_PermissionError():
    def raise_permission_error(x):
        raise PermissionError()

    mock_json = {
        "@id": "my-resource",
        "distribution": {"atLocation": {"location": "file://path"}, "contentUrl": "my-url"},
    }

    with (
        patch("app.nexus.load_json", side_effect=raise_permission_error),
        patch("app.nexus.file_as_dict", side_effect=lambda x, token: x),
    ):
        res = test_module.load_json_distribution_file(mock_json, None)
        assert res == "my-url"


def test_load_json_file__use_contentUrl_if_FileNotFoundError():
    def raise_filenotfound_error(x):
        raise FileNotFoundError()

    mock_json = {
        "@id": "my-resource",
        "distribution": {"atLocation": {"location": "file://path"}, "contentUrl": "my-url"},
    }

    with (
        patch("app.nexus.load_json", side_effect=raise_filenotfound_error),
        patch("app.nexus.file_as_dict", side_effect=lambda x, token: x),
    ):
        res = test_module.load_json_distribution_file(mock_json, None)
        assert res == "my-url"


def test_load_json_file__raise_for_other_errors():
    def raise_other_error(x):
        raise ValueError()

    mock_json = {
        "@id": "my-resource",
        "distribution": {"atLocation": {"location": "file://path"}, "contentUrl": "my-url"},
    }

    with pytest.raises(ValueError):
        with (
            patch("app.nexus.load_json", side_effect=raise_other_error),
            patch("app.nexus.file_as_dict", side_effect=lambda x, token: x),
        ):
            res = test_module.load_json_distribution_file(mock_json, None)
            assert res == "my-url"
