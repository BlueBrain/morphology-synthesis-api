from pathlib import Path
import pytest

from app.utils import load_json


DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def bio_params_file():
    return DATA_DIR / "bio_rat_L5_TPC_B_parameters.json"


@pytest.fixture(scope="session")
def bio_params(bio_params_file):
    return load_json(bio_params_file)


@pytest.fixture(scope="session")
def bio_distributions_file():
    return DATA_DIR / "bio_rat_L5_TPC_B_distribution.json"


@pytest.fixture(scope="session")
def bio_distributions(bio_distributions_file):
    return load_json(bio_distributions_file)
