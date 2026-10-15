import open3d as o3d
import numpy as np

def preprocess_point_cloud(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30))
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 5, max_nn=100))
    return pcd_down, fpfh

def execute_global_registration(src_down, tgt_down, src_fpfh, tgt_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    return o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        src_down, tgt_down, src_fpfh, tgt_fpfh, True, distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        4,  # ransac_n
        [  # Correspondence checkers
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)
        ],
        o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500))

def refine_with_icp(source, target, init_trans, max_corr_distance):
    return o3d.pipelines.registration.registration_icp(
        source, target, max_corr_distance, init_trans,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())

# === Load point clouds ===
source_raw = o3d.io.read_point_cloud("/home/moniesha/Downloads/DCD_data/tin1_a.ply")
target_raw = o3d.io.read_point_cloud("/home/moniesha/Downloads/DCD_data/tin.ply")

# === Preprocess ===
voxel_size = 0.005  # 5 mm
source_down, source_fpfh = preprocess_point_cloud(source_raw, voxel_size)
target_down, target_fpfh = preprocess_point_cloud(target_raw, voxel_size)

# === Global registration ===
result_ransac = execute_global_registration(
    source_down, target_down, source_fpfh, target_fpfh, voxel_size)

print("Global registration result:")
print(result_ransac.transformation)

# === ICP refinement ===
reg_icp = refine_with_icp(
    source_raw, target_raw,
    result_ransac.transformation,
    max_corr_distance=voxel_size * 2)

print("Refined ICP transformation:")
print(reg_icp.transformation)
print("ICP Fitness:", reg_icp.fitness)
print("ICP RMSE:", reg_icp.inlier_rmse)

# === Save aligned point cloud ===
aligned_source = source_raw.transform(reg_icp.transformation)
o3d.io.write_point_cloud("/home/moniesha/Downloads/DCD_data/tin1_a_aligned.ply", aligned_source)
o3d.io.write_point_cloud("/home/moniesha/Downloads/DCD_data/tin_reference.ply", target_raw)

# === Visualize ===
o3d.visualization.draw_geometries([aligned_source, target_raw], window_name="Final Aligned Result")
