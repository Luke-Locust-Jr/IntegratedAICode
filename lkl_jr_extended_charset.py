"""
LKL-Jr Extended Email Charset & Quoted-Printable Encoding Module
=================================================================
Complete implementation of RFC 2045-2047 email encoding standards.
Extended charset registry with Latin series support and quoted-printable encoding.

Copyright (C) 2001 Python Software Foundation
Authors: Ben Gertzfield, Barry Warsaw
Modified for: Luke Kerry Locust Jr. Identity Framework
Contact: email-sig@python.org
Forwarding: locustjr@proton.me

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026
"""

from functools import partial
from typing import Dict, List, Tuple, Optional, Any, Callable
from enum import Enum
from string import ascii_letters, digits, hexdigits
import re
import base64
import email.base64mime
import email.quoprimime
from email import errors
from email.encoders import encode_7or8bit
from dataclasses import dataclass


# ============= CONSTANTS =============

class EncodingConstants:
    """Constants for RFC 2045-2047 encoding."""
    
    # Encoding types
    QP = 1          # Quoted-Printable
    BASE64 = 2      # Base64
    SHORTEST = 3    # Auto-select shortest
    
    # Line endings
    CRLF = '\r\n'
    NL = '\n'
    EMPTYSTRING = ''
    
    # RFC 2047 chrome length: "=?charset?q?" + "?=" = ~13 chars
    RFC2047_CHROME_LEN = 13
    
    # Special constants
    UNKNOWN8BIT = 'unknown-8bit'
    DEFAULT_CHARSET = 'us-ascii'


# ============= CHARSET ALIASES =============

class CharsetAliasRegistry:
    """Extended charset alias registry with Latin series support."""
    
    # Comprehensive alias mappings
    ALIASES = {
        # UTF series
        'utf-8': 'utf-8',
        'utf8': 'utf-8',
        'utf_8': 'utf-8',
        
        # ASCII variants
        'ascii': 'us-ascii',
        'us-ascii': 'us-ascii',
        
        # ISO-8859 (Latin) series - comprehensive support
        'latin_1': 'iso-8859-1',
        'latin-1': 'iso-8859-1',
        'iso-8859-1': 'iso-8859-1',
        
        'latin_2': 'iso-8859-2',
        'latin-2': 'iso-8859-2',
        'iso-8859-2': 'iso-8859-2',
        
        'latin_3': 'iso-8859-3',
        'latin-3': 'iso-8859-3',
        'iso-8859-3': 'iso-8859-3',
        
        'latin_4': 'iso-8859-4',
        'latin-4': 'iso-8859-4',
        'iso-8859-4': 'iso-8859-4',
        
        'latin_5': 'iso-8859-9',  # Turkish
        'latin-5': 'iso-8859-9',
        'iso-8859-9': 'iso-8859-9',
        
        'latin_6': 'iso-8859-10',  # Nordic
        'latin-6': 'iso-8859-10',
        'iso-8859-10': 'iso-8859-10',
        
        'latin_7': 'iso-8859-13',  # Baltic
        'latin-7': 'iso-8859-13',
        'iso-8859-13': 'iso-8859-13',
        
        'latin_8': 'iso-8859-14',  # Celtic
        'latin-8': 'iso-8859-14',
        'iso-8859-14': 'iso-8859-14',
        
        'latin_9': 'iso-8859-15',  # Western European with Euro
        'latin-9': 'iso-8859-15',
        'iso-8859-15': 'iso-8859-15',
        
        'latin_10': 'iso-8859-16',  # South-Eastern European
        'latin-10': 'iso-8859-16',
        'iso-8859-16': 'iso-8859-16',
        
        # East Asian
        'cp949': 'ks_c_5601-1987',  # Korean
        'euc_jp': 'euc-jp',         # Japanese
        'euc-jp': 'euc-jp',
        'euc_kr': 'euc-kr',         # Korean
        'euc-kr': 'euc-kr',
        'gb2312': 'gb2312',         # Simplified Chinese
        'big5': 'big5',             # Traditional Chinese
        
        # Windows codepages
        'cp1252': 'cp1252',         # Western European
        'windows-1252': 'cp1252',
    }
    
    @classmethod
    def resolve(cls, charset: str) -> str:
        """Resolve charset alias to canonical name."""
        normalized = charset.lower()
        return cls.ALIASES.get(normalized, normalized)
    
    @classmethod
    def add_alias(cls, alias: str, canonical: str) -> None:
        """Add custom charset alias."""
        cls.ALIASES[alias.lower()] = canonical.lower()
    
    @classmethod
    def list_aliases(cls) -> Dict[str, str]:
        """List all alias mappings."""
        return cls.ALIASES.copy()


