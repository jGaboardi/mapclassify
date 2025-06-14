import geopandas
import numpy as np
import pytest
from numpy.testing import assert_array_equal

from mapclassify.util import get_color_array


@pytest.mark.filterwarnings("ignore:Geometry is in a geographic CRS.")
class TestRGBA:
    def setup_method(self):
        world = geopandas.read_file(
            "https://naciscdn.org/naturalearth/110m"
            "/cultural/ne_110m_admin_0_countries.zip"
        )
        world["area"] = world.area

        # columns are equivalent except for nan in the first position
        world["nanarea"] = world.area
        world.loc[0, "nanarea"] = np.nan

        self.world = world

    def test_rgba(self):
        colors = get_color_array(self.world["area"], cmap="viridis")[-1]
        assert_array_equal(colors, np.array([94, 201, 97, 255]))

    def test_rgba_hex(self):
        colors = get_color_array(self.world["area"], cmap="viridis", as_hex=True)[-1]
        assert_array_equal(colors, "#5ec961")

    def test_rgba_nan(self):
        colors = get_color_array(
            self.world["nanarea"], cmap="viridis", nan_color=[0, 0, 0, 0]
        )
        # should be nan_color
        assert_array_equal(colors[0], np.array([0, 0, 0, 0]))
        # still a cmap color
        assert_array_equal(colors[-1], np.array([94, 201, 97, 255]))

    def test_rgba_nan_hex(self):
        colors = get_color_array(
            self.world["nanarea"], cmap="viridis", nan_color=[0, 0, 0, 0], as_hex=True
        )
        assert_array_equal(colors[0], np.array(["#000000"]))
        assert_array_equal(colors[-1], np.array(["#5ec961"]))
