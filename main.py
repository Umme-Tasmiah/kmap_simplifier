from logic.kmap import simplify_kmap_sop


def simplify():
    try:
        print("Enter minterms as comma-separated integers (0-15, e.g., 0,1,2,3)")
        minterms_input = input("Enter Minterms: ")
        minterms = list(set(map(int, minterms_input.split(','))))

        if not minterms:
            raise ValueError("Minterm list cannot be empty.")

        for m in minterms:
            if not (0 <= m <= 15):
                raise ValueError("Minterms must be between 0 and 15.")

        print("Enter don't-care terms as comma-separated integers (0-15, optional)")
        dc_input = input("Enter Don't Cares (optional): ")
        dc_terms = list(set(map(int, dc_input.split(',')))) if dc_input.strip() else []

        for dc in dc_terms:
            if not (0 <= dc <= 15):
                raise ValueError("Don't-care terms must be between 0 and 15.")

        if set(minterms) & set(dc_terms):
            raise ValueError("Minterms and don't-care terms must not overlap.")

        sop, verilog = simplify_kmap_sop(minterms, dc_terms)

        print(f"\nSimplified SOP:\n{sop}\n")
        print(f"Verilog Code:\n{verilog}\n")

    except ValueError as e:
        print(f"Input error: {str(e)}")


if __name__ == "__main__":

    simplify()
