import open3d as o3d
import numpy as np

import recon.poses as poses


def make_fragments():
    '''
    Build local geometric surfaces
    '''


def register_rgbd_image_pair(
    s: int,
    t: int,
    source_image: o3d.geometry.RGBDImage,
    target_image: o3d.geometry.RGBDImage,
    max_depth_diff: float,
    camera_intrinsic
):
    '''
    This takes two RGBD images and registers the source to the target image.
    '''
    option = o3d.pipelines.odometry.OdometryOption()
    option.max_depth_diff = max_depth_diff

    # I don't know what s and t are but we need those. The examples don't really go into it and my theoretical knowledge
    # of this field is basically non-existent so I'm just casually copy-pasting this code...

    if abs(s - t) != 1:
        success_5pt, odo_init = poses.pose_estimation(source_image, target_image, camera_intrinsic, False)
        if success_5pt:
            [success, trans, info] = o3d.pipelines.odometry.compute_rgbd_odometry(
                source_image,
                target_image,
                camera_intrinsic,
                odo_init,
                o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(),
                option
            )
            return [success, trans, info]
    else:
        odo_init = np.identity(4)
        [success, trans, info] = o3d.pipelines.odometry.compute_rgbd_odometry(
            source_image,
            target_image,
            camera_intrinsic,
            odo_init,
            o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(),
            option
        )
        return [success, trans, info]


def make_posegraph_for_fragment(
    path_dataset,
    sid,
    eid,
    color_files,
    depth_files,
    fragment_id,
    n_fragments,
    intrinsic,
    with_opencv,
    config
):
    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)
    pose_graph = o3d.pipelines.registration.PoseGraph()
    trans_odometry = np.identity(4)
    pose_graph.nodes.append(
        o3d.pipelines.registration.PoseGraphNode(trans_odometry))
    for s in range(sid, eid):
        for t in range(s + 1, eid):
            # odometry
            if t == s + 1:
                print(
                    "Fragment %03d / %03d :: RGBD matching between frame : %d and %d"
                    % (fragment_id, n_fragments - 1, s, t))
                [success, trans,
                 info] = register_rgbd_image_pair(s, t, color_files, depth_files,
                                                  intrinsic, with_opencv, config)
                trans_odometry = np.dot(trans, trans_odometry)
                trans_odometry_inv = np.linalg.inv(trans_odometry)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(
                        trans_odometry_inv))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(s - sid,
                                                             t - sid,
                                                             trans,
                                                             info,
                                                             uncertain=False))

            # keyframe loop closure
            if s % config['n_keyframes_per_n_frame'] == 0 \
                    and t % config['n_keyframes_per_n_frame'] == 0:
                print(
                    "Fragment %03d / %03d :: RGBD matching between frame : %d and %d"
                    % (fragment_id, n_fragments - 1, s, t))
                [success, trans,
                 info] = register_rgbd_image_pair(s, t, color_files, depth_files,
                                                  intrinsic, with_opencv, config)
                if success:
                    pose_graph.edges.append(
                        o3d.pipelines.registration.PoseGraphEdge(
                            s - sid, t - sid, trans, info, uncertain=True))
    o3d.io.write_pose_graph(
        join(path_dataset, config["template_fragment_posegraph"] % fragment_id),
        pose_graph)
