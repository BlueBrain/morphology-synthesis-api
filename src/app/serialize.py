"""Serialization functions."""

import io

import pylab as plt


def figure(fig: plt.Figure, media_type: str) -> bytes:
    """Convert a figure into bytes."""
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format=media_type)
    return image_buffer.getbuffer().tobytes()
