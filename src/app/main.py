"""API entry points."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import serialize, service
from app.constants import COMMIT_SHA, DEBUG, ORIGINS, PROJECT_PATH
from app.schemas import SerializedFigures, SynthesisWithFilesInputs

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


@app.post(
    "/synthesis-with-files",
    response_class=JSONResponse,
)
async def synthesis_with_files(synthesis_inputs: SynthesisWithFilesInputs) -> SerializedFigures:
    """Synthesize a morphology and return an analysis figure."""
    parameters, distributions = service.make_synthesis_inputs(
        synthesis_inputs.files, synthesis_inputs.overrides
    )
    morphology = service.synthesize_morphology(parameters, distributions)

    with service.make_figures(morphology) as figures:
        return SerializedFigures(
            barcode=serialize.figure64(figures["barcode"]),
            diagram=serialize.figure64(figures["diagram"]),
            image=serialize.figure64(figures["image"]),
            synthesis=serialize.figure64(figures["synthesis"]),
        )
