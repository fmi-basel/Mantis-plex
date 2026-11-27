<img width="4616" height="2094" alt="Asset 16@600x" src="https://github.com/user-attachments/assets/d5f04772-56e3-4b94-9758-04306e425144" />


<br> `Mantis-plex` is a Python package for multiplexed image registration and object linking, developed as part of the [Mantis ecosystem](https://github.com/fmi-basel/Mantis) for high-content, multiplexed, and volumetric microscopy image analysis.

`Mantis-plex` provides [Fractal](https://fractal-analytics-platform.github.io/) tasks for rigid and non-rigid image registration, linking of segmented objects across imaging rounds, and illumination correction across rounds. It operates on OME-Zarr datasets and supports region-of-interest (ROI)-based processing.

## Functionality

### 1. Object linking across imaging rounds

This series of tasks is used to identify and link the same individual objects across multiplexing rounds by assigning them a common consensus label ID. Objects are assumed to have been segmented in each round. Corresponding objects are identified based on pixel overlap (e.g. > 20%) after XY shift correction of well pairs. The `calculate_object_linking` task establishes pairwise links between imaging rounds, the `calculate_linking_consensus` task assigns a common consensus label ID to linked objects across all rounds, and the `relabel_by_linking_consensus` task updates the label images using these consensus IDs.


<img width="1392" height="324" alt="Screenshot 2026-11-27 at 11 58 44" src="https://github.com/user-attachments/assets/2670b0c9-44eb-483c-b746-b6a33c847039" />


- **Input:** 2D segmentation label images and their corresponding ROI tables from multiple imaging rounds.
- **Output:** Object linking tables and consistently relabeled segmentation images across imaging rounds.

### 2. Rigid label image registration

This series of tasks is used to apply a reference segmentation to multiple moving rounds via a rigid transformation. This allows a single 3D segmentation of the reference round to be propagated across the dataset. Objects are assumed to have been segmented in 2D in each round and linked. The `calculate_2d_rigid_shift` task estimates the 2D rigid transformation (XY translation and rotation) between point clouds of linked object centroids, and the `shift_by_rigid_shift` task applies this transform to selected 3D or 2D reference label images that is saved in the moving round.

<img width="1390" height="513" alt="Screenshot 2026-11-27 at 11 58 55" src="https://github.com/user-attachments/assets/2ff7cbda-911f-45e5-845e-5b4d7bb30647" />


- **Input:** 2D linked segmentation label images from multiple imaging rounds.
- **Output:** Registration shifts and transformed 3D reference segmentation in moving rounds.

### 3. Non-rigid image registration

The `calculate_warpfield_registration` and `apply_warpfield_registration` tasks estimate and apply deformation fields to align volumetric microscopy images across imaging rounds, accounting for local tissue deformations that cannot be corrected by rigid registration alone. [Warpfield](https://github.com/danionella/warpfield/tree/main) registration is calculated using raw 3D images of a marker common to both rounds (e.g. DAPI), and the resulting deformation fields are applied to all selected channels of the moving round. Registration is run pairwise on individual objects that are assumed to have been linked and registered via rigid label image registration. 

<img width="1393" height="359" alt="Screenshot 2026-11-27 at 11 59 08" src="https://github.com/user-attachments/assets/d2b98b0f-9fc5-42d9-a2ad-844b40dcc32d" />


- **Input:** Reference and moving 3D channel and label images, with corresponding objects extracted using their respective ROI tables.
- **Output:** Deformation fields per object pair and a registered 3D OME-Zarr image for each moving round, aligned to the coordinate system of the reference round to enable direct visual overlays.

Next, the `post_registration_cleanup`, `detect_clipped_rois_across_rounds`, and `copy_data_from_ref_to_moving_rounds` tasks support cleanup of registered data, identification of ROIs that are clipped in one or more imaging rounds, and propagation of reference-round data to corresponding moving rounds.

### 4. Z-illumination correction

The `calculate_z_illumination_correction` and `apply_z_illumination_correction` tasks estimate and correct depth-dependent intensity variations in volumetric microscopy images. Intensity decay along the Z-axis is estimated using a uniform stain (e.g. NHS ester) in a given round, and the resulting correction is applied to selected channels of other rounds. Correction is calculated for individual objects, which are assumed to have been linked and registered via rigid label image registration. 

<img width="1393" height="556" alt="Screenshot 2026-11-27 at 11 59 28" src="https://github.com/user-attachments/assets/717e54ba-8ab0-45b8-adaa-fea0e86b4bd7" />


- **Input:** 3D channel image (uniform stain), with objects segmented and linked across rounds.
- **Output:** Z-illumination correction profiles per object and corrected 3D OME-Zarr images for selected rounds, with each object corrected by its corresponding correction profile. 

### Legacy tasks

The `calculate_platymatch_registration` task uses [PlatyMatch](https://github.com/juglab/PlatyMatch) for 3D point cloud-based registration of imaging rounds using child object segmentation (e.g. nuclear or cell centroids). This task is retained for legacy purposes but is no longer actively maintained or recommended for new workflows.

## Installation

### From source

Clone the repository and install Mantis-plex:

```bash
git clone https://github.com/fmi-basel/Mantis-plex.git
cd Mantis-plex
pip install .
```

To include optional dependencies for warpfield registration:

```bash
pip install ".[warpfield]"
```

## License

Unless otherwise stated in each individual module, all Mantis-plex components are released under the BSD 3-Clause License, and copyright is held by the Friedrich Miescher Institute for Biomedical Research.

## Contributors

Developed in the Liberali Lab at the Friedrich Miescher Institute for Biomedical Research (FMI), Basel, Switzerland by [@nrepina](https://github.com/nrepina), with development support from [@jluethi](https://github.com/jluethi), [@lorenzocerrone](https://github.com/lorenzocerrone), [@enricotagliavini](https://github.com/enricotagliavini), and [@tibuch](https://github.com/tibuch).

Point-cloud based multiplexed linking is built on [PlatyMatch](https://github.com/juglab/PlatyMatch) ([DOI](https://doi.org/10.1007/978-3-030-66415-2_30)) by Manan Lalit.

Warpfield registration is based on [Warpfield](https://github.com/danionella/warpfield/tree/main) ([DOI](https://doi.org/10.1038/s41467-023-43741-x)).
