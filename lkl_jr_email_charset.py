"""
LKL-Jr Email Encoding & Charset Management Module
================================================
Advanced email header encoding with support for multiple character sets and encoding schemes.
Integrated with Luke Kerry Locust Jr.'s identity framework.

Copyright (C) 2001 Python Software Foundation
Author: Ben Gertzfield, Barry Warsaw
Modified for: Luke Kerry Locust Jr. Identity Framework
Contact: email-sig@python.org
Forwarding: locustjr@proton.me

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Encoding Standards:
- QP (Quoted-Printable): Human-readable, ~3:1 expansion
- BASE64: Binary-safe, ~4:3 expansion  
- SHORTEST: Automatic selection based on content efficiency
"""

from functools import partial
from typing import Dict, List, Tuple, Optional, Any, Callable
from enum import Enum
import email.base64mime
import email.quoprimime
from email import errors
from email.encoders import encode_7or8bit
import base64
import quopri
import re
from dataclasses import dataclass


# ============= ENCODING TYPES =============

class EncodingType(Enum):
    """Email header encoding types."""
    QP = 1          # Quoted-Printable (human-readable)
    BASE64 = 2      # Base64 (binary-safe)
    SHORTEST = 3    # Auto-select shortest encoding


# ============= CONSTANTS =============

class EncodingConstants:
    """Constants for email encoding operations."""
    
    # RFC 2047 encoded-word format prefix/suffix
    ENCODED_WORD_START = "=?"
    ENCODED_WORD_END = "?="
    
    # Header overhead: "=?charset?q?" = 11 chars, "?=" = 2 chars
    # Total: 13 chars minimum overhead per encoded-word
    HEADER_OVERHEAD = 13
    
    # Character set marker positions in encoded word
    # Format: =?charset?encoding?content?=
    #         0       1        2        3  
    
    # Common character sets
    CHARSETS = {
        'utf-8': 'UTF-8',
        'utf8': 'UTF-8',
        'ascii': 'ASCII',
        'iso-8859-1': 'ISO-8859-1',
        'latin1': 'ISO-8859-1',
        'iso-8859-2': 'ISO-8859-2',
        'cp1252': 'CP1252',
        'gb2312': 'GB2312',
        'big5': 'BIG5',
    }


# ============= CHARSET CLASS =============

