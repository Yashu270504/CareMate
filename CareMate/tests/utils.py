# tests/utils.py

def format_results(results, case_name=None):
    """
    Pretty prints the engine results for a given test case.
    results: dict with "warnings" and "alternatives"
    case_name: optional string for labeling output
    """

    print("=" * 50)
    if case_name:
        print(f"🧪 Case: {case_name}")
        print("-" * 50)

    warnings = results.get("warnings", [])
    alternatives = results.get("alternatives", [])

    # Show warnings
    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   • {w}")
    else:
        print("✅ No warnings")

    # Show alternatives
    if alternatives:
        print("\n💡 Alternatives:")
        for a in alternatives:
            print(f"   → {a}")
    else:
        print("\nℹ️ No alternatives suggested")

    print("=" * 50 + "\n")
