from pathlib import Path
import morphio
import pytest
import tmd.io

from app.utils import load_json
from app import schemas


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


@pytest.fixture
def synthesis_files(bio_params_file, bio_distributions_file):
    return schemas.SynthesisFiles(
        parameters_file=str(bio_params_file), distributions_file=str(bio_distributions_file)
    )


@pytest.fixture
def synthesis_overrides():
    return schemas.SynthesisOverrides(
        total_extent=100.0,
        randomness=0.001,
        orientation=(0.0, 0.0, 1.0),
        step_size=1.0,
        radius=0.5,
    )


@pytest.fixture(scope="session")
def morphology_file():
    return DATA_DIR / "bio_rat_L5_TPC_B.h5"


@pytest.fixture(scope="session")
def morphology(morphology_file):
    return tmd.io.load_neuron_from_morphio(str(morphology_file))
