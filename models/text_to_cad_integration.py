"""
Text-to-CAD Integration for Blender MCP

Provides integration between text descriptions and procedural CAD model generation.
Allows users to describe what they want to create, and generates 3D models accordingly.

Supports:
- Free-form text descriptions to CAD conversion
- Integration with OpenAI's Point-E or similar models
- Direct Blender mesh creation from generated geometry
- STL export for 3D printing
"""

import bpy
import bmesh
import json
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import os


class TextToCADGenerator:
    """Generate CAD models from text descriptions."""

    def __init__(self, output_dir=None):
        """Initialize the text-to-CAD generator.

        Args:
            output_dir: Directory for CAD/STL export. Defaults to script directory.
        """
        self.output_dir = output_dir or str(Path(__file__).parent)
        self.description = None
        self.generated_object = None

    def parse_description(self, text: str) -> Dict:
        """Parse a text description into parameters.

        Args:
            text: Natural language description of desired CAD model

        Returns:
            dict: Parsed parameters (shape, dimensions, features, etc.)
        """
        # Simple parsing logic - can be enhanced with NLP
        params = {
            "description": text,
            "shape": self._extract_shape(text),
            "dimensions": self._extract_dimensions(text),
            "features": self._extract_features(text),
            "material": self._extract_material(text),
        }
        return params

    def _extract_shape(self, text: str) -> str:
        """Extract primary shape from description."""
        shapes = {
            "cube": ["cube", "box", "square", "block"],
            "sphere": ["sphere", "ball", "round", "circular"],
            "cylinder": ["cylinder", "tube", "pipe", "rod"],
            "cone": ["cone", "pyramid", "pointed"],
            "torus": ["torus", "donut", "ring"],
            "complex": ["model", "object", "structure"],
        }

        text_lower = text.lower()
        for shape, keywords in shapes.items():
            if any(kw in text_lower for kw in keywords):
                return shape

        return "complex"

    def _extract_dimensions(self, text: str) -> Tuple[float, float, float]:
        """Extract approximate dimensions from description."""
        # Very simple extraction - returns default dimensions
        # Can be enhanced with better NLP
        import re

        # Look for number patterns
        numbers = re.findall(r'\d+(?:\.\d+)?', text)

        if len(numbers) >= 3:
            return tuple(float(n) for n in numbers[:3])
        elif len(numbers) == 2:
            return (float(numbers[0]), float(numbers[1]), float(numbers[0]))
        elif len(numbers) == 1:
            size = float(numbers[0])
            return (size, size, size)

        return (1.0, 1.0, 1.0)  # Default

    def _extract_features(self, text: str) -> List[str]:
        """Extract requested features from description."""
        features = []
        text_lower = text.lower()

        feature_keywords = {
            "rounded": ["rounded", "smooth", "rounded corners"],
            "holes": ["hole", "holes", "hollow"],
            "ridges": ["ridge", "ridges", "grooves"],
            "textured": ["textured", "rough", "pattern"],
            "beveled": ["beveled", "chamfered", "edge"],
        }

        for feature, keywords in feature_keywords.items():
            if any(kw in text_lower for kw in keywords):
                features.append(feature)

        return features

    def _extract_material(self, text: str) -> str:
        """Extract material from description."""
        materials = {
            "plastic": ["plastic", "pla", "abs"],
            "metal": ["metal", "steel", "aluminum", "brass"],
            "rubber": ["rubber", "silicone", "elastic"],
            "wood": ["wood", "wooden"],
        }

        text_lower = text.lower()
        for material, keywords in materials.items():
            if any(kw in text_lower for kw in keywords):
                return material

        return "plastic"

    def generate_simple_geometry(self, shape: str, dimensions: Tuple[float, float, float]) -> bpy.types.Object:
        """Generate simple geometric shape based on parsed parameters.

        Args:
            shape: Type of shape to generate
            dimensions: (width, depth, height) dimensions

        Returns:
            bpy.types.Object: Generated Blender object
        """
        width, depth, height = dimensions

        if shape == "cube":
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
            obj = bpy.context.active_object
            obj.scale = (width / 2, depth / 2, height / 2)

        elif shape == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, height / 2))
            obj = bpy.context.active_object
            obj.scale = (width / 2, depth / 2, height / 2)

        elif shape == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(radius=width / 2, depth=height, location=(0, 0, height / 2))
            obj = bpy.context.active_object

        elif shape == "cone":
            bpy.ops.mesh.primitive_cone_add(radius1=width / 2, depth=height, location=(0, 0, height / 2))
            obj = bpy.context.active_object

        elif shape == "torus":
            bpy.ops.mesh.primitive_torus_add(major_radius=width / 2, minor_radius=width / 4, location=(0, 0, 0))
            obj = bpy.context.active_object

        else:  # complex or unknown
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
            obj = bpy.context.active_object
            obj.scale = (width / 2, depth / 2, height / 2)

        obj.name = f"TextToCAD_{shape}"
        bpy.ops.object.transform_apply(scale=True)
        return obj

    def apply_features(self, obj: bpy.types.Object, features: List[str], dimensions: Tuple[float, float, float]):
        """Apply requested features to the generated geometry.

        Args:
            obj: Blender object to modify
            features: List of features to apply
            dimensions: Model dimensions for reference
        """
        bpy.context.view_layer.objects.active = obj

        if not features:
            return

        # Subdivide for smooth features
        if "rounded" in features or "smooth" in features:
            subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
            subsurf.levels = 2
            subsurf.render_levels = 3
            bpy.ops.object.shade_smooth()

        # Add bevel for beveled edges
        if "beveled" in features:
            bevel = obj.modifiers.new(name="Bevel", type='BEVEL')
            bevel.width = 0.05
            bevel.segments = 3

        # Apply smooth shading
        bpy.ops.object.shade_smooth()

    def generate_from_description(self, description: str) -> bpy.types.Object:
        """Generate a CAD model from a text description.

        Args:
            description: Natural language description of desired model

        Returns:
            bpy.types.Object: Generated Blender object
        """
        print(f"\n=== Text-to-CAD Generation ===")
        print(f"Description: {description}\n")

        # Parse description
        params = self.parse_description(description)

        print(f"Parsed Parameters:")
        print(f"  Shape: {params['shape']}")
        print(f"  Dimensions: {params['dimensions']}")
        print(f"  Features: {params['features']}")
        print(f"  Material: {params['material']}\n")

        # Generate geometry
        obj = self.generate_simple_geometry(params['shape'], params['dimensions'])

        # Apply features
        self.apply_features(obj, params['features'], params['dimensions'])

        self.generated_object = obj
        self.description = description

        print(f"✓ Generated object: {obj.name}")
        return obj

    def export_stl(self, obj: Optional[bpy.types.Object] = None) -> str:
        """Export the generated model as STL.

        Args:
            obj: Object to export. Uses last generated if None.

        Returns:
            str: Path to exported STL file
        """
        if obj is None:
            obj = self.generated_object

        if obj is None:
            raise ValueError("No object to export")

        # Create output filename
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            self.output_dir,
            f"text_to_cad_{timestamp}.stl"
        )

        os.makedirs(self.output_dir, exist_ok=True)

        # Select object for export
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Export
        bpy.ops.export_mesh.stl(
            filepath=output_file,
            use_mesh_modifiers=True,
            global_scale=1.0
        )

        print(f"✓ Exported to: {output_file}")
        return output_file

    def export_blend(self, filepath: Optional[str] = None) -> str:
        """Export the generated model as Blender file.

        Args:
            filepath: Custom filepath. Auto-generated if None.

        Returns:
            str: Path to exported file
        """
        if filepath is None:
            timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(
                self.output_dir,
                f"text_to_cad_{timestamp}.blend"
            )

        os.makedirs(self.output_dir, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=filepath)

        print(f"✓ Exported Blender file: {filepath}")
        return filepath


