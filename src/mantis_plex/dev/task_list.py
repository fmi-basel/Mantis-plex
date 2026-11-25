# Copyright 2024 (C) Friedrich Miescher Institute for Biomedical Research and
# University of Zurich
#
# Original authors:
# Joel Lüthi <joel.luethi@uzh.ch>
#
# This file is part of Fractal and was originally developed by eXact lab S.r.l.
# <exact-lab.it> under contract with Liberali Lab from the Friedrich Miescher
# Institute for Biomedical Research and Pelkmans Lab from the University of
# Zurich.
"""
Fractal task list.
"""
from fractal_task_tools.task_models import CompoundTask

# executable relative to base folder to src/mantis_plex folder
# TODO: check CPU and GPU usage for each task and allocate more accurate values

AUTHORS = "Nicole Repina, Enrico Tagliavini, Tim-Oliver Buchholz, Joel Luethi"
DOCS_LINK = "https://github.com/fmi-basel/Mantis-plex"
INPUT_MODELS = [
    ["fractal_tasks_core", "channels.py", "ChannelInputModel"],
]

TASK_LIST = [
    CompoundTask(
        name="Calculate Object Linking",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/calculate_object_linking.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "2D"],
        docs_info="file:task_info/calculate_object_linking.md",
    ),
    CompoundTask(
        name="Calculate Linking Consensus",
        executable_init="fractal/init_select_reference_knowing_all.py",
        executable="fractal/calculate_linking_consensus.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "2D", "3D"],
        docs_info="file:task_info/calculate_linking_consensus.md",
    ),
    CompoundTask(
        name="Relabel by Linking Consensus",
        executable_init="fractal/init_select_all_knowing_reference.py",
        executable="fractal/relabel_by_linking_consensus.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 64000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "2D", "3D"],
        docs_info="file:task_info/relabel_by_linking_consensus.md",
    ),
    CompoundTask(
        name="Calculate Platymatch Registration",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/calculate_platymatch_registration.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D"],
        docs_info="file:task_info/calculate_platymatch_registration.md",
    ),
    CompoundTask(
        name="Calculate Z-Illumination Correction",
        executable_init="fractal/init_select_single_round.py",
        executable="fractal/calculate_z_illumination_correction.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Image Processing",
        modality="HCS",
        tags=["3D", "illumination correction"],
        docs_info="file:task_info/calculate_z_illumination_correction.md",
        input_types=dict(z_illum_corrected=False, is_3D=True),
    ),
    CompoundTask(
        name="Apply Z-Illumination Correction",
        executable_init="fractal/init_select_illumination_round.py",
        executable="fractal/apply_z_illumination_correction.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Image Processing",
        modality="HCS",
        tags=["3D", "illumination correction"],
        docs_info="file:task_info/apply_z_illumination_correction.md",
        input_types=dict(z_illum_corrected=False, is_3D=True),
        output_types=dict(z_illum_corrected=True, is_3D=True),
    ),
    CompoundTask(
        name="Shift by Shift",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/shift_by_shift.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "2D", "3D"],
        docs_info="file:task_info/shift_by_shift.md",
    ),
    CompoundTask(
        name="Shift by Rigid Shift",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/shift_by_rigid_shift.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "2D", "3D"],
        docs_info="file:task_info/shift_by_rigid_shift.md",
    ),
    CompoundTask(
        name="Calculate 2D Rigid Shift",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/calculate_2d_rigid_shift.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=[
            "multiplexing",
            "2D",
        ],
        docs_info="file:task_info/calculate_2d_rigid_shift.md",
    ),
    CompoundTask(
        name="Calculate Warpfield Registration",
        executable_init="fractal/init_select_multiplexing_pairs.py",
        executable="fractal/calculate_warpfield_registration.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000, "needs_gpu": True},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D"],
        docs_info="file:task_info/calculate_warpfield_registration.md",
        input_types=dict(is_3D=True),
    ),
    CompoundTask(
        name="Apply Warpfield Registration",
        executable_init="fractal/init_select_all_knowing_reference.py",
        executable="fractal/apply_warpfield_registration.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000, "needs_gpu": True},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D"],
        docs_info="file:task_info/apply_warpfield_registration.md",
        input_types=dict(registered=False, is_3D=True),
        output_types=dict(registered=True, is_3D=True),
    ),
    CompoundTask(
        name="Post Registration Cleanup",
        executable_init="fractal/init_select_all_knowing_reference.py",
        executable="fractal/post_registration_cleanup.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D"],
        docs_info="file:task_info/post_registration_cleanup.md",
        input_types=dict(is_3D=True),
        output_types=dict(registered=True, is_3D=True),
    ),
    CompoundTask(
        name="Detect Clipped Rois Across Rounds",
        executable_init="fractal/init_select_reference_knowing_all.py",
        executable="fractal/detect_clipped_rois_across_rounds.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D"],
    ),
    CompoundTask(
        name="Copy Data from Reference to Moving Rounds",
        executable_init="fractal/init_select_all_knowing_reference.py",
        executable="fractal/copy_data_from_ref_to_moving_rounds.py",
        meta_init={"cpus_per_task": 1, "mem": 1000},
        meta={"cpus_per_task": 4, "mem": 16000},
        category="Registration",
        modality="HCS",
        tags=["multiplexing", "3D", "2D"],
        docs_info="file:task_info/copy_data_from_ref_to_moving_rounds.md",
    ),
]
