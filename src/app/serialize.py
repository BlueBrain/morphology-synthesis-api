"""Serialization functions."""

import base64
import io

import pylab as plt


def figure(fig: plt.Figure, media_type: str = "png") -> bytes:
    """Convert a figure into bytes."""
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format=media_type)
    return image_buffer.getbuffer().tobytes()


def figure64(fig: plt.Figure) -> str:
    """Convert a figure into base64."""
    binary_file_data = figure(fig)
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode("utf-8")
    return base64_message
