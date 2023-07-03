import io
import json
import base64
import shutil
from pathlib import Path
import PIL
from unittest.mock import patch

import pytest
import pylab as plt
from fastapi.testclient import TestClient

from app import schemas
import app.main as test_module

client = TestClient(test_module.app)


def test_root_get(monkeypatch):
    project_path = "project/sbo/sonata-cell-position"
    monkeypatch.setattr(test_module, "PROJECT_PATH", project_path)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"project": project_path, "status": "OK"}


def test_version_get(monkeypatch):
    project_path = "project/sbo/sonata-cell-position"
    commit_sha = "12345678"
    monkeypatch.setattr(test_module, "PROJECT_PATH", project_path)
    monkeypatch.setattr(test_module, "COMMIT_SHA", commit_sha)

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"project": project_path, "commit_sha": commit_sha}


def _check_payload_valid_figures(response):
    payload = response.json()

    assert isinstance(payload, dict)

    for name, data in payload.items():
        img_bytes = base64.b64decode(data)
        img = PIL.Image.open(io.BytesIO(img_bytes))


def test_synthesis_with_files(synthesis_files, synthesis_overrides):
    inputs = schemas.FileInputs(
        files=synthesis_files,
        overrides=synthesis_overrides,
    )

    response = client.post("/synthesis-with-files", data=inputs.json())
    assert response.status_code == 200
    _check_payload_valid_figures(response)


def test_synthesis_with_resources(
    synthesis_resources, synthesis_overrides, synthesis_datasets, nexus_config
):
    inputs = schemas.ResourceInputs(
        resources=synthesis_resources,
        overrides=synthesis_overrides,
    )

    with patch("app.service.fetch_synthesis_datasets", return_value=synthesis_datasets) as patched:
        response = client.post(
            "/synthesis-with-resources", data=inputs.json(), headers={"nexus-token": "my-token"}
        )

        patched.assert_called_once_with(
            resources=inputs.resources, nexus_config=nexus_config, nexus_token="my-token"
        )

    assert response.status_code == 200
    _check_payload_valid_figures(response)