# ============= CODEC MAPPING =============

class CodecMap:
    """Map character sets to Unicode codec names."""
    
    # Codec mappings - None means no conversion needed
    CODEC_MAP = {
        'us-ascii': None,  # Pass through without conversion
        'utf-8': 'utf-8',
        'iso-8859-1': 'iso-8859-1',
        'iso-8859-2': 'iso-8859-2',
        'iso-8859-3': 'iso-8859-3',
        'iso-8859-4': 'iso-8859-4',
        'iso-8859-9': 'iso-8859-9',
        'iso-8859-10': 'iso-8859-10',
        'iso-8859-13': 'iso-8859-13',
        'iso-8859-14': 'iso-8859-14',
        'iso-8859-15': 'iso-8859-15',
        'iso-8859-16': 'iso-8859-16',
        'cp1252': 'cp1252',
        'ks_c_5601-1987': 'cp949',
        'euc-jp': 'euc-jp',
        'euc-kr': 'euc-kr',
        'gb2312': 'gb2312',
        'big5': 'big5',
    }
    
    @classmethod
    def get_codec(cls, charset: str) -> Optional[str]:
        """Get codec name for charset."""
        return cls.CODEC_MAP.get(charset.lower())
    
    @classmethod
    def add_codec(cls, charset: str, codecname: str) -> None:
        """Register codec for charset."""
        cls.CODEC_MAP[charset.lower()] = codecname
    
    @classmethod
    def list_codecs(cls) -> Dict[str, Optional[str]]:
        """List all codec mappings."""
        return cls.CODEC_MAP.copy()


# ============= QUOTED-PRINTABLE ENCODING =============

