import os
import torch
import open3d as o3d
import numpy as np
from utils_v2.model_utils import calc_dcd, calc_emd  # Replace with actual module or use relative import

def load_ply_pointcloud(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File does not exist: {path}")
    pcd = o3d.io.read_point_cloud(path)
    if len(pcd.points) == 0:
        raise ValueError(f"❌ Point cloud is empty: {path}")
    print(f"✅ Loaded point cloud from {path} with {len(pcd.points)} points")
    return np.asarray(pcd.points, dtype=np.float32)

def main():
    # Set paths
    # before_path = '/home/moniesha/grasping_evaluation_code/test_data/filtered_before.ply'
    # after_path = '/home/moniesha/grasping_evaluation_code/test_data/filtered_after_c.ply'

    # before_path = '/home/moniesha/grasping_evaluation_code/Data/finray_point_clouds/B140_F8_90_1.ply'
    # after_path = '/home/moniesha/grasping_evaluation_code/Data/finray_point_clouds/B140_F8_90_1_G_C.ply'

    before_path = '/home/moniesha/object score/objectsxcb/2xb.ply'
    after_path = '/home/moniesha/object score/objectsxcb/2xgb.ply'

    # Load PLY point clouds
    pc_before = load_ply_pointcloud(before_path)
    pc_after = load_ply_pointcloud(after_path)

    # Convert to PyTorch tensors and move to GPU
    pc_before_tensor = torch.tensor(pc_before, dtype=torch.float32).unsqueeze(0).cuda()  # (1, N, 3)
    pc_after_tensor = torch.tensor(pc_after, dtype=torch.float32).unsqueeze(0).cuda()    # (1, M, 3)

    # Compute DCD
    dcd, _, _ = calc_dcd(pc_before_tensor, pc_after_tensor)
    print(f"DCD between before and after compression: {dcd.item():.10f}")

    # # Compute EMD
    # emd = calc_emd(pc_before_tensor, pc_after_tensor)
    # print(f"📏 EMD between before and after compression: {emd.item():.10f}")

if __name__ == "__main__":
    main()
