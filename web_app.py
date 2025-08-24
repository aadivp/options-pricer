import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from formulas import blackScholes, calculate_implied_volatility

# Page configuration
st.set_page_config(
    page_title="Options Pricer - Black-Scholes Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stSlider > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Options Pricer - Black-Scholes Model</h1>', unsafe_allow_html=True)
    
    # Sidebar for parameters
    with st.sidebar:
        st.header("🎛️ Parameters")
        
        # Parameter sliders
        S = st.slider("Stock Price (S)", 10.0, 200.0, 100.0, 1.0, help="Current price of the underlying asset")
        K = st.slider("Strike Price (K)", 10.0, 200.0, 100.0, 1.0, help="Option exercise price")
        T = st.slider("Time to Expiry (T)", 0.1, 5.0, 1.0, 0.1, help="Time until option expiration in years")
        r = st.slider("Risk-free Rate (r)", 0.0, 0.15, 0.05, 0.01, help="Annual risk-free interest rate")
        sigma = st.slider("Volatility (σ)", 0.05, 0.8, 0.2, 0.01, help="Annualized volatility of the underlying")
        
        st.markdown("---")
        
        # Implied Volatility Calculator
        st.header("🔍 Implied Volatility")
        market_price = st.number_input("Market Price", 0.0, 100.0, 10.0, 0.1)
        option_type = st.selectbox("Option Type", ["call", "put"])
        
        if st.button("Calculate Implied Volatility"):
            try:
                iv = calculate_implied_volatility(S, K, T, r, market_price, option_type)
                if iv > 0:
                    st.success(f"Implied Volatility: {iv:.4f} ({iv*100:.2f}%)")
                else:
                    st.error("Implied volatility not found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Option Prices
        st.header("💰 Option Prices")
        
        try:
            result = blackScholes(S, K, T, r, sigma)
            
            # Create metrics display
            col1_1, col1_2 = st.columns(2)
            
            with col1_1:
                st.metric("Call Price", f"${result['call_price']:.4f}")
                st.metric("Put Price", f"${result['put_price']:.4f}")
            
            with col1_2:
                # Risk metrics
                moneyness = S / K
                intrinsic_call = max(0, S - K)
                intrinsic_put = max(0, K - S)
                time_value_call = result['call_price'] - intrinsic_call
                time_value_put = result['put_price'] - intrinsic_put
                
                st.metric("Moneyness", f"{moneyness:.2f}")
                st.metric("Intrinsic Value (Call)", f"${intrinsic_call:.2f}")
                st.metric("Time Value (Call)", f"${time_value_call:.2f}")
        
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")
    
    with col2:
        # Greeks
        st.header("📊 Option Greeks")
        
        try:
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                st.metric("Delta (Call)", f"{result['delta_call']:.4f}")
                st.metric("Delta (Put)", f"{result['delta_put']:.4f}")
                st.metric("Gamma", f"{result['gamma']:.4f}")
            
            with col2_2:
                st.metric("Theta (Call)", f"{result['theta_call']:.4f}")
                st.metric("Theta (Put)", f"{result['theta_put']:.4f}")
                st.metric("Vega", f"{result['vega']:.4f}")
        
        except Exception as e:
            st.error(f"Greeks calculation error: {str(e)}")
    
    # Charts section
    st.markdown("---")
    st.header("📈 Charts & Analysis")
    
    # Sensitivity Analysis
    st.subheader("Sensitivity Analysis")
    sensitivity_param = st.selectbox(
        "Select Parameter for Sensitivity Analysis",
        ["Stock Price", "Strike Price", "Time to Expiry", "Volatility"]
    )
    
    # Create sensitivity chart
    fig_sensitivity = create_sensitivity_chart(S, K, T, r, sigma, sensitivity_param)
    st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    # Payoff Diagram
    st.subheader("Payoff Diagram")
    fig_payoff = create_payoff_chart(S, K, T, r, sigma)
    st.plotly_chart(fig_payoff, use_container_width=True)
    
    # Greeks Visualization
    st.subheader("Greeks Visualization")
    fig_greeks = create_greeks_chart(S, K, T, r, sigma)
    st.plotly_chart(fig_greeks, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit • Black-Scholes Model • Real-time Calculations</p>
    </div>
    """, unsafe_allow_html=True)

def create_sensitivity_chart(S, K, T, r, sigma, param_name):
    """Create sensitivity analysis chart"""
    if param_name == "Stock Price":
        x_range = np.linspace(50, 150, 100)
        x_label = "Stock Price ($)"
        param_values = [(s, K, T, r, sigma) for s in x_range]
    elif param_name == "Strike Price":
        x_range = np.linspace(50, 150, 100)
        x_label = "Strike Price ($)"
        param_values = [(S, k, T, r, sigma) for k in x_range]
    elif param_name == "Time to Expiry":
        x_range = np.linspace(0.1, 5, 100)
        x_label = "Time to Expiry (years)"
        param_values = [(S, K, t, r, sigma) for t in x_range]
    else:  # Volatility
        x_range = np.linspace(0.05, 0.8, 100)
        x_label = "Volatility"
        param_values = [(S, K, T, r, s) for s in x_range]
    
    call_prices = []
    put_prices = []
    
    for params in param_values:
        try:
            result = blackScholes(*params)
            call_prices.append(result['call_price'])
            put_prices.append(result['put_price'])
        except:
            call_prices.append(0)
            put_prices.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_range, y=call_prices,
        mode='lines',
        name='Call Price',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=x_range, y=put_prices,
        mode='lines',
        name='Put Price',
        line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title=f'Sensitivity to {param_name}',
        xaxis_title=x_label,
        yaxis_title='Option Price ($)',
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

def create_payoff_chart(S, K, T, r, sigma):
    """Create payoff diagram"""
    S_range = np.linspace(50, 150, 100)
    
    # Payoff calculations
    call_payoff = np.maximum(S_range - K, 0)
    put_payoff = np.maximum(K - S_range, 0)
    
    # Current option prices
    try:
        result = blackScholes(S, K, T, r, sigma)
        call_price = result['call_price']
        put_price = result['put_price']
    except:
        call_price = put_price = 0
    
    # Profit/Loss (subtract option premium)
    call_profit = call_payoff - call_price
    put_profit = put_payoff - put_price
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=S_range, y=call_profit,
        mode='lines',
        name='Call Profit/Loss',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=S_range, y=put_profit,
        mode='lines',
        name='Put Profit/Loss',
        line=dict(color='red', width=3)
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
    
    # Add strike price line
    fig.add_vline(x=K, line_dash="dash", line_color="green", opacity=0.5,
                  annotation_text=f"Strike Price (${K})")
    
    fig.update_layout(
        title='Option Payoff Diagram',
        xaxis_title='Stock Price at Expiry ($)',
        yaxis_title='Profit/Loss ($)',
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

def create_greeks_chart(S, K, T, r, sigma):
    """Create Greeks visualization chart"""
    S_range = np.linspace(50, 150, 100)
    
    deltas_call = []
    deltas_put = []
    gammas = []
    vegas = []
    
    for s in S_range:
        try:
            result = blackScholes(s, K, T, r, sigma)
            deltas_call.append(result['delta_call'])
            deltas_put.append(result['delta_put'])
            gammas.append(result['gamma'])
            vegas.append(result['vega'])
        except:
            deltas_call.append(0)
            deltas_put.append(0)
            gammas.append(0)
            vegas.append(0)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Delta (Call)', 'Delta (Put)', 'Gamma', 'Vega'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Delta Call
    fig.add_trace(
        go.Scatter(x=S_range, y=deltas_call, mode='lines', name='Delta Call',
                  line=dict(color='blue', width=2)),
        row=1, col=1
    )
    
    # Delta Put
    fig.add_trace(
        go.Scatter(x=S_range, y=deltas_put, mode='lines', name='Delta Put',
                  line=dict(color='red', width=2)),
        row=1, col=2
    )
    
    # Gamma
    fig.add_trace(
        go.Scatter(x=S_range, y=gammas, mode='lines', name='Gamma',
                  line=dict(color='green', width=2)),
        row=2, col=1
    )
    
    # Vega
    fig.add_trace(
        go.Scatter(x=S_range, y=vegas, mode='lines', name='Vega',
                  line=dict(color='purple', width=2)),
        row=2, col=2
    )
    
    fig.update_layout(
        title='Option Greeks Visualization',
        height=500,
        showlegend=False
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Stock Price ($)", row=2, col=1)
    fig.update_xaxes(title_text="Stock Price ($)", row=2, col=2)
    fig.update_yaxes(title_text="Delta", row=1, col=1)
    fig.update_yaxes(title_text="Delta", row=1, col=2)
    fig.update_yaxes(title_text="Gamma", row=2, col=1)
    fig.update_yaxes(title_text="Vega", row=2, col=2)
    
    return fig

if __name__ == "__main__":
    main() 