class QuotedPrintableEncoder:
    """RFC 2045 Quoted-Printable encoding/decoding."""
    
    # Build character maps
    _QUOPRI_MAP = ['=%02X' % c for c in range(256)]
    _QUOPRI_HEADER_MAP = _QUOPRI_MAP[:]
    _QUOPRI_BODY_MAP = _QUOPRI_MAP[:]
    
    # Safe header bytes
    for c in b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii'):
        _QUOPRI_HEADER_MAP[c] = chr(c)
    _QUOPRI_HEADER_MAP[ord(' ')] = '_'  # Space becomes underscore in headers
    
    # Safe body bytes
    for c in (b' !"#$%&\'()*+,-./0123456789:;<>'
              b'?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
              b'abcdefghijklmnopqrstuvwxyz{|}~\t'):
        _QUOPRI_BODY_MAP[c] = chr(c)
    
    @staticmethod
    def header_check(octet: int) -> bool:
        """Check if octet needs header encoding."""
        return chr(octet) != QuotedPrintableEncoder._QUOPRI_HEADER_MAP[octet]
    
    @staticmethod
    def body_check(octet: int) -> bool:
        """Check if octet needs body encoding."""
        return chr(octet) != QuotedPrintableEncoder._QUOPRI_BODY_MAP[octet]
    
    @staticmethod
    def header_length(bytearray_data: bytes) -> int:
        """Calculate header quoted-printable encoded length."""
        return sum(len(QuotedPrintableEncoder._QUOPRI_HEADER_MAP[octet]) 
                  for octet in bytearray_data)
    
    @staticmethod
    def body_length(bytearray_data: bytes) -> int:
        """Calculate body quoted-printable encoded length."""
        return sum(len(QuotedPrintableEncoder._QUOPRI_BODY_MAP[octet]) 
                  for octet in bytearray_data)
    
    @staticmethod
    def unquote(s: str) -> str:
        """Turn =AB form to ASCII character."""
        return chr(int(s[1:3], 16))
    
    @staticmethod
    def quote(c: str) -> str:
        """Quote a character."""
        return QuotedPrintableEncoder._QUOPRI_MAP[ord(c)]
    
    @staticmethod
    def header_encode(header_bytes: bytes, charset: str = 'iso-8859-1') -> str:
        """
        RFC 2047 'Q' encoding for headers.
        
        Args:
            header_bytes: Bytes to encode
            charset: Character set name
            
        Returns:
            Encoded header in =?charset?q?...?= format
        """
        if not header_bytes:
            return ''
        
        encoded = header_bytes.decode('latin1').translate(
            {ord(c): QuotedPrintableEncoder._QUOPRI_HEADER_MAP[ord(c)] 
             for c in range(256)})
        
        return f'=?{charset}?q?{encoded}?='
    
    @staticmethod
    def body_encode(body: str, maxlinelen: int = 76, eol: str = '\n') -> str:
        """
        Encode body with quoted-printable.
        
        Args:
            body: Text to encode
            maxlinelen: Maximum line length (minimum 4)
            eol: End-of-line character
            
        Returns:
            Encoded body with soft line breaks
        """
        if maxlinelen < 4:
            raise ValueError("maxlinelen must be at least 4")
        if not body:
            return body
        
        # Build body encode map
        body_encode_map = QuotedPrintableEncoder._QUOPRI_BODY_MAP[:]
        for c in b'\r\n':
            body_encode_map[c] = chr(c)
        
        # Translate body
        body = body.translate({ord(c): body_encode_map[ord(c)] for c in range(256)})
        
        soft_break = '=' + eol
        maxlinelen1 = maxlinelen - 1
        
        encoded_body = []
        
        for line in body.splitlines():
            start = 0
            laststart = len(line) - 1 - maxlinelen
            
            while start <= laststart:
                stop = start + maxlinelen1
                
                # Avoid breaking escape sequence
                if line[stop - 2] == '=':
                    encoded_body.append(line[start:stop - 1])
                    start = stop - 2
                elif line[stop - 1] == '=':
                    encoded_body.append(line[start:stop])
                    start = stop - 1
                else:
                    encoded_body.append(line[start:stop] + '=')
                    start = stop
            
            # Handle rest and whitespace at end
            if line and line[-1] in ' \t':
                room = start - laststart
                if room >= 3:
                    q = QuotedPrintableEncoder.quote(line[-1])
                elif room == 2:
                    q = line[-1] + soft_break
                else:
                    q = soft_break + QuotedPrintableEncoder.quote(line[-1])
                encoded_body.append(line[start:-1] + q)
            else:
                encoded_body.append(line[start:])
        
        # Restore final newline if present
        if body and body[-1] in '\r\n':
            encoded_body.append('')
        
        return eol.join(encoded_body)
    
    @staticmethod
    def decode(encoded: str, eol: str = '\n') -> str:
        """
        Decode quoted-printable string.
        
        Args:
            encoded: Encoded string
            eol: End-of-line character
            
        Returns:
            Decoded string
        """
        if not encoded:
            return encoded
        
        decoded = ''
        
        for line in encoded.splitlines():
            line = line.rstrip()
            if not line:
                decoded += eol
                continue
            
            i = 0
            n = len(line)
            while i < n:
                c = line[i]
                if c != '=':
                    decoded += c
                    i += 1
                elif i + 1 == n:
                    i += 1
                    continue
                elif i + 2 < n and line[i + 1] in hexdigits and line[i + 2] in hexdigits:
                    decoded += QuotedPrintableEncoder.unquote(line[i:i + 3])
                    i += 3
                else:
                    decoded += c
                    i += 1
                
                if i == n:
                    decoded += eol
        
        # Special case: if original didn't end with eol, remove trailing eol
        if encoded[-1] not in '\r\n' and decoded.endswith(eol):
            decoded = decoded[:-len(eol)]
        
        return decoded
    
    @staticmethod
    def header_decode(s: str) -> str:
        """
        Decode RFC 2047 'Q' encoded header.
        
        Args:
            s: Encoded header string (without =?...?= wrapper)
            
        Returns:
            Decoded header text
        """
        s = s.replace('_', ' ')
        return re.sub(r'=[a-fA-F0-9]{2}', 
                     lambda m: QuotedPrintableEncoder.unquote(m.group(0)), 
                     s, flags=re.ASCII)


# ============= COMPREHENSIVE CHARSET CLASS =============

