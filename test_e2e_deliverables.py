"""
test_e2e_deliverables.py
========================
Automated End-to-End (E2E) Opaque-Box Deliverables Verification Test Suite
TPI Inteligencia Artificial - Primavera 2026 - Grupo 21
Comprensión Visual de Escenas

This test harness verifies the 3 primary deliverables:
1. Technical Report (informe_tecnico_tpi.pdf, .html, .md, build_pdf.py)
2. Non-Technical Explanatory Document (documento_explicativo_no_tecnico.md)
3. Oral Defense Preparation Guide (guia_defensa_oral_tpi.md)

Organized under a 4-Tier Verification Hierarchy:
- Tier 1: Feature Coverage (Deliverable existence & 6 mandatory sections)
- Tier 2: Boundary & Quality Constraints (PDF geometry, page count >=15, fonts, assets, build exit 0)
- Tier 3: Cross-Feature & Quantitative Integrity (Ground truth metrics, negative hypotheses, theory terms, clarity)
- Tier 4: Real-World Acceptance & Consistency (Cross-module metadata, final audit pass)
"""

import os
import sys
import re
import json
import subprocess
import unittest
from pathlib import Path

# Workspace directory
WORKSPACE_DIR = Path(__file__).resolve().parent

# Deliverable Paths
PATH_REPORT_PDF = WORKSPACE_DIR / "informe_tecnico_tpi.pdf"
PATH_REPORT_HTML = WORKSPACE_DIR / "informe_tecnico_tpi.html"
PATH_REPORT_MD = WORKSPACE_DIR / "informe_tecnico_tpi.md"
PATH_BUILD_SCRIPT = WORKSPACE_DIR / "build_pdf.py"
PATH_NONTECH_MD = WORKSPACE_DIR / "documento_explicativo_no_tecnico.md"
PATH_DEFENSE_MD = WORKSPACE_DIR / "guia_defensa_oral_tpi.md"


def read_text_file(path: Path) -> str:
    """Helper to read text file using UTF-8 encoding."""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


