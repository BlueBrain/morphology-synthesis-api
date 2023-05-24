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

    assert isinstance(parameters, dict)
    assert isinstance(distributions, dict)


def test_synthesize_morphology(bio_params, bio_distributions, morphology):
    result = test_module.synthesize_morphology(bio_params, bio_distributions)
    assert result.neurites


def test_make_figure(morphology):
    figure = test_module.make_figure(morphology)
    assert figure.get_axes()