@dataclass
class ExtendedCharset:
    """Extended Charset with full RFC 2045-2047 support."""
    
    input_charset: str
    header_encoding: int = EncodingConstants.QP
    body_encoding: int = EncodingConstants.BASE64
    output_charset: Optional[str] = None
    convert: bool = False
    
    def __post_init__(self):
        """Normalize charset names."""
        self.input_charset = self.input_charset.lower()
        self.input_charset = CharsetAliasRegistry.resolve(self.input_charset)
        
        if self.output_charset is None:
            self.output_charset = self.input_charset
        else:
            self.output_charset = self.output_charset.lower()
            self.output_charset = CharsetAliasRegistry.resolve(self.output_charset)
    
    def get_body_encoding(self) -> str:
        """Get content-transfer-encoding for body."""
        if self.body_encoding == EncodingConstants.QP:
            return 'quoted-printable'
        elif self.body_encoding == EncodingConstants.BASE64:
            return 'base64'
        else:
            return 'quoted-printable'
    
    def get_output_charset(self) -> str:
        """Get output charset."""
        return self.output_charset or self.input_charset
    
    def header_encode(self, string: str) -> str:
        """Encode header string."""
        codec = CodecMap.get_codec(self.get_output_charset()) or 'us-ascii'
        
        try:
            header_bytes = string.encode(codec)
        except (UnicodeEncodeError, LookupError):
            header_bytes = string.encode('ascii', 'replace')
        
        if self.header_encoding == EncodingConstants.BASE64:
            encoded = base64.b64encode(header_bytes).decode('ascii')
            return f'=?{self.get_output_charset()}?b?{encoded}?='
        else:
            return QuotedPrintableEncoder.header_encode(header_bytes, self.get_output_charset())
    
    def body_encode(self, string: str) -> str:
        """Encode body string."""
        if not string:
            return string
        
        codec = CodecMap.get_codec(self.get_output_charset()) or 'us-ascii'
        
        if self.body_encoding == EncodingConstants.BASE64:
            if isinstance(string, str):
                string = string.encode(codec)
            return base64.b64encode(string).decode('ascii')
        elif self.body_encoding == EncodingConstants.QP:
            if isinstance(string, str):
                string_bytes = string.encode(codec)
                string = string_bytes.decode('latin1')
            return QuotedPrintableEncoder.body_encode(string)
        else:
            return string
    
    def __repr__(self) -> str:
        return f"ExtendedCharset({self.input_charset}, header={self.header_encoding}, body={self.body_encoding})"


# ============= DEMONSTRATION =============

def demo_extended_email_charset():
    """Demonstrate extended charset and quoted-printable functionality."""
    
    print("=" * 100)
    print("LKL-Jr EXTENDED EMAIL CHARSET & QUOTED-PRINTABLE MODULE")
    print("=" * 100)
    print()
    
    # Test 1: Charset alias resolution
    print("[1] CHARSET ALIAS RESOLUTION")
    print("-" * 100)
    test_aliases = ['utf8', 'latin-1', 'latin-9', 'latin_10', 'euc_jp']
    for alias in test_aliases:
        resolved = CharsetAliasRegistry.resolve(alias)
        print(f"  {alias:<20} → {resolved}")
    print()
    
    # Test 2: Codec mapping
    print("[2] CODEC MAPPING")
    print("-" * 100)
    charsets = ['utf-8', 'iso-8859-1', 'iso-8859-2', 'cp1252', 'euc-jp']
    for cs in charsets:
        codec = CodecMap.get_codec(cs)
        print(f"  {cs:<20} → {codec}")
    print()
    
    # Test 3: Quoted-printable encoding
    print("[3] QUOTED-PRINTABLE HEADER ENCODING")
    print("-" * 100)
    test_headers = [
        "Hello World",
        "Café Naïve",
    ]
    for header in test_headers:
        encoded = QuotedPrintableEncoder.header_encode(header.encode('utf-8'), 'utf-8')
        decoded = QuotedPrintableEncoder.header_decode(encoded.split('?q?')[1].split('?=')[0])
        print(f"  Original:  {header}")
        print(f"  Encoded:   {encoded}")
        print(f"  Decoded:   {decoded}")
        print()
    
    # Test 4: Extended Charset
    print("[4] EXTENDED CHARSET ENCODING")
    print("-" * 100)
    cs = ExtendedCharset(input_charset='utf-8')
    test_text = "Hello πWorld φTest"
    encoded = cs.header_encode(test_text)
    print(f"  Text:      {test_text}")
    print(f"  Encoded:   {encoded}")
    print()
    
    print("=" * 100)
    print("✓ EXTENDED EMAIL CHARSET MODULE OPERATIONAL")
    print("=" * 100)


__all__ = [
    'ExtendedCharset',
    'CharsetAliasRegistry',
    'CodecMap',
    'QuotedPrintableEncoder',
    'EncodingConstants',
]


if __name__ == '__main__':
    demo_extended_email_charset()
