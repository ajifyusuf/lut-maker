import json
import pytest
from lut_maker.lut import Lut

SIZE = 17
LUT = Lut(SIZE, 1024)

class TestUnits:
    def test_color_order(self):
        colors = LUT.generate_colors()
        color = colors[SIZE+2]
        # r should change the fastest, then g, then b
        assert color[0] > color[1] > color[2]

    def test_lattice_order(self):
        column, row, z  = LUT.lattice_coords(SIZE+2)
        # column should change the fastest, then row, then z
        assert column > row > z

    def test_cell_center_return_format(self):
        #center of size 1 should be a single point
        assert len(LUT.cell_center(0,1)) == 2
        #center of size > 1 should be a rect
        assert len(LUT.cell_center(0,10)) == 4
