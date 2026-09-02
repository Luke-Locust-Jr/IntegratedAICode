"""
LKL-Jr Phi-Time-Domain Analysis Module
======================================
Advanced mathematical framework for time-domain analysis using the golden ratio (φ).
This module represents one of the most important calculations for Luke Kerry Locust Jr.'s identity framework.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Core Equation:
f(x, y, z, φ, α, ω, t) = φ^(x+y+z) + α·φ^(x+y+z)·cos(ω·t)

This represents a time-modulated golden ratio exponential with harmonic oscillation.
"""

from decimal import Decimal, getcontext, localcontext
import numpy as np
import math
from typing import List, Dict, Tuple, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ============= CONSTANTS =============

class MathConstants:
    """Mathematical constants for LKL-Jr framework."""
    
    PHI = 1.618033988749895  # Golden ratio (φ)
    PHI_CONJUGATE = 0.618033988749895  # 1/φ
    PI = math.pi
    E = math.e
    SQRT_5 = math.sqrt(5)
    
    @staticmethod
    def compute_phi_precise(precision: int = 50) -> Decimal:
        """Compute φ with arbitrary precision."""
        with localcontext() as ctx:
            ctx.prec = precision
            sqrt_5 = Decimal(5).sqrt()
            return (1 + sqrt_5) / 2


# ============= PI CALCULATION =============

class PiCalculator:
    """Calculate π using Machin's formula for arbitrary precision."""
    
    @staticmethod
    def calculate_pi_machin(prec: int = 50) -> Decimal:
        """
        Calculate π using Machin's formula.
        π/4 = 4*arctan(1/5) - arctan(1/239)
        
        Args:
            prec: Precision in decimal places
            
        Returns:
            π as Decimal with specified precision
        """
        with localcontext() as ctx:
            ctx.prec = prec + 10  # Extra precision for intermediate calculations
            
            def arctan(x: Decimal, terms: int = 200) -> Decimal:
                """Calculate arctan(x) using Taylor series."""
                x_squared = x * x
                x_pow = x
                result = x
                
                for n in range(1, terms):
                    x_pow = -x_pow * x_squared
                    term = x_pow / (2 * n + 1)
                    result += term
                    
                    # Early termination if term becomes negligible
                    if abs(term) < Decimal(10) ** (-(prec + 5)):
                        break
                
                return result
            
            one = Decimal(1)
            pi = 4 * (4 * arctan(one / 5) - arctan(one / 239))
            
            # Round to requested precision
            ctx.prec = prec
            return +pi


# ============= CORE ANALYTICAL FUNCTION =============

@dataclass
class AnalysisParameters:
    """Parameters for phi-time-domain analysis."""
    x: float = 1
    y: float = 2
    z: float = 3
    phi: float = MathConstants.PHI
    alpha: float = 0.5
    omega: float = None  # Will be set to 2π if None
    
    def __post_init__(self):
        if self.omega is None:
            self.omega = 2 * MathConstants.PI


