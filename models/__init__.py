"""
Blender MCP Models Package

This package contains procedural 3D model generators that integrate with
the Blender MCP server, allowing Claude to generate and manipulate 3D models
directly in Blender.

Available Modules:
    - lunuff_character: Complete Lunuff character model generator
    - mcp_lunuff_integration: MCP server integration for Lunuff models

Example Usage:
    from models.lunuff_character import LunuffModelGenerator

    generator = LunuffModelGenerator()
    model = generator.generate()
"""

__version__ = "1.0.0"
__author__ = "Blender MCP Contributors"

try:
    from .lunuff_character import LunuffModelGenerator
except ImportError:
    # Blender context may not be available
    pass

try:
    from .mcp_lunuff_integration import LunuffMCPTool
except ImportError:
    # Blender context may not be available
    pass

__all__ = [
    "LunuffModelGenerator",
    "LunuffMCPTool",
]
