"""
MCP Integration for Lunuff Character Model

This module provides integration with the Blender MCP server, allowing
Claude to generate Lunuff character models through the MCP protocol.

Can be used as:
1. A standalone tool in the MCP server
2. A Blender addon command
3. A direct Python import
"""

import json
import bpy
from pathlib import Path


class LunuffMCPTool:
    """MCP tool wrapper for Lunuff character generation."""

    def __init__(self):
        """Initialize the MCP tool."""
        self.script_dir = Path(__file__).parent

    def generate_lunuff(self, options=None):
        """Generate a Lunuff character model.

        Args:
            options: Dictionary with optional parameters
                - output_dir: Custom output directory for STL export
                - auto_export: Whether to auto-export as STL (default: True)
                - scale: Scale multiplier for the model (default: 1.0)

        Returns:
            dict: Status and result information
        """
        try:
            # Import the generator
            import sys
            sys.path.insert(0, str(self.script_dir))
            from lunuff_character import LunuffModelGenerator

            options = options or {}
            output_dir = options.get('output_dir', str(self.script_dir))
            auto_export = options.get('auto_export', True)
            scale = options.get('scale', 1.0)

            # Generate model
            generator = LunuffModelGenerator(output_dir=output_dir)
            model = generator.generate()

            # Apply scale if different from 1.0
            if scale != 1.0:
                model.scale = (scale, scale, scale)
                bpy.ops.object.transform_apply(scale=True)

            return {
                "status": "success",
                "message": "Lunuff character model generated successfully",
                "model_name": model.name,
                "vertices": len(model.data.vertices),
                "faces": len(model.data.polygons),
                "edges": len(model.data.edges),
                "scale": scale
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate Lunuff model: {str(e)}",
                "error_type": type(e).__name__
            }

    def get_model_info(self):
        """Get information about the Lunuff model.

        Returns:
            dict: Model information
        """
        return {
            "name": "Lunuff Character Model",
            "version": "1.0.0",
            "description": "A complete 3D character model of the Lunuff creature",
            "components": [
                "Body (egg-shaped sphere)",
                "Head (rounded sphere)",
                "Ears (2, with floppy bend)",
                "Snout (small protrusion)",
                "Eyes (2, with irises)",
                "Tail (curved sphere)",
                "Paws (4, positioned naturally)",
                "Sigil Recess (chest placement)",
                "Print Base (for 3D printing)"
            ],
            "features": [
                "Smooth subdivision surfaces",
                "Manifold geometry verification",
                "STL export ready",
                "3D print optimized"
            ],
            "recommended_scale": "1.0",
            "recommended_height": "100mm",
            "print_time_estimate": "6 hours at 100mm",
            "infill_suggestion": "15-20%"
        }

    def list_variants(self):
        """List available Lunuff variants.

        Returns:
            dict: Available variants
        """
        return {
            "Common": {
                "description": "Standard Lunuff with chest sigil recess",
                "sigil_placement": "chest"
            },
            "Rare": {
                "description": "Variant with back sigil placement",
                "sigil_placement": "back"
            },
            "Legendary": {
                "description": "Enhanced model with additional features",
                "sigil_placement": "full_body"
            }
        }


def execute_in_blender(command, params=None):
    """Execute a Lunuff command in Blender.

    This function is meant to be called from the MCP server
    when it has an active Blender connection.

    Args:
        command: The command to execute
        params: Optional parameters dictionary

    Returns:
        dict: Command result
    """
    tool = LunuffMCPTool()

    if command == "generate":
        return tool.generate_lunuff(params)
    elif command == "info":
        return tool.get_model_info()
    elif command == "variants":
        return tool.list_variants()
    else:
        return {
            "status": "error",
            "message": f"Unknown command: {command}",
            "available_commands": ["generate", "info", "variants"]
        }


# MCP Tool Definition
LUNUFF_MCP_TOOL = {
    "name": "generate_lunuff_character",
    "description": "Generate a complete 3D Lunuff character model in Blender",
    "parameters": {
        "type": "object",
        "properties": {
            "output_dir": {
                "type": "string",
                "description": "Directory for STL export (optional)"
            },
            "auto_export": {
                "type": "boolean",
                "description": "Automatically export as STL (default: true)"
            },
            "scale": {
                "type": "number",
                "description": "Scale multiplier for the model (default: 1.0)"
            }
        }
    }
}


# Alternative: MCP Resource Definition (for discovery)
LUNUFF_MCP_RESOURCE = {
    "type": "resource",
    "name": "lunuff_models",
    "description": "Lunuff character model generation and management",
    "uri": "lunuff://models",
    "mimeType": "application/json"
}


def get_mcp_tools():
    """Return the list of MCP tools provided by this module."""
    return [LUNUFF_MCP_TOOL]


def get_mcp_resources():
    """Return the list of MCP resources provided by this module."""
    return [LUNUFF_MCP_RESOURCE]


if __name__ == "__main__":
    # Test when run directly
    print("Lunuff MCP Integration Module")
    print("=" * 60)

    tool = LunuffMCPTool()

    print("\n1. Model Information:")
    info = tool.get_model_info()
    print(json.dumps(info, indent=2))

    print("\n2. Available Variants:")
    variants = tool.list_variants()
    print(json.dumps(variants, indent=2))

    print("\n3. To generate model in Blender:")
    print("   - Run this module in Blender's Python console")
    print("   - Or call: execute_in_blender('generate')")
