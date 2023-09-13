from pathlib import Path
import os
import morphio
import pytest
import tmd.io

from app.utils import load_json
from app import schemas
from app.constants import NEXUS_ENDPOINT, NEXUS_BUCKET

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def nexus_config():
    return schemas.NexusConfig(endpoint=NEXUS_ENDPOINT, bucket=NEXUS_BUCKET)


@pytest.fixture(scope="session")
def nexus_token():
    return os.getenv("NEXUS_TOKEN")


@pytest.fixture(scope="session")
def params_file():
    return DATA_DIR / "params_L5_TPC:B.json"


@pytest.fixture(scope="session")
def params(params_file):
    return load_json(params_file)


@pytest.fixture(scope="session")
def distributions_file():
    return DATA_DIR / "distr_L5_TPC:B.json"


@pytest.fixture(scope="session")
def distributions(distributions_file):
    return load_json(distributions_file)


@pytest.fixture
def synthesis_files(params_file, distributions_file):
    return schemas.SynthesisFiles(
        parameters_file=str(params_file), distributions_file=str(distributions_file)
    )


@pytest.fixture(scope="session")
def params_id():
    return "https://bbp.epfl.ch/neurosciencegraph/data/16d47353-41e9-483d-90b8-522e430f4278"


@pytest.fixture(scope="session")
def distributions_id():
    return "https://bbp.epfl.ch/neurosciencegraph/data/8391281e-9cbf-4424-a41b-d31774475753"


@pytest.fixture
def synthesis_resources(params_id, distributions_id):
    return schemas.SynthesisResources(
        parameters_id=params_id,
        distributions_id=distributions_id,
    )


@pytest.fixture
def synthesis_datasets(params_file, distributions_file):
    return schemas.SynthesisDatasets(
        parameters=load_json(params_file),
        distributions=load_json(distributions_file),
    )


@pytest.fixture
def synthesis_overrides():
    return {
        "apical_dendrite": schemas.SynthesisOverrides(
            total_extent=10.0,
            randomness=0.001,
            orientation=[[0.0, 0.0, 1.0]],
            step_size={"norm": {"mean": 1.5, "std": 0.1}},
            radius=0.5,
        )
    }


@pytest.fixture(scope="session")
def morphology_file():
    return DATA_DIR / "bio_rat_L5_TPC_B.h5"


@pytest.fixture(scope="session")
def morphology(morphology_file):
    return tmd.io.load_neuron_from_morphio(str(morphology_file))
