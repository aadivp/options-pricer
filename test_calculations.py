#!/usr/bin/env python3
"""
Test script for Black-Scholes calculations
Verifies the accuracy of option pricing calculations
"""

from formulas import blackScholes, calculate_implied_volatility

def test_basic_calculations():
    """Test basic Black-Scholes calculations with known values"""
    print("Testing Basic Black-Scholes Calculations")
    print("=" * 50)
    
    # Test case 1: At-the-money option
    print("\nTest Case 1: At-the-money option")
    print("S=100, K=100, T=1, r=0.05, sigma=0.2")
    
    result = blackScholes(100, 100, 1, 0.05, 0.2)
    print(f"Call Price: ${result['call_price']:.4f}")
    print(f"Put Price: ${result['put_price']:.4f}")
    print(f"Delta (Call): {result['delta_call']:.4f}")
    print(f"Delta (Put): {result['delta_put']:.4f}")
    print(f"Gamma: {result['gamma']:.4f}")
    print(f"Vega: {result['vega']:.4f}")
    
    # Expected values (approximate)
    expected_call = 10.45  # Approximate
    expected_put = 5.57    # Approximate
    print(f"\nExpected Call Price: ~${expected_call}")
    print(f"Expected Put Price: ~${expected_put}")
    
    # Test case 2: In-the-money call
    print("\nTest Case 2: In-the-money call")
    print("S=110, K=100, T=1, r=0.05, sigma=0.2")
    
    result2 = blackScholes(110, 100, 1, 0.05, 0.2)
    print(f"Call Price: ${result2['call_price']:.4f}")
    print(f"Put Price: ${result2['put_price']:.4f}")
    print(f"Delta (Call): {result2['delta_call']:.4f}")
    print(f"Delta (Put): {result2['delta_put']:.4f}")
    
    # Test case 3: Out-of-the-money put
    print("\nTest Case 3: Out-of-the-money put")
    print("S=90, K=100, T=1, r=0.05, sigma=0.2")
    
    result3 = blackScholes(90, 100, 1, 0.05, 0.2)
    print(f"Call Price: ${result3['call_price']:.4f}")
    print(f"Put Price: ${result3['put_price']:.4f}")
    print(f"Delta (Call): {result3['delta_call']:.4f}")
    print(f"Delta (Put): {result3['delta_put']:.4f}")

def test_implied_volatility():
    """Test implied volatility calculation"""
    print("\n\nTesting Implied Volatility Calculation")
    print("=" * 50)
    
    # Use the call price from test case 1 to calculate implied volatility
    call_price = 10.45
    print(f"Market Call Price: ${call_price}")
    print("S=100, K=100, T=1, r=0.05")
    
    iv = calculate_implied_volatility(100, 100, 1, 0.05, call_price, "call")
    print(f"Calculated Implied Volatility: {iv:.4f} ({iv*100:.2f}%)")
    print(f"Original Volatility: 0.2000 (20.00%)")
    print(f"Difference: {abs(iv - 0.2):.4f}")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n\nTesting Edge Cases")
    print("=" * 50)
    
    # Test with very low time to expiry
    print("\nTest: Very low time to expiry (T=0.01)")
    result = blackScholes(100, 100, 0.01, 0.05, 0.2)
    print(f"Call Price: ${result['call_price']:.4f}")
    print(f"Put Price: ${result['put_price']:.4f}")
    
    # Test with very high volatility
    print("\nTest: Very high volatility (sigma=0.8)")
    result = blackScholes(100, 100, 1, 0.05, 0.8)
    print(f"Call Price: ${result['call_price']:.4f}")
    print(f"Put Price: ${result['put_price']:.4f}")
    
    # Test with zero risk-free rate
    print("\nTest: Zero risk-free rate (r=0)")
    result = blackScholes(100, 100, 1, 0, 0.2)
    print(f"Call Price: ${result['call_price']:.4f}")
    print(f"Put Price: ${result['put_price']:.4f}")

def test_put_call_parity():
    """Test put-call parity relationship"""
    print("\n\nTesting Put-Call Parity")
    print("=" * 50)
    
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    result = blackScholes(S, K, T, r, sigma)
    
    call_price = result['call_price']
    put_price = result['put_price']
    
    # Put-call parity: C - P = S - K*e^(-rT)
    left_side = call_price - put_price
    right_side = S - K * (2.71828 ** (-r * T))
    
    print(f"Call Price: ${call_price:.4f}")
    print(f"Put Price: ${put_price:.4f}")
    print(f"C - P: ${left_side:.4f}")
    print(f"S - K*e^(-rT): ${right_side:.4f}")
    print(f"Difference: ${abs(left_side - right_side):.6f}")
    
    if abs(left_side - right_side) < 0.01:
        print("✓ Put-call parity holds (within tolerance)")
    else:
        print("✗ Put-call parity violation detected")

if __name__ == "__main__":
    test_basic_calculations()
    test_implied_volatility()
    test_edge_cases()
    test_put_call_parity()
    
    print("\n\nAll tests completed!")
    print("If all calculations look reasonable, the implementation is working correctly.") 