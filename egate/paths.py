"""Folder locations, all relative to the repository root."""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
MODEL_DIR = os.path.join(ROOT, "models")
RESULTS_DIR = os.path.join(ROOT, "results")
FIGURE_DIR = os.path.join(RESULTS_DIR, "figures")
CALIB_DIR = os.path.join(ROOT, "calibration")     # per-rig settings written at run time
