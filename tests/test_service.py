import pytest
from pathlib import Path

import app.service as test_module


from app import service as test_module


def test_make_synthesis_inputs(synthesis_files, synthesis_overrides):
    parameters, distributions = test_module.make_synthesis_inputs(
        files=synthesis_files,
        overrides=synthesis_overrides,
    )
    assert isinstance(parameters, dict)
    assert isinstance(distributions, dict)


def test_synthesize_morphology(bio_params, bio_distributions, morphology):
    result = test_module.synthesize_morphology(bio_params, bio_distributions)
    assert result.neurites


def test_make_figure(morphology):
    figure = test_module.make_figure(morphology)
    assert figure.get_axes()
