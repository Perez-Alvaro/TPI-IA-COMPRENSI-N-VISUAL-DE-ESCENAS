"""
test_e2e_deliverables.py
========================
Automated End-to-End (E2E) Deliverables Verification Test Suite
TPI Inteligencia Artificial - Primavera 2026 - Grupo 21
Comprensión Visual de Escenas

Verifies the final deliverable artifacts:
1. Technical Report (INFORME_TPI_IA_2026P_21.md)
2. Submission CSV (submission.csv)
3. Jupyter Notebook (tpi-ia-2026p-21.ipynb)
4. Oral Defense Guide (guia_defensa_oral_tpi.md)
5. Non-Technical Explanatory Document (documento_explicativo_no_tecnico.md)
6. Repository README (README.md)
"""

import os
import sys
import re
import json
import csv
import unittest
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent

PATH_REPORT_MD = WORKSPACE_DIR / "INFORME_TPI_IA_2026P_21.md"
PATH_SUBMISSION_CSV = WORKSPACE_DIR / "submission.csv"
PATH_NOTEBOOK_IPYNB = WORKSPACE_DIR / "tpi-ia-2026p-21.ipynb"
PATH_NONTECH_MD = WORKSPACE_DIR / "documento_explicativo_no_tecnico.md"
PATH_DEFENSE_MD = WORKSPACE_DIR / "guia_defensa_oral_tpi.md"
PATH_README_MD = WORKSPACE_DIR / "README.md"


def read_text_file(path: Path) -> str:
    """Helper to read text file using UTF-8 encoding."""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


class TestTier1DeliverablesCoverage(unittest.TestCase):
    """Tier 1 validates that all required deliverable artifacts exist and are non-empty."""

    def test_t1_1_primary_deliverables_exist(self):
        """Verify all final deliverable files exist at workspace root and are non-empty."""
        expected_artifacts = [
            ("INFORME_TPI_IA_2026P_21.md", PATH_REPORT_MD),
            ("submission.csv", PATH_SUBMISSION_CSV),
            ("tpi-ia-2026p-21.ipynb", PATH_NOTEBOOK_IPYNB),
            ("documento_explicativo_no_tecnico.md", PATH_NONTECH_MD),
            ("guia_defensa_oral_tpi.md", PATH_DEFENSE_MD),
            ("README.md", PATH_README_MD),
        ]

        missing = []
        empty = []
        for name, path in expected_artifacts:
            if not path.exists():
                missing.append(name)
            elif path.stat().st_size == 0:
                empty.append(name)

        error_msg = ""
        if missing:
            error_msg += f"Missing deliverables ({len(missing)}): {', '.join(missing)}. "
        if empty:
            error_msg += f"Empty deliverables ({len(empty)}): {', '.join(empty)}. "

        self.assertFalse(missing or empty, error_msg.strip())

    def test_t1_2_technical_report_structure(self):
        """Verify the academic sections exist in INFORME_TPI_IA_2026P_21.md."""
        content = read_text_file(PATH_REPORT_MD)
        self.assertGreater(len(content), 10000, "INFORME_TPI_IA_2026P_21.md is too short")

        required_sections = [
            ("Resumen ejecutivo", r"##\s*Resumen ejecutivo"),
            ("1. Exploración del dataset", r"##\s*1\.\s*Exploración del dataset"),
            ("2. Pipeline de percepción y representación", r"##\s*2\.\s*Pipeline de percepción"),
            ("3. Módulo de preguntas y respuestas", r"##\s*3\.\s*Módulo de preguntas"),
            ("4. Mejoras y decisiones de diseño", r"##\s*4\.\s*Mejoras y decisiones"),
            ("5. Evaluación de resultados", r"##\s*5\.\s*Evaluación de resultados"),
            ("6. Discusión y análisis crítico", r"##\s*6\.\s*Discusión y análisis"),
            ("7. Conclusiones", r"##\s*7\.\s*Conclusiones"),
            ("8. Trabajo futuro", r"##\s*8\.\s*Trabajo futuro"),
        ]

        for sec_name, pattern in required_sections:
            match = re.search(pattern, content)
            self.assertIsNotNone(match, f"Section '{sec_name}' not found in INFORME_TPI_IA_2026P_21.md")

    def test_t1_3_submission_csv_format(self):
        """Verify submission.csv has 80 test image predictions with image_id and SceneJSON columns."""
        self.assertTrue(PATH_SUBMISSION_CSV.exists(), "submission.csv not found")
        csv.field_size_limit(2147483647)
        with open(PATH_SUBMISSION_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, ["image_id", "SceneJSON"], "Header must be image_id,SceneJSON")
            rows = list(reader)
            self.assertEqual(len(rows), 80, f"Expected 80 predictions in submission.csv, found {len(rows)}")
            for row in rows:
                self.assertEqual(len(row), 2, "Each row must have exactly 2 columns")
                self.assertTrue(row[0].strip(), "image_id cannot be empty")
                self.assertTrue(row[1].strip().startswith("{"), "SceneJSON must be a JSON object string")

    def test_t1_4_notebook_validity(self):
        """Verify tpi-ia-2026p-21.ipynb is valid JSON and contains cells with outputs."""
        self.assertTrue(PATH_NOTEBOOK_IPYNB.exists(), "Notebook not found")
        with open(PATH_NOTEBOOK_IPYNB, "r", encoding="utf-8") as f:
            nb = json.load(f)
        self.assertIn("cells", nb, "Notebook missing cells")
        self.assertGreaterEqual(len(nb["cells"]), 70, "Notebook should have >= 70 cells")


