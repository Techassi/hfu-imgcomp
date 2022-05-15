# Plane sweep algo:
# - Sweep planes parallel to the ref camera
# - Reproject neighbors onto each plane (homography)
# - Compare reprojections

# In detail
# - Get matching keypoints
# - Compute fundamental matrix
# - Get epilines
# - Find homography
#   - iterate over planes
#   - reproject images (warp)
#   - blur and diff
# - We now should have a depth map


def plane_sweep():
    ''''''
    # Some random pseudo code
    depths, d = 0
    while d < depths:
        # Iterrate over all depths
        pass

# Calculate steps based on min, max and layers
# import numpy as np

# min_depth = 24
# max_depth = 45
# depth_layers = 128

# r = max_depth - min_depth
# s = r / depth_layers

# d = np.arange(min_depth, max_depth, s)
# print(len(d))
