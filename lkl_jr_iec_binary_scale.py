"""
LKL-Jr IEC Binary Scale & Half-K Utilities
===========================================
International Electrotechnical Commission (IEC) binary prefixes.
Utilities for working with binary data sizes and the geometric mean (half-K = 32 bytes).

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

IEC Binary Prefixes:
- B:    Bytes        (2^0)
- KiB:  Kibibytes    (2^10)    - 1024 bytes
- MiB:  Mebibytes    (2^20)    - 1,048,576 bytes
- GiB:  Gibibytes    (2^30)    - 1,073,741,824 bytes
- TiB:  Tebibytes    (2^40)    - 1,099,511,627,776 bytes
- EiB:  Exbibytes    (2^50)
- ZiB:  Zebibytes    (2^60)
- YiB:  Yobibytes    (2^70)

Special: Half-K (32 bytes) is the geometric mean of 1 B and 1024 B
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# ============= IEC BINARY SCALE =============

class IECBinaryPrefix(Enum):
    """IEC binary prefix definitions."""
    B = (0, 1, 'Byte', 'B')
    KiB = (10, 1024, 'Kibibyte', 'KiB')
    MiB = (20, 1048576, 'Mebibyte', 'MiB')
    GiB = (30, 1073741824, 'Gibibyte', 'GiB')
    TiB = (40, 1099511627776, 'Tebibyte', 'TiB')
    EiB = (50, 1125899906842624, 'Exbibyte', 'EiB')
    ZiB = (60, 1152921504606846976, 'Zebibyte', 'ZiB')
    YiB = (70, 1208925819614629174706176, 'Yobibyte', 'YiB')
    
    def __init__(self, exponent: int, factor: int, fullname: str, symbol: str):
        self.exponent = exponent
        self.factor = factor
        self.fullname = fullname
        self.symbol = symbol
    
    @classmethod
    def by_symbol(cls, symbol: str) -> Optional['IECBinaryPrefix']:
        """Get prefix by symbol (e.g., 'KiB', 'GiB')."""
        for prefix in cls:
            if prefix.symbol == symbol:
                return prefix
        return None
    
    @classmethod
    def by_exponent(cls, exponent: int) -> Optional['IECBinaryPrefix']:
        """Get prefix by exponent (e.g., 10, 20, 30)."""
        for prefix in cls:
            if prefix.exponent == exponent:
                return prefix
        return None


@dataclass
class BinarySize:
    """Represents a data size in IEC binary units."""
    bytes_value: int
    
    def to_kib(self) -> float:
        """Convert to Kibibytes."""
        return self.bytes_value / 1024
    
    def to_mib(self) -> float:
        """Convert to Mebibytes."""
        return self.bytes_value / (1024 ** 2)
    
    def to_gib(self) -> float:
        """Convert to Gibibytes."""
        return self.bytes_value / (1024 ** 3)
    
    def to_tib(self) -> float:
        """Convert to Tebibytes."""
        return self.bytes_value / (1024 ** 4)
    
    def to_eib(self) -> float:
        """Convert to Exbibytes."""
        return self.bytes_value / (1024 ** 5)
    
    def to_prefix(self, prefix: IECBinaryPrefix) -> float:
        """Convert to specified prefix."""
        return self.bytes_value / prefix.factor
    
    def auto_format(self) -> Tuple[float, str]:
        """
        Automatically select appropriate prefix and format size.
        
        Returns:
            (value, prefix_symbol) tuple
        """
        if self.bytes_value < 1024:
            return float(self.bytes_value), 'B'
        elif self.bytes_value < 1024 ** 2:
            return self.to_kib(), 'KiB'
        elif self.bytes_value < 1024 ** 3:
            return self.to_mib(), 'MiB'
        elif self.bytes_value < 1024 ** 4:
            return self.to_gib(), 'GiB'
        elif self.bytes_value < 1024 ** 5:
            return self.to_tib(), 'TiB'
        else:
            return self.to_eib(), 'EiB'
    
    def __str__(self) -> str:
        value, prefix = self.auto_format()
        return f"{value:.2f} {prefix}"
    
    def __repr__(self) -> str:
        return f"BinarySize({self.bytes_value} bytes)"


# ============= HALF-K SPECIAL VALUE =============

class HalfK:
    """
    Half-K: The geometric mean of 1 Byte and 1 Kibibyte.
    
    Mathematical properties:
    - Geometric mean: √(1 × 1024) = 32
    - Value: 2^5 = 32 bytes
    - In binary: 00100000
    - In hex: 0x20
    
    This is a mathematically significant threshold often used for
    buffer sizes, cache lines, and data alignment.
    """
    
    BYTES = 2 ** 5  # 32 bytes
    BITS = BYTES * 8  # 256 bits
    GEOMETRIC_MEAN = math.sqrt(1 * 1024)  # 32.0
    
    @staticmethod
    def verify_geometric_mean() -> bool:
        """Verify that 32 is the geometric mean of 1 and 1024."""
        return abs(HalfK.GEOMETRIC_MEAN - HalfK.BYTES) < 0.001
    
    @staticmethod
    def to_bytes() -> bytes:
        """Create a Half-K (32-byte) byte array."""
        return b'\x00' * HalfK.BYTES
    
    @staticmethod
    def to_hex_string() -> str:
        """Get hex representation of Half-K bytes."""
        return HalfK.to_bytes().hex()
    
    @staticmethod
    def get_info() -> Dict[str, any]:
        """Get comprehensive Half-K information."""
        return {
            'name': 'Half-K',
            'bytes': HalfK.BYTES,
            'bits': HalfK.BITS,
            'geometric_mean': HalfK.GEOMETRIC_MEAN,
            'exponent': 5,
            'hex_representation': '0x20',
            'binary_representation': bin(HalfK.BYTES)[2:].zfill(8),
            'description': 'Geometric mean of 1 B and 1 KiB'
        }


# ============= SCALE CALCULATOR =============

class BinaryScaleCalculator:
    """
    Calculator for IEC binary scale conversions.
    """
    
    @staticmethod
    def get_scale_ladder() -> List[Tuple[str, int, int]]:
        """
        Get complete IEC binary scale ladder.
        
        Returns:
            List of (prefix, exponent, factor) tuples
        """
        scale = []
        for prefix in IECBinaryPrefix:
            scale.append((prefix.symbol, prefix.exponent, prefix.factor))
        return scale
    
    @staticmethod
    def bytes_to_all_units(bytes_value: int) -> Dict[str, float]:
        """
        Convert bytes to all IEC binary units.
        
        Args:
            bytes_value: Number of bytes
            
        Returns:
            Dictionary mapping unit symbols to converted values
        """
        result = {}
        for prefix in IECBinaryPrefix:
            result[prefix.symbol] = bytes_value / prefix.factor
        return result
    
    @staticmethod
    def from_unit(value: float, unit: str) -> Optional[int]:
        """
        Convert from specified unit to bytes.
        
        Args:
            value: Numeric value
            unit: Unit symbol (e.g., 'GiB')
            
        Returns:
            Number of bytes or None if unit unknown
        """
        prefix = IECBinaryPrefix.by_symbol(unit)
        if prefix is None:
            return None
        return int(value * prefix.factor)


# ============= DEMONSTRATION =============

def demo_iec_binary_scale():
    """Demonstrate IEC binary scale and Half-K utilities."""
    
    print("="*100)
    print("LKL-Jr IEC BINARY SCALE & HALF-K UTILITIES")
    print("="*100)
    print()
    
    # Test 1: IEC Binary Scale
    print("[1] IEC BINARY SCALE LADDER")
    print("-"*100)
    print(f"{'Prefix':<10} {'Exponent':<12} {'Factor':<30} {'Full Name':<20}")
    print("-"*100)
    for prefix in IECBinaryPrefix:
        print(f"{prefix.symbol:<10} 2^{prefix.exponent:<10} {prefix.factor:>29,} {prefix.fullname:<20}")
    print()
    
    # Test 2: Half-K Properties
    print("[2] HALF-K (GEOMETRIC MEAN) PROPERTIES")
    print("-"*100)
    half_k_info = HalfK.get_info()
    for key, value in half_k_info.items():
        print(f"  {key:<25} {value}")
    print()
    print(f"  Geometric mean verification: {HalfK.verify_geometric_mean()}")
    print(f"  √(1 × 1024) = {HalfK.GEOMETRIC_MEAN:.1f}")
    print(f"  2^5 = {HalfK.BYTES}")
    print()
    
    # Test 3: Half-K Byte Array
    print("[3] HALF-K BYTE REPRESENTATIONS")
    print("-"*100)
    half_k_bytes = HalfK.to_bytes()
    print(f"  Hex (first 16 chars): {HalfK.to_hex_string()[:16]}...")
    print(f"  Byte array length: {len(half_k_bytes)} bytes")
    print(f"  Hex string length: {len(HalfK.to_hex_string())} characters")
    print()
    
    # Test 4: Binary Size Conversions
    print("[4] BINARY SIZE CONVERSIONS")
    print("-"*100)
    test_sizes = [512, 1024, 1048576, 1073741824]
    for size_bytes in test_sizes:
        bs = BinarySize(size_bytes)
        value, unit = bs.auto_format()
        print(f"  {size_bytes:>15,} bytes = {value:>10.2f} {unit}")
    print()
    
    # Test 5: Scale Calculator
    print("[5] SCALE CALCULATOR - 1 GiB IN ALL UNITS")
    print("-"*100)
    gib_in_bytes = BinaryScaleCalculator.from_unit(1.0, 'GiB')
    conversions = BinaryScaleCalculator.bytes_to_all_units(gib_in_bytes)
    
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'EiB']:
        value = conversions.get(unit, 0)
        print(f"  1 GiB = {value:>20,.2f} {unit}")
    print()
    
    print("="*100)
    print("✓ IEC BINARY SCALE & HALF-K UTILITIES OPERATIONAL")
    print("="*100)


__all__ = [
    'IECBinaryPrefix',
    'BinarySize',
    'HalfK',
    'BinaryScaleCalculator',
]

if __name__ == '__main__':
    demo_iec_binary_scale()
