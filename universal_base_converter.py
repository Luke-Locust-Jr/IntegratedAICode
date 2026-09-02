"""
Universal Base Conversion Framework
====================================
Extensible base conversion system supporting arbitrary radixes with custom alphabets.
Integrates with LKL-Jr identity framework for number representation across bases.

Identity: LKL-Jr @ locust@therootedpi.polly
Date: 02 Sep 2026
"""

from decimal import Decimal, getcontext, localcontext
from typing import Tuple, Dict, List, Any, Optional, Callable
import math


class BaseConverter:
    """
    Universal base converter supporting arbitrary radixes (2-64+).
    Handles custom alphabets for flexible encoding/decoding.
    """
    
    # Standard alphabets for common bases
    ALPHABETS = {
        'binary': '01',
        'octal': '01234567',
        'decimal': '0123456789',
        'hex': '0123456789ABCDEF',
        'base32': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
        'base64': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
        'safe_base52': 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz',
        'base62': '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
    }
    
    def __init__(self, alphabet: str = None, base: int = None):
        """
        Initialize converter with optional alphabet and base.
        
        Args:
            alphabet: Custom alphabet string. If provided, base is derived from length.
            base: Target base (2-64). If alphabet not provided, uses standard for this base.
        """
        if alphabet and base:
            if len(alphabet) != base:
                raise ValueError(f"Alphabet length ({len(alphabet)}) must match base ({base})")
            self.alphabet = alphabet
            self.base = base
        elif alphabet:
            self.base = len(alphabet)
            self.alphabet = alphabet
        elif base:
            if base < 2 or base > 64:
                raise ValueError(f"Base must be 2-64, got {base}")
            self.base = base
            self.alphabet = self._get_default_alphabet(base)
        else:
            raise ValueError("Must provide either alphabet or base")
    
    @staticmethod
    def _get_default_alphabet(base: int) -> str:
        """Get default alphabet for standard bases."""
        if base == 2:
            return BaseConverter.ALPHABETS['binary']
        elif base == 8:
            return BaseConverter.ALPHABETS['octal']
        elif base == 10:
            return BaseConverter.ALPHABETS['decimal']
        elif base == 16:
            return BaseConverter.ALPHABETS['hex']
        elif base == 32:
            return BaseConverter.ALPHABETS['base32']
        elif base == 64:
            return BaseConverter.ALPHABETS['base64']
        else:
            # Generic: use base62 subset or create dynamically
            base62 = BaseConverter.ALPHABETS['base62']
            return base62[:base]
    
    def to_base(self, n: int) -> str:
        """
        Convert integer to base representation.
        
        Args:
            n: Non-negative integer
            
        Returns:
            String representation in target base using custom alphabet
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected int, got {type(n).__name__}")
        if n < 0:
            raise ValueError("Negative integers not supported")
        if n == 0:
            return self.alphabet[0]
        
        result = []
        while n > 0:
            n, digit_index = divmod(n, self.base)
            result.append(self.alphabet[digit_index])
        
        return ''.join(reversed(result))
    
    def from_base(self, s: str) -> int:
        """
        Convert base representation back to integer.
        
        Args:
            s: String in target base using custom alphabet
            
        Returns:
            Decoded integer value
        """
        if not isinstance(s, str):
            raise TypeError(f"Expected str, got {type(s).__name__}")
        
        n = 0
        for ch in s:
            if ch not in self.alphabet:
                raise ValueError(f"Character '{ch}' not in alphabet")
            digit = self.alphabet.index(ch)
            n = n * self.base + digit
        
        return n
    
    def round_trip_test(self, n: int) -> Tuple[bool, str]:
        """
        Verify encode-decode round trip.
        
        Args:
            n: Integer to test
            
        Returns:
            (success: bool, encoded: str)
        """
        encoded = self.to_base(n)
        decoded = self.from_base(encoded)
        success = decoded == n
        return success, encoded
    
    def __repr__(self) -> str:
        return f"BaseConverter(base={self.base}, alphabet_len={len(self.alphabet)})"


class StandardBaseConverters:
    """Convenient wrappers for common base conversions."""
    
    # Instances for standard bases
    _converters = {
        'binary': BaseConverter(base=2),
        'octal': BaseConverter(base=8),
        'decimal': BaseConverter(base=10),
        'hex': BaseConverter(base=16),
        'base32': BaseConverter(base=32),
        'base64': BaseConverter(base=64),
        'base62': BaseConverter(base=62),
        'safe_base52': BaseConverter(alphabet=BaseConverter.ALPHABETS['safe_base52']),
    }
    
    @staticmethod
    def to_binary(n: int) -> str:
        """Convert integer to binary (base 2)."""
        return StandardBaseConverters._converters['binary'].to_base(n)
    
    @staticmethod
    def to_octal(n: int) -> str:
        """Convert integer to octal (base 8)."""
        return StandardBaseConverters._converters['octal'].to_base(n)
    
    @staticmethod
    def to_decimal(n: int) -> str:
        """Convert integer to decimal (base 10)."""
        return StandardBaseConverters._converters['decimal'].to_base(n)
    
    @staticmethod
    def to_hex(n: int) -> str:
        """Convert integer to hexadecimal (base 16)."""
        return StandardBaseConverters._converters['hex'].to_base(n)
    
    @staticmethod
    def to_base32(n: int) -> str:
        """Convert integer to base32."""
        return StandardBaseConverters._converters['base32'].to_base(n)
    
    @staticmethod
    def to_base64(n: int) -> str:
        """Convert integer to base64."""
        return StandardBaseConverters._converters['base64'].to_base(n)
    
    @staticmethod
    def to_base62(n: int) -> str:
        """Convert integer to base62 (alphanumeric)."""
        return StandardBaseConverters._converters['base62'].to_base(n)
    
    @staticmethod
    def to_safe_base52(n: int) -> str:
        """Convert integer to safe base52 (no confusing characters 0/O/1/I/l)."""
        return StandardBaseConverters._converters['safe_base52'].to_base(n)
    
    @staticmethod
    def from_binary(s: str) -> int:
        """Convert binary string to integer."""
        return StandardBaseConverters._converters['binary'].from_base(s)
    
    @staticmethod
    def from_octal(s: str) -> int:
        """Convert octal string to integer."""
        return StandardBaseConverters._converters['octal'].from_base(s)
    
    @staticmethod
    def from_decimal(s: str) -> int:
        """Convert decimal string to integer."""
        return StandardBaseConverters._converters['decimal'].from_base(s)
    
    @staticmethod
    def from_hex(s: str) -> int:
        """Convert hexadecimal string to integer."""
        return StandardBaseConverters._converters['hex'].from_base(s)
    
    @staticmethod
    def from_base32(s: str) -> int:
        """Convert base32 string to integer."""
        return StandardBaseConverters._converters['base32'].from_base(s)
    
    @staticmethod
    def from_base64(s: str) -> int:
        """Convert base64 string to integer."""
        return StandardBaseConverters._converters['base64'].from_base(s)
    
    @staticmethod
    def from_base62(s: str) -> int:
        """Convert base62 string to integer."""
        return StandardBaseConverters._converters['base62'].from_base(s)
    
    @staticmethod
    def from_safe_base52(s: str) -> int:
        """Convert safe base52 string to integer."""
        return StandardBaseConverters._converters['safe_base52'].from_base(s)


class PiCalculator:
    """Compute π to arbitrary precision using multiple algorithms."""
    
    @staticmethod
    def compute_pi_machin(prec: int = 50) -> Decimal:
        """
        Compute π using Machin's formula.
        π/4 = 4*arctan(1/5) - arctan(1/239)
        Fast convergence, suitable for high precision.
        
        Args:
            prec: Number of decimal places
            
        Returns:
            π as Decimal with specified precision
        """
        with localcontext() as ctx:
            ctx.prec = prec + 10  # Extra precision for intermediate calculations
            
            one = Decimal(1)
            
            def arctan(x: Decimal, num_terms: int = None) -> Decimal:
                """Compute arctan(x) using Taylor series."""
                if num_terms is None:
                    num_terms = prec + 20
                
                x_squared = x * x
                x_power = x
                result = x
                
                for n in range(1, num_terms):
                    x_power *= -x_squared
                    term = x_power / (2 * n + 1)
                    if abs(term) < Decimal(10) ** (-(prec + 5)):
                        break
                    result += term
                
                return result
            
            pi = 4 * (4 * arctan(one / 5) - arctan(one / 239))
            
            # Round to requested precision
            ctx.prec = prec
            return +pi  # Unary + forces rounding to context precision
    
    @staticmethod
    def compute_pi_chudnovsky(prec: int = 50) -> Decimal:
        """
        Compute π using Chudnovsky algorithm.
        Extremely fast convergence (≈14 digits per term).
        Better for very high precision.
        
        Args:
            prec: Number of decimal places
            
        Returns:
            π as Decimal with specified precision
        """
        with localcontext() as ctx:
            ctx.prec = prec + 20
            
            C = 426880 * Decimal(10005).sqrt()
            K = Decimal(6)
            M = Decimal(1)
            X = Decimal(1)
            L = Decimal(13591409)
            S = Decimal(13591409)
            
            for i in range(1, prec):
                M = M * (K**3 - 16*K) / ((i)**3)
                K += 12
                L += 545140134
                X *= -262537412640768000
                S += Decimal(M * L) / X
                
                if abs(Decimal(M * L) / X) < Decimal(10) ** (-(prec + 5)):
                    break
            
            pi = C / S
            
            ctx.prec = prec
            return +pi
    
    @staticmethod
    def compute_pi_bailey(prec: int = 50) -> Decimal:
        """
        Compute π using Bailey–Borwein–Plouffe formula.
        Allows computation of hexadecimal digits without computing earlier digits.
        
        Args:
            prec: Number of decimal places
            
        Returns:
            π as Decimal with specified precision
        """
        with localcontext() as ctx:
            ctx.prec = prec + 20
            
            pi = Decimal(0)
            for k in range(prec):
                term = (
                    Decimal(1) / (16**k) * (
                        Decimal(4) / (8*k + 1) -
                        Decimal(2) / (8*k + 4) -
                        Decimal(1) / (8*k + 5) -
                        Decimal(1) / (8*k + 6)
                    )
                )
                pi += term
                
                if abs(term) < Decimal(10) ** (-(prec + 5)):
                    break
            
            ctx.prec = prec
            return +pi


class PiBaseRepresentation:
    """Convert π to various base representations."""
    
    @staticmethod
    def pi_in_base(base: int, prec: int = 50, algorithm: str = 'machin') -> Dict[str, Any]:
        """
        Compute π and represent it in specified base.
        
        Args:
            base: Target base (2-64)
            prec: Decimal precision for π computation
            algorithm: 'machin', 'chudnovsky', or 'bailey'
            
        Returns:
            Dictionary with π value and base representations
        """
        # Compute π
        if algorithm == 'machin':
            pi_decimal = PiCalculator.compute_pi_machin(prec)
        elif algorithm == 'chudnovsky':
            pi_decimal = PiCalculator.compute_pi_chudnovsky(prec)
        elif algorithm == 'bailey':
            pi_decimal = PiCalculator.compute_pi_bailey(prec)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Convert integer part (3 for π)
        pi_int_part = int(pi_decimal)
        
        # Convert fractional part as scaled integer
        pi_scaled = int(pi_decimal * Decimal(10) ** (prec - 1))
        
        # Get base representation
        converter = BaseConverter(base=base)
        int_representation = converter.to_base(pi_int_part)
        scaled_representation = converter.to_base(pi_scaled)
        
        return {
            'pi_decimal': str(pi_decimal),
            'pi_int_part': pi_int_part,
            'base': base,
            'integer_repr': int_representation,
            'scaled_repr': scaled_representation,
            'algorithm': algorithm,
            'precision': prec
        }


class UniversalRoundTripTester:
    """Test round-trip conversions across all standard bases."""
    
    @staticmethod
    def test_all_bases(number: int) -> Dict[str, Any]:
        """
        Round-trip test across all standard bases.
        
        Args:
            number: Integer to test
            
        Returns:
            Dictionary with results for each base
        """
        converters = {
            'Binary': StandardBaseConverters.to_binary,
            'Octal': StandardBaseConverters.to_octal,
            'Decimal': StandardBaseConverters.to_decimal,
            'Hex': StandardBaseConverters.to_hex,
            'Base32': StandardBaseConverters.to_base32,
            'Base64': StandardBaseConverters.to_base64,
            'Base62': StandardBaseConverters.to_base62,
            'Safe Base52': StandardBaseConverters.to_safe_base52,
        }
        
        decoders = {
            'Binary': StandardBaseConverters.from_binary,
            'Octal': StandardBaseConverters.from_octal,
            'Decimal': StandardBaseConverters.from_decimal,
            'Hex': StandardBaseConverters.from_hex,
            'Base32': StandardBaseConverters.from_base32,
            'Base64': StandardBaseConverters.from_base64,
            'Base62': StandardBaseConverters.from_base62,
            'Safe Base52': StandardBaseConverters.from_safe_base52,
        }
        
        results = {'original': number, 'tests': {}}
        
        for name, encoder in converters.items():
            encoded = encoder(number)
            decoded = decoders[name](encoded)
            success = decoded == number
            
            results['tests'][name] = {
                'encoded': encoded,
                'decoded': decoded,
                'success': success,
                'length': len(encoded)
            }
        
        return results
    
    @staticmethod
    def print_results(results: Dict[str, Any]) -> None:
        """Pretty-print round-trip test results."""
        print(f"\nOriginal: {results['original']}")
        print("=" * 100)
        print(f"{'Base':<15} {'Encoded':<35} {'Decoded':<20} {'Status':<8} {'Length':<8}")
        print("-" * 100)
        
        for name, data in results['tests'].items():
            status = "✓" if data['success'] else "✗ FAIL"
            print(f"{name:<15} {data['encoded']:<35} {data['decoded']:<20} {status:<8} {data['length']:<8}")
        
        all_pass = all(data['success'] for data in results['tests'].values())
        print("=" * 100)
        print(f"Overall: {'✓ ALL TESTS PASSED' if all_pass else '✗ SOME TESTS FAILED'}")


class PSIDEncoder:
    """Encode/decode PSID (Personal Security Identifier) using safe base52."""
    
    def __init__(self):
        self.converter = StandardBaseConverters._converters['safe_base52']
    
    def encode_psid(self, psid_string: str) -> str:
        """
        Encode PSID from decimal string to safe base52.
        
        Args:
            psid_string: PSID as decimal string (e.g., "06761207479583521855784950595087")
            
        Returns:
            Safe base52 encoded string
        """
        psid_int = int(psid_string)
        return self.converter.to_base(psid_int)
    
    def decode_psid(self, encoded: str) -> str:
        """
        Decode PSID from safe base52 back to decimal string.
        
        Args:
            encoded: Safe base52 encoded string
            
        Returns:
            PSID as decimal string
        """
        psid_int = self.converter.from_base(encoded)
        return str(psid_int)
    
    def round_trip_psid(self, psid_string: str) -> Tuple[str, bool]:
        """
        Verify PSID round-trip conversion.
        
        Args:
            psid_string: Original PSID decimal string
            
        Returns:
            (encoded: str, success: bool)
        """
        encoded = self.encode_psid(psid_string)
        decoded = self.decode_psid(encoded)
        success = decoded == psid_string
        return encoded, success


# ============= DEMONSTRATION =============

def demo_base_conversions():
    """Demonstrate universal base conversion framework."""
    
    print("=" * 100)
    print("UNIVERSAL BASE CONVERSION FRAMEWORK")
    print("=" * 100)
    
    # Test number from earlier context
    test_number = 168576171
    
    print("\n[1] ROUND-TRIP TESTING ACROSS ALL STANDARD BASES")
    print("-" * 100)
    results = UniversalRoundTripTester.test_all_bases(test_number)
    UniversalRoundTripTester.print_results(results)
    
    # Pi computations
    print("\n[2] PI COMPUTATIONS - MACHIN ALGORITHM")
    print("-" * 100)
    getcontext().prec = 50
    pi_value = PiCalculator.compute_pi_machin(50)
    print(f"π (50 digits): {pi_value}")
    
    print("\n[3] PI IN DIFFERENT BASES")
    print("-" * 100)
    for base in [2, 8, 16, 32, 64]:
        pi_repr = PiBaseRepresentation.pi_in_base(base, 40, 'machin')
        print(f"Base {base:<2}: {pi_repr['integer_repr']:<30} (integer part: {pi_repr['pi_int_part']})")
    
    print("\n[4] PSID ENCODING - SAFE BASE52")
    print("-" * 100)
    psid_encoder = PSIDEncoder()
    psid = "06761207479583521855784950595087"
    encoded = psid_encoder.encode_psid(psid)
    decoded, success = psid_encoder.round_trip_psid(psid)
    
    print(f"Original PSID:   {psid}")
    print(f"Encoded (SB52):  {encoded}")
    print(f"Round-trip OK:   {success}")
    
    print("\n[5] CUSTOM BASE CONVERTER - BASE 36 (ALPHANUMERIC)")
    print("-" * 100)
    converter_b36 = BaseConverter(base=36)
    test_val = 123456789
    encoded_b36 = converter_b36.to_base(test_val)
    decoded_b36 = converter_b36.from_base(encoded_b36)
    print(f"Value:     {test_val}")
    print(f"Base36:    {encoded_b36}")
    print(f"Decoded:   {decoded_b36}")
    print(f"Success:   {decoded_b36 == test_val}")
    
    print("\n" + "=" * 100)
    print("✓ UNIVERSAL BASE CONVERSION FRAMEWORK OPERATIONAL")
    print("=" * 100)


if __name__ == '__main__':
    demo_base_conversions()
