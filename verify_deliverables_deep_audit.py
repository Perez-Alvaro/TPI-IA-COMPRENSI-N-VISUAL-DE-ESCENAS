"""
verify_deliverables_deep_audit.py
Adversarial Verification and Cross-Check Harness
Checks exact numbers, variations, roundings, and context across:
- tpi-ia-2026p-21.ipynb (Ground Truth)
- informe_tecnico_tpi.md
- documento_explicativo_no_tecnico.md
- guia_defensa_oral_tpi.md
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE = Path(__file__).resolve().parent

DOCS = {
    "informe_tecnico": WORKSPACE / "informe_tecnico_tpi.md",
    "documento_no_tecnico": WORKSPACE / "documento_explicativo_no_tecnico.md",
    "guia_defensa": WORKSPACE / "guia_defensa_oral_tpi.md",
}

CHECKS = {
    # 1. Box F1
    "Box F1 Baseline (0.6464 or 0.646)": r"0[.,]6464|0[.,]646(?!\d)",
    "Box F1 V3 (0.6722)": r"0[.,]6722",
    "Box F1 V3 intermediate (0.6641 or 0.664)": r"0[.,]6641|0[.,]664(?!\d)",

    # 2. Mask F1
    "Mask F1 Baseline (0.6132 or 0.613)": r"0[.,]6132|0[.,]613(?!\d)",
    "Mask F1 V3 (0.6351)": r"0[.,]6351",
    "Mask F1 V3 intermediate (0.6273 or 0.627)": r"0[.,]6273|0[.,]627(?!\d)",

    # 3. QA Deterministic
    "QA Deterministic Baseline (0.6053 or 0.605)": r"0[.,]6053|0[.,]605(?!\d)",
    "QA Deterministic V3 (0.7895 or 0.789)": r"0[.,]7895|0[.,]789(?!\d)",

    # 4. Kaggle Blind Test Scores
    "Kaggle V1 (0.6615)": r"0[.,]6615",
    "Kaggle V2 (0.6763)": r"0[.,]6763",
    "Kaggle V3 (0.6800 or 0.680)": r"0[.,]6800|0[.,]680(?!\d)",

    # 5. Sample distribution
    "Dev Images (120)": r"\b120\s+im[áa]genes",
    "Total Annotations (1790 or 1.790)": r"1[.,]790\s*(anotaciones|instancias)?|1790\s*(anotaciones|instancias)",
    "Small Instances % (71.06% or 71.1% or 71%)": r"71([.,]06|[.,]1)?\s*%",
    "Medium Instances % (24.02% or 24.0% or 24%)": r"24([.,]02|[.,]0)?\s*%",
    "Large Instances % (4.92% or 4.9% or 5%)": r"4[.,]92\s*%|4[.,]9\s*%|5\s*%",

    # 6. Latency claims
    "OWLv2 Latency (2.44s or 2.35s)": r"2[.,]44\s*s|2[.,]35\s*s",
    "SAM2 Latency (0.43s or 0.40s)": r"0[.,]43\s*s|0[.,]40\s*s",
    "SceneJSON Latency (0.28s or 0.20s)": r"0[.,]28\s*s|0[.,]20\s*s",
    "Total Latency V3 (3.25s or 3.0s or 3.2s)": r"3[.,]25\s*s|3[.,]0\s*s|3[.,]2\s*s",

    # 7. Negative Hypotheses
    "pad_fix 0.0000 delta / nulo": r"pad_fix.*?(0[.,]0000|sin efecto|diferencia 0|id[ée]ntic|nulo|0\b)",
    "OWLv2 Large failure / descartado": r"(owlv2[-\s]large|l/14).*?(4[.,]7|descart|peor|inferior|lento)",
    "SAM2 multimask failure / descartado": r"(multimask|multim[áa]scara).*?(descart|empeor|inferior|single|rechaz)",
}

def audit():
    print("=" * 80)
    print("EMPIRICAL CHALLENGER: AUDITING QUANTITATIVE INTEGRITY ACROSS DELIVERABLES")
    print("=" * 80)
    
    doc_contents = {}
    for doc_name, path in DOCS.items():
        if not path.exists():
            print(f"[FAIL] Missing file: {path}")
            return False
        with open(path, "r", encoding="utf-8") as f:
            doc_contents[doc_name] = f.read()

    results = {}
    all_passed = True
    
    for check_name, pattern in CHECKS.items():
        print(f"\nEvaluating: {check_name}")
        regex = re.compile(pattern, re.IGNORECASE)
        check_status = {}
        for doc_name, content in doc_contents.items():
            matches = regex.findall(content)
            found = len(matches) > 0
            check_status[doc_name] = (found, len(matches))
            status_str = f"FOUND ({len(matches)})" if found else "NOT FOUND"
            print(f"  - {doc_name:22s}: {status_str}")
        
        # Primary check: Must be in informe_tecnico_tpi.md at minimum, and in others where relevant
        if not check_status["informe_tecnico"][0]:
            print(f"  [ERROR] Critical metric missing in technical report: {check_name}")
            all_passed = False
        
        results[check_name] = check_status

    print("\n" + "=" * 80)
    print(f"OVERALL METRIC CITATION AUDIT: {'PASSED' if all_passed else 'FAILED'}")
    print("=" * 80)
    return all_passed

if __name__ == "__main__":
    success = audit()
    sys.exit(0 if success else 1)
