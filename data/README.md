# data

Nothing in this folder is committed, because it holds photos of people and large datasets.
The code expects:

| Folder | Contents | Made by |
|---|---|---|
| `card_photos/` | one photo per person, `Name_1234.jpg` (add `_fake` for a doctored card) | you |
| `cards/` | card images, print sheet and `records.csv` | `python -m egate.make_id_cards` |
| `ids/` | record photos, `Name.jpg` | `python -m egate.make_id_cards` |
| `calib/` | gate-camera frames for the match threshold, `Name_01.jpg` ... | `python -m tools.calibrate_ids` |
| `calib_poses_*/` | checkerboard images for lens calibration | `python -m tools.capture_grid` |
| `celeba/` | CelebA images and attribute files | download |
| `sets/`, `aligned/` | CelebA training sets and aligned faces | `python -m tools.prep_celeba` |
| `ffhq_thumbs/` | FFHQ thumbnails for the Eigenfaces | download |
| `lfw/` | LFW pairs | `python -m tools.get_lfw` |
