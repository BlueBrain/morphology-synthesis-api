import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

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


def test_synthesize(bio_params_file, bio_distributions_file):
    response = client.post(
        "/synthesize",
        json={
            "parameters_file": str(bio_params_file),
            "distributions_file": str(bio_distributions_file),
            "total_extent": 100.0,
            "randomness": 0.001,
            "orientation": (0.0, 0.0, 1.0),
            "step_size": 1.0,
            "radius": 0.5,
        },
    )
    assert response.status_code == 200
