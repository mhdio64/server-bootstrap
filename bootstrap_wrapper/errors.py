"""User-facing wrapper errors."""


class BootstrapWrapperError(Exception):
    """Base class for wrapper failures."""


class InventoryError(BootstrapWrapperError):
    """Inventory parsing or validation failed."""


class HostTrustError(BootstrapWrapperError):
    """Host key trust could not be established or verified."""
