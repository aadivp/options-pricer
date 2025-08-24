import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from formulas import blackScholes, calculate_implied_volatility

class OptionsPricerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Options Pricer - Black-Scholes Model")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Default parameters
        self.S = tk.DoubleVar(value=100.0)  # Stock price
        self.K = tk.DoubleVar(value=100.0)  # Strike price
        self.T = tk.DoubleVar(value=1.0)    # Time to expiration
        self.r = tk.DoubleVar(value=0.05)   # Risk-free rate
        self.sigma = tk.DoubleVar(value=0.2) # Volatility
        
        # Implied volatility variables
        self.market_price = tk.DoubleVar(value=10.0)
        self.option_type = tk.StringVar(value="call")
        
        self.setup_ui()
        self.update_calculations()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Options Pricer - Black-Scholes Model", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Parameters
        self.create_parameter_panel(main_frame)
        
        # Center panel - Results
        self.create_results_panel(main_frame)
        
        # Right panel - Unique Features
        self.create_features_panel(main_frame)
        
        # Bottom panel - Charts
        self.create_charts_panel(main_frame)
        
    def create_parameter_panel(self, parent):
        param_frame = ttk.LabelFrame(parent, text="Parameters", padding="10")
        param_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Stock Price
        ttk.Label(param_frame, text="Stock Price (S):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.S_slider = ttk.Scale(param_frame, from_=10, to=200, variable=self.S, 
                                 orient=tk.HORIZONTAL, length=200, command=self.on_parameter_change)
        self.S_slider.grid(row=0, column=1, pady=5)
        self.S_label = ttk.Label(param_frame, text="100.0")
        self.S_label.grid(row=0, column=2, padx=(10, 0), pady=5)
        
        # Strike Price
        ttk.Label(param_frame, text="Strike Price (K):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.K_slider = ttk.Scale(param_frame, from_=10, to=200, variable=self.K, 
                                 orient=tk.HORIZONTAL, length=200, command=self.on_parameter_change)
        self.K_slider.grid(row=1, column=1, pady=5)
        self.K_label = ttk.Label(param_frame, text="100.0")
        self.K_label.grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # Time to Expiration
        ttk.Label(param_frame, text="Time to Expiry (T):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.T_slider = ttk.Scale(param_frame, from_=0.1, to=5.0, variable=self.T, 
                                 orient=tk.HORIZONTAL, length=200, command=self.on_parameter_change)
        self.T_slider.grid(row=2, column=1, pady=5)
        self.T_label = ttk.Label(param_frame, text="1.0")
        self.T_label.grid(row=2, column=2, padx=(10, 0), pady=5)
        
        # Risk-free Rate
        ttk.Label(param_frame, text="Risk-free Rate (r):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.r_slider = ttk.Scale(param_frame, from_=0.0, to=0.15, variable=self.r, 
                                 orient=tk.HORIZONTAL, length=200, command=self.on_parameter_change)
        self.r_slider.grid(row=3, column=1, pady=5)
        self.r_label = ttk.Label(param_frame, text="0.05")
        self.r_label.grid(row=3, column=2, padx=(10, 0), pady=5)
        
        # Volatility
        ttk.Label(param_frame, text="Volatility (σ):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.sigma_slider = ttk.Scale(param_frame, from_=0.05, to=0.8, variable=self.sigma, 
                                     orient=tk.HORIZONTAL, length=200, command=self.on_parameter_change)
        self.sigma_slider.grid(row=4, column=1, pady=5)
        self.sigma_label = ttk.Label(param_frame, text="0.2")
        self.sigma_label.grid(row=4, column=2, padx=(10, 0), pady=5)
        
    def create_results_panel(self, parent):
        results_frame = ttk.LabelFrame(parent, text="Option Prices & Greeks", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Option Prices
        prices_frame = ttk.LabelFrame(results_frame, text="Option Prices", padding="5")
        prices_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(prices_frame, text="Call Price:").grid(row=0, column=0, sticky=tk.W)
        self.call_price_label = ttk.Label(prices_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.call_price_label.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(prices_frame, text="Put Price:").grid(row=1, column=0, sticky=tk.W)
        self.put_price_label = ttk.Label(prices_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.put_price_label.grid(row=1, column=1, padx=(10, 0))
        
        # Greeks
        greeks_frame = ttk.LabelFrame(results_frame, text="Greeks", padding="5")
        greeks_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Delta
        ttk.Label(greeks_frame, text="Delta (Call):").grid(row=0, column=0, sticky=tk.W)
        self.delta_call_label = ttk.Label(greeks_frame, text="0.0000")
        self.delta_call_label.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(greeks_frame, text="Delta (Put):").grid(row=1, column=0, sticky=tk.W)
        self.delta_put_label = ttk.Label(greeks_frame, text="0.0000")
        self.delta_put_label.grid(row=1, column=1, padx=(10, 0))
        
        # Gamma
        ttk.Label(greeks_frame, text="Gamma:").grid(row=2, column=0, sticky=tk.W)
        self.gamma_label = ttk.Label(greeks_frame, text="0.0000")
        self.gamma_label.grid(row=2, column=1, padx=(10, 0))
        
        # Theta
        ttk.Label(greeks_frame, text="Theta (Call):").grid(row=3, column=0, sticky=tk.W)
        self.theta_call_label = ttk.Label(greeks_frame, text="0.0000")
        self.theta_call_label.grid(row=3, column=1, padx=(10, 0))
        
        ttk.Label(greeks_frame, text="Theta (Put):").grid(row=4, column=0, sticky=tk.W)
        self.theta_put_label = ttk.Label(greeks_frame, text="0.0000")
        self.theta_put_label.grid(row=4, column=1, padx=(10, 0))
        
        # Vega
        ttk.Label(greeks_frame, text="Vega:").grid(row=5, column=0, sticky=tk.W)
        self.vega_label = ttk.Label(greeks_frame, text="0.0000")
        self.vega_label.grid(row=5, column=1, padx=(10, 0))
        
    def create_features_panel(self, parent):
        features_frame = ttk.LabelFrame(parent, text="Advanced Features", padding="10")
        features_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Implied Volatility Calculator
        iv_frame = ttk.LabelFrame(features_frame, text="Implied Volatility Calculator", padding="5")
        iv_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(iv_frame, text="Market Price:").grid(row=0, column=0, sticky=tk.W)
        market_price_entry = ttk.Entry(iv_frame, textvariable=self.market_price, width=10)
        market_price_entry.grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(iv_frame, text="Option Type:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        option_type_combo = ttk.Combobox(iv_frame, textvariable=self.option_type, 
                                        values=["call", "put"], state="readonly", width=8)
        option_type_combo.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        
        calculate_iv_btn = ttk.Button(iv_frame, text="Calculate IV", command=self.calculate_implied_volatility)
        calculate_iv_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.iv_result_label = ttk.Label(iv_frame, text="IV: --", font=('Arial', 10, 'bold'))
        self.iv_result_label.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        # Sensitivity Analysis
        sensitivity_frame = ttk.LabelFrame(features_frame, text="Sensitivity Analysis", padding="5")
        sensitivity_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.sensitivity_var = tk.StringVar(value="stock_price")
        ttk.Radiobutton(sensitivity_frame, text="Stock Price", variable=self.sensitivity_var, 
                       value="stock_price", command=self.update_sensitivity_chart).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(sensitivity_frame, text="Strike Price", variable=self.sensitivity_var, 
                       value="strike_price", command=self.update_sensitivity_chart).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(sensitivity_frame, text="Time to Expiry", variable=self.sensitivity_var, 
                       value="time", command=self.update_sensitivity_chart).grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(sensitivity_frame, text="Volatility", variable=self.sensitivity_var, 
                       value="volatility", command=self.update_sensitivity_chart).grid(row=3, column=0, sticky=tk.W)
        
        # Risk Metrics
        risk_frame = ttk.LabelFrame(features_frame, text="Risk Metrics", padding="5")
        risk_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(risk_frame, text="Moneyness:").grid(row=0, column=0, sticky=tk.W)
        self.moneyness_label = ttk.Label(risk_frame, text="1.00")
        self.moneyness_label.grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(risk_frame, text="Intrinsic Value (Call):").grid(row=1, column=0, sticky=tk.W)
        self.intrinsic_call_label = ttk.Label(risk_frame, text="$0.00")
        self.intrinsic_call_label.grid(row=1, column=1, padx=(10, 0))
        
        ttk.Label(risk_frame, text="Intrinsic Value (Put):").grid(row=2, column=0, sticky=tk.W)
        self.intrinsic_put_label = ttk.Label(risk_frame, text="$0.00")
        self.intrinsic_put_label.grid(row=2, column=1, padx=(10, 0))
        
        ttk.Label(risk_frame, text="Time Value (Call):").grid(row=3, column=0, sticky=tk.W)
        self.time_value_call_label = ttk.Label(risk_frame, text="$0.00")
        self.time_value_call_label.grid(row=3, column=1, padx=(10, 0))
        
        ttk.Label(risk_frame, text="Time Value (Put):").grid(row=4, column=0, sticky=tk.W)
        self.time_value_put_label = ttk.Label(risk_frame, text="$0.00")
        self.time_value_put_label.grid(row=4, column=1, padx=(10, 0))
        
    def create_charts_panel(self, parent):
        charts_frame = ttk.LabelFrame(parent, text="Charts & Analysis", padding="10")
        charts_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial charts
        self.update_sensitivity_chart()
        self.update_payoff_chart()
        
    def on_parameter_change(self, event=None):
        """Update all calculations when parameters change"""
        # Update labels
        self.S_label.config(text=f"{self.S.get():.1f}")
        self.K_label.config(text=f"{self.K.get():.1f}")
        self.T_label.config(text=f"{self.T.get():.2f}")
        self.r_label.config(text=f"{self.r.get():.3f}")
        self.sigma_label.config(text=f"{self.sigma.get():.2f}")
        
        # Update calculations
        self.update_calculations()
        
    def update_calculations(self):
        """Update all option prices and Greeks"""
        try:
            result = blackScholes(self.S.get(), self.K.get(), self.T.get(), 
                                self.r.get(), self.sigma.get())
            
            # Update option prices
            self.call_price_label.config(text=f"${result['call_price']:.4f}")
            self.put_price_label.config(text=f"${result['put_price']:.4f}")
            
            # Update Greeks
            self.delta_call_label.config(text=f"{result['delta_call']:.4f}")
            self.delta_put_label.config(text=f"{result['delta_put']:.4f}")
            self.gamma_label.config(text=f"{result['gamma']:.4f}")
            self.theta_call_label.config(text=f"{result['theta_call']:.4f}")
            self.theta_put_label.config(text=f"{result['theta_put']:.4f}")
            self.vega_label.config(text=f"{result['vega']:.4f}")
            
            # Update risk metrics
            self.update_risk_metrics(result)
            
            # Update charts
            self.update_sensitivity_chart()
            self.update_payoff_chart()
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def update_risk_metrics(self, result):
        """Update risk metrics display"""
        S, K = self.S.get(), self.K.get()
        
        # Moneyness
        moneyness = S / K
        self.moneyness_label.config(text=f"{moneyness:.2f}")
        
        # Intrinsic values
        intrinsic_call = max(0, S - K)
        intrinsic_put = max(0, K - S)
        self.intrinsic_call_label.config(text=f"${intrinsic_call:.2f}")
        self.intrinsic_put_label.config(text=f"${intrinsic_put:.2f}")
        
        # Time values
        time_value_call = result['call_price'] - intrinsic_call
        time_value_put = result['put_price'] - intrinsic_put
        self.time_value_call_label.config(text=f"${time_value_call:.2f}")
        self.time_value_put_label.config(text=f"${time_value_put:.2f}")
    
    def calculate_implied_volatility(self):
        """Calculate implied volatility from market price"""
        try:
            iv = calculate_implied_volatility(
                self.S.get(), self.K.get(), self.T.get(), self.r.get(),
                self.market_price.get(), self.option_type.get()
            )
            
            if iv > 0:
                self.iv_result_label.config(text=f"IV: {iv:.4f} ({iv*100:.2f}%)")
            else:
                self.iv_result_label.config(text="IV: Not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"IV calculation error: {str(e)}")
    
    def update_sensitivity_chart(self):
        """Update sensitivity analysis chart"""
        self.ax1.clear()
        
        param_name = self.sensitivity_var.get()
        
        if param_name == "stock_price":
            x_range = np.linspace(50, 150, 100)
            x_label = "Stock Price ($)"
            param_values = [(S, self.K.get(), self.T.get(), self.r.get(), self.sigma.get()) for S in x_range]
        elif param_name == "strike_price":
            x_range = np.linspace(50, 150, 100)
            x_label = "Strike Price ($)"
            param_values = [(self.S.get(), K, self.T.get(), self.r.get(), self.sigma.get()) for K in x_range]
        elif param_name == "time":
            x_range = np.linspace(0.1, 5, 100)
            x_label = "Time to Expiry (years)"
            param_values = [(self.S.get(), self.K.get(), T, self.r.get(), self.sigma.get()) for T in x_range]
        else:  # volatility
            x_range = np.linspace(0.05, 0.8, 100)
            x_label = "Volatility"
            param_values = [(self.S.get(), self.K.get(), self.T.get(), self.r.get(), sigma) for sigma in x_range]
        
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
        
        self.ax1.plot(x_range, call_prices, label='Call Price', color='blue', linewidth=2)
        self.ax1.plot(x_range, put_prices, label='Put Price', color='red', linewidth=2)
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel('Option Price ($)')
        self.ax1.set_title(f'Sensitivity to {param_name.replace("_", " ").title()}')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def update_payoff_chart(self):
        """Update payoff diagram chart"""
        self.ax2.clear()
        
        S_range = np.linspace(50, 150, 100)
        K = self.K.get()
        
        # Payoff calculations
        call_payoff = np.maximum(S_range - K, 0)
        put_payoff = np.maximum(K - S_range, 0)
        
        # Current option prices
        call_price = blackScholes(self.S.get(), K, self.T.get(), self.r.get(), self.sigma.get())['call_price']
        put_price = blackScholes(self.S.get(), K, self.T.get(), self.r.get(), self.sigma.get())['put_price']
        
        # Profit/Loss (subtract option premium)
        call_profit = call_payoff - call_price
        put_profit = put_payoff - put_price
        
        self.ax2.plot(S_range, call_profit, label='Call Profit/Loss', color='blue', linewidth=2)
        self.ax2.plot(S_range, put_profit, label='Put Profit/Loss', color='red', linewidth=2)
        self.ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        self.ax2.axvline(x=K, color='green', linestyle='--', alpha=0.5, label=f'Strike Price (${K})')
        self.ax2.set_xlabel('Stock Price at Expiry ($)')
        self.ax2.set_ylabel('Profit/Loss ($)')
        self.ax2.set_title('Option Payoff Diagram')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = OptionsPricerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 