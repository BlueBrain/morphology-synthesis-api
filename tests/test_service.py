import pytest
from pathlib import Path

import app.service as test_module


from app import service as test_module


def test_make_synthesis_inputs(bio_params_file, bio_distributions_file):
    parameters, distributions = test_module.make_synthesis_inputs(
        parameters_file=bio_params_file,
        distributions_file=bio_distributions_file,
        total_extent=100.0,
        randomness=0.001,
        orientation=(0.0, 0.0, 1.0),
        step_size=1.0,
        radius=0.5,
    )


def test_synthesize_morphology(bio_params_file, bio_distributions_file):
    morphology = test_module.synthesize_morphology(
        parameters=bio_params_file,
        distributions=bio_distributions_file,
    )
    assert morphology is not None


def test_make_figure(bio_params, bio_distributions):
    morphology = test_module.synthesize_morphology(
        parameters=bio_params,
        distributions=bio_distributions,
    )

    figure = test_module.make_figure(morphology)