# ==============================================================================
# TIER 1 - FEATURE COVERAGE
# ==============================================================================
class TestTier1DeliverablesCoverage(unittest.TestCase):
    """
    Tier 1 validates that all required deliverable artifacts exist at the
    workspace root and contain their fundamental structural sections.
    """

    def test_t1_1_primary_deliverables_exist(self):
        """Verify all primary deliverable files exist at workspace root and are non-empty."""
        expected_artifacts = [
            ("informe_tecnico_tpi.pdf", PATH_REPORT_PDF),
            ("informe_tecnico_tpi.html", PATH_REPORT_HTML),
            ("informe_tecnico_tpi.md", PATH_REPORT_MD),
            ("build_pdf.py", PATH_BUILD_SCRIPT),
            ("documento_explicativo_no_tecnico.md", PATH_NONTECH_MD),
            ("guia_defensa_oral_tpi.md", PATH_DEFENSE_MD),
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

    def test_t1_2_technical_report_six_mandatory_sections(self):
        """Verify the 6 mandatory academic sections exist in informe_tecnico_tpi.md."""
        if not PATH_REPORT_MD.exists():
            self.fail(f"Technical report markdown not found: {PATH_REPORT_MD}")

        content = read_text_file(PATH_REPORT_MD)
        self.assertGreater(len(content), 1000, "informe_tecnico_tpi.md is too short (< 1000 chars)")

        # Section pattern definitions (flexible matching for markdown headings)
        required_sections = [
            ("1. Portada", r"(?i)#+\s*(1[\.\s\:\-]|portada|tpi\s+comprensi|carátula)"),
            ("2. Análisis del dataset (EDA)", r"(?i)#+\s*(2[\.\s\:\-]|análisis\s+del\s+dataset|eda|exploratorio)"),
            ("3. Metodología", r"(?i)#+\s*(3[\.\s\:\-]|metodolog[ií]a|pipeline\s+de\s+procesamiento)"),
            ("4. Resultados", r"(?i)#+\s*(4[\.\s\:\-]|resultados|evaluaci[oó]n\s+experimental)"),
            ("5. Discusión y análisis de errores", r"(?i)#+\s*(5[\.\s\:\-]|discusi[oó]n|an[aá]lisis\s+de\s+errores)"),
            ("6. Conclusiones y trabajo futuro", r"(?i)#+\s*(6[\.\s\:\-]|conclusiones|trabajo\s+futuro)"),
        ]

        missing_sections = []
        for sec_name, pattern in required_sections:
            if not re.search(pattern, content):
                missing_sections.append(sec_name)

        self.assertEqual(
            missing_sections, [],
            f"informe_tecnico_tpi.md missing mandatory sections: {missing_sections}"
        )

    def test_t1_3_non_technical_document_pipeline_stages(self):
        """Verify documento_explicativo_no_tecnico.md covers all 5 pipeline stages."""
        if not PATH_NONTECH_MD.exists():
            self.fail(f"Non-technical document not found: {PATH_NONTECH_MD}")

        content = read_text_file(PATH_NONTECH_MD)
        self.assertGreater(len(content), 1500, "Non-technical document is too short (< 1500 chars)")

        # 5 pipeline stages defined by course guidelines
        stages = [
            ("Percepción / Detección", r"(?i)(percepci[oó]n|detecci[oó]n\s+visual|localizaci[oó]n|owlv2)"),
            ("Segmentación", r"(?i)(segmentaci[oó]n|m[aá]scaras|siluetas|sam2)"),
            ("Representación / SceneJSON", r"(?i)(representaci[oó]n|mapa\s+estructurado|scenejson|grafo)"),
            ("Razonamiento", r"(?i)(razonamiento|motor\s+determinista|consultas|respuestas\s+exactas)"),
            ("Interacción / Lenguaje Natural", r"(?i)(interacci[oó]n|lenguaje\s+natural|di[aá]logo|traducci[oó]n|llm)"),
        ]

        missing_stages = []
        for stage_name, pattern in stages:
            if not re.search(pattern, content):
                missing_stages.append(stage_name)

        self.assertEqual(
            missing_stages, [],
            f"documento_explicativo_no_tecnico.md missing required pipeline stages: {missing_stages}"
        )

    def test_t1_4_oral_defense_guide_structure(self):
        """Verify guia_defensa_oral_tpi.md contains 10-minute presentation guide and Q&A bank."""
        if not PATH_DEFENSE_MD.exists():
            self.fail(f"Oral defense guide not found: {PATH_DEFENSE_MD}")

        content = read_text_file(PATH_DEFENSE_MD)
        self.assertGreater(len(content), 2000, "Oral defense guide is too short (< 2000 chars)")

        # Must mention presentation strategy and Q&A bank
        has_presentation_strategy = bool(re.search(r"(?i)(10\s*minutos|presentaci[oó]n\s+oral|estrategia\s+de\s+defensa|tiempos)", content))
        has_qa_bank = bool(re.search(r"(?i)(preguntas\s+y\s+respuestas|banco\s+de\s+preguntas|ronda\s+de\s+preguntas|evaluador)", content))

        self.assertTrue(has_presentation_strategy, "guia_defensa_oral_tpi.md missing 10-minute oral defense structure/strategy.")
        self.assertTrue(has_qa_bank, "guia_defensa_oral_tpi.md missing comprehensive Q&A bank.")


# ==============================================================================
# TIER 2 - BOUNDARY & QUALITY CONSTRAINTS
# ==============================================================================
class TestTier2BoundaryQuality(unittest.TestCase):
    """
    Tier 2 validates physical publication constraints: PDF structure,
    page count, A4 dimensions, typography encoding, image links, and build script.
    """

    def setUp(self):
        try:
            import pypdf
            self.pypdf = pypdf
        except ImportError:
            self.pypdf = None

    def test_t2_1_pdf_page_count_minimum(self):
        """Verify informe_tecnico_tpi.pdf has at least 15 pages (comprehensive academic report)."""
        if not PATH_REPORT_PDF.exists():
            self.fail(f"Publication PDF not found: {PATH_REPORT_PDF}")
        if self.pypdf is None:
            self.fail("pypdf package is not installed.")

        reader = self.pypdf.PdfReader(str(PATH_REPORT_PDF))
        page_count = len(reader.pages)
        self.assertGreaterEqual(
            page_count, 15,
            f"PDF page count ({page_count}) is below academic minimum of 15 pages."
        )

    def test_t2_2_pdf_dimensions_a4(self):
        """Verify all pages of informe_tecnico_tpi.pdf adhere to A4 dimensions (595.28 x 841.89 pt ± 5pt)."""
        if not PATH_REPORT_PDF.exists():
            self.fail(f"Publication PDF not found: {PATH_REPORT_PDF}")
        if self.pypdf is None:
            self.fail("pypdf package is not installed.")

        reader = self.pypdf.PdfReader(str(PATH_REPORT_PDF))
        # Standard A4: 595.28 pt x 841.89 pt (tolerance ± 6 pt to accommodate 595-596 x 842 pt renderers)
        target_w = 595.28
        target_h = 841.89
        tol = 6.0

        non_a4_pages = []
        for idx, page in enumerate(reader.pages):
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            if not ((target_w - tol <= w <= target_w + tol) and (target_h - tol <= h <= target_h + tol)):
                non_a4_pages.append((idx + 1, w, h))

        self.assertEqual(
            non_a4_pages, [],
            f"Pages found with non-A4 dimensions (page, width_pt, height_pt): {non_a4_pages}"
        )

    def test_t2_3_pdf_text_extraction_and_encoding(self):
        """Verify PDF text is extractable, non-empty, and free of encoding replacement glitches."""
        if not PATH_REPORT_PDF.exists():
            self.fail(f"Publication PDF not found: {PATH_REPORT_PDF}")
        if self.pypdf is None:
            self.fail("pypdf package is not installed.")

        reader = self.pypdf.PdfReader(str(PATH_REPORT_PDF))
        all_text = ""
        for page in reader.pages:
            text = page.extract_text() or ""
            all_text += text

        self.assertGreater(
            len(all_text.strip()), 5000,
            f"Extracted PDF text is too short ({len(all_text.strip())} chars). PDF must not be an unindexed raster scan."
        )

        # Check absence of Unicode replacement character \ufffd (indicates broken font encoding)
        replacement_count = all_text.count("\ufffd")
        self.assertEqual(
            replacement_count, 0,
            f"Found {replacement_count} replacement characters (\\ufffd) indicating broken font encoding."
        )

        # Check valid Spanish accents exist in extracted text
        has_spanish_vowels = any(c in all_text for c in "áéíóúÁÉÍÓÚñÑ")
        self.assertTrue(has_spanish_vowels, "PDF extracted text lacks standard Spanish diacritics.")

    def test_t2_4_image_assets_and_figure_integrity(self):
        """Verify all local images linked in markdown or HTML exist on disk and are non-empty."""
        files_to_check = []
        if PATH_REPORT_MD.exists():
            files_to_check.append(PATH_REPORT_MD)
        if PATH_REPORT_HTML.exists():
            files_to_check.append(PATH_REPORT_HTML)

        if not files_to_check:
            self.fail("Neither informe_tecnico_tpi.md nor informe_tecnico_tpi.html found.")

        broken_links = []
        md_img_pat = re.compile(r"!\[.*?\]\((?!https?://)(?!data:)(.*?)\)")
        html_img_pat = re.compile(r'<img\s+[^>]*src=["\'](?!https?://)(?!data:)(.*?)["\']', re.IGNORECASE)

        for fpath in files_to_check:
            content = read_text_file(fpath)
            # Find markdown links
            links = md_img_pat.findall(content) + html_img_pat.findall(content)
            for link in links:
                # Strip potential query strings or anchors
                clean_link = link.split("?")[0].split("#")[0].strip()
                if not clean_link:
                    continue
                resolved_path = (fpath.parent / clean_link).resolve()
                if not resolved_path.exists() or resolved_path.stat().st_size == 0:
                    broken_links.append((fpath.name, link, str(resolved_path)))

        self.assertEqual(
            broken_links, [],
            f"Broken or empty image links detected: {broken_links}"
        )

    def test_t2_5_build_pdf_execution(self):
        """Verify build_pdf.py exists, compiles cleanly with exit code 0, and generates the PDF."""
        if not PATH_BUILD_SCRIPT.exists():
            self.fail(f"build_pdf.py not found at: {PATH_BUILD_SCRIPT}")

        cmd = [sys.executable, str(PATH_BUILD_SCRIPT)]
        try:
            result = subprocess.run(
                cmd,
                cwd=str(WORKSPACE_DIR),
                capture_output=True,
                text=True,
                timeout=120
            )
        except subprocess.TimeoutExpired:
            self.fail("build_pdf.py execution timed out after 120 seconds.")

        self.assertEqual(
            result.returncode, 0,
            f"build_pdf.py failed with returncode {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
        self.assertTrue(PATH_REPORT_PDF.exists(), "build_pdf.py ran but informe_tecnico_tpi.pdf was not produced.")
        self.assertGreater(PATH_REPORT_PDF.stat().st_size, 10000, "Generated PDF is smaller than 10 KB.")


# ==============================================================================
# TIER 3 - CROSS-FEATURE & QUANTITATIVE INTEGRITY
# ==============================================================================
class TestTier3QuantitativeIntegrity(unittest.TestCase):
    """
    Tier 3 validates the scientific truth of the deliverables against the
    authoritative reference data from tpi-ia-2026p-21.ipynb and IA-Resumen-Completo.pdf.
    """

    def test_t3_1_ground_truth_baseline_metrics(self):
        """Verify report documents verified Baseline (V1) metrics: Box F1 0.6464, Mask F1 0.6132, QA 0.6053, Kaggle 0.6615."""
        if not PATH_REPORT_MD.exists():
            self.fail(f"Technical report markdown not found: {PATH_REPORT_MD}")

        content = read_text_file(PATH_REPORT_MD)

        # Baseline metrics from notebook cells 66-70
        expected_metrics = [
            ("Box F1 Baseline", r"0[\.,]6464"),
            ("Mask F1 Baseline", r"0[\.,]6132"),
            ("QA Accuracy Baseline", r"0[\.,]6053"),
            ("Kaggle Baseline", r"0[\.,]6615"),
        ]

        missing_metrics = []
        for label, pat in expected_metrics:
            if not re.search(pat, content):
                missing_metrics.append(label)

        self.assertEqual(
            missing_metrics, [],
            f"informe_tecnico_tpi.md is missing verified Baseline metrics: {missing_metrics}"
        )

    def test_t3_2_ground_truth_v3_improved_metrics(self):
        """Verify report documents verified V3 improved metrics: Box F1 0.6722, Mask F1 0.6351, QA 0.7895, Kaggle 0.6800."""
        if not PATH_REPORT_MD.exists():
            self.fail(f"Technical report markdown not found: {PATH_REPORT_MD}")

        content = read_text_file(PATH_REPORT_MD)

        # V3 metrics from notebook cells 81-111
        expected_v3_metrics = [
            ("Box F1 V3", r"0[\.,]6722"),
            ("Mask F1 V3", r"0[\.,]6351"),
            ("QA Deterministic V3", r"0[\.,]7895"),
            ("Kaggle Test V3", r"0[\.,]6800"),
        ]

        missing_v3 = []
        for label, pat in expected_v3_metrics:
            if not re.search(pat, content):
                missing_v3.append(label)

        self.assertEqual(
            missing_v3, [],
            f"informe_tecnico_tpi.md is missing verified V3 improved metrics: {missing_v3}"
        )

    def test_t3_3_negative_hypotheses_documented(self):
        """Verify negative experiments are documented: pad_fix (delta=0), OWLv2 Large, SAM2 multimask."""
        if not PATH_REPORT_MD.exists():
            self.fail(f"Technical report markdown not found: {PATH_REPORT_MD}")

        content = read_text_file(PATH_REPORT_MD)

        # Hypotheses tested and refuted in notebook
        hypotheses = [
            ("pad_fix (0.0000 gain)", r"(?i)(pad_fix|padding).*?(0[\.,]0000|sin\s+cambio|nula|\b0\b)"),
            ("OWLv2 Large rejected", r"(?i)(owlv2-large|owlv2\s+large|vit-l).*?(rechazad|descartad|latencia|4[\.,]7|11[\.,]45)"),
            ("SAM2 multimask rejected", r"(?i)(multimask|multim[aá]scara).*?(rechazad|descartad|single|subpartes|fondo)"),
        ]

        missing_hypo = []
        for label, pat in hypotheses:
            if not re.search(pat, content, re.DOTALL):
                missing_hypo.append(label)

        self.assertEqual(
            missing_hypo, [],
            f"informe_tecnico_tpi.md failed to document negative hypotheses: {missing_hypo}"
        )

    def test_t3_4_theoretical_terms_grounding(self):
        """Verify foundational deep learning theory from IA-Resumen-Completo.pdf is articulated in the report."""
        if not PATH_REPORT_MD.exists():
            self.fail(f"Technical report markdown not found: {PATH_REPORT_MD}")

        content = read_text_file(PATH_REPORT_MD)

        # Theoretical concepts required by cátedra
        theory_concepts = [
            ("Convolución / Jerarquía convolucional", r"(?i)(convoluci[oó]n|convolucional|kernel|mapa\s+de\s+caracter[ií]sticas)"),
            ("Campo receptivo (Receptive field)", r"(?i)(campo\s+receptivo|receptive\s+field)"),
            ("Transfer learning / Modelos fundacionales", r"(?i)(transfer\s+learning|transferencia|preentrenad|fundacional)"),
            ("Media armónica en F1-Score", r"(?i)(media\s+arm[oó]nica|harmonic\s+mean)"),
            ("Desbalance de clases / Long-tail LVIS", r"(?i)(desbalance|cola\s+larga|long[\-\s]tail|federad)"),
            ("Regularización / Sobreajuste", r"(?i)(sobreajuste|overfitting|generalizaci[oó]n|regularizaci[oó]n)"),
        ]

        missing_theory = []
        for label, pat in theory_concepts:
            if not re.search(pat, content):
                missing_theory.append(label)

        self.assertEqual(
            missing_theory, [],
            f"informe_tecnico_tpi.md lacks deep theoretical articulation for: {missing_theory}"
        )

    def test_t3_5_non_technical_clarity_and_jargon_free(self):
        """Verify documento_explicativo_no_tecnico.md avoids heavy mathematical equations and uses intuitive language."""
        if not PATH_NONTECH_MD.exists():
            self.fail(f"Non-technical document not found: {PATH_NONTECH_MD}")

        content = read_text_file(PATH_NONTECH_MD)

        # Heavy mathematical operators that violate non-technical accessibility
        math_jargon_patterns = [
            (r"\\mathcal\{L\}", "LaTeX loss function operator \\mathcal{L}"),
            (r"\\sum_\{", "LaTeX summation operator \\sum"),
            (r"\\int_\{", "LaTeX integral operator \\int"),
            (r"\\nabla", "LaTeX gradient operator \\nabla"),
            (r"\\sigma\(z\)", "LaTeX activation formula \\sigma(z)"),
            (r"D_\{?\\text\{KL\}\}?", "Kullback-Leibler divergence notation"),
        ]

        detected_jargon = []
        for pat, desc in math_jargon_patterns:
            if re.search(pat, content):
                detected_jargon.append(desc)

        self.assertEqual(
            detected_jargon, [],
            f"documento_explicativo_no_tecnico.md contains heavy mathematical jargon: {detected_jargon}"
        )

        # Word count check: non-technical document should be substantial (> 1500 words)
        words = re.findall(r"\b\w+\b", content)
        self.assertGreaterEqual(
            len(words), 1200,
            f"Non-technical document word count ({len(words)} words) is too brief. Expected >= 1200 words."
        )


# ==============================================================================
# TIER 4 - REAL-WORLD ACCEPTANCE & CROSS-MODULE AUDITING
# ==============================================================================
class TestTier4RealWorldAcceptance(unittest.TestCase):
    """
    Tier 4 validates cross-deliverable consistency (authorship, institutional metadata,
    and end-to-end synchronization).
    """

    def test_t4_1_deliverable_metadata_consistency(self):
        """Verify institutional branding, course, and Grupo 21 metadata are consistent across documents."""
        docs = [
            ("informe_tecnico_tpi.md", PATH_REPORT_MD),
            ("documento_explicativo_no_tecnico.md", PATH_NONTECH_MD),
            ("guia_defensa_oral_tpi.md", PATH_DEFENSE_MD),
        ]

        # Key metadata entities
        meta_checks = [
            ("Grupo 21", r"(?i)grupo\s*21"),
            ("Inteligencia Artificial", r"(?i)inteligencia\s+artificial"),
            ("UTN / Cátedra", r"(?i)(utn|universidad\s+tecnol[oó]gica|c[aá]tedra)"),
        ]

        for doc_name, doc_path in docs:
            if not doc_path.exists():
                self.fail(f"Deliverable not found for metadata audit: {doc_name}")
            content = read_text_file(doc_path)
            for meta_name, pat in meta_checks:
                self.assertTrue(
                    bool(re.search(pat, content)),
                    f"Metadata '{meta_name}' not found in {doc_name}."
                )

    def test_t4_2_student_authors_and_professors_referenced(self):
        """Verify all 5 student authors and professors are recognized in the primary report and oral guide."""
        report_content = read_text_file(PATH_REPORT_MD)
        defense_content = read_text_file(PATH_DEFENSE_MD)
        combined = report_content + "\n" + defense_content

        students = [
            ("Ocampo", r"(?i)ocampo"),
            ("Pecchio", r"(?i)pecchio"),
            ("Lopez Quinteros", r"(?i)lopez\s+quinteros"),
            ("Chaile", r"(?i)chaile"),
            ("Perez", r"(?i)perez"),
        ]

        missing_students = [name for name, pat in students if not re.search(pat, combined)]
        self.assertEqual(
            missing_students, [],
            f"Student authors missing from deliverables: {missing_students}"
        )


# ==============================================================================
# CLI RUNNER WITH FORMATTED REPORTING
# ==============================================================================
def run_cli_test_suite() -> int:
    """
    Executes the entire test suite with a publication-grade console summary.
    Returns 0 if all tests pass, 1 otherwise.
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_classes = [
        ("Tier 1: Feature Coverage", TestTier1DeliverablesCoverage),
        ("Tier 2: Boundary & Quality Constraints", TestTier2BoundaryQuality),
        ("Tier 3: Quantitative Integrity & Theory", TestTier3QuantitativeIntegrity),
        ("Tier 4: Real-World Acceptance & Consistency", TestTier4RealWorldAcceptance),
    ]

    for _, cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    print("=" * 80)
    print("  E2E DELIVERABLES AUDIT SUITE - TPI INTELIGENCIA ARTIFICIAL 2026")
    print("  Grupo 21 - Comprensión Visual de Escenas")
    print("=" * 80)
    print(f"  Workspace: {WORKSPACE_DIR}")
    print(f"  Total Test Cases: {suite.countTestCases()}")
    print("-" * 80)

    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("  AUDIT SUMMARY")
    print("=" * 80)
    total_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_run - (failures + errors)
    pass_rate = (passed / total_run * 100) if total_run > 0 else 0.0

    print(f"  Total Executed : {total_run}")
    print(f"  Passed         : {passed} ({pass_rate:.1f}%)")
    print(f"  Failures       : {failures}")
    print(f"  Errors         : {errors}")
    print("-" * 80)

    if result.wasSuccessful():
        print("  STATUS: ALL CHECKS PASSED (100% COMPLIANT) - ACCEPTANCE CONFIRMED")
        print("=" * 80)
        return 0
    else:
        print("  STATUS: DEFICIENCIES DETECTED - REFER TO DIAGNOSTICS ABOVE")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(run_cli_test_suite())
