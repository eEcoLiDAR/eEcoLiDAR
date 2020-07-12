import numpy as np
import pylas

from laserchicken import keys


def add_normalized_height(las, pc):

    las = convert_and_add_dim(las)

    las = populate_expanded_las(las,pc)
    
    
    return las




def convert_and_add_dim(las):
    las = pylas.convert(las,file_version=1.4)
    las.add_extra_dim(name='normalized_height',type='f8',description='Height above minimum in cells.')
    return las


def populate_expanded_las(las,pc):

    affected_attributes = {
        'normalized_height',
        'raw_classification',
        'classification',
        'return_number',
        'number_of_returns',
        'bit_fields'
        }

    for name in affected_attributes:
        las[name] = pc[keys.point][name]['data']

    return las

