import open3d as o3d
import numpy as np

# File paths
input_path = "/home/moniesha/Downloads/DCD_data/tina_gc.ply"
output_path = "/home/moniesha/Downloads/DCD_data/tina_gc_filtered.ply"

# Load point cloud
pcd = o3d.io.read_point_cloud(input_path)

# Convert colors to uint8
colors = np.asarray(pcd.colors)
colors_uint8 = (colors * 255).round().astype(np.uint8)

# Define color ranges
def is_black(c):
    return np.all(c == [0, 0, 0])

def is_red_range(c):
    return (
        20 <= c[0] <= 255 and  # R near 146
        0 <= c[1] <= 30 and     # G near 0
        0 <= c[2] <= 30         # B near 10
    )

# Create mask for colors to keep
mask = np.array([not (is_black(c) or is_red_range(c)) for c in colors_uint8])

# Apply mask
pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points)[mask])
pcd.colors = o3d.utility.Vector3dVector(colors[mask])  # use float version

# Save filtered point cloud
o3d.io.write_point_cloud(output_path, pcd)
print(f"Filtered point cloud saved to: {output_path}")
