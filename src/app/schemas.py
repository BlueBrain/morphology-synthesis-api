"""Data schemas."""
from pydantic import BaseModel


class SynthesisFiles(BaseModel):
    """Synthesis input files."""

    parameters_file: str
    distributions_file: str


class SynthesisOverrides(BaseModel):
    """Synthesis inputs overrides."""

    total_extent: float | None = None
    randomness: float | None = None
    orientation: tuple[float, float, float] | None = None
    step_size: float | None = None
    radius: float | None = None
