"""Data schemas."""
from pathlib import Path

from pydantic import BaseModel


class SynthesisFiles(BaseModel):
    """Synthesis input files."""

    parameters_file: Path
    distributions_file: Path


class SynthesisOverrides(BaseModel):
    """Synthesis inputs overrides."""

    total_extent: float | None = None
    randomness: float | None = None
    orientation: tuple[float, float, float] | None = None
    step_size: float | None = None
    radius: float | None = None


class SynthesisWithFilesInputs(BaseModel):
    """Synthesis file endpoint input."""

    files: SynthesisFiles
    overrides: dict[str, SynthesisOverrides]


class SerializedFigures(BaseModel):
    """Serialized figures."""

    barcode: str
    diagram: str
    image: str
    synthesis: str