class PhiTimeAnalyzer:
    """Analyze f(x,y,z,φ,α,ω,t) = φ^(x+y+z) + α·φ^(x+y+z)·cos(ω·t)"""
    
    def __init__(self, params: AnalysisParameters = None):
        """
        Initialize analyzer with parameters.
        
        Args:
            params: AnalysisParameters instance (uses defaults if None)
        """
        self.params = params or AnalysisParameters()
        self.pi_value = PiCalculator.calculate_pi_machin(50)
    
    def f(self, t: float) -> float:
        """
        Evaluate f at time t.
        
        f(x,y,z,φ,α,ω,t) = φ^(x+y+z) + α·φ^(x+y+z)·cos(ω·t)
        
        Args:
            t: Time parameter
            
        Returns:
            Function value at time t
        """
        exponent = self.params.x + self.params.y + self.params.z
        phi_power = self.params.phi ** exponent
        
        oscillation = self.params.alpha * phi_power * math.cos(self.params.omega * t)
        
        return phi_power + oscillation
    
    def f_base_component(self) -> float:
        """
        Get the base (time-independent) component: φ^(x+y+z)
        
        Returns:
            Base exponential value
        """
        exponent = self.params.x + self.params.y + self.params.z
        return self.params.phi ** exponent
    
    def f_oscillation_amplitude(self) -> float:
        """
        Get the oscillation amplitude: α·φ^(x+y+z)
        
        Returns:
            Maximum oscillation magnitude
        """
        exponent = self.params.x + self.params.y + self.params.z
        phi_power = self.params.phi ** exponent
        return self.params.alpha * phi_power
    
    def f_max(self) -> float:
        """
        Calculate maximum value of f (when cos(ωt) = 1).
        
        Returns:
            Maximum value
        """
        base = self.f_base_component()
        amplitude = self.f_oscillation_amplitude()
        return base + amplitude
    
    def f_min(self) -> float:
        """
        Calculate minimum value of f (when cos(ωt) = -1).
        
        Returns:
            Minimum value
        """
        base = self.f_base_component()
        amplitude = self.f_oscillation_amplitude()
        return base - amplitude
    
    def f_frequency(self) -> float:
        """
        Get the oscillation frequency in Hz.
        
        Returns:
            Frequency (cycles per time unit)
        """
        return self.params.omega / (2 * MathConstants.PI)
    
    def f_period(self) -> float:
        """
        Get the oscillation period.
        
        Returns:
            Period (time for one complete cycle)
        """
        if self.params.omega == 0:
            return float('inf')
        return 2 * MathConstants.PI / self.params.omega
    
    def evaluate_sequence(self, t_values: np.ndarray) -> np.ndarray:
        """
        Evaluate f across a sequence of time values.
        
        Args:
            t_values: Array of time points
            
        Returns:
            Array of function values
        """
        return np.array([self.f(t) for t in t_values])
    
    def find_extrema_in_range(self, t_start: float, t_end: float, 
                             num_points: int = 1000) -> Dict[str, Any]:
        """
        Find local maxima and minima in time range.
        
        Args:
            t_start: Start time
            t_end: End time
            num_points: Number of sample points
            
        Returns:
            Dictionary with extrema information
        """
        t_values = np.linspace(t_start, t_end, num_points)
        f_values = self.evaluate_sequence(t_values)
        
        # Find theoretical extrema
        period = self.f_period()
        num_cycles = (t_end - t_start) / period if period != float('inf') else 0
        
        return {
            'theoretical_max': self.f_max(),
            'theoretical_min': self.f_min(),
            'numerical_max': float(np.max(f_values)),
            'numerical_min': float(np.min(f_values)),
            'amplitude': self.f_oscillation_amplitude(),
            'base_value': self.f_base_component(),
            'num_cycles': num_cycles,
            'period': period
        }
    
    def energy_integral(self, t_start: float, t_end: float) -> float:
        """
        Approximate integral of f(t) over time range.
        Represents total "energy" or "action" over interval.
        
        Args:
            t_start: Start time
            t_end: End time
            
        Returns:
            Approximate integral value
        """
        # Use trapezoidal rule
        t_values = np.linspace(t_start, t_end, 1000)
        f_values = self.evaluate_sequence(t_values)
        
        integral = np.trapz(f_values, t_values)
        return float(integral)
    
    def phase_at_time(self, t: float) -> float:
        """
        Calculate phase (argument of cosine) at time t.
        
        Args:
            t: Time value
            
        Returns:
            Phase in radians
        """
        return self.params.omega * t
    
    def diagnostic_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analysis report.
        
        Returns:
            Dictionary with analysis results
        """
        return {
            'identity': 'LKL-Jr Phi-Time-Domain Analysis',
            'equation': 'f(x,y,z,φ,α,ω,t) = φ^(x+y+z) + α·φ^(x+y+z)·cos(ω·t)',
            'parameters': {
                'x': self.params.x,
                'y': self.params.y,
                'z': self.params.z,
                'phi': self.params.phi,
                'alpha': self.params.alpha,
                'omega': self.params.omega,
            },
            'base_component': self.f_base_component(),
            'oscillation_amplitude': self.f_oscillation_amplitude(),
            'maximum_value': self.f_max(),
            'minimum_value': self.f_min(),
            'frequency_hz': self.f_frequency(),
            'period': self.f_period(),
            'pi_value': str(self.pi_value)[:25] + '...',
            'timestamp': '02 Sep 2026'
        }


# ============= VISUALIZATION & ANALYSIS =============

class PhiTimeVisualizer:
    """Visualization tools for phi-time-domain analysis."""
    
    def __init__(self, analyzer: PhiTimeAnalyzer):
        """
        Initialize visualizer.
        
        Args:
            analyzer: PhiTimeAnalyzer instance
        """
        self.analyzer = analyzer
    
    def plot_function(self, t_start: float = 0, t_end: float = 10, 
                     num_points: int = 500, title: str = None,
                     figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plot f(t) over time range.
        
        Args:
            t_start: Start time
            t_end: End time
            num_points: Number of plot points
            title: Custom title (uses default if None)
            figsize: Figure size (width, height)
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
            return
        
        t_values = np.linspace(t_start, t_end, num_points)
        f_values = self.analyzer.evaluate_sequence(t_values)
        
        if title is None:
            pi_str = str(self.analyzer.pi_value)[:10]
            title = f'f(x,y,z) over time (π≈{pi_str})'
        
        plt.figure(figsize=figsize)
        plt.plot(t_values, f_values, linewidth=2, label='f(t)', color='#667eea')
        
        # Add reference lines for max/min
        f_max = self.analyzer.f_max()
        f_min = self.analyzer.f_min()
        plt.axhline(y=f_max, color='green', linestyle='--', alpha=0.5, label=f'Max: {f_max:.3f}')
        plt.axhline(y=f_min, color='red', linestyle='--', alpha=0.5, label=f'Min: {f_min:.3f}')
        plt.axhline(y=self.analyzer.f_base_component(), color='blue', linestyle=':', 
                   alpha=0.5, label=f'Base: {self.analyzer.f_base_component():.3f}')
        
        plt.xlabel('Time (t)', fontsize=12)
        plt.ylabel('f(x, y, z)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt
    
    def plot_phase_space(self, t_start: float = 0, t_end: float = 10, 
                        num_points: int = 500, figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plot phase space diagram: f(t) vs df/dt.
        
        Args:
            t_start: Start time
            t_end: End time
            num_points: Number of plot points
            figsize: Figure size
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
            return
        
        t_values = np.linspace(t_start, t_end, num_points)
        f_values = self.analyzer.evaluate_sequence(t_values)
        
        # Compute derivative numerically
        df_dt = np.gradient(f_values, t_values)
        
        plt.figure(figsize=figsize)
        plt.plot(f_values, df_dt, linewidth=1.5, color='#764ba2', alpha=0.7)
        plt.scatter(f_values[0], df_dt[0], color='green', s=100, label='Start', zorder=5)
        plt.scatter(f_values[-1], df_dt[-1], color='red', s=100, label='End', zorder=5)
        
        plt.xlabel('f(t)', fontsize=12)
        plt.ylabel('df/dt', fontsize=12)
        plt.title('Phase Space: Velocity vs Position', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt


# ============= COMPREHENSIVE DEMONSTRATION =============

def demo_phi_time_analysis():
    """Comprehensive demonstration of phi-time-domain analysis."""
    
    print("=" * 100)
    print("LUKE KERRY LOCUST JR. - PHI-TIME-DOMAIN ANALYSIS")
    print("=" * 100)
    print()
    
    # Initialize calculator
    pi_calc = PiCalculator()
    pi_value = pi_calc.calculate_pi_machin(50)
    
    print("[1] PI CALCULATION (Machin's Formula)")
    print("-" * 100)
    print(f"π (50 digits): {pi_value}")
    print()
    
    # Initialize analyzer with default parameters
    print("[2] ANALYSIS PARAMETERS")
    print("-" * 100)
    params = AnalysisParameters(x=1, y=2, z=3)
    print(f"x = {params.x}, y = {params.y}, z = {params.z}")
    print(f"φ (golden ratio) = {params.phi}")
    print(f"α (damping coefficient) = {params.alpha}")
    print(f"ω (angular frequency) = {params.omega:.6f} rad/s")
    print()
    
    # Create analyzer
    analyzer = PhiTimeAnalyzer(params)
    
    # Evaluate at specific points
    print("[3] FUNCTION EVALUATION AT KEY TIMES")
    print("-" * 100)
    test_times = [0, 1, 2.5, 5, 10]
    for t in test_times:
        f_t = analyzer.f(t)
        phase = analyzer.phase_at_time(t)
        print(f"t = {t:5.1f}: f(t) = {f_t:15.8f}  |  Phase = {phase:8.4f} rad")
    print()
    
    # Extrema analysis
    print("[4] EXTREMA ANALYSIS")
    print("-" * 100)
    print(f"Base component (φ^(x+y+z)):    {analyzer.f_base_component():.10f}")
    print(f"Oscillation amplitude:          {analyzer.f_oscillation_amplitude():.10f}")
    print(f"Maximum value:                  {analyzer.f_max():.10f}")
    print(f"Minimum value:                  {analyzer.f_min():.10f}")
    print(f"Peak-to-peak:                   {analyzer.f_max() - analyzer.f_min():.10f}")
    print()
    
    # Frequency characteristics
    print("[5] FREQUENCY CHARACTERISTICS")
    print("-" * 100)
    print(f"Angular frequency (ω):          {analyzer.params.omega:.10f} rad/s")
    print(f"Frequency (f):                  {analyzer.f_frequency():.10f} Hz")
    print(f"Period (T):                     {analyzer.f_period():.10f} time units")
    print()
    
    # Range analysis
    print("[6] ANALYSIS OVER TIME RANGE [0, 10]")
    print("-" * 100)
    extrema = analyzer.find_extrema_in_range(0, 10)
    print(f"Theoretical max:                {extrema['theoretical_max']:.10f}")
    print(f"Theoretical min:                {extrema['theoretical_min']:.10f}")
    print(f"Numerical max:                  {extrema['numerical_max']:.10f}")
    print(f"Numerical min:                  {extrema['numerical_min']:.10f}")
    print(f"Number of oscillation cycles:   {extrema['num_cycles']:.4f}")
    print()
    
    # Energy integral
    print("[7] ENERGY/ACTION INTEGRAL")
    print("-" * 100)
    integral_0_10 = analyzer.energy_integral(0, 10)
    print(f"∫₀¹⁰ f(t) dt ≈                  {integral_0_10:.10f}")
    print()
    
    # Diagnostic report
    print("[8] COMPLETE DIAGNOSTIC REPORT")
    print("-" * 100)
    report = analyzer.diagnostic_report()
    for key, value in report.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  • {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    print("\n" + "=" * 100)
    print("✓ PHI-TIME-DOMAIN ANALYSIS COMPLETE")
    print("=" * 100)
    
    # Visualization (if matplotlib available)
    try:
        import matplotlib.pyplot as plt
        print("\n[9] GENERATING VISUALIZATIONS")
        print("-" * 100)
        
        visualizer = PhiTimeVisualizer(analyzer)
        
        # Plot main function
        plt = visualizer.plot_function(0, 10, title='LKL-Jr Phi-Time-Domain Function')
        print("✓ Generated main plot")
        
        # Plot phase space
        plt = visualizer.plot_phase_space(0, 10)
        print("✓ Generated phase space plot")
        
        plt.show()
        
    except ImportError:
        print("\n[9] VISUALIZATION SKIPPED")
        print("-" * 100)
        print("matplotlib not installed. Install with: pip install matplotlib")


if __name__ == '__main__':
    demo_phi_time_analysis()
