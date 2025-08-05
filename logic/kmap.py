from itertools import combinations

# gray code for kmap
gray_map = {
    '00': 0,
    '01': 1,
    '11': 2,
    '10': 3
}
inv_gray_map = {v: k for k, v in gray_map.items()} # To invert the gray map key,value e.g: 0 : '00'
variables = ('A', 'B', 'C', 'D')

# convert minterm (0-15) to (row, col) using gray code
def position(minterm: int):
    binary = format(minterm, '04b')
    return gray_map[binary[:2]], gray_map[binary[2:]]

# encode the minterms to positions
def min_to_position(minterms, dc_terms = []): # dc_terms = don't care terms
    kmap = [[0] * 4 for _ in range(4)] # 4*4 grid filled with 0 initially
    for m in minterms:
        r, c = position(m)
        kmap[r][c] = 1 # set 1 in minterm position
    for dc in dc_terms:
        r, c = position(dc)
        kmap[r][c] = 2 # set 2 in dc position
    return kmap

# decode the position to minterm for SOP
def position_to_min(cells):
    minterms = set() # not to take duplicate minterms
    for r, c in cells:
        minterms.add(int(inv_gray_map[r] + inv_gray_map[c], 2))
    return minterms


# to find all possible valid groups
def find_all_groups(kmap):
    groups = set()
    rows, cols = 4, 4

    # wrap around: (0,4) becomes (0,0) since 4 is outside the 4×4 grid
    def add_group(cells):
        wrapped = frozenset(((r % 4, c % 4) for r, c in cells))
        if all(kmap[r % 4][c % 4] in (1, 2) for r, c in wrapped):
            groups.add(wrapped)

    for r in range(rows):
        for c in range(cols):
            pair = (r, c)
            if kmap[r][c] == 1:
                groups.add(frozenset({pair})) # single group

            add_group({(r, c), (r, c + 1)}) # horizontal pair
            add_group({(r, c), (r + 1, c)}) # vertical pair
            add_group({(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)}) # 2*2 square quad group
            add_group({(r, c + i) for i in range(4)}) # horizontal 4
            add_group({(r + i, c) for i in range(4)}) # vertical 4

    # ensuring to find full row or full column quad
    for r in range(4):
        add_group({(r, i) for i in range(4)})
        add_group({(i, r) for i in range(4)})

    # to find octet group
    for r in range(4):
        octet_rows = {(r, c) for c in range(4)} | {((r + 1) % 4, c) for c in range(4)}
        add_group(octet_rows)

    for c in range(4):
        octet_cols = {(r, c) for r in range(4)} | {(r, (c + 1) % 4) for r in range(4)}
        add_group(octet_cols)

    return list(groups)


# Returns the simplified Boolean expression literals (variables A, B, C, D)
def get_literals_from_minterms(minterm_set):
    if not minterm_set:
        return ""
    bits = [format(m, '04b') for m in minterm_set]
    expression = ''
    for i in range(4):
        column = {b[i] for b in bits}
        if len(column) == 1:
            bit = column.pop()
            expression += variables[i] + ('' if bit == '1' else "'")
    return expression


# Converts a group of K-map cells (e.g., [(0, 0), (0, 1)]) into a simplified Boolean expression like A'B'C'
def group_to_expression(group_cells):
    minterms = position_to_min(group_cells)
    return get_literals_from_minterms(minterms)

# Combines multiple group expressions into a full simplified SOP expression
def simplify_expression(groups):
    if not groups:
        return "0"
    terms = [group_to_expression(group) for group in groups]
    return ' + '.join(sorted(terms))
'''    if not terms:
        return "1" '''



# Converts a simplified SOP expression into verilog code
def sop_to_verilog(sop_expr, module_name="kmap_simplified"):
    inputs = ', '.join(variables) # Join inputs: "A, B, C, D"
    verilog_code = f"module {module_name} (\n    input wire {inputs},\n    output wire F\n);\n\n"

    # Handle constant expressions
    if sop_expr.strip() == "1":
        verilog_code += "    assign F = 1'b1;\n"
    elif sop_expr.strip() == "0":
        verilog_code += "    assign F = 1'b0;\n"
    else:
        terms = sop_expr.replace(" ", "").split('+')
        verilog_terms = []
        for term in terms:
            factors = []
            i = 0
            while i < len(term):
                if i + 1 < len(term) and term[i + 1] == "'":
                    factors.append(f"~{term[i]}") # Negated variable in Verilog
                    i += 2
                else:
                    factors.append(term[i])
                    i += 1
            verilog_terms.append(' & '.join(factors)) # AND within term for sop
        or_logic = ' | '.join(f"({t})" for t in verilog_terms) # OR between terms for sop
        verilog_code += f"    assign F = {or_logic};\n"

    verilog_code += "\nendmodule\n"
    return verilog_code

# Find minimal group covers using essential prime implicants
def find_minimal_covers(groups, minterms):
    coverage = {m: [] for m in minterms}
    for i, group in enumerate(groups):
        group_minterms = position_to_min(group)
        for m in minterms:
            if m in group_minterms:
                coverage[m].append(i)

    for m in minterms:
        if not coverage[m]:
            return []

    essential_groups = set()
    covered_minterms = set()

    # Identify essential prime implicants
    for m, group_indices in coverage.items():
        if len(group_indices) == 1:
            essential_groups.add(group_indices[0])
            covered_minterms.update(position_to_min(groups[group_indices[0]]))

    if covered_minterms >= minterms:
        return [list(groups[i] for i in sorted(essential_groups))]

    remaining_minterms = minterms - covered_minterms # Remaining minterms to be covered
    results = []

    # Try combinations of non-essential groups to cover remaining minterms
    non_essential_indices = [i for i in range(len(groups)) if i not in essential_groups]

    for r in range(1, len(non_essential_indices) + 1):
        for comb in combinations(non_essential_indices, r):
            comb_minterms = set()
            for i in comb:
                comb_minterms.update(position_to_min(groups[i]))
            if remaining_minterms <= comb_minterms:
                cover = list(essential_groups) + list(comb)
                results.append([groups[i] for i in cover])
        if results:
            min_len = min(len(res) for res in results) # Among all valid covers, choose those with minimum number of groups
            minimal_covers = [res for res in results if len(res) == min_len]

            def literal_count(cover):
                return sum(len(group_to_expression(g)) for g in cover)

            return sorted(minimal_covers, key=literal_count)[:1]

    return []

# main function to simplify expression and return sop and verilog
def simplify_kmap_sop(minterms, dc_terms=[]):
    all_covered = set(minterms + dc_terms)
    if all_covered >= set(range(16)):
        return "1", "assign F = 1'b1;" # Case 1: All 16 cells are 1 or don't-care then output is always 1
    elif not minterms:
        return "0", "assign F = 1'b0;" # Case 2: No minterms then output is always 0

    kmap = min_to_position(minterms, dc_terms)
    all_groups = find_all_groups(kmap)
    all_min_solutions = find_minimal_covers(all_groups, set(minterms))

    if not all_min_solutions:
        return "0", "assign F = 1'b0;"

    best = all_min_solutions[0] # Select the best minimal cover
    sop_expr = simplify_expression(best)
    verilog_code = sop_to_verilog(sop_expr)
    return sop_expr, verilog_code



