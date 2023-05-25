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


def test_synthesis_with_files(synthesis_files, synthesis_overrides):
    json = {
        "files": synthesis_files.dict(),
        "overrides": synthesis_overrides.dict(),
    }
    response = client.post("/synthesis-with-files", json=json)
    assert response.status_code == 200
