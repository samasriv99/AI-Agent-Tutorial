from pkg.calculator import Calculator

def test_repro():
    calc = Calculator()
    # 3 + 7 * 2 should be 17.
    # If current precedence is buggy, it might result in 20.
    result = calc.evaluate("3 + 7 * 2")
    print(f"Result of '3 + 7 * 2': {result}")
    if result == 20:
        print("BUG REPRODUCED: result is 20")
    elif result == 17:
        print("SUCCESS: result is 17")
    else:
        print(f"Unexpected result: {result}")

if __name__ == '__main__':
    test_repro()
