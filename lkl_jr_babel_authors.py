"""
LKL-Jr Babel Authors Integration
=================================
Integrates repository author metadata with Babel message catalogs.
Enables localization of author information, attribution, and credentials
across multiple languages and locales.

Identity: LKL-Jr @ locust@therootedpi.polly
Project: πB, πP, πA-she Secret Systems
Date: 02 Sep 2026

This module bridges author management with Babel's translation framework,
allowing author names, emails, affiliations, and bios to be translated
and localized for different audiences and regions.
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional, Any, Iterable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from babel.messages.catalog import Catalog, Message, DEFAULT_HEADER
from babel.core import Locale
import json


# ============= CONSTANTS =============

DEFAULT_AUTHOR_HEADER = """\
# Author Localization Template for PROJECT.
# Copyright (C) YEAR ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# Translators: Please localize author names, titles, and bios appropriately.
# FIRST TRANSLATOR <EMAIL@ADDRESS>, YEAR.
#"""

AUTHOR_FIELDS = [
    'name',
    'email',
    'role',
    'title',
    'affiliation',
    'bio',
    'website',
    'location',
]


@dataclass
class Author:
    """Represents a repository author with localization metadata."""
    id: str
    name: str
    email: str
    role: str = "Contributor"
    title: str = ""
    affiliation: str = ""
    bio: str = ""
    website: str = ""
    location: str = ""
    joined_date: Optional[str] = None
    contributions: int = 0
    verified: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_translation_tuples(self) -> List[Tuple[str, str]]:
        """Convert to (msgid, context) tuples for translation."""
        tuples = []
        for field in AUTHOR_FIELDS:
            value = getattr(self, field, "")
            if value:
                tuples.append((value, f"author_field:{self.id}:{field}"))
        return tuples


@dataclass
class AuthorCatalogEntry:
    """Represents an author entry in a localized catalog."""
    author: Author
    translations: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    def get_translated(self, locale: str | Locale, field: str) -> str:
        """Get translated field value for a locale."""
        if isinstance(locale, Locale):
            locale = str(locale)
        
        locale_str = str(locale)
        if locale_str in self.translations and field in self.translations[locale_str]:
            return self.translations[locale_str][field]
        
        # Fallback to original
        return getattr(self.author, field, "")
    
    def set_translated(self, locale: str | Locale, field: str, value: str) -> None:
        """Set translated field value for a locale."""
        if isinstance(locale, Locale):
            locale = str(locale)
        
        locale_str = str(locale)
        if locale_str not in self.translations:
            self.translations[locale_str] = {}
        self.translations[locale_str][field] = value


