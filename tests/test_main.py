import io
import json
import base64
import shutil
from pathlib import Path
import PIL

import pytest
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


@pytest.fixture
def synthesis_inputs(synthesis_files, synthesis_overrides):
    return schemas.SynthesisWithFilesInputs(
        files=synthesis_files,
        overrides=synthesis_overrides,
    )


import pylab as plt


def test_synthesis_with_files(synthesis_inputs):
    response = client.post("/synthesis-with-files", data=synthesis_inputs.json())
    assert response.status_code == 200

    payload = json.loads(response.content)

    assert isinstance(payload, dict)

    for name, data in payload.items():
        img_bytes = base64.b64decode(data)
        img = PIL.Image.open(io.BytesIO(img_bytes))
