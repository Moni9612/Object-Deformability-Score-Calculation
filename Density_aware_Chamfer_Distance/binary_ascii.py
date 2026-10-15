import open3d as o3d

# Input and output file paths
ascii_ply = "/home/moniesha/object score/objectsxcfinal/18x.ply"
binary_ply = "/home/moniesha/object score/objectsxcb/18xb.ply"

# Load ASCII .ply
pcd = o3d.io.read_point_cloud(ascii_ply)

# Save as binary
o3d.io.write_point_cloud(binary_ply, pcd, write_ascii=False)

print(f"Converted to binary format: {binary_ply}")
