"""
LKL-Jr Scale Symmetry Analysis
==============================
Analyzes mirror pair symmetry in the IEC binary scale.
Explores symmetrical relationships: B ↔ YiB, KiB ↔ ZiB, MiB ↔ EiB, GiB ↔ TiB

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Symmetry Principle:
The 8-level scale can be viewed as 4 mirror pairs arranged around a geometric center.
Each pair's product gives 2^(70) = total scale product.
This reveals hidden balance and harmonic structure.
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
import math


# ============= CONSTANTS =============

SCALE_PREFIXES = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'EiB', 'ZiB', 'YiB']
SCALE_EXPONENTS = [0, 10, 20, 30, 40, 50, 60, 70]
TOTAL_EXPONENT = sum(SCALE_EXPONENTS)  # 280


@dataclass
class SymmetryPair:
    """Represents a mirror pair in the scale."""
    left_index: int
    right_index: int
    left_name: str
    right_name: str
    left_exponent: int
    right_exponent: int
    left_factor: int
    right_factor: int
    
    def product_exponent(self) -> int:
        """Sum of exponents (power when multiplied)."""
        return self.left_exponent + self.right_exponent
    
    def product_factor(self) -> int:
        """Product of the two factors."""
        return self.left_factor * self.right_factor
    
    def geometric_mean_exponent(self) -> float:
        """Geometric mean of the two exponents."""
        return (self.left_exponent + self.right_exponent) / 2
    
    def geometric_mean_factor(self) -> float:
        """Geometric mean of the two factors."""
        return math.sqrt(self.left_factor * self.right_factor)
    
    def distance_from_center(self) -> int:
        """Absolute distance of indices from center."""
        center = (len(SCALE_PREFIXES) - 1) / 2
        left_dist = abs(self.left_index - center)
        right_dist = abs(self.right_index - center)
        return int(left_dist)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'left': {
                'name': self.left_name,
                'index': self.left_index,
                'exponent': self.left_exponent,
                'factor': self.left_factor,
            },
            'right': {
                'name': self.right_name,
                'index': self.right_index,
                'exponent': self.right_exponent,
                'factor': self.right_factor,
            },
            'product_exponent': self.product_exponent(),
            'product_factor': self.product_factor(),
            'geometric_mean_exponent': self.geometric_mean_exponent(),
            'geometric_mean_factor': self.geometric_mean_factor(),
        }


class ScaleSymmetry:
    """
    Analyzes mirror pair symmetry in the IEC binary scale.
    Reveals harmonic relationships and balance properties.
    """
    
    def __init__(self, prefixes: List[str] = None, exponents: List[int] = None):
        """
        Initialize symmetry analyzer.
        
        Args:
            prefixes: List of prefix names (defaults to standard IEC)
            exponents: List of exponents (defaults to standard IEC)
        """
        self.prefixes = prefixes or SCALE_PREFIXES
        self.exponents = exponents or SCALE_EXPONENTS
        self.scale_length = len(self.prefixes)
        self.pairs = self._generate_pairs()
    
    def _generate_pairs(self) -> List[SymmetryPair]:
        """Generate mirror pairs from scale."""
        pairs = []
        half = self.scale_length // 2
        
        # Pair from outside-in: (0,n-1), (1,n-2), ...
        for i in range(half):
            left_idx = i
            right_idx = self.scale_length - 1 - i
            
            pair = SymmetryPair(
                left_index=left_idx,
                right_index=right_idx,
                left_name=self.prefixes[left_idx],
                right_name=self.prefixes[right_idx],
                left_exponent=self.exponents[left_idx],
                right_exponent=self.exponents[right_idx],
                left_factor=2 ** self.exponents[left_idx],
                right_factor=2 ** self.exponents[right_idx],
            )
            pairs.append(pair)
        
        return pairs
    
    def get_pair(self, index: int) -> SymmetryPair:
        """Get pair by index (0-based from outside-in)."""
        if 0 <= index < len(self.pairs):
            return self.pairs[index]
        return None
    
    def center_of_symmetry(self) -> float:
        """Calculate geometric center of scale."""
        return (self.scale_length - 1) / 2
    
    def average_product_exponent(self) -> float:
        """Average product exponent across all pairs."""
        if not self.pairs:
            return 0
        return sum(p.product_exponent() for p in self.pairs) / len(self.pairs)
    
    def symmetry_verification(self) -> Dict[str, Any]:
        """Verify symmetry properties."""
        if len(self.pairs) == 0:
            return {'verified': False, 'reason': 'No pairs'}
        
        # Check if all pairs have same product exponent
        products = [p.product_exponent() for p in self.pairs]
        all_equal = len(set(products)) == 1
        
        return {
            'verified': all_equal,
            'product_exponent': products[0] if all_equal else None,
            'all_products': products,
            'is_constant': all_equal,
        }
    
    def mirror_index(self, index: int) -> int:
        """Get mirror index for given position."""
        return self.scale_length - 1 - index
    
    def print_pairs(self, max_width: int = 110) -> None:
        """Print formatted symmetry pair table."""
        print(f"\nSCALE SYMMETRY (mirror pairs):")
        print("-" * max_width)
        print(f"{'Pair':>4}  {'Left':>4} (2^{' '*2})  ↔  {'Right':>4} (2^{' '*2})  "
              f"{'Sum':>4}  {'Product':>15}  {'Geom Mean':>15}")
        print("-" * max_width)
        
        for i, pair in enumerate(self.pairs):
            prod = pair.product_factor()
            geom = pair.geometric_mean_factor()
            print(f"{i:>4}  {pair.left_name:>4} (2^{pair.left_exponent:>2})  ↔  "
                  f"{pair.right_name:>4} (2^{pair.right_exponent:>2})  "
                  f"{pair.product_exponent():>4}  {prod:>15,}  {geom:>15.0f}")
        
        print("-" * max_width)
        verification = self.symmetry_verification()
        if verification['is_constant']:
            print(f"All pairs have constant product exponent: 2^{verification['product_exponent']}")
    
    def print_symmetry_analysis(self) -> None:
        """Print detailed symmetry analysis."""
        print(f"\nSYMMETRY ANALYSIS:")
        print("-" * 80)
        
        center = self.center_of_symmetry()
        print(f"Scale length:        {self.scale_length}")
        print(f"Center position:     {center:.1f}")
        print(f"Number of pairs:     {len(self.pairs)}")
        print()
        
        verification = self.symmetry_verification()
        print(f"Symmetry verified:   {verification['is_constant']}")
        if verification['is_constant']:
            print(f"Product exponent:    2^{verification['product_exponent']}")
            print(f"Product factor:      2^{verification['product_exponent']} = {2**verification['product_exponent']:,}")
        print()
        
        avg_prod = self.average_product_exponent()
        print(f"Average product exp: {avg_prod:.1f}")
    
    def print_mirror_relationships(self) -> None:
        """Print individual pair details."""
        print(f"\nMIRROR PAIR DETAILS:")
        print("-" * 100)
        
        for i, pair in enumerate(self.pairs):
            print(f"\nPair {i}:")
            print(f"  {pair.left_name:>4} ↔ {pair.right_name:>4}")
            print(f"  Exponents:     {pair.left_exponent:>2} + {pair.right_exponent:>2} = {pair.product_exponent():>2}")
            print(f"  Factors:       2^{pair.left_exponent} × 2^{pair.right_exponent} = 2^{pair.product_exponent()}")
            print(f"  Numeric:       {pair.left_factor:>15,} × {pair.right_factor:>15,} = {pair.product_factor():>20,}")
            print(f"  Geom mean:     {pair.geometric_mean_factor():>20,.0f}")
            print(f"  Distance:      {pair.distance_from_center()} from center")


# ============= DEMONSTRATION =============

def demo_scale_symmetry():
    """Demonstrate scale symmetry analysis."""
    
    print("="*100)
    print("LKL-Jr SCALE SYMMETRY ANALYSIS")
    print("="*100)
    
    symmetry = ScaleSymmetry()
    
    # Print pair table
    print()
    symmetry.print_pairs()
    
    # Print symmetry analysis
    print()
    symmetry.print_symmetry_analysis()
    
    # Print detailed relationships
    print()
    symmetry.print_mirror_relationships()
    
    print("\n" + "="*100)
    print("✓ SCALE SYMMETRY ANALYSIS COMPLETE")
    print("="*100)


__all__ = [
    'ScaleSymmetry',
    'SymmetryPair',
    'SCALE_PREFIXES',
    'SCALE_EXPONENTS',
]

if __name__ == '__main__':
    demo_scale_symmetry()
