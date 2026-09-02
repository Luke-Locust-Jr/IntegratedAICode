"""
LKL-Jr Pygments Alabaster Syntax Highlighting Style
====================================================
Alabaster style theme for Pygments syntax highlighting.
Based on FlaskyStyle and tango color scheme.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

Usage:
    from lkl_jr_pygments_alabaster import Alabaster
    from pygments import highlight
    from pygments.lexers import PythonLexer
    
    code = 'print("Hello World")'
    result = highlight(code, PythonLexer(), HtmlFormatter(style=Alabaster))
"""

from typing import Dict, Tuple, Optional
from enum import Enum


class TokenType(Enum):
    """Pygments token types for style definition."""
    WHITESPACE = 'w'
    ERROR = 'err'
    OTHER = 'x'
    COMMENT = 'c'
    COMMENT_PREPROC = 'cp'
    KEYWORD = 'k'
    KEYWORD_CONSTANT = 'kc'
    KEYWORD_DECLARATION = 'kd'
    KEYWORD_NAMESPACE = 'kn'
    KEYWORD_PSEUDO = 'kp'
    KEYWORD_RESERVED = 'kr'
    KEYWORD_TYPE = 'kt'
    OPERATOR = 'o'
    OPERATOR_WORD = 'ow'
    PUNCTUATION = 'p'
    NAME = 'n'
    NAME_ATTRIBUTE = 'na'
    NAME_BUILTIN = 'nb'
    NAME_BUILTIN_PSEUDO = 'bp'
    NAME_CLASS = 'nc'
    NAME_CONSTANT = 'no'
    NAME_DECORATOR = 'nd'
    NAME_ENTITY = 'ni'
    NAME_EXCEPTION = 'ne'
    NAME_FUNCTION = 'nf'
    NAME_PROPERTY = 'py'
    NAME_LABEL = 'nl'
    NAME_NAMESPACE = 'nn'
    NAME_OTHER = 'nx'
    NAME_TAG = 'nt'
    NAME_VARIABLE = 'nv'
    NAME_VARIABLE_CLASS = 'vc'
    NAME_VARIABLE_GLOBAL = 'vg'
    NAME_VARIABLE_INSTANCE = 'vi'
    NUMBER = 'm'
    LITERAL = 'l'
    LITERAL_DATE = 'ld'
    STRING = 's'
    STRING_BACKTICK = 'sb'
    STRING_CHAR = 'sc'
    STRING_DOC = 'sd'
    STRING_DOUBLE = 's2'
    STRING_ESCAPE = 'se'
    STRING_HEREDOC = 'sh'
    STRING_INTERPOL = 'si'
    STRING_OTHER = 'sx'
    STRING_REGEX = 'sr'
    STRING_SINGLE = 's1'
    STRING_SYMBOL = 'ss'
    GENERIC = 'g'
    GENERIC_DELETED = 'gd'
    GENERIC_EMPH = 'ge'
    GENERIC_ERROR = 'gr'
    GENERIC_HEADING = 'gh'
    GENERIC_INSERTED = 'gi'
    GENERIC_OUTPUT = 'go'
    GENERIC_PROMPT = 'gp'
    GENERIC_STRONG = 'gs'
    GENERIC_SUBHEADING = 'gu'
    GENERIC_TRACEBACK = 'gt'