@dataclass
class Charset:
    """
    Represents a character set for email encoding.
    
    Properties:
    - charset: Character set name (e.g., 'utf-8')
    - input_codec: Codec for decoding from charset
    - output_codec: Codec for encoding to charset
    - header_encoding: QP, BASE64, or SHORTEST
    - body_encoding: 7bit, 8bit, quoted-printable, base64
    - convert: Whether to convert between input/output codecs
    """
    
    charset: str
    input_codec: Optional[str] = None
    output_codec: Optional[str] = None
    header_encoding: EncodingType = EncodingType.QP
    body_encoding: str = '7bit'
    convert: bool = False
    
    def __post_init__(self):
        """Normalize and validate charset."""
        self.charset = self.charset.lower()
        
        if self.input_codec is None:
            self.input_codec = self.charset
        
        if self.output_codec is None:
            self.output_codec = self.charset
    
    def get_header_encoding(self) -> str:
        """Get email header encoding type as string."""
        if self.header_encoding == EncodingType.QP:
            return 'q'
        elif self.header_encoding == EncodingType.BASE64:
            return 'b'
        elif self.header_encoding == EncodingType.SHORTEST:
            return 'shortest'
        else:
            return 'q'
    
    def encode_header(self, header_text: str) -> str:
        """
        Encode header string using RFC 2047 format.
        
        Args:
            header_text: Text to encode
            
        Returns:
            Encoded header string (=?charset?encoding?content?=)
        """
        if self._is_ascii_safe(header_text):
            return header_text
        
        if self.header_encoding == EncodingType.BASE64:
            return self._encode_header_base64(header_text)
        elif self.header_encoding == EncodingType.QP:
            return self._encode_header_qp(header_text)
        else:  # SHORTEST
            qp_encoded = self._encode_header_qp(header_text)
            b64_encoded = self._encode_header_base64(header_text)
            return qp_encoded if len(qp_encoded) <= len(b64_encoded) else b64_encoded
    
    def decode_header(self, encoded_text: str) -> str:
        """
        Decode RFC 2047 encoded header.
        
        Args:
            encoded_text: Encoded header string
            
        Returns:
            Decoded header text
        """
        # Pattern: =?charset?encoding?encoded-text?=
        pattern = r'=\?(.+?)\?(.)\?(.+?)\?='
        match = re.match(pattern, encoded_text)
        
        if not match:
            return encoded_text
        
        charset, encoding, content = match.groups()
        
        try:
            if encoding.lower() == 'b':
                decoded_bytes = base64.b64decode(content)
            elif encoding.lower() == 'q':
                decoded_bytes = quopri.decodestring(content.replace('_', ' ').encode('ascii'))
            else:
                return encoded_text
            
            return decoded_bytes.decode(charset, errors='replace')
        
        except (ValueError, LookupError):
            return encoded_text
    
    def _is_ascii_safe(self, text: str) -> bool:
        """Check if text is safe ASCII (no encoding needed)."""
        try:
            text.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False
    
    def _encode_header_qp(self, header_text: str) -> str:
        """Encode header using Quoted-Printable."""
        encoded_bytes = header_text.encode(self.output_codec)
        qp_encoded = quopri.encodestring(encoded_bytes).decode('ascii')
        # Replace spaces with underscores in quoted-printable headers
        qp_encoded = qp_encoded.replace(' ', '_')
        return f"=?{self.charset}?q?{qp_encoded}?="
    
    def _encode_header_base64(self, header_text: str) -> str:
        """Encode header using Base64."""
        encoded_bytes = header_text.encode(self.output_codec)
        b64_encoded = base64.b64encode(encoded_bytes).decode('ascii')
        return f"=?{self.charset}?b?{b64_encoded}?="
    
    def encode_body(self, body_text: str) -> Tuple[str, str]:
        """
        Encode email body according to body_encoding type.
        
        Args:
            body_text: Email body text
            
        Returns:
            (encoded_body, encoding_used)
        """
        body_bytes = body_text.encode(self.output_codec)
        
        if self.body_encoding == 'base64':
            encoded = base64.b64encode(body_bytes).decode('ascii')
            return encoded, 'base64'
        elif self.body_encoding == 'quoted-printable':
            encoded = quopri.encodestring(body_bytes).decode('ascii')
            return encoded, 'quoted-printable'
        else:  # 7bit, 8bit
            return body_text, self.body_encoding
    
    def decode_body(self, encoded_text: str, encoding: str) -> str:
        """
        Decode email body.
        
        Args:
            encoded_text: Encoded body text
            encoding: Encoding type used
            
        Returns:
            Decoded body text
        """
        if encoding == 'base64':
            decoded_bytes = base64.b64decode(encoded_text)
        elif encoding == 'quoted-printable':
            decoded_bytes = quopri.decodestring(encoded_text.encode('ascii'))
        else:
            return encoded_text
        
        return decoded_bytes.decode(self.input_codec, errors='replace')
    
    def __repr__(self) -> str:
        return (f"Charset(charset={self.charset!r}, "
                f"header_encoding={self.header_encoding.name}, "
                f"body_encoding={self.body_encoding!r})")


# ============= CHARSET REGISTRY =============

class CharsetRegistry:
    """Global registry for character set definitions."""
    
    _registry: Dict[str, Charset] = {}
    
    @classmethod
    def add_charset(cls, charset: str, header_encoding: EncodingType = EncodingType.QP,
                   body_encoding: str = '7bit', input_codec: Optional[str] = None,
                   output_codec: Optional[str] = None, convert: bool = False) -> None:
        """
        Register a new character set.
        
        Args:
            charset: Character set name
            header_encoding: Header encoding type
            body_encoding: Body encoding type
            input_codec: Input codec (defaults to charset)
            output_codec: Output codec (defaults to charset)
            convert: Whether to convert between codecs
        """
        cs = Charset(
            charset=charset,
            input_codec=input_codec or charset,
            output_codec=output_codec or charset,
            header_encoding=header_encoding,
            body_encoding=body_encoding,
            convert=convert
        )
        cls._registry[charset.lower()] = cs
    
    @classmethod
    def get_charset(cls, charset: str) -> Optional[Charset]:
        """
        Retrieve character set from registry.
        
        Args:
            charset: Character set name
            
        Returns:
            Charset instance or None
        """
        return cls._registry.get(charset.lower())
    
    @classmethod
    def list_charsets(cls) -> List[str]:
        """List all registered character sets."""
        return sorted(cls._registry.keys())
    
    @classmethod
    def clear_registry(cls) -> None:
        """Clear all registered character sets."""
        cls._registry.clear()


