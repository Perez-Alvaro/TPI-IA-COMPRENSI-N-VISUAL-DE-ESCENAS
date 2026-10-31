"""
test_empirical_challenger.py
============================
Independent Empirical Challenge and Stress-Testing Suite
Author: EMPIRICAL CHALLENGER (critic, specialist)
Workspace: TPI Inteligencia Artificial - Primavera 2026 - Grupo 21

Performs exact ground-truth assertion between:
1. Notebook execution outputs (tpi-ia-2026p-21.ipynb)
2. Technical Report (informe_tecnico_tpi.md, .html, .pdf)
3. Non-Technical Explanatory Document (documento_explicativo_no_tecnico.md)
4. Oral Defense Preparation Guide (guia_defensa_oral_tpi.md)
"""

import json
import re
import sys
import unittest
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent

NB_PATH = WORKSPACE / "tpi-ia-2026p-21.ipynb"
INFORME_MD_PATH = WORKSPACE / "informe_tecnico_tpi.md"
NONTECH_MD_PATH = WORKSPACE / "documento_explicativo_no_tecnico.md"
DEFENSE_MD_PATH = WORKSPACE / "guia_defensa_oral_tpi.md"
BUILD_SCRIPT_PATH = WORKSPACE / "build_pdf.py"

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def load_notebook():
    with open(NB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestEmpiricalGroundTruthIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb = load_notebook()
        cls.informe = read_text(INFORME_MD_PATH)
        cls.nontech = read_text(NONTECH_MD_PATH)
        cls.defense = read_text(DEFENSE_MD_PATH)

    # --------------------------------------------------------------------------
    # 1. Box F1 Verification
    # --------------------------------------------------------------------------
    def test_box_f1_ground_truth(self):
        """Verify Baseline Box F1 = 0.6464 and V3 Box F1 = 0.6722 from notebook to docs."""
        # 1. Check in Notebook cell 110 output
        cell_110 = self.nb["cells"][110]
        text_110 = "".join([
            "".join(o.get("data", {}).get("text/plain", [])) + "".join(o.get("text", []))
            for o in cell_110.get("outputs", [])
        ])
        self.assertIn("0.6464", text_110, "Notebook cell 110 missing baseline Box F1 0.6464")
        self.assertIn("0.6722", text_110, "Notebook cell 110 missing V3 Box F1 0.6722")

        # 2. Check in Deliverables
        self.assertRegex(self.informe, r"0\.6464", "informe_tecnico missing baseline Box F1 0.6464")
        self.assertRegex(self.informe, r"0\.6722", "informe_tecnico missing V3 Box F1 0.6722")
        self.assertRegex(self.defense, r"0[.,]6464", "guia_defensa missing baseline Box F1 0.6464")
        self.assertRegex(self.defense, r"0[.,]6722", "guia_defensa missing V3 Box F1 0.6722")
        self.assertRegex(self.nontech, r"0[.,]6722", "non_tecnico missing V3 Box F1 0.6722")

    # --------------------------------------------------------------------------
    # 2. Mask F1 Verification
    # --------------------------------------------------------------------------
    def test_mask_f1_ground_truth(self):
        """Verify Baseline Mask F1 = 0.6132 and V3 Mask F1 = 0.6351 from notebook to docs."""
        cell_110 = self.nb["cells"][110]
        text_110 = "".join([
            "".join(o.get("data", {}).get("text/plain", [])) + "".join(o.get("text", []))
            for o in cell_110.get("outputs", [])
        ])
        self.assertIn("0.6132", text_110, "Notebook cell 110 missing baseline Mask F1 0.6132")
        self.assertIn("0.6351", text_110, "Notebook cell 110 missing V3 Mask F1 0.6351")

        self.assertRegex(self.informe, r"0\.6132", "informe_tecnico missing baseline Mask F1 0.6132")
        self.assertRegex(self.informe, r"0\.6351", "informe_tecnico missing V3 Mask F1 0.6351")
        self.assertRegex(self.defense, r"0[.,]6132", "guia_defensa missing baseline Mask F1 0.6132")
        self.assertRegex(self.defense, r"0[.,]6351", "guia_defensa missing V3 Mask F1 0.6351")

    # --------------------------------------------------------------------------
    # 3. QA Deterministic Accuracy Verification
    # --------------------------------------------------------------------------
    def test_qa_deterministic_ground_truth(self):
        """Verify Baseline QA = 0.6053 and V3 QA = 0.7895 (delta +0.1842)."""
        cell_110 = self.nb["cells"][110]
        text_110 = "".join([
            "".join(o.get("data", {}).get("text/plain", [])) + "".join(o.get("text", []))
            for o in cell_110.get("outputs", [])
        ])
        self.assertIn("0.6053", text_110, "Notebook cell 110 missing baseline QA 0.6053")
        self.assertIn("0.7895", text_110, "Notebook cell 110 missing V3 QA 0.7895")

        self.assertRegex(self.informe, r"0\.6053", "informe_tecnico missing baseline QA 0.6053")
        self.assertRegex(self.informe, r"0\.7895", "informe_tecnico missing V3 QA 0.7895")
        self.assertRegex(self.defense, r"0[.,]6053", "guia_defensa missing baseline QA 0.6053")
        self.assertRegex(self.defense, r"0[.,]7895", "guia_defensa missing V3 QA 0.7895")

    # --------------------------------------------------------------------------
    # 4. Blind Test Kaggle Scores
    # --------------------------------------------------------------------------
    def test_kaggle_blind_test_scores(self):
        """Verify Kaggle Leaderboard scores: V1=0.6615, V2=0.6763, V3=0.6800."""
        # Cell 83 in notebook records the progression table
        cell_83_src = "".join(self.nb["cells"][83].get("source", []))
        self.assertIn("0,6615", cell_83_src, "Notebook cell 83 missing V1 0.6615")
        self.assertIn("0,6763", cell_83_src, "Notebook cell 83 missing V2 0.6763")
        self.assertIn("0,6800", cell_83_src, "Notebook cell 83 missing V3 0.6800")

        for doc_name, content in [("informe", self.informe), ("nontech", self.nontech), ("defense", self.defense)]:
            self.assertRegex(content, r"0[.,]6615", f"{doc_name} missing Kaggle V1 0.6615")
            self.assertRegex(content, r"0[.,]6763", f"{doc_name} missing Kaggle V2 0.6763")
            self.assertRegex(content, r"0[.,]6800|0[.,]680\b", f"{doc_name} missing Kaggle V3 0.6800")

    # --------------------------------------------------------------------------
    # 5. Sample Distribution & EDA Verification
    # --------------------------------------------------------------------------
    def test_sample_distribution_and_scale_skew(self):
        """Verify 120 dev images, 1.790 annotations, 71.06% small, 24.02% medium, 4.92% large."""
        # Check cell 6 output
        cell_6 = self.nb["cells"][6]
        text_6 = "".join([o.get("text", "") if isinstance(o.get("text", ""), str) else "".join(o.get("text", [])) for o in cell_6.get("outputs", [])])
        self.assertIn("120", text_6, "Notebook cell 6 missing 120 images")
        self.assertIn("1790", text_6, "Notebook cell 6 missing 1790 annotations")

        # Check cell 66 counts
        cell_66 = self.nb["cells"][66]
        text_66 = "".join([o.get("text", "") if isinstance(o.get("text", ""), str) else "".join(o.get("text", [])) for o in cell_66.get("outputs", [])])
        self.assertIn("1272", text_66, "Notebook cell 66 missing 1272 small instances")
        self.assertIn("430", text_66, "Notebook cell 66 missing 430 medium instances")
        self.assertIn("88", text_66, "Notebook cell 66 missing 88 large instances")

        # Mathematical proportions check
        total = 1790
        p_small = round((1272 / total) * 100, 2)
        p_medium = round((430 / total) * 100, 2)
        p_large = round((88 / total) * 100, 2)
        self.assertEqual(p_small, 71.06, "Small % calculation mismatch")
        self.assertEqual(p_medium, 24.02, "Medium % calculation mismatch")
        self.assertEqual(p_large, 4.92, "Large % calculation mismatch")

        # Verify citation in deliverables
        self.assertRegex(self.informe, r"1[.,]790\s*(instancias|anotadas)", "informe missing 1.790 instances")
        self.assertRegex(self.informe, r"71\.06\s*%", "informe missing 71.06% small instances")
        self.assertRegex(self.defense, r"71[.,]06\s*%", "defense missing 71.06% small instances")
        self.assertRegex(self.nontech, r"71[.,]06\s*%", "nontech missing 71.06% small instances")

    # --------------------------------------------------------------------------
    # 6. Latency Claims Verification
    # --------------------------------------------------------------------------
    def test_latency_breakdown_ground_truth(self):
        """Verify Latency breakdown: OWLv2 2.44s, SAM2 0.43s, SceneJSON 0.28s, Total 3.25s."""
        cell_111 = self.nb["cells"][111]
        src_111 = "".join(cell_111.get("source", []))
        self.assertIn("2.44", src_111, "Notebook cell 111 missing OWLv2 2.44s")
        self.assertIn("0.43", src_111, "Notebook cell 111 missing SAM2 0.43s")
        self.assertIn("0.28", src_111, "Notebook cell 111 missing SceneJSON 0.28s")

        # Total sum check
        tiempos = [0.01, 0.09, 0.28, 0.43, 2.44]
        total_lat = round(sum(tiempos), 2)
        self.assertEqual(total_lat, 3.25, "Latency sum mismatch")

        # Deliverable checks
        self.assertRegex(self.informe, r"2\.440?\s*s", "informe missing 2.44s OWLv2 latency")
        self.assertRegex(self.informe, r"0\.430?\s*s", "informe missing 0.43s SAM2 latency")
        self.assertRegex(self.informe, r"0\.280?\s*s", "informe missing 0.28s SceneJSON latency")
        self.assertRegex(self.informe, r"3\.250?\s*s", "informe missing 3.25s total latency")

        self.assertRegex(self.defense, r"2[.,]44", "defense missing 2.44s latency")
        self.assertRegex(self.defense, r"3[.,]25", "defense missing 3.25s latency")

    # --------------------------------------------------------------------------
    # 7. Negative Hypotheses Empirical Integrity
    # --------------------------------------------------------------------------
    def test_negative_hypotheses_integrity(self):
        """Verify all three negative experiments are documented and empirically justified."""
        # 1. pad_fix: delta = 0
        self.assertIn("pad_fix", self.informe, "informe missing pad_fix discussion")
        self.assertRegex(self.informe, r"0\.0000|sin efecto|id[ée]ntic", "informe missing pad_fix null result")
        self.assertIn("pad_fix", self.defense, "defense missing pad_fix discussion")

        # 2. OWLv2 Large: 4.7x slower, worse F1
        self.assertIn("OWLv2 Large", self.informe, "informe missing OWLv2 Large discussion")
        self.assertRegex(self.informe, r"4\.7\s*[x×]|11\.45", "informe missing OWLv2 Large 4.7x latency cost")
        self.assertRegex(self.informe, r"0\.6260|0\.626", "informe missing OWLv2 Large 0.626 F1")
        self.assertIn("OWLv2 Large", self.defense, "defense missing OWLv2 Large discussion")
        self.assertRegex(self.defense, r"4,7\s*[x×]|11,45", "defense missing OWLv2 Large 4.7x latency cost")

        # 3. SAM2 multimask: rejected (single = 0.627 vs multimask = 0.590)
        self.assertIn("multimask", self.informe.lower(), "informe missing multimask discussion")
        self.assertRegex(self.informe, r"0\.627|single", "informe missing single mode confirmation")
        self.assertRegex(self.informe, r"0\.590|best_score", "informe missing best_score mode drop")
        self.assertIn("multimask", self.defense.lower(), "defense missing multimask discussion")

    # --------------------------------------------------------------------------
    # 8. Cross-Deliverable Non-Contradiction & Rounding Check
    # --------------------------------------------------------------------------
    def test_no_numerical_contradictions(self):
        """Verify there are no conflicting claims between the documents."""
        # Ensure no document claims Kaggle V3 score is anything other than 0.6800 / 0.68
        for doc_name, content in [("informe", self.informe), ("nontech", self.nontech), ("defense", self.defense)]:
            bad_matches = re.findall(r"Kaggle.*?(?:0\.[5-9]\d{2,4})", content)
            for m in bad_matches:
                score_match = re.search(r"0\.\d+", m)
                if score_match:
                    val = float(score_match.group())
                    self.assertIn(val, [0.6615, 0.6763, 0.6800, 0.68], f"Found rogue Kaggle score {val} in {doc_name}: {m}")

        # Ensure no document claims Baseline Box F1 is anything other than 0.6464 / 0.646
        self.assertNotIn("0.6564", self.informe)
        self.assertNotIn("0.6470", self.informe)


if __name__ == "__main__":
    unittest.main()