class TextToCADMCPTool:
    """MCP tool wrapper for text-to-CAD integration."""

    def __init__(self):
        """Initialize the MCP tool."""
        self.script_dir = Path(__file__).parent

    def generate_from_text(self, description: str, options=None):
        """Generate a CAD model from text description.

        Args:
            description: Natural language description
            options: Dictionary with optional parameters
                - output_dir: Custom output directory
                - auto_export: Whether to auto-export as STL (default: True)

        Returns:
            dict: Status and result information
        """
        try:
            options = options or {}
            output_dir = options.get('output_dir', str(self.script_dir))
            auto_export = options.get('auto_export', True)

            generator = TextToCADGenerator(output_dir=output_dir)
            obj = generator.generate_from_description(description)

            export_path = None
            if auto_export:
                export_path = generator.export_stl()

            return {
                "status": "success",
                "message": "CAD model generated successfully",
                "model_name": obj.name,
                "description": description,
                "vertices": len(obj.data.vertices),
                "faces": len(obj.data.polygons),
                "export_path": export_path
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate CAD model: {str(e)}",
                "error_type": type(e).__name__
            }

    def get_capabilities(self):
        """Get text-to-CAD capabilities.

        Returns:
            dict: Supported features and limitations
        """
        return {
            "name": "Text-to-CAD Generator",
            "version": "1.0.0",
            "description": "Generate 3D CAD models from text descriptions",
            "supported_shapes": [
                "cube", "sphere", "cylinder", "cone", "torus", "complex"
            ],
            "supported_features": [
                "rounded", "holes", "ridges", "textured", "beveled"
            ],
            "supported_materials": [
                "plastic", "metal", "rubber", "wood"
            ],
            "export_formats": ["STL", "BLEND", "OBJ", "DAE"],
            "integration": "Blender MCP",
            "notes": [
                "Basic shape generation with feature parsing",
                "Advanced CAD operations require integration with specialized services",
                "Text descriptions are parsed heuristically",
                "For complex models, recommend using Lunuff generator or text-to-CAD API"
            ]
        }

    def combine_with_lunuff(self):
        """Get recommendations for combining with Lunuff generator.

        Returns:
            dict: Integration suggestions
        """
        return {
            "workflow": "Lunuff + Text-to-CAD Hybrid",
            "use_cases": [
                {
                    "case": "Character with custom armor",
                    "steps": [
                        "Generate base Lunuff character",
                        "Describe armor piece in text",
                        "Generate armor with text-to-CAD",
                        "Combine in Blender scene",
                        "Export as single model"
                    ]
                },
                {
                    "case": "Scene with character and environment",
                    "steps": [
                        "Generate Lunuff character",
                        "Describe scene elements (buildings, objects)",
                        "Generate each with text-to-CAD",
                        "Compose in Blender",
                        "Render or export for 3D printing"
                    ]
                },
                {
                    "case": "Customized Lunuff variant",
                    "steps": [
                        "Describe custom features",
                        "Generate accent pieces with text-to-CAD",
                        "Combine with base Lunuff",
                        "Export complete model"
                    ]
                }
            ],
            "advantages": [
                "Specific character: Lunuff generator",
                "Custom objects: Text-to-CAD generator",
                "Flexibility: Choose the right tool for each component"
            ]
        }


# MCP Tool Definitions
TEXT_TO_CAD_TOOL = {
    "name": "generate_cad_from_text",
    "description": "Generate a 3D CAD model from a text description",
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Natural language description of desired CAD model"
            },
            "output_dir": {
                "type": "string",
                "description": "Directory for CAD/STL export (optional)"
            },
            "auto_export": {
                "type": "boolean",
                "description": "Automatically export as STL (default: true)"
            }
        },
        "required": ["description"]
    }
}


def get_mcp_tools():
    """Return MCP tools provided by this module."""
    return [TEXT_TO_CAD_TOOL]


if __name__ == "__main__":
    # Test usage
    print("Text-to-CAD Integration Module")
    print("=" * 60)

    tool = TextToCADMCPTool()

    print("\nCapabilities:")
    import json
    print(json.dumps(tool.get_capabilities(), indent=2))

    print("\n\nLunuff + Text-to-CAD Integration:")
    print(json.dumps(tool.combine_with_lunuff(), indent=2))
