from app import serialize as test_module
import io
import pylab as plt


def test_image():
    f, ax = plt.subplots()

    ax.scatter([0, 1], [1, 2])

    res = test_module.figure(f, media_type="jpg")

    assert res
