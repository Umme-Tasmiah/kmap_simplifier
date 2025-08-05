# KMap Simplifier

A Python tool to simplify 4-variable Karnaugh maps (K-Maps) and generate the corresponding simplified Sum of Products (SOP) expressions along with Verilog code.

---

## Project Structure
```
kmap_simplifier
├── logic
│   └── kmap.py # Core logic for K-map simplification
├── main.py # For input/output
└── test
└── test.py # Test cases for validation
```


---

## Features

- Input minterms and optional don't-care terms for a 4-variable K-map (variables: A, B, C, D).
- Automatically finds minimal groupings and simplifies to the minimal SOP form.
- Generates synthesizable Verilog module code corresponding to the simplified SOP.
- Supports wrapping groups, essential prime implicants, and multiple group sizes (singles, pairs, quads, octets).
- Includes a test suite with multiple test cases and expected outputs.

---

## Instruction

Run the simplifier interactively with:

```bash
python main.py
```

## Demo
```
Enter minterms as comma-separated integers (0-15, e.g., 0,1,2,3)
Enter Minterms: 5,6,9,13,15
Enter don't-care terms as comma-separated integers (0-15, optional)
Enter Don't Cares (optional): 1,7,14
```
Simplified SOP:
```
BC + C'D
```
Verilog Code:
```
module kmap_simplified (
    input wire A, B, C, D,
    output wire F
);

    assign F = (B & C) | (~C & D);

endmodule
```
