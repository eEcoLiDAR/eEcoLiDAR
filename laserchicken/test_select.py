import unittest

import numpy as np
import pytest

from laserchicken.select import select_below, select_above


class TestSelectBelow(unittest.TestCase):
    def test_selectBelow_None(self):
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_below)

    def test_selectBelow_unknownKey(self):
        """ If key is not in point cloud, raise Value Error. """
        assert_unknown_key_raises_value_error(select_below)

    def test_selectBelow_noneKey(self):
        """ If key is None, raise Value Error. """
        assert_none_key_raises_value_error(select_below)

    def test_selectBelow_outputIsNotInput(self):
        """ Even when selecting all points, the function should never return the actual input object. """
        pc_in = get_test_data()
        pc_out = select_below_ridiculous_high_z(pc_in)
        assert (pc_in is not pc_out)

    def test_selectBelow_everything(self):
        """ Selecting all point under some super high value should return all the points. """
        pc_in = get_test_data()
        pc_out = select_below_ridiculous_high_z(pc_in)
        self.assertEqual(len(pc_out['points']['x']['data']), 3)
        assert_points_equal(pc_in, pc_out)

    def test_selectBelow_onlyOnePoint(self):
        """ Selecting below some threshold should only result the correct lowest point. """
        pc_in = get_test_data()
        pc_out = select_below(pc_in, 'z', 3.2)
        self.assertEqual(len(pc_out['points']['x']['data']), 1)
        np.testing.assert_almost_equal(pc_out['points']['x']['data'][0], 1.1)
        np.testing.assert_almost_equal(pc_out['points']['y']['data'][0], 2.1)
        np.testing.assert_almost_equal(pc_out['points']['z']['data'][0], 3.1)
        np.testing.assert_almost_equal(pc_out['points']['return']['data'][0], 1)


class TestSelectAbove(unittest.TestCase):
    def test_selectAbove_None(self):
        """ None input raises Value Error. """
        assert_none_pc_raises_value_error(select_above)

    def test_selectAbove_unknownKey(self):
        """ If key is not in point cloud, raise Value Error. """
        assert_unknown_key_raises_value_error(select_above)

    def test_selectAbove_noneKey(self):
        """ If key is None, raise Value Error. """
        assert_none_key_raises_value_error(select_above)

    def test_selectAbove_everything(self):
        """ Selecting all point above some super low value should return all the points. """
        pc_in = get_test_data()
        pc_out = select_above(pc_in, 'z', -100000)
        assert_points_equal(pc_in, pc_out)

    def test_selectBelow_onlyOnePoint(self):
        """ Selecting above some threshold should only result the correct highest point. """
        pc_in = get_test_data()
        pc_out = select_above(pc_in, 'z', 3.2)
        self.assertEqual(len(pc_out['points']['x']['data']), 1)
        np.testing.assert_almost_equal(pc_out['points']['x']['data'][0], 1.3)
        np.testing.assert_almost_equal(pc_out['points']['y']['data'][0], 2.3)
        np.testing.assert_almost_equal(pc_out['points']['z']['data'][0], 3.3)
        np.testing.assert_almost_equal(pc_out['points']['return']['data'][0], 2)


def get_test_data():
    return {'log': ['Processed by module load', 'Processed by module filter using parameters(x,y,z)'],
            'pointcloud': {'offset': {'type': 'double', 'data': 12.1}},
            'points':
                {'x': {'type': 'double', 'data': np.array([1.1, 1.2, 1.3])},
                 'y': {'type': 'double', 'data': np.array([2.1, 2.2, 2.3])},
                 'z': {'type': 'double', 'data': np.array([3.1, 3.2, 3.3])},
                 'return': {'type': 'int', 'data': np.array([1, 1, 2])}}}


def select_below_ridiculous_high_z(pc_in):
    return select_below(pc_in, 'z', 100000)


def assert_points_equal(pc_in, pc_out):
    np.testing.assert_equal(len(pc_out['points']['x']['data']), len(pc_in['points']['x']['data']))
    np.testing.assert_almost_equal(pc_out['points']['x']['data'], pc_in['points']['x']['data'])
    np.testing.assert_almost_equal(pc_out['points']['y']['data'], pc_in['points']['y']['data'])
    np.testing.assert_almost_equal(pc_out['points']['z']['data'], pc_in['points']['z']['data'])
    np.testing.assert_almost_equal(pc_out['points']['return']['data'], pc_in['points']['return']['data'])


def assert_none_pc_raises_value_error(function):
    with pytest.raises(ValueError):
        pc_in = None
        function(pc_in, 'x', 13)


def assert_unknown_key_raises_value_error(function):
    pc = get_test_data()
    with pytest.raises(ValueError):
        function(pc, 'unknown_key_123', 13)


def assert_none_key_raises_value_error(function):
    pc = get_test_data()
    with pytest.raises(ValueError):
        function(pc, None, 13)
