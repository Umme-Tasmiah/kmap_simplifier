from logic.kmap import simplify_kmap_sop

def normalize(expr):
    return sorted(expr.replace(" ", "").split('+'))

def run_test(minterms, dc_terms=None, expected=None, index=None):
    dc_terms = dc_terms or []
    sop, verilog = simplify_kmap_sop(minterms, dc_terms)
    print(f"\nTest Case {index}:")
    print(f"  Minterms     : {minterms}")
    print(f"  Don't Cares  : {dc_terms}")
    print(f"  Output SOP   : {sop}")
    if expected:
        print(f"  Expected SOP : {expected}")
        result = "PASS" if normalize(sop) == normalize(expected) else "FAIL"
        print(f"  {result}")
    else:
        print("  (No expected SOP provided — manual verification needed)")
    print("-" * 60)

if __name__ == "__main__":
    cases = [
        ([0,2,3,7,11,13,14,15], [], "CD + A'B'D' + ABC + ABD"),
        ([0,2,3,5,7,8,10,11,14,15], [], "B'D' + CD + A'BD + AC"),
        ([1,5,7,9,11,13,15], [], "C'D + AD + BD"),
        ([4,5,6,9,13,14], [], "A'BC' + AC'D + BCD'"),
        ([4,5,6,7,9,13,14,15], [], "A'B + BC + AC'D"),
        ([0,1,5,6,7,8,9,13,15], [], "B'C' + BD + A'BC"),
        ([0,1,4,5,7,8,9,11,12,13,15], [], "C' + AD + BD"),
        ([5,7,8,10,11,12,13,14,15], [], "AC + AD' + BD"),
        ([5,6,9,13,15], [1,7,14], "C'D + BC"),
        ([0,1,5,7,8,10,14,15], [], "A'B'C' + A'BD + AB'D' + ABC"),
        ([0,1,5,6,7,8,9,13,15], [2,10], "A'BC + B'C' + BD"),
        ([0,1,8,9], [2,3,10,11], "B'"),
        ([0,1,3,4,5,7,12,13,15], [], "A'C' + A'D + BC' + BD"),
        ([0,2,8,15], [], "A'B'D' + ABCD + B'C'D'"),
        ([0,2,8,10], [], "B'D'"),
        ([0,1,2,3,4,6,8,9,10,12,14,11], [], "B'+D'"),
        ([4,5,6,12,13], [3,7,9], "A'B + BC'"),
        ([0,1,2,4,6,8,12,13], [3,7,10,14,11,15], "D' + A'B' + AB"),  # No expected SOP provided
    ]

    for idx, (minterms, dc, expected) in enumerate(cases, 1):
        run_test(minterms, dc, expected, idx)
