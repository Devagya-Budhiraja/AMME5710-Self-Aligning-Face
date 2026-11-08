# Self-Aligning Face Scanner with 3D Liveness Check and ID Matching

A small-scale airport e-gate built around one USB webcam carried by an upright XY plotter.
The gate reads a printed mock ID card, moves the camera to centre the traveller's face,
asks them to take off glasses or a hat, checks that the face is three-dimensional by
sliding the camera 40 mm between two still pictures, and then compares the live face with
both the card photo and an enrolled record photo. If the face doesn't match, it shows a
STOP screen and alerts an officer.

Michael Delano, Devagya Budhiraja and Shun Ying Wong. AMME5710 major project, University of Sydney, 2026.

## How the gate works

| Step | What happens | Main methods | Code |
|---|---|---|---|
| 1. Scan ID | Find the card, flatten it, read the 4-digit number, look up the record | adaptive threshold, contours, homography, HOG + SVM digits | `id_card.py`, `digits.py` |
| 2. Position | Move the camera until the nose is centred | YuNet landmarks, calibrated image-to-rig mapping, proportional control | `face_follow.py` |
| 3. Glasses / hat | Ask the traveller to remove them | eye alignment, HOG + HSV features, RBF SVM | `face_align.py`, `accessories.py` |
| 4. Live check | Camera stops 20 mm either side of centre, stereo pairs tested for depth | SIFT, depth from disparity, plane / homography / quadratic tests, RANSAC plane of the surroundings | `face_liveness.py`, `stereo_face_liveness.py` |
| 5. Face match | Live face vs card photo and vs record photo | SFace embedding, threshold set on the gate camera | `id_match.py` |
| Alert | STOP screen, chime, officer view, one-to-many search | | `id_alert.py` |

`egate/main.py` runs all of these in order. Without the plotter, `egate/run_no_rig.py` runs the
same gate on a plain webcam and swaps the stereo check for a head-turn test.

## Repository layout

```
egate/                  the gate itself
  main.py               full gate on the rig
  run_no_rig.py         full gate on a plain webcam (head-turn live check)
  rig_grid.py           GRBL serial control of the plotter
  face_follow.py        rig calibration and centring on the nose
  face_liveness.py      stereo pairs on the rig and the live / not-live decision
  stereo_face_liveness.py  3D points and tests A to C for one stereo pair
  face_detect.py        YuNet face and landmark detection
  face_align.py         eye alignment and crop regions
  accessories.py        glasses and hat classifiers (training and live use)
  id_card.py            card detection, flattening, sharpness and orientation
  digits.py             digit reader (training and live use)
  id_match.py           face features, LFW benchmark and enrolment
  id_alert.py           STOP screen, officer view and one-to-many search
  make_id_cards.py      printable mock ID cards and the records file
  paths.py              folder locations
tools/                  one-off scripts
  find_cameras.py       which camera number is the rig webcam
  capture_grid.py       checkerboard images for lens calibration
  prep_celeba.py        glasses / hat training sets from CelebA
  get_lfw.py            download the LFW pairs
  calibrate_ids.py      set the face match threshold on the gate camera
models/                 trained models and the OpenCV ONNX models
results/                cross-validation table, card check log, early liveness logs
data/                   your own photos and datasets (not in the repository, see data/README.md)
calibration/            per-rig settings written at run time
```

## Setup

Python 3.11 or newer.

```bash
pip install -r requirements.txt
```

The trained models in `models/` were saved with scikit-learn 1.8. A newer version loads them
with a warning. Retrain them (see below) if anything looks wrong.

Hardware used:
- an upright XY plotter running GRBL 1.1 (EleksMaker Mana SE), usable travel 323 x 248 mm
- a 1280 x 720 USB webcam mounted on its side on the carriage
- foot markers about 0.8 to 0.95 m in front of the camera

Set the serial port in `egate/rig_grid.py` (`PORT`) and the webcam number in
`egate/face_liveness.py` (`CAMERA_INDEX`). `python -m tools.find_cameras` shows which number is which.

All commands are run from the repository root.

## Before the first run

1. **Make the ID cards.** Put one front-on photo per person in `data/card_photos/`, named
   `Name_1234.jpg`, then run
   ```bash
   python -m egate.make_id_cards
   ```
   This writes the cards and a print sheet to `data/cards/`, the records file
   `data/cards/records.csv`, and copies the record photos to `data/ids/`. Print the sheet at
   100% scale.
2. **Enrol the record photos.**
   ```bash
   python -m egate.id_match
   ```
3. **Set the match threshold on your camera** (recommended, since a threshold from LFW does not
   carry over to front-on photos):
   ```bash
   python -m tools.calibrate_ids
   ```

## Running the gate

On the rig, with the carriage in the bottom-left corner:

```bash
python -m egate.main
```

Press SPACE to connect the rig, then `c` once with a face in view to calibrate the tracking
(the result is kept in `calibration/`). Other keys: `n` new traveller, `d` operator details,
`v` voice on/off, `r` turn the view, `w` full screen, `q` quit.

With only a webcam:

```bash
python -m egate.run_no_rig
```

Each stage can also be run on its own, for example `python -m egate.face_follow` (tracking
only), `python -m egate.face_liveness` (tracking and the 3D check) or `python -m egate.id_card`
(card reading and a quick face check).

## Retraining the models

| Model | Data | Command |
|---|---|---|
| Glasses / hat | CelebA in `data/celeba/` | `python -m tools.prep_celeba`, then `python -m egate.accessories` |
| Digits | rendered from the card font, no download needed | `python -m egate.digits` |
| Eigenfaces | FFHQ thumbnails in `data/ffhq_thumbs/` | set `RUN_EIGEN_TRAINING = True` in `egate/id_match.py`, then `python -m egate.id_match` |
| LFW benchmark | `python -m tools.get_lfw` | set `RUN_LFW = True` in `egate/id_match.py`, then `python -m egate.id_match` |
| Lens calibration | checkerboard on the rig | `python -m tools.capture_grid`, then `python -m egate.face_liveness --intrinsics data/calib_poses_<date>_<time>` |

The YuNet and SFace models come from the [OpenCV Zoo](https://github.com/opencv/opencv_zoo).

## Results

| Stage | Result |
|---|---|
| Glasses (held-out CelebA) | 96.5% accuracy, F1 0.965 |
| Hat (held-out CelebA) | 92.7% accuracy, F1 0.928 |
| Digits | 1,000 / 1,000 rendered test digits, all numbers correct on cards at least 180 px wide |
| Face match on the gate camera | SFace 98.2% balanced accuracy (HOG 61.6%) at threshold 1.128 |
| Face match on LFW | HOG 64.3%, Eigenfaces 62.5% |

The main lesson was that the face match threshold has to be set on the camera the gate uses.
The threshold chosen on LFW would have accepted every pair of different people on the gate's
evenly lit, front-on photos. The full write-up is in the project report.

## Privacy

The repository contains no photos of real people. Card photos, record photos, calibration
frames and the session database (`session_db/`) stay on your machine and are ignored by git.
