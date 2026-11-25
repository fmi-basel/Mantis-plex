<img width="4616" height="2094" alt="Asset 16@600x" src="https://github.com/user-attachments/assets/d5f04772-56e3-4b94-9758-04306e425144" />


<br> `Mantis-plex` is a Python package for multiplexed image registration and object linking, developed as part of the [Mantis ecosystem](https://github.com/fmi-basel/Mantis) for high-content, multiplexed, and volumetric microscopy image analysis.

`Mantis-plex` provides [Fractal](https://fractal-analytics-platform.github.io/) tasks for rigid and non-rigid image registration, linking of segmented objects across imaging rounds, and illumination correction across rounds. It operates on OME-Zarr datasets and supports region-of-interest (ROI)-based processing.

## Functionality

### 1. Object linking across imaging rounds

The `calculate_object_linking` task establishes correspondences between segmented objects across imaging rounds. The `calculate_linking_consensus` task identifies consistent object correspondences across multiple rounds, and the `relabel_by_linking_consensus` task assigns consistent labels to corresponding objects.

This enables individual objects, such as organoids or tissue regions, to be identified and processed across multiple rounds of multiplexed imaging.

- **Input:** Segmentation label images and corresponding ROI tables from multiple imaging rounds.
- **Output:** Object linking tables and consistently relabeled segmentation images across imaging rounds.

### 2. Rigid image registration

The `calculate_2d_rigid_shift`, `shift_by_rigid_shift`, and `shift_by_shift` tasks calculate and apply translational shifts to align microscopy images across imaging rounds.

- **Input:** Reference and moving microscopy images or previously calculated shifts.
- **Output:** Registration shifts and spatially aligned images.

### 3. Non-rigid image registration

The `calculate_warpfield_registration` and `apply_warpfield_registration` tasks estimate and apply deformation fields to align volumetric microscopy images across imaging rounds, accounting for local tissue deformations that cannot be corrected by rigid registration alone.

- **Input:** Reference and moving 3D microscopy images and corresponding ROIs.
- **Output:** Deformation fields and non-rigidly registered images.

### 4. Post-registration processing

The `post_registration_cleanup`, `detect_clipped_rois_across_rounds`, and `copy_data_from_ref_to_moving_rounds` tasks support the preparation of registered multiplexed datasets for downstream analysis. These tasks enable cleanup of registered data, identification of ROIs that are clipped in one or more imaging rounds, and propagation of reference-round data to corresponding moving rounds.

- **Input:** Registered multiplexed OME-Zarr datasets and corresponding segmentation label images and ROI tables.
- **Output:** Processed and consistently annotated multiplexed datasets for downstream analysis.

### 5. Z-illumination correction

The `calculate_z_illumination_correction` and `apply_z_illumination_correction` tasks estimate and correct depth-dependent intensity variations in volumetric microscopy images, improving intensity consistency along the Z-axis.

- **Input:** 3D microscopy images from an OME-Zarr dataset.
- **Output:** Z-illumination correction profiles and intensity-corrected images.

### 6. PlatyMatch registration

The `calculate_platymatch_registration` task uses [PlatyMatch](https://github.com/juglab/PlatyMatch) to estimate spatial transformations between imaging rounds based on the spatial organization of segmented objects, such as nuclei. This enables object-based registration of individual 3D tissue regions across imaging rounds.

- **Input:** Segmented objects and their spatial coordinates in reference and moving imaging rounds.
- **Output:** Object-based registration transformations.
  
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
