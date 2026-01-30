"""Water Guardian LIW-01 integration
Author: M4hSzyna (@mackowskim)
"""

from .helpers import setup_helpers

async def async_setup(hass, config):
    """Setup integration."""
    # Tworzymy wszystkie helpery wymagane przez blueprint
    await setup_helpers(hass)
    return True
