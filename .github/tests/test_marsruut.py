"""Testid marsruut.py jaoks."""
import glob
import re
import sys


def _find(name):
    matches = [f for f in glob.glob(f'**/{name}', recursive=True) if not f.startswith('.github')]
    if not matches:
        print(f"VIGA: '{name}' ei leitud repos (otsisin kõikidest kaustadest)")
        sys.exit(1)
    return matches[0]


FILE = _find("marsruut.py")


def get_function_active_body(path, func_name):
    """Leia funktsiooni aktiivne keha (ilma kommentaarideta)."""
    with open(path) as f:
        code = f.read()

    pattern = rf"def {func_name}\(.*?\):"
    match = re.search(pattern, code)
    if not match:
        return ""

    start = match.end()
    func_line = code[: match.start()].split("\n")[-1]
    base_indent = len(func_line) - len(func_line.lstrip())

    lines = code[start:].split("\n")[1:]
    body_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= base_indent and line.strip():
            break
        body_lines.append(line)

    active = [l for l in body_lines if l.strip() and not l.strip().startswith("#")]
    return "\n".join(active)


def test_control_loop_implemented():
    """control_loop peab sisaldama olekumasina loogikat."""
    body = get_function_active_body(FILE, "control_loop")
    has_state_check = "self.olek ==" in body or "self.olek==" in body
    has_movement = "linear.x" in body or "angular.z" in body or "SOIDUKIIRUS" in body or "POORDEKIIRUS" in body

    if not has_state_check:
        print("FAIL: control_loop() ei sisalda olekukontrolli (self.olek == ...)")
        return False
    if not has_movement:
        print("FAIL: control_loop() ei sisalda liikumiskaskude (linear.x, angular.z)")
        return False
    print("OK: control_loop() implementeeritud")
    return True


def test_all_states():
    """Koik 4 olekut peavad olema implementeeritud."""
    body = get_function_active_body(FILE, "control_loop")
    states = ["OLEK_EDASI_1", "OLEK_POORDE_1", "OLEK_EDASI_2", "OLEK_POORDE_2"]
    missing = []
    for s in states:
        if f"== {s}" not in body and f"=={s}" not in body:
            missing.append(s)
    if missing:
        print(f"FAIL: Puuduvad olekud aktiivses koodis: {missing}")
        print("  Vihje: eemalda kommentaarid ja lisa koik olekud (EDASI_1, POORDE_1, EDASI_2, POORDE_2)")
        return False
    print("OK: koik 4 olekut leitud")
    return True


def test_valmis_state():
    """OLEK_VALMIS peab olema implementeeritud."""
    body = get_function_active_body(FILE, "control_loop")
    if "OLEK_VALMIS" not in body:
        print("FAIL: OLEK_VALMIS puudub aktiivses koodis")
        return False
    if "cancel" not in body:
        print("FAIL: timer.cancel() puudub (marsruut ei lope)")
        return False
    print("OK: OLEK_VALMIS implementeeritud")
    return True


if __name__ == "__main__":
    test_name = sys.argv[1] if len(sys.argv) > 1 else "all"
    tests = {
        "control_loop": test_control_loop_implemented,
        "states": test_all_states,
        "valmis": test_valmis_state,
    }

    if test_name in tests:
        sys.exit(0 if tests[test_name]() else 1)
    elif test_name == "all":
        ok = all(fn() for fn in tests.values())
        sys.exit(0 if ok else 1)
    else:
        print(f"Tundmatu test: {test_name}")
        sys.exit(2)
