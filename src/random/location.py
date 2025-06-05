import numpy as np









topography_colors = [[0.1450980392156863, 0.5411764705882353, 0.4549019607843137],
                     [0.3803921568627451, 0.596078431372549, 0.20392156862745098],
                     [0.4235294117647059, 0.5215686274509804, 0.48627450980392156],
                     [0.5215686274509804, 0.45098039215686275, 0.17254901960784313],
                     [0.39215686274509803, 0.16862745098039217, 0.0784313725490196],
                     [0.1098, 0.4196, 0.6275]] # test value

def get_topography_colors_array():
    return np.array(topography_colors, dtype=np.float32)






## TODO

# make np dtype with the values present in a location
# Climate, terrain, vegetation, local good, rank (rural, town, city), harbor suitability?
#
# population, development,
# proximity, control, satisfaction, market access, literacy
# rgo level, road lvl, harbor, other buildings
# estate stuff
# tax base
# distance cost? proximity

# all goods to market



