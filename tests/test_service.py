from copy import deepcopy

import pytest
import numpy as np
import pylab as plt
from numpy import testing as npt
from pathlib import Path

import app.service as test_module


from app import service as test_module
from app import schemas


def test_make_synthesis_inputs(synthesis_files, synthesis_overrides):
    parameters, distributions = test_module.make_synthesis_inputs(
        files=synthesis_files,
        overrides=synthesis_overrides,
    )
    assert isinstance(parameters, dict)
    assert isinstance(distributions, dict)


def test_scale_barcode_list():
    barcode_list = [[[2.0, 1.0, 3.0, 4.0], [0.2, 0.1, 0.3, 0.4], [0.002, 0.001, np.nan, np.nan]]]

    res = test_module._scale_barcode_list(barcode_list, 10.0)

    expected = [[[10.0, 5.0, 3.0, 4.0], [1.0, 0.5, 0.3, 0.4], [0.01, 0.005, np.nan, np.nan]]]

    npt.assert_allclose(res, expected)


def test_apply_overrides__None(bio_params, bio_distributions):
    # by default all overrides are None
    overrides = {"basal_dendrite": schemas.SynthesisOverrides()}

    old_params = deepcopy(bio_params)
    old_distrs = deepcopy(bio_distributions)

    test_module._apply_overrides(bio_params, bio_distributions, overrides)

    assert old_params == bio_params
    assert old_distrs == bio_distributions


def test_apply_overrides(bio_params, bio_distributions, synthesis_overrides):
    old_params = deepcopy(bio_params)
    old_distrs = deepcopy(bio_distributions)

    test_module._apply_overrides(bio_params, bio_distributions, synthesis_overrides)

    assert bio_params["basal_dendrite"] == old_params["basal_dendrite"]
    assert bio_distributions["basal_dendrite"] == old_distrs["basal_dendrite"]

    apical_params = bio_params["apical_dendrite"]
    apical_distrs = bio_distributions["apical_dendrite"]
    apical_overrides = synthesis_overrides["apical_dendrite"]

    assert apical_distrs != old_distrs["apical_dendrite"]

    assert apical_params["randomness"] == apical_overrides.randomness
    assert apical_params["radius"] == apical_overrides.radius
    assert apical_params["step_size"]["norm"]["mean"] == apical_overrides.step_size
    assert apical_params["orientation"] == {
        "mode": "use_predefined",
        "values": {"orientations": [list(apical_overrides.orientation)]},
    }


def test_synthesize_morphology(bio_params, bio_distributions, morphology):
    result = test_module.synthesize_morphology(bio_params, bio_distributions)
    assert result.neurites


def test_make_figure(morphology):
    figures = test_module.make_figure(morphology)
    assert isinstance(figures, dict)
    for fig in figures.values():
        assert isinstance(fig, plt.Figure)
