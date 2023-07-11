from copy import deepcopy

import numpy as np
import pylab as plt
from numpy import testing as npt
from unittest.mock import patch

from app import service as test_module
from app import schemas


def test_fetch_synthesis_datasets(synthesis_resources, nexus_config):
    mock_resources = {
        synthesis_resources.parameters_id: {
            "distribution": {"atLocation": {"location": "file://path1"}}
        },
        synthesis_resources.distributions_id: {
            "distribution": {"atLocation": {"location": "file://path2"}}
        },
    }

    path_to_mock_data = {
        "path1": {"foo": "bar"},
        "path2": {"bar": "foo"},
    }

    with (
        patch(
            "app.nexus.get_resource_json_ld",
            side_effect=lambda resource_id, nexus_config, nexus_token: mock_resources[resource_id],
        ),
        patch(
            "app.nexus.load_json",
            side_effect=lambda p: path_to_mock_data[p],
        ),
    ):
        res = test_module.fetch_synthesis_datasets(synthesis_resources, nexus_config, None)

        assert res.parameters == {"foo": "bar"}
        assert res.distributions == {"bar": "foo"}


def test_scale_barcode_list():
    barcode_list = [[[2.0, 1.0, 3.0, 4.0], [0.2, 0.1, 0.3, 0.4], [0.002, 0.001, np.nan, np.nan]]]

    res = test_module._scale_barcode_list(barcode_list, 10.0)

    expected = [[[10.0, 5.0, 3.0, 4.0], [1.0, 0.5, 0.3, 0.4], [0.01, 0.005, np.nan, np.nan]]]

    npt.assert_allclose(res, expected)


def test_apply_overrides__None(synthesis_datasets):
    # by default all overrides are None
    overrides = {"basal_dendrite": schemas.SynthesisOverrides()}

    datasets = deepcopy(synthesis_datasets)

    test_module.apply_overrides(datasets, overrides)

    assert synthesis_datasets == datasets


def test_apply_overrides(synthesis_datasets, synthesis_overrides):
    datasets = deepcopy(synthesis_datasets)

    test_module.apply_overrides(datasets, synthesis_overrides)

    assert datasets.parameters["basal_dendrite"] == synthesis_datasets.parameters["basal_dendrite"]
    assert (
        datasets.distributions["basal_dendrite"]
        == synthesis_datasets.distributions["basal_dendrite"]
    )

    apical_params = datasets.parameters["apical_dendrite"]
    apical_distrs = datasets.distributions["apical_dendrite"]
    apical_overrides = synthesis_overrides["apical_dendrite"]

    assert apical_distrs != synthesis_datasets.distributions["apical_dendrite"]

    assert apical_params["randomness"] == apical_overrides.randomness
    assert apical_params["radius"] == apical_overrides.radius
    assert apical_params["step_size"] == apical_overrides.step_size
    assert apical_params["orientation"] == {
        "mode": "use_predefined",
        "values": {"orientations": [list(apical_overrides.orientation)]},
    }


def test_synthesize_morphology(synthesis_datasets, morphology):
    result = test_module.synthesize_morphology(synthesis_datasets)
    assert result.neurites


def test_make_figures(morphology):
    before_fignums = plt.get_fignums()

    with test_module.make_figures(morphology) as figures:
        assert isinstance(figures, dict)
        for fig in figures.values():
            assert isinstance(fig, plt.Figure)

        assert len(plt.get_fignums()) == len(before_fignums) + len(figures)

    assert plt.get_fignums() == before_fignums
