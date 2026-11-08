"""Download the LFW pairs used by the face matching benchmark (python -m tools.get_lfw)."""

import os

from sklearn.datasets import fetch_lfw_pairs

from egate.paths import DATA_DIR

lfw = fetch_lfw_pairs(subset="10_folds", data_home=os.path.join(DATA_DIR, "lfw"))
print("LFW downloaded:", lfw.pairs.shape)
