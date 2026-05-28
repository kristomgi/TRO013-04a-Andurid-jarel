"""Testid raja_andur.py jaoks."""
import glob
import re
import sys


def _find(name):
    matches = [f for f in glob.glob(f'**/{name}', recursive=True) if not f.startswith('.github')]
    if not matches:
        print(f"VIGA: '{name}' ei leitud repos (otsisin kõikidest kaustadest)")
        sys.exit(1)
    return matches[0]


FILE = _find("raja_andur.py")


def read_active_lines(path):
    """Loe fail ja tagasta ainult aktiivsed koodiread."""
    with open(path) as f:
        lines = f.readlines()
    active = []
    in_docstring = False
    for line in lines:
        stripped = line.strip()
        # Docstring toggle
        if '"""' in stripped:
            count = stripped.count('"""')
            if count == 1:
                in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        if stripped.startswith("#") or not stripped:
            continue
        active.append(line)
    return active


def get_function_active_body(path, func_name):
    """Leia funktsiooni aktiivne keha (ilma kommentaaride ja docstring-ideta)."""
    with open(path) as f:
        code = f.read()

    # Leia funktsiooni algus
    pattern = rf"def {func_name}\(.*?\):"
    match = re.search(pattern, code)
    if not match:
        return ""

    start = match.end()
    # Leia funktsiooni indent
    func_line = code[: match.start()].split("\n")[-1]
    base_indent = len(func_line) - len(func_line.lstrip())

    lines = code[start:].split("\n")[1:]  # jata esimene tyhi rida vahele
    body_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent and line.strip():
            break
        body_lines.append(line)

    # Filtreeri kommentaarid
    active = [l for l in body_lines if l.strip() and not l.strip().startswith("#")]
    return "\n".join(active)


def test_sektori_min():
    """sektori_min peab sisaldama filtreerimisloogikat."""
    body = get_function_active_body(FILE, "sektori_min")
    # Eemaldame def rea ja return float('inf') rea
    has_filtering = any(
        kw in body for kw in ["min(", "for ", "range(", "filter(", "sorted(", "kehtivad"]
    )
    # Kontrollime et pole ainult return float('inf')
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    is_stub = len(lines) <= 1 and "return float" in body

    if is_stub or not has_filtering:
        print("FAIL: sektori_min() on endiselt stub (return float('inf'))")
        print("  Vihje: lisa filtreerimisloogika (for-tsukkel, min(), kehtivuse kontroll)")
        return False
    print("OK: sektori_min() sisaldab loogikat")
    return True


def test_sectors_not_stub():
    """5 sektori kaugused peavad olema arvutatud (mitte inf TODO)."""
    with open(FILE) as f:
        code = f.read()
    stubs = re.findall(r"=\s*float\(['\"]inf['\"]\)\s*#\s*TODO", code)
    if stubs:
        print(f"FAIL: {len(stubs)} sektorit on endiselt float('inf') # TODO stub-id")
        return False
    print("OK: sektorid arvutatud")
    return True


def test_table_printed():
    """Tabel peab olema trukitud aktiivses koodis."""
    body = get_function_active_body(FILE, "print_table")
    # Peab sisaldama logimist voi printimist koos sektori nimedega
    has_output = (
        ("get_logger" in body or "print(" in body or "info(" in body)
        and ("vasak" in body.lower() or "ette" in body.lower() or "raja" in body.lower())
    )
    if not has_output:
        print("FAIL: print_table() ei trueki tabelit aktiivses koodis")
        print("  Vihje: eemalda kommentaar self.get_logger().info(...) realt")
        return False
    print("OK: tabel trukitakse")
    return True


if __name__ == "__main__":
    test_name = sys.argv[1] if len(sys.argv) > 1 else "all"
    tests = {
        "sektori_min": test_sektori_min,
        "sectors": test_sectors_not_stub,
        "table": test_table_printed,
    }

    if test_name in tests:
        sys.exit(0 if tests[test_name]() else 1)
    elif test_name == "all":
        ok = all(fn() for fn in tests.values())
        sys.exit(0 if ok else 1)
    else:
        print(f"Tundmatu test: {test_name}")
        sys.exit(2)
