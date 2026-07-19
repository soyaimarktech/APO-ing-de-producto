"""
Core exception hierarchy.

All APO exceptions inherit from APOError.
"""


class APOError(Exception):
    """Base exception for APO."""


class ConfigurationError(APOError):
    """Configuration related errors."""


class ValidationError(APOError):
    """Configuration validation errors."""


class FilesystemError(APOError):
    """Filesystem operation errors."""


class InventoryError(APOError):
    """Inventory generation errors."""


class ReportError(APOError):
    """Report generation errors."""


class CLIError(APOError):
    """Command line interface errors."""
