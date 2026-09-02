"""
LKL-Jr Scale Bites (Segments) & Pattern Analysis
================================================
Analyzes the IEC binary scale as segmented "bites" (chunks) separated by delimiters.
Studies Half-K byte patterns and scale segmentation structure.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Concept: "Bites" are segments of the scale, like how data is chunked or
delimited in protocols. The scale can be visualized as: B|KiB|MiB|GiB|TiB|EiB|ZiB|YiB
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
import binascii


# ============= CONSTANTS =============

HALF_K_BYTES = 32  # 2^5 - geometric mean of 1B and 1024B
HALF_K_BITS = HALF_K_BYTES * 8  # 256 bits
HALF_K_HEX_REPEAT = 0x20  # Space character (32 decimal)


@dataclass
class BiteSample:
    """Represents a single "bite" (segment) in the scale."""
    name: str
    bytes_value: bytes
    index: int
    
    def length(self) -> int:
        """Length of bite in bytes."""
        return len(self.bytes_value)
    
    def hex(self) -> str:
        """Hexadecimal representation."""
        return self.bytes_value.hex()
    
    def ascii(self) -> str:
        """ASCII representation if possible."""
        try:
            return self.bytes_value.decode('ascii')
        except UnicodeDecodeError:
            return "[non-ASCII]"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'index': self.index,
            'length': self.length(),
            'hex': self.hex(),
            'ascii': self.ascii(),
        }


class ScaleBites:
    """
    Analyzes IEC binary scale as segmented "bites" (chunks).
    Provides pattern analysis and Half-K relationship investigation.
    """
    
    # Standard IEC prefixes as byte segments
    SCALE_BYTES = b'B|KiB|MiB|GiB|TiB|EiB|ZiB|YiB'
    DELIMITER = b'|'
    PREFIXES = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'EiB', 'ZiB', 'YiB']
    
    def __init__(self):
        """Initialize scale bites analyzer."""
        self.raw_bytes = self.SCALE_BYTES
        self.bites = self._extract_bites()
        self.half_k_pattern = self._create_half_k_pattern()
    
    def _extract_bites(self) -> List[BiteSample]:
        """Extract individual bites from scale bytes."""
        segments = self.raw_bytes.split(self.DELIMITER)
        
        bites = []
        for i, segment in enumerate(segments):
            bite = BiteSample(
                name=segment.decode('ascii'),
                bytes_value=segment,
                index=i
            )
            bites.append(bite)
        
        return bites
    
    def _create_half_k_pattern(self) -> Dict[str, Any]:
        """Create Half-K (32-byte) pattern."""
        half_k_bytes = bytes([HALF_K_HEX_REPEAT]) * HALF_K_BYTES
        
        return {
            'bytes': half_k_bytes,
            'length': HALF_K_BYTES,
            'hex': half_k_bytes.hex(),
            'hex_length': len(half_k_bytes.hex()),
            'as_literal': f"b'\\x{HALF_K_HEX_REPEAT:02x}' * {HALF_K_BYTES}",
            'description': 'Geometric mean of 1B and 1024B as repeated byte pattern'
        }
    
    def get_bite(self, index: int) -> BiteSample:
        """Get bite by index."""
        if 0 <= index < len(self.bites):
            return self.bites[index]
        return None
    
    def get_bite_by_name(self, name: str) -> BiteSample:
        """Get bite by prefix name."""
        for bite in self.bites:
            if bite.name == name:
                return bite
        return None
    
    def bite_statistics(self) -> Dict[str, Any]:
        """Compute statistics about bites."""
        lengths = [bite.length() for bite in self.bites]
        
        return {
            'total_bites': len(self.bites),
            'total_bytes': sum(lengths),
            'total_with_delimiters': len(self.raw_bytes),
            'min_bite_length': min(lengths),
            'max_bite_length': max(lengths),
            'avg_bite_length': sum(lengths) / len(lengths),
            'bite_lengths': lengths,
        }
    
    def half_k_relationships(self) -> Dict[str, Any]:
        """
        Analyze relationships between bites and Half-K.
        """
        relationships = {}
        
        for bite in self.bites:
            byte_len = bite.length()
            half_k_groups = byte_len / HALF_K_BYTES if byte_len > 0 else 0
            
            relationships[bite.name] = {
                'bytes': byte_len,
                'half_k_groups': half_k_groups,
                'is_multiple_of_half_k': (byte_len % HALF_K_BYTES == 0) if byte_len > 0 else False,
            }
        
        return relationships
    
    def print_bites(self) -> None:
        """Print formatted bites table."""
        print(f"\nSCALE BITES (segments):")
        print("-" * 80)
        print(f"{'Idx':>3}  {'Name':>6}  {'Length':>8}  {'Hex':>30}  {'ASCII':>10}")
        print("-" * 80)
        
        for bite in self.bites:
            hex_str = bite.hex()[:30] + '...' if len(bite.hex()) > 30 else bite.hex()
            print(f"{bite.index:>3}  {bite.name:>6}  {bite.length():>8}  {hex_str:>30}  {bite.ascii():>10}")
        
        stats = self.bite_statistics()
        print("-" * 80)
        print(f"Total segments: {stats['total_bites']} | "
              f"Total bytes (with delimiters): {stats['total_with_delimiters']} | "
              f"Total bite content: {stats['total_bytes']}")
    
    def print_half_k_pattern(self) -> None:
        """Print Half-K pattern information."""
        print(f"\nHALF-K PATTERN (32-byte):")
        print("-" * 80)
        
        pattern = self.half_k_pattern
        print(f"Description:     {pattern['description']}")
        print(f"Byte value:      0x{HALF_K_HEX_REPEAT:02x} (space character)")
        print(f"Length:          {pattern['length']} bytes")
        print(f"Hex (first 32):  {pattern['hex'][:32]}...")
        print(f"Total hex chars: {pattern['hex_length']}")
        print(f"Literal form:    {pattern['as_literal']}")
    
    def print_half_k_relationships(self) -> None:
        """Print Half-K relationships with bites."""
        print(f"\nHALF-K RELATIONSHIPS:")
        print("-" * 80)
        
        rels = self.half_k_relationships()
        for name, data in rels.items():
            is_multiple = "✓" if data['is_multiple_of_half_k'] else "✗"
            print(f"{name:>6}: {data['bytes']:>3} bytes | "
                  f"Half-K groups: {data['half_k_groups']:>6.2f} | "
                  f"Multiple of Half-K: {is_multiple}")


# ============= DEMONSTRATION =============

def demo_scale_bites():
    """Demonstrate scale bites analysis."""
    
    print("="*100)
    print("LKL-Jr SCALE BITES & PATTERN ANALYSIS")
    print("="*100)
    
    bites = ScaleBites()
    
    # Print bites
    print()
    bites.print_bites()
    
    # Print Half-K pattern
    print()
    bites.print_half_k_pattern()
    
    # Print Half-K relationships
    print()
    bites.print_half_k_relationships()
    
    print("\n" + "="*100)
    print("✓ SCALE BITES ANALYSIS COMPLETE")
    print("="*100)


__all__ = [
    'ScaleBites',
    'BiteSample',
    'HALF_K_BYTES',
    'HALF_K_BITS',
]

if __name__ == '__main__':
    demo_scale_bites()
