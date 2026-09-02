"""
LKL-Jr Scale Sieve Algorithm
============================
Advanced analysis of IEC binary scale indices using modular arithmetic.
Identifies patterns: "4-even-10", "7-odd-3", and "12-forced" cycles.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Mathematical Framework:
- "Four in even tens": index % 4 == 0 at even positions (i % 2 == 0)
- "Seven in odd 3s": index % 3 == 1 at odd positions (7 mod 12 = 7)
- "Forcing 12": the modulus cycle is 12 (full period)

These patterns reveal hidden structure in the binary scale progression.
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum


# ============= CONSTANTS =============

HALF_K = 32  # Geometric mean of 1B and 1024B = 2^5
FORCING_MODULUS = 12  # The complete cycle period


class SievePattern(Enum):
    """Recognized patterns in the scale sieve."""
    FOUR_EVEN_TEN = "4-even-10"      # Appears at even indices where i % 4 == 0
    SEVEN_ODD_THREE = "7-odd-3"      # Appears where i ≡ 1 (mod 3) at odd indices
    TWELVE_FORCED = "12-forced"      # Full cycle reset at multiples of 12


@dataclass
class SieveEntry:
    """Single entry in the scale sieve analysis."""
    index: int
    name: str
    exponent: int
    factor: int
    patterns: List[SievePattern]
    half_k_groups: int
    
    def pattern_tags(self) -> List[str]:
        """Get human-readable pattern tags."""
        return [p.value for p in self.patterns]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'index': self.index,
            'name': self.name,
            'exponent': self.exponent,
            'factor': self.factor,
            'patterns': self.pattern_tags(),
            'half_k_groups': self.half_k_groups,
        }


class ScaleSieve:
    """
    Analyzes IEC binary scale using modular arithmetic sieve.
    Identifies recurring patterns and structural properties.
    """
    
    def __init__(self, prefixes: List[str], exponents: List[int]):
        """
        Initialize scale sieve.
        
        Args:
            prefixes: List of prefix names (e.g., ['B', 'KiB', 'MiB', ...])
            exponents: List of exponents (e.g., [0, 10, 20, ...])
        """
        if len(prefixes) != len(exponents):
            raise ValueError("prefixes and exponents must have same length")
        
        self.prefixes = prefixes
        self.exponents = exponents
        self.scale_length = len(prefixes)
        self.sieve_entries = self._compute_sieve()
    
    def _compute_sieve(self) -> List[SieveEntry]:
        """Compute the scale sieve for all entries."""
        entries = []
        
        for i, (name, exp) in enumerate(zip(self.prefixes, self.exponents)):
            factor = 2 ** exp
            patterns = self._identify_patterns(i)
            half_k_groups = factor // HALF_K
            
            entry = SieveEntry(
                index=i,
                name=name,
                exponent=exp,
                factor=factor,
                patterns=patterns,
                half_k_groups=half_k_groups
            )
            entries.append(entry)
        
        return entries
    
    def _identify_patterns(self, index: int) -> List[SievePattern]:
        """
        Identify which patterns apply to given index.
        
        Args:
            index: Position in scale
            
        Returns:
            List of matching SievePattern enums
        """
        patterns = []
        
        # "Four in even tens": appears at even indices where i % 4 == 0
        if (index % 2 == 0) and (index % 4 == 0):
            patterns.append(SievePattern.FOUR_EVEN_TEN)
        
        # "Seven in odd 3s": appears where i ≡ 1 (mod 3) at odd indices
        if (index % 2 == 1) and (index % 3 == 1):
            patterns.append(SievePattern.SEVEN_ODD_THREE)
        
        # "Forcing 12": full cycle resets at multiples of 12
        if index % FORCING_MODULUS == 0:
            patterns.append(SievePattern.TWELVE_FORCED)
        
        return patterns
    
    def get_entries_with_pattern(self, pattern: SievePattern) -> List[SieveEntry]:
        """Get all entries matching a specific pattern."""
        return [e for e in self.sieve_entries if pattern in e.patterns]
    
    def pattern_statistics(self) -> Dict[str, Any]:
        """Compute statistics about pattern occurrences."""
        stats = {}
        
        for pattern in SievePattern:
            matching = self.get_entries_with_pattern(pattern)
            stats[pattern.value] = {
                'count': len(matching),
                'indices': [e.index for e in matching],
                'names': [e.name for e in matching],
            }
        
        return stats
    
    def modular_analysis(self) -> Dict[int, List[int]]:
        """
        Analyze distribution across different moduli.
        
        Returns:
            Dictionary mapping modulus to list of indices
        """
        analysis = {}
        
        for modulus in [2, 3, 4, 6, 12]:
            analysis[modulus] = {}
            for remainder in range(modulus):
                indices = [i for i in range(self.scale_length) if i % modulus == remainder]
                if indices:
                    analysis[modulus][remainder] = indices
        
        return analysis
    
    def print_sieve(self, max_width: int = 100) -> None:
        """Print formatted sieve table."""
        print(f"\nSCALE SIEVE (forcing modulus={FORCING_MODULUS}):")
        print("-" * max_width)
        print(f"{'Idx':>3}  {'Name':>4}  {'2^exp':>25}  {'Half-K':>14}  {'Patterns':>40}")
        print("-" * max_width)
        
        for entry in self.sieve_entries:
            tags = ', '.join(entry.pattern_tags()) if entry.patterns else '—'
            print(f"{entry.index:>3}  {entry.name:>4}  {entry.factor:>25,}  "
                  f"{entry.half_k_groups:>14,}  {tags:>40}")
    
    def print_pattern_analysis(self) -> None:
        """Print pattern occurrence analysis."""
        print(f"\nPATTERN ANALYSIS:")
        print("-" * 80)
        
        stats = self.pattern_statistics()
        for pattern_name, data in stats.items():
            print(f"\n{pattern_name}:")
            print(f"  Occurrences: {data['count']}")
            print(f"  Indices: {data['indices']}")
            print(f"  Names: {data['names']}")
    
    def print_modular_analysis(self) -> None:
        """Print modular arithmetic analysis."""
        print(f"\nMODULAR ANALYSIS:")
        print("-" * 80)
        
        analysis = self.modular_analysis()
        for modulus, remainders in sorted(analysis.items()):
            print(f"\nModulus {modulus}:")
            for remainder in sorted(remainders.keys()):
                indices = remainders[remainder]
                names = [self.prefixes[i] for i in indices]
                print(f"  {modulus} ≡ {remainder}: indices={indices}, names={names}")


# ============= DEMONSTRATION =============

def demo_scale_sieve():
    """Demonstrate scale sieve algorithm."""
    
    print("="*100)
    print("LKL-Jr SCALE SIEVE ALGORITHM")
    print("="*100)
    
    # Standard IEC prefixes
    prefixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'EiB', 'ZiB', 'YiB']
    exponents = [0, 10, 20, 30, 40, 50, 60, 70]
    
    # Create sieve
    sieve = ScaleSieve(prefixes, exponents)
    
    # Print sieve table
    print()
    sieve.print_sieve()
    
    # Print pattern analysis
    print()
    sieve.print_pattern_analysis()
    
    # Print modular analysis
    print()
    sieve.print_modular_analysis()
    
    print("\n" + "="*100)
    print("✓ SCALE SIEVE ANALYSIS COMPLETE")
    print("="*100)


__all__ = [
    'ScaleSieve',
    'SieveEntry',
    'SievePattern',
    'HALF_K',
    'FORCING_MODULUS',
]

if __name__ == '__main__':
    demo_scale_sieve()
