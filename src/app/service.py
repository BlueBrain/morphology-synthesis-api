"""Service functions."""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager

import neurots
import numpy as np
import pylab as plt
import tmd.io
import tmd.view

from app import nexus, utils
from app.schemas import (
    NexusConfig,
    SynthesisDatasets,
    SynthesisFiles,
    SynthesisOverrides,
    SynthesisResources,
)


def load_synthesis_datasets(files: SynthesisFiles) -> SynthesisDatasets:
    """Load synthesis datasets from files.

    Args:
        files: Synthesis files to load.

    Returns:
        The loaded synthesis datasets.
    """
    return SynthesisDatasets(
        parameters=utils.load_json(files.parameters_file),
        distributions=utils.load_json(files.distributions_file),
    )


def fetch_synthesis_datasets(
    resources: SynthesisResources, nexus_config: NexusConfig, nexus_token: str
) -> SynthesisDatasets:
    """Fetch synthesis datasets for Nexus resources.

    Args:
        resources: Synthesis resources to fetch.
        nexus_config: Configuration for nexus endpoint and bucket.
        nexus_token: Nexus authentication token.

    Returns:
        The loaded synthesis datasets.
    """
    parameters_resource = nexus.get_resource_json_ld(
        resource_id=resources.parameters_id,
        nexus_config=nexus_config,
        nexus_token=nexus_token,
    )
    parameters = nexus.load_json_distribution_file(parameters_resource, nexus_token)

    distributions_resource = nexus.get_resource_json_ld(
        resource_id=resources.distributions_id,
        nexus_config=nexus_config,
        nexus_token=nexus_token,
    )
    distributions = nexus.load_json_distribution_file(distributions_resource, nexus_token)

    return SynthesisDatasets(
        parameters=parameters,
        distributions=distributions,
    )


def apply_overrides(
    datasets: SynthesisDatasets, overrides: Mapping[str, SynthesisOverrides]
) -> None:
    """Update synthesis inputs based on overrides."""
    parameters, distributions = datasets.parameters, datasets.distributions

    available_grow_types = parameters["grow_types"]

    for grow_type, neurite_overrides in overrides.items():
        assert grow_type in available_grow_types

        neurite_parameters = parameters[grow_type]
        neurite_distributions = distributions[grow_type]

        if neurite_overrides.total_extent:
            neurite_distributions["persistence_diagram"] = _scale_barcode_list(
                neurite_distributions["persistence_diagram"],
                neurite_overrides.total_extent,
            )

        if neurite_overrides.randomness:
            neurite_parameters["randomness"] = neurite_overrides.randomness

        if neurite_overrides.radius:
            neurite_parameters["radius"] = neurite_overrides.radius

        if neurite_overrides.step_size:
            neurite_parameters["step_size"]["norm"]["mean"] = neurite_overrides.step_size

        if neurite_overrides.orientation:
            neurite_parameters["orientation"] = {
                "mode": "use_predefined",
                "values": {"orientations": [list(neurite_overrides.orientation)]},
            }


def _scale_barcode_list(barcode_list: list, total_extent: float) -> list:
    def scale_spatial_barcode_component(barcode: list, total_extent: float) -> list:
        barcode_array = np.array(barcode)
        barcode_array[:, (0, 1)] *= total_extent / np.nanmax(barcode_array[:, (0, 1)])
        return barcode_array.tolist()

    return [scale_spatial_barcode_component(barcode, total_extent) for barcode in barcode_list]


def synthesize_morphology(synthesis_datasets: SynthesisDatasets) -> tmd.Neuron:
    """Grow a morphology using the parameters and distributions."""
    grower = neurots.NeuronGrower(synthesis_datasets.parameters, synthesis_datasets.distributions)
    grower.grow()
    return tmd.io.load_neuron_from_morphio(grower.neuron.as_immutable())


@contextmanager
def make_figures(morphology: tmd.Neuron) -> Iterator[dict[str, plt.Figure]]:
    """Make an analysis figure."""
    barcode = tmd.methods.get_ph_neuron(morphology, neurite_type="dendrites")

    fig_barcode, _ = tmd.view.plot.barcode(
        barcode, color="b", new_fig=True, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )
    fig_diagram, _ = tmd.view.plot.diagram(
        barcode, color="b", new_fig=True, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )
    fig_image, _ = tmd.view.plot.persistence_image(
        barcode, new_fig=True, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )[1]

    fig_synthesis, _ = tmd.view.view.neuron(
        morphology,
        new_fig=True,
        treecolors="b",
        xlim=(-300, 300),
        ylim=(-300, 300),
        no_axes=True,
    )

    figures = {
        "barcode": fig_barcode,
        "diagram": fig_diagram,
        "image": fig_image,
        "synthesis": fig_synthesis,
    }

    try:
        yield figures
    finally:
        # Remove figures from pylab's state machine
        for fig in figures.values():
            plt.close(fig)
