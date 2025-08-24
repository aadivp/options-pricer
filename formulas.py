import math
from scipy.stats import norm

def blackScholes(S, K, T, r, sigma):
    """
    Calculate Black-Scholes option prices and Greeks
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate
    sigma: Volatility
    
    Returns:
    dict: Dictionary containing call price, put price, and Greeks
    """
    if T <= 0 or sigma <= 0:
        return {
            'call_price': 0,
            'put_price': 0,
            'delta_call': 0,
            'delta_put': 0,
            'gamma': 0,
            'theta_call': 0,
            'theta_put': 0,
            'vega': 0
        }
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    # Option prices
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    # Greeks
    delta_call = norm.cdf(d1)
    delta_put = delta_call - 1
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) - 
                  r * K * math.exp(-r * T) * norm.cdf(d2))
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) + 
                 r * K * math.exp(-r * T) * norm.cdf(-d2))
    vega = S * math.sqrt(T) * norm.pdf(d1)
    
    return {
        'call_price': call_price,
        'put_price': put_price,
        'delta_call': delta_call,
        'delta_put': delta_put,
        'gamma': gamma,
        'theta_call': theta_call,
        'theta_put': theta_put,
        'vega': vega
    }

def calculate_implied_volatility(S, K, T, r, option_price, option_type='call', tolerance=1e-5, max_iterations=100):
    """
    Calculate implied volatility using Newton-Raphson method
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to expiration
    r: Risk-free interest rate
    option_price: Market price of the option
    option_type: 'call' or 'put'
    tolerance: Convergence tolerance
    max_iterations: Maximum number of iterations
    
    Returns:
    float: Implied volatility
    """
    if option_price <= 0:
        return 0
    
    # Initial guess
    sigma = 0.5
    
    for i in range(max_iterations):
        result = blackScholes(S, K, T, r, sigma)
        price = result['call_price'] if option_type == 'call' else result['put_price']
        vega = result['vega']
        
        diff = option_price - price
        
        if abs(diff) < tolerance:
            return sigma
        
        if abs(vega) < 1e-10:
            break
            
        sigma = sigma + diff / vega
        
        # Ensure sigma stays positive
        sigma = max(0.001, sigma)
    
    return sigma

if __name__ == "__main__":
    # Test the function
    result = blackScholes(100, 100, 1, 0.05, 0.2)
    print(f"Call Price: ${result['call_price']:.4f}")
    print(f"Put Price: ${result['put_price']:.4f}")
    print(f"Delta (Call): {result['delta_call']:.4f}")
    print(f"Delta (Put): {result['delta_put']:.4f}")
    print(f"Gamma: {result['gamma']:.4f}")
    print(f"Vega: {result['vega']:.4f}")