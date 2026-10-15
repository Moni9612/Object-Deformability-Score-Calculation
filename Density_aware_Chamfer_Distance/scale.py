import open3d as o3d
import numpy as np

# Load point clouds
pcd1 = o3d.io.read_point_cloud("/home/moniesha/Downloads/DCD_data/box_filtered.ply")
pcd2 = o3d.io.read_point_cloud("/home/moniesha/Downloads/DCD_data/box_g_c_filtered.ply")

# Compute bounding box sizes
bbox1 = pcd1.get_axis_aligned_bounding_box()
bbox2 = pcd2.get_axis_aligned_bounding_box()

print("Size of box_filtered:", bbox1.get_extent())
print("Size of box_g_c_filtered:", bbox2.get_extent())

# Estimate scale ratio
scale_ratio = np.mean(bbox2.get_extent() / bbox1.get_extent())
print("Estimated scale ratio:", scale_ratio)
