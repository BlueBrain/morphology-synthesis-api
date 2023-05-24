"""API entry points."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from app import serialize, service
from app.constants import COMMIT_SHA, DEBUG, ORIGINS, PROJECT_PATH

app = FastAPI(debug=DEBUG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Config(BaseModel):
    """Config model."""

    parameters_file: Path
    distributions_file: Path
    total_extent: float
    randomness: float
    orientation: tuple[float, float, float]
    step_size: float
    radius: float


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


@app.post("/synthesize_morphology")
async def synthesize_morphology(config: Config):
    """Synthesize a morphology and return an analysis figure."""
    parameters, distributions = service.make_synthesis_inputs(
        parameters_file=config.parameters_file,
        distributions_file=config.distributions_file,
        total_extent=config.total_extent,
        randomness=config.randomness,
        orientation=config.orientation,
        step_size=config.step_size,
        radius=config.radius,
    )

    morphology = service.synthesize_morphology(parameters, distributions)

    figure = service.make_figure(morphology)

    return Response(content=serialize.figure(figure, media_type="jpg"), media_type="image/jpeg")