class AuthorCatalog(Catalog):
    """
    Extended Babel Catalog specialized for author localization.
    Manages author metadata across multiple locales.
    """
    
    def __init__(
        self,
        locale: Locale | str | None = None,
        domain: str = "authors",
        project: str | None = None,
        version: str | None = None,
        copyright_holder: str | None = None,
        header_comment: str | None = DEFAULT_AUTHOR_HEADER,
        **kwargs
    ):
        """
        Initialize author catalog.
        
        Args:
            locale: Target locale for this catalog
            domain: Message domain (default: "authors")
            project: Project name
            version: Project version
            copyright_holder: Copyright holder
            header_comment: Custom header comment
        """
        super().__init__(
            locale=locale,
            domain=domain,
            project=project or "PROJECT",
            version=version or "VERSION",
            copyright_holder=copyright_holder or "ORGANIZATION",
            header_comment=header_comment,
            **kwargs
        )
        
        self._authors: Dict[str, Author] = {}
        self._author_entries: Dict[str, AuthorCatalogEntry] = {}
    
    def add_author(
        self,
        author: Author,
        locations: Iterable[Tuple[str, int]] = (),
        auto_comments: Iterable[str] = (),
        user_comments: Iterable[str] = (),
    ) -> Author:
        """
        Add an author to the catalog.
        
        Args:
            author: Author object
            locations: Source file locations
            auto_comments: Automatic comments
            user_comments: User comments
            
        Returns:
            The added Author object
        """
        self._authors[author.id] = author
        self._author_entries[author.id] = AuthorCatalogEntry(author)
        
        # Add author fields as translatable messages
        for msgid, context in author.to_translation_tuples():
            msg = self.add(
                msgid,
                locations=locations,
                auto_comments=auto_comments,
                user_comments=user_comments,
                context=context,
            )
        
        return author
    
    def get_author(self, author_id: str) -> Optional[Author]:
        """Get author by ID."""
        return self._authors.get(author_id)
    
    def get_authors(self) -> Dict[str, Author]:
        """Get all authors."""
        return self._authors.copy()
    
    def set_author_translation(
        self,
        author_id: str,
        field: str,
        translated_value: str,
        locale: str | Locale | None = None,
    ) -> bool:
        """
        Set translated value for an author field.
        
        Args:
            author_id: Author ID
            field: Field name
            translated_value: Translated value
            locale: Target locale (uses catalog locale if not provided)
            
        Returns:
            True if successful
        """
        if author_id not in self._author_entries:
            return False
        
        target_locale = locale or self.locale_identifier
        if not target_locale:
            return False
        
        entry = self._author_entries[author_id]
        entry.set_translated(target_locale, field, translated_value)
        
        # Also update the message in the catalog
        author = self._authors[author_id]
        original_value = getattr(author, field, "")
        context = f"author_field:{author_id}:{field}"
        
        self.add(
            original_value,
            string=translated_value,
            context=context,
        )
        
        return True
    
    def get_author_translation(
        self,
        author_id: str,
        field: str,
        locale: str | Locale | None = None,
    ) -> Optional[str]:
        """
        Get translated value for an author field.
        
        Args:
            author_id: Author ID
            field: Field name
            locale: Target locale (uses catalog locale if not provided)
            
        Returns:
            Translated value or None
        """
        if author_id not in self._author_entries:
            return None
        
        target_locale = locale or self.locale_identifier
        if not target_locale:
            return None
        
        entry = self._author_entries[author_id]
        return entry.get_translated(target_locale, field)
    
    def export_author_json(self, author_id: str, include_translations: bool = True) -> Dict[str, Any]:
        """
        Export author as JSON with optional translations.
        
        Args:
            author_id: Author ID
            include_translations: Whether to include all translations
            
        Returns:
            JSON-serializable dictionary
        """
        if author_id not in self._authors:
            return {}
        
        author = self._authors[author_id]
        entry = self._author_entries[author_id]
        
        data = {
            'author': author.to_dict(),
        }
        
        if include_translations:
            data['translations'] = entry.translations
        
        return data
    
    def export_authors_json(self, include_translations: bool = True) -> Dict[str, Any]:
        """
        Export all authors as JSON.
        
        Args:
            include_translations: Whether to include all translations
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            author_id: self.export_author_json(author_id, include_translations)
            for author_id in self._authors
        }
    
    def print_authors(self, locale: str | Locale | None = None) -> None:
        """
        Print formatted author list.
        
        Args:
            locale: Locale for translations (uses catalog locale if not provided)
        """
        target_locale = locale or self.locale_identifier or "en"
        print(f"\nAUTHOR CATALOG ({target_locale}):".upper())
        print("-" * 100)
        print(f"{'ID':>12}  {'Name':>20}  {'Email':>25}  {'Role':>15}  {'Title':>15}")
        print("-" * 100)
        
        for author_id, author in self._authors.items():
            entry = self._author_entries[author_id]
            
            # Get translated or fallback to original
            name = entry.get_translated(target_locale, 'name')
            role = entry.get_translated(target_locale, 'role')
            title = entry.get_translated(target_locale, 'title')
            
            print(f"{author_id:>12}  {name:>20}  {author.email:>25}  {role:>15}  {title:>15}")
        
        print("-" * 100)
    
    def print_author_details(self, author_id: str, locale: str | Locale | None = None) -> None:
        """
        Print detailed author information.
        
        Args:
            author_id: Author ID
            locale: Locale for translations
        """
        if author_id not in self._authors:
            print(f"Author not found: {author_id}")
            return
        
        target_locale = locale or self.locale_identifier or "en"
        author = self._authors[author_id]
        entry = self._author_entries[author_id]
        
        print(f"\nAUTHOR DETAILS: {author_id}")
        print("-" * 80)
        
        for field in AUTHOR_FIELDS + ['joined_date', 'contributions', 'verified']:
            original_value = getattr(author, field, "")
            if original_value:
                translated_value = entry.get_translated(target_locale, field)
                print(f"{field:>15}: {translated_value or original_value}")
                
                if translated_value and translated_value != original_value:
                    print(f"  (original:   {original_value})")
        
        print("-" * 80)


class AuthorLocalizationManager:
    """
    Manages author localization across multiple catalogs and locales.
    """
    
    def __init__(self, project: str = "PROJECT", version: str = "1.0"):
        """
        Initialize manager.
        
        Args:
            project: Project name
            version: Project version
        """
        self.project = project
        self.version = version
        self.catalogs: Dict[str, AuthorCatalog] = {}
        self.authors: Dict[str, Author] = {}
    
    def create_catalog(self, locale: str | Locale | None = None) -> AuthorCatalog:
        """
        Create a new author catalog for a locale.
        
        Args:
            locale: Target locale
            
        Returns:
            New AuthorCatalog
        """
        locale_str = str(locale) if locale else "template"
        catalog = AuthorCatalog(
            locale=locale,
            project=self.project,
            version=self.version,
        )
        self.catalogs[locale_str] = catalog
        return catalog
    
    def register_author(self, author: Author) -> Author:
        """
        Register an author globally.
        
        Args:
            author: Author to register
            
        Returns:
            The registered Author
        """
        self.authors[author.id] = author
        
        # Add to all existing catalogs
        for catalog in self.catalogs.values():
            catalog.add_author(author)
        
        return author
    
    def add_author_to_locale(
        self,
        author: Author,
        locale: str | Locale,
    ) -> bool:
        """
        Add author to a specific locale's catalog.
        
        Args:
            author: Author to add
            locale: Target locale
            
        Returns:
            True if successful
        """
        locale_str = str(locale)
        if locale_str not in self.catalogs:
            self.create_catalog(locale)
        
        self.catalogs[locale_str].add_author(author)
        return True
    
    def translate_author_field(
        self,
        author_id: str,
        field: str,
        translated_value: str,
        locale: str | Locale,
    ) -> bool:
        """
        Set author field translation for a locale.
        
        Args:
            author_id: Author ID
            field: Field name
            translated_value: Translated value
            locale: Target locale
            
        Returns:
            True if successful
        """
        locale_str = str(locale)
        if locale_str not in self.catalogs:
            return False
        
        return self.catalogs[locale_str].set_author_translation(
            author_id, field, translated_value, locale
        )
    
    def get_localized_author(
        self,
        author_id: str,
        locale: str | Locale,
    ) -> Optional[AuthorCatalogEntry]:
        """
        Get localized author entry.
        
        Args:
            author_id: Author ID
            locale: Target locale
            
        Returns:
            Localized AuthorCatalogEntry or None
        """
        locale_str = str(locale)
        if locale_str not in self.catalogs:
            return None
        
        return self.catalogs[locale_str]._author_entries.get(author_id)
    
    def print_all_catalogs(self) -> None:
        """Print all author catalogs."""
        for locale, catalog in sorted(self.catalogs.items()):
            print(f"\n{'='*100}")
            catalog.print_authors(locale)


# ============= DEMONSTRATION =============

def demo_author_localization():
    """Demonstrate author localization."""
    
    print("="*100)
    print("LKL-Jr BABEL AUTHOR LOCALIZATION")
    print("="*100)
    
    # Create manager
    manager = AuthorLocalizationManager(
        project="IntegratedAICode",
        version="1.0"
    )
    
    # Create authors
    luke = Author(
        id="lkl_jr",
        name="Luke Locust Jr",
        email="locustjr@proton.me",
        role="Primary Developer",
        title="AI Integration Architect",
        affiliation="The Rooted Pi Collective",
        bio="Specialist in π-based calculations and IEC scale analysis",
        website="https://therootedpi.polly",
        location="Digital Space",
        joined_date="2026-01-15",
        contributions=42,
        verified=True,
    )
    
    copilot = Author(
        id="copilot",
        name="GitHub Copilot",
        email="support@github.com",
        role="Assistant Developer",
        title="AI Code Assistant",
        affiliation="GitHub",
        bio="Advanced code generation and integration support",
        website="https://github.com/copilot",
        joined_date="2026-02-01",
        contributions=87,
        verified=True,
    )
    
    # Register authors
    manager.register_author(luke)
    manager.register_author(copilot)
    
    # Create catalogs for different locales
    en_catalog = manager.create_catalog('en_US')
    de_catalog = manager.create_catalog('de_DE')
    ja_catalog = manager.create_catalog('ja_JP')
    
    print("\n✓ Authors registered in template catalog")
    print("\n✓ Localized catalogs created:")
    for locale in ['en_US', 'de_DE', 'ja_JP']:
        print(f"  • {locale}")
    
    # Add translations
    print("\n✓ Adding German translations...")
    manager.translate_author_field('lkl_jr', 'name', 'Luke Lokus Jr', 'de_DE')
    manager.translate_author_field('lkl_jr', 'title', 'KI-Integrations-Architekt', 'de_DE')
    manager.translate_author_field('lkl_jr', 'bio', 'Spezialist für π-basierte Berechnungen und IEC-Skalenanalyse', 'de_DE')
    
    print("✓ Adding Japanese translations...")
    manager.translate_author_field('lkl_jr', 'name', 'ルーク・ロカスト・ジュニア', 'ja_JP')
    manager.translate_author_field('lkl_jr', 'title', 'AI統合アーキテクト', 'ja_JP')
    manager.translate_author_field('lkl_jr', 'bio', 'πベースの計算とIECスケール分析の専門家', 'ja_JP')
    
    # Print all catalogs
    print()
    manager.print_all_catalogs()
    
    # Print detailed view
    print(f"\n{'='*100}")
    print("DETAILED AUTHOR VIEW (German):")
    de_catalog.print_author_details('lkl_jr', 'de_DE')
    
    print(f"\n{'='*100}")
    print("DETAILED AUTHOR VIEW (Japanese):")
    ja_catalog.print_author_details('lkl_jr', 'ja_JP')
    
    # Export as JSON
    print(f"\n{'='*100}")
    print("JSON EXPORT (German Locale):")
    import json
    export_data = de_catalog.export_authors_json(include_translations=True)
    print(json.dumps(export_data, indent=2, ensure_ascii=False))
    
    print("\n" + "="*100)
    print("✓ BABEL AUTHOR LOCALIZATION COMPLETE")
    print("="*100)


__all__ = [
    'Author',
    'AuthorCatalog',
    'AuthorCatalogEntry',
    'AuthorLocalizationManager',
    'DEFAULT_AUTHOR_HEADER',
    'AUTHOR_FIELDS',
]

if __name__ == '__main__':
    demo_author_localization()
