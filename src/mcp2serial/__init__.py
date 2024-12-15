from . import server
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(server.main())

# Expose important items at package level
__version__ = "0.1.0"
__all__ = ['main', 'server']
