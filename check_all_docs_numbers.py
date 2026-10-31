"""
check_all_docs_numbers.py
"""
import re
from pathlib import Path

docs = {
    "informe": Path("informe_tecnico_tpi.md").read_text(encoding="utf-8"),
    "no_tecnico": Path("documento_explicativo_no_tecnico.md").read_text(encoding="utf-8"),
    "defensa": Path("guia_defensa_oral_tpi.md").read_text(encoding="utf-8")
}

patterns = {
    "small_instances": [r"71[.,]06\s*%", r"71[.,]1\s*%", r"71\s*%", r"1[.,]?272"],
    "medium_instances": [r"24[.,]02\s*%", r"24[.,]0\s*%", r"24\s*%", r"430"],
    "large_instances": [r"4[.,]92\s*%", r"4[.,]9\s*%", r"5\s*%", r"\b88\b"],
    "box_f1_baseline": [r"0[.,]6464", r"0[.,]646"],
    "box_f1_v3": [r"0[.,]6722"],
    "mask_f1_baseline": [r"0[.,]6132", r"0[.,]613"],
    "mask_f1_v3": [r"0[.,]6351"],
    "qa_det_baseline": [r"0[.,]6053", r"0[.,]605"],
    "qa_det_v3": [r"0[.,]7895", r"0[.,]789"],
    "kaggle_v1": [r"0[.,]6615"],
    "kaggle_v2": [r"0[.,]6763"],
    "kaggle_v3": [r"0[.,]6800", r"0[.,]680"],
    "latency_owlv2": [r"2[.,]44"],
    "latency_sam2": [r"0[.,]43"],
    "latency_scenejson": [r"0[.,]28"],
    "latency_total": [r"3[.,]25"],
    "pad_fix": [r"pad_fix"],
    "owlv2_large": [r"owlv2.*large|owlv2-large"],
    "sam2_multimask": [r"multimask|multim[áa]scara"],
}

for name, pat_list in patterns.items():
    print(f"\nMetric: {name}")
    for doc_name, text in docs.items():
        matches = []
        for p in pat_list:
            matches.extend(re.findall(p, text, re.IGNORECASE))
        print(f"  {doc_name:12s}: {len(matches)} matches -> {set(matches)}")
