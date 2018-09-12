import numpy as np
import scipy.stats.stats as stat

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point


class SkewZFeatureExtractor(AbstractFeatureExtractor):
    """Calculates the skew on the z axis."""
    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['skew_z']

    def extract(self, sourcepc, neighborhood, targetpc, targetindex, volume_description):
        if neighborhood:
            z = sourcepc[point]['z']['data'][neighborhood]
            var_z = stat.skew(z)
        else:
            var_z = np.NaN
        return var_z
