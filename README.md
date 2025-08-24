# Advanced Options Pricer - Black-Scholes Model

A comprehensive GUI application for calculating option prices using the Black-Scholes model with real-time sensitivity analysis and advanced features.

## Features

### Core Functionality
- **Black-Scholes Option Pricing**: Calculate call and put option prices
- **Option Greeks**: Delta, Gamma, Theta, and Vega calculations
- **Interactive Sliders**: Real-time parameter adjustment for all Black-Scholes inputs
- **Risk Metrics**: Moneyness, intrinsic value, and time value calculations

### Advanced Features (Unique Additions)
1. **Implied Volatility Calculator**: Reverse-engineer volatility from market prices
2. **Sensitivity Analysis**: Interactive charts showing how option prices change with different parameters
3. **Payoff Diagrams**: Visual representation of option profit/loss scenarios
4. **Real-time Updates**: All calculations and charts update instantly when parameters change

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python gui.py
```

## Usage

### Parameter Panel (Left)
- **Stock Price (S)**: Current price of the underlying asset ($10-$200)
- **Strike Price (K)**: Option exercise price ($10-$200)
- **Time to Expiry (T)**: Time until option expiration (0.1-5 years)
- **Risk-free Rate (r)**: Annual risk-free interest rate (0%-15%)
- **Volatility (σ)**: Annualized volatility of the underlying (5%-80%)

### Results Panel (Center)
- **Option Prices**: Call and put option premiums
- **Greeks**: Risk measures (Delta, Gamma, Theta, Vega)

### Advanced Features Panel (Right)
- **Implied Volatility Calculator**: Enter market price and option type to calculate implied volatility
- **Sensitivity Analysis**: Choose parameter to analyze (Stock Price, Strike Price, Time, Volatility)
- **Risk Metrics**: Moneyness ratio, intrinsic values, and time values

### Charts Panel (Bottom)
- **Sensitivity Chart**: Shows how option prices change with selected parameter
- **Payoff Diagram**: Visualizes profit/loss scenarios at expiration

## Mathematical Background

### Black-Scholes Formula
The application uses the standard Black-Scholes formula for European options:

**Call Option:**
```
C = S * N(d1) - K * e^(-rT) * N(d2)
```

**Put Option:**
```
P = K * e^(-rT) * N(-d2) - S * N(-d1)
```

Where:
- d1 = (ln(S/K) + (r + σ²/2)T) / (σ√T)
- d2 = d1 - σ√T
- N(x) = Cumulative normal distribution function

### Option Greeks
- **Delta**: Rate of change of option price with respect to underlying price
- **Gamma**: Rate of change of delta with respect to underlying price
- **Theta**: Rate of change of option price with respect to time
- **Vega**: Rate of change of option price with respect to volatility

## Unique Features Explained

### 1. Implied Volatility Calculator
Uses Newton-Raphson method to find the volatility that matches a given market price. This is useful for:
- Understanding market expectations
- Identifying mispriced options
- Risk management

### 2. Sensitivity Analysis
Interactive charts showing how option prices respond to parameter changes:
- **Stock Price Sensitivity**: Shows option value as underlying price changes
- **Strike Price Sensitivity**: Shows option value across different strike prices
- **Time Decay**: Shows how option value changes as expiration approaches
- **Volatility Impact**: Shows option value sensitivity to volatility changes

### 3. Risk Metrics
- **Moneyness**: Ratio of stock price to strike price (S/K)
- **Intrinsic Value**: Immediate exercise value of the option
- **Time Value**: Option premium minus intrinsic value

## Example Scenarios

### At-the-Money Option
- Stock Price: $100
- Strike Price: $100
- Time to Expiry: 1 year
- Risk-free Rate: 5%
- Volatility: 20%

### In-the-Money Call
- Stock Price: $110
- Strike Price: $100
- Higher intrinsic value, lower time value

### Out-of-the-Money Put
- Stock Price: $90
- Strike Price: $100
- No intrinsic value, all time value

## Technical Notes

- The application uses scipy.stats for normal distribution calculations
- Matplotlib provides real-time chart updates
- Tkinter creates the responsive GUI interface
- All calculations are performed in real-time as parameters change

## Limitations

- Assumes European-style options (no early exercise)
- Assumes constant volatility (no volatility smile)
- Assumes no dividends
- Assumes efficient markets and no transaction costs

## Future Enhancements

Potential additions could include:
- American option pricing (binomial/trinomial models)
- Dividend adjustments
- Volatility surface modeling
- Portfolio analysis tools
- Historical data integration
- Monte Carlo simulation 