# ============= CODEC REGISTRATION =============

class CodecRegistry:
    """Registry for encoding/decoding codecs."""
    
    _codecs: Dict[str, Callable] = {}
    
    @classmethod
    def add_codec(cls, name: str, encoder: Callable, decoder: Callable) -> None:
        """
        Register encoding/decoding codec.
        
        Args:
            name: Codec name
            encoder: Encoding function
            decoder: Decoding function
        """
        cls._codecs[name.lower()] = {
            'encode': encoder,
            'decode': decoder
        }
    
    @classmethod
    def get_codec(cls, name: str) -> Optional[Dict[str, Callable]]:
        """Retrieve codec by name."""
        return cls._codecs.get(name.lower())
    
    @classmethod
    def list_codecs(cls) -> List[str]:
        """List all registered codecs."""
        return sorted(cls._codecs.keys())


# ============= ALIAS MANAGEMENT =============

class CharsetAliases:
    """Manage character set aliases."""
    
    _aliases: Dict[str, str] = {
        'utf-8': 'UTF-8',
        'utf8': 'UTF-8',
        'ascii': 'ASCII',
        'us-ascii': 'ASCII',
        'iso-8859-1': 'ISO-8859-1',
        'latin1': 'ISO-8859-1',
        'latin-1': 'ISO-8859-1',
        'iso-8859-2': 'ISO-8859-2',
        'latin2': 'ISO-8859-2',
        'cp1252': 'CP1252',
        'windows-1252': 'CP1252',
        'gb2312': 'GB2312',
        'gbk': 'GBK',
        'big5': 'BIG5',
    }
    
    @classmethod
    def add_alias(cls, alias: str, target_charset: str) -> None:
        """
        Register character set alias.
        
        Args:
            alias: Alias name
            target_charset: Target character set
        """
        cls._aliases[alias.lower()] = target_charset
    
    @classmethod
    def resolve_alias(cls, charset: str) -> str:
        """
        Resolve charset alias to canonical form.
        
        Args:
            charset: Charset name or alias
            
        Returns:
            Canonical charset name
        """
        return cls._aliases.get(charset.lower(), charset)
    
    @classmethod
    def list_aliases(cls) -> Dict[str, str]:
        """List all registered aliases."""
        return cls._aliases.copy()


# ============= UTILITY FUNCTIONS =============

def add_alias(alias: str, canonical_charset: str) -> None:
    """Register charset alias (module-level function)."""
    CharsetAliases.add_alias(alias, canonical_charset)


def add_charset(charset: str, header_encoding: str = 'q', 
               body_encoding: str = '7bit', input_codec: str = None,
               output_codec: str = None, convert: bool = False) -> None:
    """Register character set (module-level function)."""
    header_enc_type = (EncodingType.BASE64 if header_encoding.lower() == 'b' 
                      else EncodingType.QP if header_encoding.lower() == 'q'
                      else EncodingType.SHORTEST)
    
    CharsetRegistry.add_charset(
        charset,
        header_encoding=header_enc_type,
        body_encoding=body_encoding,
        input_codec=input_codec,
        output_codec=output_codec,
        convert=convert
    )


def add_codec(name: str, encoder: Callable, decoder: Callable) -> None:
    """Register codec (module-level function)."""
    CodecRegistry.add_codec(name, encoder, decoder)


# ============= INITIALIZATION =============

def initialize_default_charsets() -> None:
    """Initialize standard character sets."""
    
    # UTF-8 (Quoted-Printable for headers, Base64 for bodies)
    add_charset('utf-8', header_encoding='q', body_encoding='base64')
    add_charset('utf8', header_encoding='q', body_encoding='base64')
    
    # ASCII (7-bit safe)
    add_charset('ascii', header_encoding='q', body_encoding='7bit')
    add_charset('us-ascii', header_encoding='q', body_encoding='7bit')
    
    # ISO-8859-1 (Latin-1)
    add_charset('iso-8859-1', header_encoding='q', body_encoding='quoted-printable')
    add_charset('latin1', header_encoding='q', body_encoding='quoted-printable')
    
    # Windows-1252
    add_charset('cp1252', header_encoding='b', body_encoding='base64')
    add_charset('windows-1252', header_encoding='b', body_encoding='base64')
    
    # CJK character sets
    add_charset('gb2312', header_encoding='b', body_encoding='base64')
    add_charset('big5', header_encoding='b', body_encoding='base64')


