"""Service functions."""

import neurots
import pylab as plt
import tmd.io
import tmd.view

from app import utils
from app.schemas import SynthesisFiles, SynthesisOverrides

# pylint: disable=unused-argument


def make_synthesis_inputs(
    files: SynthesisFiles, overrides: dict[str, SynthesisOverrides] | None = None
) -> tuple[dict, dict]:
    """Generate and update the synthesis inputs."""
    parameters = utils.load_json(files.parameters_file)
    distributions = utils.load_json(files.distributions_file)

    # if overrides:
    #    parameters, distribution = _apply_overrides(parameters, distributions, overrides)

    return parameters, distributions


def synthesize_morphology(parameters: dict, distributions: dict) -> tmd.Neuron:
    """Grow a morphology using the parameters and distributions."""
    grower = neurots.NeuronGrower(parameters, distributions)
    grower.grow()
    return tmd.io.load_neuron_from_morphio(grower.neuron.as_immutable())


def make_figure(morphology: tmd.Neuron) -> plt.Figure:
    """Make an analysis figure."""
    barcode = tmd.methods.get_ph_neuron(morphology, neurite_type="dendrites")

    fig = plt.figure()

    # ruff: noqa: F841
    # pylint: disable=unused-variable

    ax1 = fig.add_subplot(321)
    tmd.view.plot.barcode(
        barcode, color="b", new_fig=False, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )
    ax2 = fig.add_subplot(323)
    tmd.view.plot.diagram(
        barcode, color="b", new_fig=False, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )
    ax3 = fig.add_subplot(325)
    tmd.view.plot.persistence_image(
        barcode, new_fig=False, xlim=(0, 100), ylim=(0, 100), xlabel="", ylabel=""
    )
    ax4 = fig.add_subplot(122)
    tmd.view.view.neuron(
        morphology,
        new_fig=False,
        treecolors="b",
        subplot=(122),
        xlim=(-300, 300),
        ylim=(-1000, 1000),
        no_axes=True,
    )

    return fig
