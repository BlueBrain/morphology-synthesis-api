"""API entry points."""

from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import serialize, service
from app.constants import COMMIT_SHA, DEBUG, ORIGINS, PROJECT_PATH
from app.schemas import (
    FileInputs,
    ResourceInputs,
    SerializedFigures,
    SynthesisDatasets,
    SynthesisOverrides,
)

app = FastAPI(debug=DEBUG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "project": PROJECT_PATH,
        "status": "OK",
    }


@app.get("/version")
async def version() -> dict:
    """Version endpoint."""
    return {
        "project": PROJECT_PATH,
        "commit_sha": COMMIT_SHA,
    }


def _synthesize_and_produce_figures(
    synthesis_datasets: SynthesisDatasets, overrides: dict[str, SynthesisOverrides]
) -> SerializedFigures:
    """Apply overrides, synthesis, and return analysis figures."""
    if overrides is not None:
        service.apply_overrides(synthesis_datasets, overrides)

    morphology = service.synthesize_morphology(synthesis_datasets)

    with service.make_figures(morphology) as figures:
        return SerializedFigures(
            barcode=serialize.figure64(figures["barcode"]),
            diagram=serialize.figure64(figures["diagram"]),
            image=serialize.figure64(figures["image"]),
            synthesis=serialize.figure64(figures["synthesis"]),
        )


@app.post("/synthesis-with-files", response_class=JSONResponse)
async def synthesis_with_files(synthesis_inputs: FileInputs) -> SerializedFigures:
    """Synthesize a morphology and return an analysis figure using files."""
    synthesis_datasets = service.load_synthesis_datasets(synthesis_inputs.files)
    return _synthesize_and_produce_figures(synthesis_datasets, synthesis_inputs.overrides)


@app.post("/synthesis-with-resources", response_class=JSONResponse)
async def synthesis_with_resources(
    synthesis_inputs: ResourceInputs,
    nexus_token: Annotated[str, Header()],
) -> SerializedFigures:
    """Synthesize a morphology and return analysis figures using resources."""
    synthesis_datasets = service.fetch_synthesis_datasets(
        resources=synthesis_inputs.resources,
        nexus_config=synthesis_inputs.nexus_config,
        nexus_token=nexus_token,
    )
    return _synthesize_and_produce_figures(synthesis_datasets, synthesis_inputs.overrides)
