from pathlib import Path

import anndata as ad
import numpy as np
from fractal_tasks_core.channels import ChannelInputModel
from numpy.testing import assert_almost_equal

from mantis_plex.fractal.calculate_linking_consensus import calculate_linking_consensus
from mantis_plex.fractal.calculate_object_linking import calculate_object_linking
from mantis_plex.fractal.calculate_platymatch_registration import (
    calculate_platymatch_registration,
)
from mantis_plex.fractal.init_select_all_knowing_reference import (
    init_select_all_knowing_reference,
)
from mantis_plex.fractal.init_select_multiplexing_pairs import (
    init_select_multiplexing_pairs,
)
from mantis_plex.fractal.init_select_reference_knowing_all import (
    init_select_reference_knowing_all,
)
from mantis_plex.fractal.relabel_by_linking_consensus import (
    relabel_by_linking_consensus,
)

name_3d = "220605_151046.zarr"
name_mip = "220605_151046_mip.zarr"

test_calculate_object_linking_expected_output = np.array(
    [[1.0, 1.0, 0.9727956], [2.0, 2.0, 0.8249731], [3.0, 3.0, 0.9644809]]
)

test_calculate_linking_consensus_expected_output = np.array(
    [[1.0, 1.0, 0.0, 1.0], [2.0, 2.0, 1.0, 2.0], [3.0, 3.0, 2.0, 3.0]]
)

test_relabel_by_linking_consensus_output_dict = {
    "0": np.array(
        [
            [13.216666, 21.016666, 0.0, 22.1, 20.583334, 0.6],
            [13.866667, 91.433334, 0.0, 18.85, 15.816667, 0.6],
            [39.0, 103.566666, 0.0, 23.183332, 28.166666, 0.6],
        ]
    ),
    "1": np.array(
        [
            [49.616665, 11.05, 0.0, 22.533333, 20.583334, 0.6],
            [51.783333, 81.9, 0.0, 18.85, 15.816667, 0.6],
            [75.4, 93.816666, 0.0, 23.4, 27.95, 0.6],
        ]
    ),
}

test_calculate_platymatch_registration_output = np.array(
    [
        [1.0, 1.0],
        [2.0, 2.0],
        [3.0, 3.0],
        [4.0, 4.0],
        [8.0, 7.0],
        [9.0, 8.0],
        [10.0, 9.0],
        [11.0, 10.0],
        [13.0, 12.0],
        [14.0, 13.0],
        [15.0, 14.0],
        [16.0, 15.0],
        [17.0, 16.0],
        [19.0, 17.0],
        [18.0, 18.0],
        [20.0, 19.0],
    ]
)


def select_zarr_urls(name, linking_zenodo_zarrs):
    zarr = None
    for z in linking_zenodo_zarrs:
        if z.endswith(name):
            zarr = z
            break
    assert zarr is not None

    # construct zarr url list
    zarr_urls = [f"{zarr}/C/02/0", f"{zarr}/C/02/1"]

    return zarr_urls


def test_calculate_object_linking(linking_zenodo_zarrs, name=name_mip):
    zarr_urls = select_zarr_urls(name, linking_zenodo_zarrs)
    parallelization_list = init_select_multiplexing_pairs(
        zarr_urls=zarr_urls,
        zarr_dir="",
        reference_acquisition=0,
    )

    for img in parallelization_list["parallelization_list"]:
        zarr_url = img["zarr_url"]
        init_args = img["init_args"]
        label_name = "org"
        roi_table = "well_ROI_table"
        level = 0

        calculate_object_linking(
            zarr_url=zarr_url,
            init_args=init_args,
            label_name=label_name,
            roi_table=roi_table,
            level=level,
            iou_cutoff=0.2,
        )
        output_table_path = f"{zarr_url}/tables/{label_name}_match_table"

        output = ad.read_zarr(output_table_path).to_df().to_numpy()
        assert_almost_equal(output, test_calculate_object_linking_expected_output)


def test_calculate_linking_consensus(linking_zenodo_zarrs, name=name_mip):
    zarr_urls = select_zarr_urls(name, linking_zenodo_zarrs)
    parallelization_list = init_select_reference_knowing_all(
        zarr_urls=zarr_urls,
        zarr_dir="",
        reference_acquisition=0,
    )

    for img in parallelization_list["parallelization_list"]:
        zarr_url = img["zarr_url"]
        init_args = img["init_args"]
        roi_table = "org_match_table"

        calculate_linking_consensus(
            zarr_url=zarr_url,
            init_args=init_args,
            roi_table=roi_table,
        )

        output_table_path = f"{zarr_url}/tables/{roi_table}_consensus"

        output = ad.read_zarr(output_table_path).to_df().to_numpy()

        assert_almost_equal(output, test_calculate_linking_consensus_expected_output)


def test_relabel_by_linking_consensus(linking_zenodo_zarrs, name=name_mip):
    zarr_urls = select_zarr_urls(name, linking_zenodo_zarrs)
    parallelization_list = init_select_all_knowing_reference(
        zarr_urls=zarr_urls,
        zarr_dir="",
        reference_acquisition=0,
    )
    for img in parallelization_list["parallelization_list"]:
        zarr_url = img["zarr_url"]
        init_args = img["init_args"]
        label_name = "org"
        consensus_table = "org_match_table_consensus"

        relabel_by_linking_consensus(
            zarr_url=zarr_url,
            init_args=init_args,
            label_name=label_name,
            consensus_table=consensus_table,
        )

        output_table_path = f"{zarr_url}/tables/{label_name}_linked_ROI_table"
        output = ad.read_zarr(output_table_path).to_df().to_numpy()
        assert_almost_equal(
            output,
            test_relabel_by_linking_consensus_output_dict[Path(zarr_url).name],
            decimal=3,
        )


def test_calculate_platymatch_registration(linking_zenodo_zarrs, name=name_3d):
    zarr_urls = select_zarr_urls(name, linking_zenodo_zarrs)
    parallelization_list = init_select_multiplexing_pairs(
        zarr_urls=zarr_urls,
        zarr_dir="",
        reference_acquisition=0,
    )

    for img in parallelization_list["parallelization_list"]:
        zarr_url = img["zarr_url"]
        init_args = img["init_args"]
        label_name_to_register = "nuc"
        label_name_obj = "org"
        roi_table = "org_ROI_table"
        channel = ChannelInputModel(wavelength_id="A04_C01")

        calculate_platymatch_registration(
            zarr_url=zarr_url,
            init_args=init_args,
            label_name_to_register=label_name_to_register,
            label_name_obj=label_name_obj,
            roi_table=roi_table,
            level=0,
            save_transformation=True,
            mask_by_parent=True,
            calculate_ffd=True,
            seg_channel=channel,
            volume_filter=True,
            volume_filter_threshold=0.10,
        )

        output_table_path_affine = (
            f"{zarr_url}/tables/{label_name_to_register}_match_table_affine"
        )
        output_affine = ad.read_zarr(output_table_path_affine).to_df().to_numpy()
        output_table_path_ffd = (
            f"{zarr_url}/tables/{label_name_to_register}_match_table_ffd"
        )
        output_ffd = ad.read_zarr(output_table_path_ffd).to_df().to_numpy()
        # test that matches are correct; ignore confidence columns
        assert_almost_equal(
            output_affine[:, 0:2],
            test_calculate_platymatch_registration_output,
            decimal=3,
        )
        assert_almost_equal(
            output_ffd[:, 0:2], test_calculate_platymatch_registration_output, decimal=3
        )
