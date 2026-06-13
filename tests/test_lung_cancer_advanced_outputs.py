import os
import subprocess
import sys
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "example" / "lung-cancer" / "analysis" / "lung_cancer_analysis.py"
OUTPUT_DIR = REPO_ROOT / "example" / "lung-cancer" / "analysis" / "outputs" / "kaggle_survey"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"
README_PATH = REPO_ROOT / "example" / "lung-cancer" / "README.md"


ADVANCED_TABLES = [
    TABLE_DIR / "correlation_matrix.csv",
    TABLE_DIR / "pca_explained_variance.csv",
    TABLE_DIR / "pca_loadings.csv",
    TABLE_DIR / "calibration_table.csv",
    TABLE_DIR / "risk_deciles.csv",
    TABLE_DIR / "subgroup_odds_ratios.csv",
    TABLE_DIR / "permutation_importance.csv",
    TABLE_DIR / "model_comparison.csv",
]

ADVANCED_FIGURES = [
    FIGURE_DIR / "fig4_correlation_heatmap.png",
    FIGURE_DIR / "fig5_pca_biplot.png",
    FIGURE_DIR / "fig6_subgroup_forest.png",
    FIGURE_DIR / "fig7_calibration_distribution.png",
    FIGURE_DIR / "fig8_clustermap.png",
    FIGURE_DIR / "fig9_permutation_importance.png",
]


class LungCancerAdvancedOutputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_outputs = ADVANCED_TABLES + ADVANCED_FIGURES
        cls.previous_mtimes = {
            path: path.stat().st_mtime_ns
            for path in cls.expected_outputs
            if path.exists()
        }

        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = "/tmp/python-med-stats-pycache"
        env["MPLCONFIGDIR"] = "/tmp/python-med-stats-mpl"
        env["XDG_CACHE_HOME"] = "/tmp/python-med-stats-cache"

        time.sleep(0.02)
        cls.script_result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_analysis_script_generates_advanced_outputs(self):
        self.assertEqual(
            self.script_result.returncode,
            0,
            msg=f"stdout:\n{self.script_result.stdout}\nstderr:\n{self.script_result.stderr}",
        )

        missing = [str(path.relative_to(REPO_ROOT)) for path in self.expected_outputs if not path.exists()]
        self.assertEqual(missing, [], msg=f"Missing advanced outputs: {missing}")

        stale = [
            str(path.relative_to(REPO_ROOT))
            for path, previous_mtime in self.previous_mtimes.items()
            if path.stat().st_mtime_ns <= previous_mtime
        ]
        self.assertEqual(stale, [], msg=f"Advanced outputs were not regenerated: {stale}")

        empty = [
            str(path.relative_to(REPO_ROOT))
            for path in self.expected_outputs
            if path.stat().st_size <= 100
        ]
        self.assertEqual(empty, [], msg=f"Advanced outputs look empty: {empty}")

    def test_readme_documents_advanced_outputs(self):
        readme = README_PATH.read_text(encoding="utf-8")
        for path in ADVANCED_TABLES + ADVANCED_FIGURES:
            self.assertIn(path.name, readme)


if __name__ == "__main__":
    unittest.main()
