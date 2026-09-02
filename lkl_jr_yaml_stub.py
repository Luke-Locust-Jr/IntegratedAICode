"""
LKL-Jr YAML Module Stub
=======================
Stub package designed to emulate the _yaml extension module.
Previously existed as a standalone module, now integrated into yaml package namespace.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

This module provides compatibility for code that imports from _yaml directly,
while supporting the modern yaml package structure with LibYAML bindings.
"""

import sys
import warnings
from typing import Any, Dict, Optional


class YAMLStubConfig:
    """Configuration for YAML stub behavior."""
    
    enable_libyaml = True
    deprecation_warnings = True
    legacy_mode = False


class YAMLModule:
    """
    YAML module stub providing backwards compatibility.
    Bridges between old _yaml extension API and new yaml package.
    """
    
    def __init__(self, yaml_module: Optional[Any] = None):
        """Initialize YAML stub with optional yaml module reference."""
        self.yaml = yaml_module
        self.__with_libyaml__ = False
        self._setup_yaml()
    
    def _setup_yaml(self):
        """Setup YAML module with LibYAML support if available."""
        try:
            import yaml
            self.yaml = yaml
            
            # Check for LibYAML support
            if hasattr(yaml, '__with_libyaml__') and yaml.__with_libyaml__:
                self.__with_libyaml__ = True
            elif hasattr(yaml, 'CSafeLoader'):
                self.__with_libyaml__ = True
            
            if not self.__with_libyaml__:
                version_info = sys.version_info
                exc = ModuleNotFoundError if version_info >= (3, 6) else ImportError
                raise exc("No module named '_yaml' (LibYAML not available)")
            
            if YAMLStubConfig.deprecation_warnings:
                warnings.warn(
                    'The _yaml extension module is now located at yaml._yaml '
                    'and its location is subject to change. To use the '
                    'LibYAML-based parser and emitter, import from `yaml`: '
                    '`from yaml import CLoader as Loader, CDumper as Dumper`.',
                    DeprecationWarning,
                    stacklevel=2
                )
        
        except ImportError:
            version_info = sys.version_info
            exc = ModuleNotFoundError if version_info >= (3, 6) else ImportError
            raise exc("yaml module not found")
    
    def get_loader(self) -> Any:
        """Get the C-based YAML loader."""
        if hasattr(self.yaml, 'CLoader'):
            return self.yaml.CLoader
        elif hasattr(self.yaml, 'CSafeLoader'):
            return self.yaml.CSafeLoader
        else:
            return self.yaml.SafeLoader
    
    def get_dumper(self) -> Any:
        """Get the C-based YAML dumper."""
        if hasattr(self.yaml, 'CDumper'):
            return self.yaml.CDumper
        else:
            return self.yaml.SafeDumper
    
    def load(self, stream: Any, Loader: Optional[Any] = None) -> Any:
        """Load YAML from stream."""
        if Loader is None:
            Loader = self.get_loader()
        return self.yaml.load(stream, Loader=Loader)
    
    def dump(self, data: Any, stream: Optional[Any] = None, **kwargs) -> Optional[str]:
        """Dump data to YAML."""
        Dumper = kwargs.pop('Dumper', None) or self.get_dumper()
        return self.yaml.dump(data, stream, Dumper=Dumper, **kwargs)
    
    def safe_load(self, stream: Any) -> Any:
        """Load YAML safely."""
        return self.yaml.safe_load(stream)
    
    def safe_dump(self, data: Any, **kwargs) -> str:
        """Dump YAML safely."""
        return self.yaml.safe_dump(data, **kwargs)


# ============= DEMONSTRATION =============

def demo_yaml_stub():
    """Demonstrate YAML stub functionality."""
    
    print("="*100)
    print("LKL-Jr YAML MODULE STUB")
    print("="*100)
    print()
    
    try:
        yaml_stub = YAMLModule()
        
        print("[1] YAML CONFIGURATION")
        print("-"*100)
        print(f"LibYAML support available: {yaml_stub.__with_libyaml__}")
        print(f"Loader: {yaml_stub.get_loader()}")
        print(f"Dumper: {yaml_stub.get_dumper()}")
        print()
        
        print("[2] YAML DATA HANDLING")
        print("-"*100)
        
        test_data = {
            'name': 'Luke Kerry Locust Jr.',
            'identity': 'LKL-Jr',
            'email': 'locustjr@proton.me',
            'systems': ['πB', 'πP', 'πA-she']
        }
        
        yaml_str = yaml_stub.safe_dump(test_data)
        print("YAML output:")
        print(yaml_str)
        
        loaded = yaml_stub.safe_load(yaml_str)
        print(f"Round-trip success: {loaded == test_data}")
        print()
        
        print("="*100)
        print("✓ YAML STUB OPERATIONAL")
        print("="*100)
    
    except Exception as e:
        print(f"YAML module setup: {e}")
        print("(This is expected if yaml/libyaml not installed)")


__all__ = [
    'YAMLModule',
    'YAMLStubConfig',
]

__name__ = '_yaml'
__package__ = ''

if __name__ == '__main__':
    demo_yaml_stub()
