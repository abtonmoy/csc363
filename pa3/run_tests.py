import os
import glob
import subprocess
import sys

def run_tests():
    passed = 0
    failed = 0
    total = 0
    
    # Ensure tests and outputs directories exist
    if not os.path.exists('tests'):
        print("[ERROR] 'tests' directory not found")
        return
    if not os.path.exists('outputs'):
        print("[ERROR] 'outputs' directory not found")
        return

    test_files = glob.glob('tests/*.ac')
    test_files.sort()

    for acfile in test_files:
        base = os.path.basename(acfile).replace('.ac', '')
        out_test = f"tests/{base}.dc"
        out_expected = f"outputs/{base}.dc"
        
        if not os.path.exists(out_expected):
            print(f"[ERROR] Expected output not found: {out_expected}")
            continue

        print(f"Running {base}...")
        
        # Run acdc.py
        try:
            # We use check=False because acdc.py exits with 1 on parse errors, 
            # but we still want to compare the output file content (which contains the error message).
            subprocess.run([sys.executable, 'acdc.py', acfile, out_test], check=False, capture_output=True)
        except Exception as e:
            print(f"  [FAIL] execution failed: {e}")
            failed += 1
            total += 1
            continue

        # Compare outputs
        with open(out_test, 'r', encoding='utf-8') as f1, open(out_expected, 'r', encoding='utf-8') as f2:
            content_test = f1.read().strip()
            content_expected = f2.read().strip()
        
        # Normalize newlines
        content_test = content_test.replace('\r\n', '\n')
        content_expected = content_expected.replace('\r\n', '\n')

        if content_test == content_expected:
            print("  [PASS]")
            passed += 1
        else:
            print("  [FAIL]")
            print("     Differences:")
            print(f"     Expected:\n{content_expected}\n")
            print(f"     Got:\n{content_test}\n")
            failed += 1
        
        total += 1
        print()

    print("========================")
    print("Test Summary")
    print("------------------------")
    print(f"Total:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("[WARNING] Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