# ============= DEMONSTRATION =============

def demo_email_encoding():
    """Demonstrate email encoding capabilities."""
    
    print("=" * 100)
    print("LKL-Jr EMAIL ENCODING & CHARSET MANAGEMENT MODULE")
    print("=" * 100)
    print()
    
    # Initialize charsets
    initialize_default_charsets()
    
    # Test 1: Charset registry
    print("[1] CHARACTER SET REGISTRY")
    print("-" * 100)
    charsets = CharsetRegistry.list_charsets()
    print(f"Registered charsets ({len(charsets)}):")
    for cs in charsets[:5]:
        charset_obj = CharsetRegistry.get_charset(cs)
        print(f"  • {cs:<15} → Header: {charset_obj.get_header_encoding():>3} | Body: {charset_obj.body_encoding}")
    print(f"  ... and {len(charsets) - 5} more")
    print()
    
    # Test 2: Header encoding
    print("[2] HEADER ENCODING (RFC 2047)")
    print("-" * 100)
    
    test_headers = [
        ("Hello World", "ascii"),
        ("Привет Мир", "utf-8"),
        ("你好世界", "utf-8"),
    ]
    
    for text, charset_name in test_headers:
        cs = CharsetRegistry.get_charset(charset_name)
        if cs:
            encoded = cs.encode_header(text)
            decoded = cs.decode_header(encoded)
            print(f"Text:    {text}")
            print(f"Charset: {charset_name}")
            print(f"Encoded: {encoded}")
            print(f"Decoded: {decoded}")
            print(f"Match:   {'✓' if decoded == text else '✗'}")
            print()
    
    # Test 3: Body encoding
    print("[3] BODY ENCODING")
    print("-" * 100)
    
    body_text = "This is an email body with some special characters: café, naïve."
    cs_utf8 = CharsetRegistry.get_charset('utf-8')
    
    encoded_b64, enc_type_b64 = cs_utf8.encode_body(body_text)
    decoded_b64 = cs_utf8.decode_body(encoded_b64, enc_type_b64)
    
    print(f"Original body:")
    print(f"  {body_text}")
    print()
    print(f"Base64 encoded:")
    print(f"  {encoded_b64[:60]}...")
    print()
    print(f"Decoded back:")
    print(f"  {decoded_b64}")
    print(f"Match: {'✓' if decoded_b64 == body_text else '✗'}")
    print()
    
    # Test 4: Alias resolution
    print("[4] CHARSET ALIAS RESOLUTION")
    print("-" * 100)
    
    test_aliases = ['utf8', 'latin1', 'us-ascii', 'windows-1252']
    
    for alias in test_aliases:
        resolved = CharsetAliases.resolve_alias(alias)
        print(f"  {alias:<20} → {resolved}")
    print()
    
    # Test 5: Contact information
    print("[5] CONTACT INFORMATION")
    print("-" * 100)
    print("Email Signature List (email-sig@python.org)")
    print("Project Contact: locustjr@proton.me")
    print("LKL-Jr Identity: locust@therootedpi.polly")
    print()
    
    # Test 6: Module metadata
    print("[6] MODULE METADATA")
    print("-" * 100)
    print(f"Author: Ben Gertzfield, Barry Warsaw")
    print(f"Modified for: Luke Kerry Locust Jr. (LKL-Jr)")
    print(f"Project: πB, πP, πA-she Secret Systems")
    print(f"Date: 02 Sep 2026")
    print()
    
    print("=" * 100)
    print("✓ EMAIL ENCODING MODULE OPERATIONAL")
    print("=" * 100)


__all__ = [
    'Charset',
    'CharsetRegistry',
    'CodecRegistry',
    'CharsetAliases',
    'EncodingType',
    'EncodingConstants',
    'add_alias',
    'add_charset',
    'add_codec',
]


if __name__ == '__main__':
    demo_email_encoding()