class TestTier2DeliverablesContent(unittest.TestCase):
    """Tier 2 validates quantitative integrity, metrics consistency, and theoretical alignment."""

    def test_t2_1_metrics_consistency_across_deliverables(self):
        """Verify metrics (0.6926 Kaggle, 0.6722 Box F1, 0.6351 Mask F1) in report and guides."""
        report_text = read_text_file(PATH_REPORT_MD)
        defense_text = read_text_file(PATH_DEFENSE_MD)
        nontech_text = read_text_file(PATH_NONTECH_MD)

        for text, name in [(report_text, "INFORME_TPI_IA_2026P_21.md"),
                           (defense_text, "guia_defensa_oral_tpi.md"),
                           (nontech_text, "documento_explicativo_no_tecnico.md")]:
            self.assertTrue("0,6926" in text or "0.6926" in text, f"Kaggle score 0.6926 not found in {name}")
            self.assertTrue("0,6722" in text or "0.6722" in text, f"Box F1 0.6722 not found in {name}")
            self.assertTrue("0,6351" in text or "0.6351" in text, f"Mask F1 0.6351 not found in {name}")

    def test_t2_2_oral_defense_guide_structure(self):
        """Verify guia_defensa_oral_tpi.md contains 10-minute presentation guide and Q&A bank."""
        content = read_text_file(PATH_DEFENSE_MD)
        self.assertIn("CRONOGRAMA MAESTRO DE DEFENSA (10 MINUTOS ESTRICTOS)", content)
        self.assertIn("Gabriel Ocampo", content)
        self.assertIn("Valentina Pecchio", content)
        self.assertIn("Manuel López Quinteros", content)
        self.assertIn("Emmanuel Ricardo Chaile", content)
        self.assertIn("Alvaro Perez", content)
        self.assertIn("Bloque A:", content)
        self.assertIn("Bloque G:", content)
        self.assertIn("0,6926", content)

    def test_t2_3_non_technical_document_pipeline_stages(self):
        """Verify documento_explicativo_no_tecnico.md covers all pipeline stages intuitively."""
        content = read_text_file(PATH_NONTECH_MD)
        self.assertIn("ETAPA 1: EL DETECTIVE", content)
        self.assertIn("ETAPA 2: EL ESCULTOR", content)
        self.assertIn("ETAPA 3: EL CARTÓGRAFO", content)
        self.assertIn("ETAPA 4: EL VERIFICADOR", content)
        self.assertIn("ETAPA 5: EL INSPECTOR", content)
        self.assertIn("0,6926", content)


class TestTier3MetadataAndCleanliness(unittest.TestCase):
    """Tier 3 validates metadata, student and teacher references, and absence of superseded files."""

    def test_t3_1_teachers_and_students_referenced(self):
        """Verify all 5 student authors and professors are recognized in final report and oral guide."""
        defense_text = read_text_file(PATH_DEFENSE_MD)
        report_text = read_text_file(PATH_REPORT_MD)

        for text in [defense_text, report_text]:
            self.assertIn("García, Mario", text)
            self.assertIn("Guzman, Analía", text)
            self.assertIn("Gramatica, Martin", text)
            self.assertIn("89767", text)
            self.assertIn("99026", text)
            self.assertIn("93368", text)
            self.assertIn("94416", text)
            self.assertIn("97986", text)

    def test_t3_2_superseded_files_removed(self):
        """Verify old superseded report files do not exist in workspace."""
        superseded = [
            WORKSPACE_DIR / "informe_tecnico_tpi.md",
            WORKSPACE_DIR / "informe_tecnico_tpi.html",
            WORKSPACE_DIR / "informe_tecnico_tpi.pdf",
            WORKSPACE_DIR / "build_pdf.py",
        ]
        existing_superseded = [p.name for p in superseded if p.exists()]
        self.assertEqual(existing_superseded, [], f"Old files should be removed: {existing_superseded}")


if __name__ == "__main__":
    unittest.main()