class AlabasterStyle:
    """Alabaster syntax highlighting style configuration."""
    
    # Background and default style
    background_color = "#f8f8f8"
    default_style = ""
    
    # Color palette
    COLORS = {
        'white': '#ffffff',
        'light_gray': '#f8f8f8',
        'medium_gray': '#888',
        'dark_gray': '#555',
        'black': '#000000',
        'red': '#a40000',
        'bright_red': '#ef2929',
        'dark_red': '#cc0000',
        'green': '#4e9a06',
        'dark_green': '#00A000',
        'yellow': '#f57900',
        'gold': '#c4a000',
        'orange': '#ce5c00',
        'dark_orange': '#582800',
        'blue': '#004461',
        'light_blue': '#3465a4',
        'dark_blue': '#800080',
        'brown': '#745334',
    }
    
    # Token styles
    styles: Dict[str, str] = {
        'Whitespace': f"bg:{COLORS['light_gray']}",
        'Error': f"{COLORS['red']} bg:{COLORS['bright_red']}",
        'Other': COLORS['black'],
        'Comment': f"italic {COLORS['orange']}",
        'Comment.Preproc': "noitalic",
        'Keyword': f"bold {COLORS['blue']}",
        'Keyword.Constant': f"bold {COLORS['blue']}",
        'Keyword.Declaration': f"bold {COLORS['blue']}",
        'Keyword.Namespace': f"bold {COLORS['blue']}",
        'Keyword.Pseudo': f"bold {COLORS['blue']}",
        'Keyword.Reserved': f"bold {COLORS['blue']}",
        'Keyword.Type': f"bold {COLORS['blue']}",
        'Operator': COLORS['dark_orange'],
        'Operator.Word': f"bold {COLORS['blue']}",
        'Punctuation': f"bold {COLORS['black']}",
        'Name': COLORS['black'],
        'Name.Attribute': COLORS['gold'],
        'Name.Builtin': COLORS['blue'],
        'Name.Builtin.Pseudo': COLORS['light_blue'],
        'Name.Class': COLORS['black'],
        'Name.Constant': COLORS['black'],
        'Name.Decorator': COLORS['medium_gray'],
        'Name.Entity': COLORS['orange'],
        'Name.Exception': f"bold {COLORS['dark_red']}",
        'Name.Function': COLORS['black'],
        'Name.Property': COLORS['black'],
        'Name.Label': COLORS['yellow'],
        'Name.Namespace': COLORS['black'],
        'Name.Other': COLORS['black'],
        'Name.Tag': f"bold {COLORS['blue']}",
        'Name.Variable': COLORS['black'],
        'Name.Variable.Class': COLORS['black'],
        'Name.Variable.Global': COLORS['black'],
        'Name.Variable.Instance': COLORS['black'],
        'Number': '#990000',
        'Literal': COLORS['black'],
        'Literal.Date': COLORS['black'],
        'String': COLORS['green'],
        'String.Backtick': COLORS['green'],
        'String.Char': COLORS['green'],
        'String.Doc': f"italic {COLORS['orange']}",
        'String.Double': COLORS['green'],
        'String.Escape': COLORS['green'],
        'String.Heredoc': COLORS['green'],
        'String.Interpol': COLORS['green'],
        'String.Other': COLORS['green'],
        'String.Regex': COLORS['green'],
        'String.Single': COLORS['green'],
        'String.Symbol': COLORS['green'],
        'Generic': COLORS['black'],
        'Generic.Deleted': COLORS['red'],
        'Generic.Emph': f"italic {COLORS['black']}",
        'Generic.Error': COLORS['bright_red'],
        'Generic.Heading': f"bold {COLORS['dark_blue']}",
        'Generic.Inserted': COLORS['dark_green'],
        'Generic.Output': COLORS['medium_gray'],
        'Generic.Prompt': COLORS['brown'],
        'Generic.Strong': f"bold {COLORS['black']}",
        'Generic.Subheading': f"bold {COLORS['dark_blue']}",
        'Generic.Traceback': f"bold {COLORS['red']}",
    }
    
    @classmethod
    def get_style(cls, token_type: str) -> str:
        """Get style string for token type."""
        return cls.styles.get(token_type, "")
    
    @classmethod
    def get_color(cls, color_name: str) -> Optional[str]:
        """Get color hex value by name."""
        return cls.COLORS.get(color_name.lower())
    
    @classmethod
    def color_palette(cls) -> Dict[str, str]:
        """Return complete color palette."""
        return cls.COLORS.copy()
    
    @classmethod
    def style_map(cls) -> Dict[str, str]:
        """Return complete style map."""
        return cls.styles.copy()


class Alabaster(AlabasterStyle):
    """Alabaster Pygments style - based on Tango color scheme."""
    pass


# ============= DEMONSTRATION =============

def demo_alabaster_style():
    """Demonstrate Alabaster style configuration."""
    
    print("="*100)
    print("LKL-Jr PYGMENTS ALABASTER SYNTAX HIGHLIGHTING STYLE")
    print("="*100)
    print()
    
    print("[1] COLOR PALETTE")
    print("-"*100)
    palette = Alabaster.color_palette()
    for name, hex_code in sorted(palette.items()):
        print(f"  {name:<20} {hex_code}")
    print()
    
    print("[2] BACKGROUND CONFIGURATION")
    print("-"*100)
    print(f"Background color:    {Alabaster.background_color}")
    print(f"Default style:       {Alabaster.default_style or '(none)'}")
    print()
    
    print("[3] SELECTED TOKEN STYLES")
    print("-"*100)
    selected_tokens = [
        'Keyword',
        'String',
        'Comment',
        'Name.Function',
        'Number',
        'Operator',
        'Error',
    ]
    
    for token in selected_tokens:
        style = Alabaster.get_style(token)
        print(f"  {token:<20} {style}")
    print()
    
    print("[4] STYLE STATISTICS")
    print("-"*100)
    styles = Alabaster.style_map()
    print(f"Total token styles defined: {len(styles)}")
    print(f"Background color:          {Alabaster.background_color}")
    print()
    
    print("="*100)
    print("✓ ALABASTER STYLE CONFIGURATION COMPLETE")
    print("="*100)


__all__ = [
    'Alabaster',
    'AlabasterStyle',
    'TokenType',
]

if __name__ == '__main__':
    demo_alabaster_style()
