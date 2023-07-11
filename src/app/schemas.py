"""Data schemas."""
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from app.constants import NEXUS_BUCKET, NEXUS_ENDPOINT


class SynthesisDatasets(BaseModel):
    """Synthesis datasets."""

    parameters: dict[str, Any]
    distributions: dict[str, Any]


class SynthesisFiles(BaseModel):
    """Synthesis input files."""

    parameters_file: Path
    distributions_file: Path


class SynthesisOverrides(BaseModel):
    """Synthesis inputs overrides."""

    total_extent: float | None = None
    randomness: float | None = None
    orientation: tuple[float, float, float] | None = None
    step_size: dict[str, dict[str, float]] | None = None
    radius: float | None = None


class FileInputs(BaseModel):
    """Synthesis file endpoint input."""

    files: SynthesisFiles
    overrides: dict[str, SynthesisOverrides]


class SerializedFigures(BaseModel):
    """Serialized figures."""

    barcode: str
    diagram: str
    image: str
    synthesis: str


class SynthesisResources(BaseModel):
    """Synthesis inputs resources."""

    parameters_id: str
    distributions_id: str


class NexusConfig(BaseModel):
    """Nexus configuration."""

    bucket: str
    endpoint: str

    @property
    def org(self):
        """Return Nexus organization."""
        return self.bucket.split("/")[0]

    @property
    def project(self):
        """Return Nexus project."""
        return self.bucket.split("/")[1]


class ResourceInputs(BaseModel):
    """Synthesis resource endpoint input."""

    resources: SynthesisResources
    overrides: dict[str, SynthesisOverrides]
    nexus_config: NexusConfig = NexusConfig(endpoint=NEXUS_ENDPOINT, bucket=NEXUS_BUCKET)
