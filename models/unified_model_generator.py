"""
Unified Model Generation System

Provides a single interface for generating 3D models using either:
- Lunuff Character Generator (for the Lunuff creature)
- Text-to-CAD Generator (for arbitrary descriptions)

Allows intelligent routing based on the user's request.
"""

import json
from typing import Optional, Dict
from pathlib import Path
import sys

# Add models directory to path for imports
models_dir = Path(__file__).parent
sys.path.insert(0, str(models_dir))


class UnifiedModelGenerator:
    """Unified interface for all model generation tools."""

    def __init__(self):
        """Initialize the unified generator."""
        self.lunuff_available = False
        self.text_to_cad_available = False

        # Try to import generators
        try:
            from lunuff_character import LunuffModelGenerator
            self.LunuffModelGenerator = LunuffModelGenerator
            self.lunuff_available = True
        except Exception as e:
            print(f"Warning: Lunuff generator not available: {e}")

        try:
            from text_to_cad_integration import TextToCADGenerator
            self.TextToCADGenerator = TextToCADGenerator
            self.text_to_cad_available = True
        except Exception as e:
            print(f"Warning: Text-to-CAD generator not available: {e}")

    def route_request(self, request: str) -> Dict:
        """Route a generation request to the appropriate generator.

        Args:
            request: User's natural language request

        Returns:
            dict: Router decision with tool selection and reasoning
        """
        lunuff_keywords = [
            "lunuff",
            "character",
            "creature",
            "cute",
            "floppy ears",
            "character model"
        ]

        request_lower = request.lower()
        is_lunuff_request = any(kw in request_lower for kw in lunuff_keywords)

        if is_lunuff_request and self.lunuff_available:
            return {
                "tool": "lunuff",
                "reasoning": "Request mentions Lunuff character",
                "available": True
            }
        elif self.text_to_cad_available:
            return {
                "tool": "text_to_cad",
                "reasoning": "Using text-to-CAD for custom description",
                "available": True
            }
        else:
            return {
                "tool": None,
                "reasoning": "No suitable generator available",
                "available": False,
                "error": "Please ensure Blender context is available"
            }

    def generate(self, request: str, output_dir: Optional[str] = None) -> Dict:
        """Generate a 3D model based on the request.

        Args:
            request: Description or request for model generation
            output_dir: Optional output directory for exports

        Returns:
            dict: Generation result with metadata
        """
        # Route the request
        routing = self.route_request(request)

        if not routing["available"]:
            return {
                "status": "error",
                "message": routing.get("error", "No generator available"),
                "routing": routing
            }

        # Generate using appropriate tool
        if routing["tool"] == "lunuff":
            return self._generate_lunuff(output_dir)
        elif routing["tool"] == "text_to_cad":
            return self._generate_text_to_cad(request, output_dir)
        else:
            return {
                "status": "error",
                "message": "Unable to determine appropriate generator"
            }

    def _generate_lunuff(self, output_dir: Optional[str]) -> Dict:
        """Generate using Lunuff generator."""
        try:
            if not self.lunuff_available:
                return {
                    "status": "error",
                    "message": "Lunuff generator not available in this context"
                }

            generator = self.LunuffModelGenerator(output_dir=output_dir)
            model = generator.generate()

            return {
                "status": "success",
                "tool": "lunuff",
                "model_name": model.name,
                "vertices": len(model.data.vertices),
                "faces": len(model.data.polygons),
                "type": "character",
                "components": 9,
                "print_ready": True
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "lunuff",
                "error": str(e)
            }

    def _generate_text_to_cad(self, description: str, output_dir: Optional[str]) -> Dict:
        """Generate using Text-to-CAD generator."""
        try:
            if not self.text_to_cad_available:
                return {
                    "status": "error",
                    "message": "Text-to-CAD generator not available in this context"
                }

            generator = self.TextToCADGenerator(output_dir=output_dir)
            model = generator.generate_from_description(description)
            export_path = generator.export_stl()

            return {
                "status": "success",
                "tool": "text_to_cad",
                "description": description,
                "model_name": model.name,
                "vertices": len(model.data.vertices),
                "faces": len(model.data.polygons),
                "export_path": export_path,
                "print_ready": True
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "text_to_cad",
                "error": str(e)
            }

    def get_available_tools(self) -> Dict:
        """Get list of available generation tools.

        Returns:
            dict: Available tools and their capabilities
        """
        tools = {}

        if self.lunuff_available:
            tools["lunuff"] = {
                "name": "Lunuff Character Generator",
                "type": "procedural character",
                "components": 9,
                "best_for": "Generating the Lunuff creature character",
                "export_formats": ["STL", "OBJ", "DAE"],
                "generation_time": "2-5 seconds",
                "print_ready": True
            }

        if self.text_to_cad_available:
            tools["text_to_cad"] = {
                "name": "Text-to-CAD Generator",
                "type": "descriptive geometry",
                "best_for": "Creating custom objects from text descriptions",
                "supports": ["basic shapes", "feature requests", "custom objects"],
                "export_formats": ["STL", "BLEND", "OBJ"],
                "generation_time": "1-3 seconds",
                "print_ready": True
            }

        return tools

    def suggest_workflow(self, request: str) -> Dict:
        """Suggest a workflow for the given request.

        Args:
            request: User's request

        Returns:
            dict: Suggested workflow steps
        """
        routing = self.route_request(request)

        if routing["tool"] == "lunuff":
            return {
                "workflow": "Generate Lunuff Character",
                "steps": [
                    "1. Use Lunuff generator to create base character",
                    "2. Customize if needed (scale, materials)",
                    "3. Export as STL for 3D printing",
                    "4. Or render in Blender for visualization"
                ],
                "estimated_time": "5-10 seconds",
                "output": "Complete 3D model of Lunuff creature"
            }

        elif routing["tool"] == "text_to_cad":
            return {
                "workflow": "Generate Custom Model from Description",
                "steps": [
                    "1. Parse description into shape parameters",
                    "2. Generate basic geometry",
                    "3. Apply requested features",
                    "4. Export as STL or Blender file"
                ],
                "estimated_time": "3-8 seconds",
                "output": "Custom 3D model based on description"
            }

        else:
            return {
                "workflow": "No suitable workflow",
                "reason": "No available generator matches the request",
                "suggestion": "Try requesting 'Lunuff' for character or describe your object"
            }

    def get_help(self) -> str:
        """Get help on using the unified generator.

        Returns:
            str: Help text with usage examples
        """
        help_text = """
UNIFIED MODEL GENERATOR - HELP

Available Generators:
"""
        for tool_name, tool_info in self.get_available_tools().items():
            help_text += f"\n  • {tool_info['name']} ({tool_name})"
            help_text += f"\n    Best for: {tool_info['best_for']}"

        help_text += """

EXAMPLES:

1. Generate Lunuff Character:
   "Generate a Lunuff character model"
   "Create a cute Lunuff with floppy ears"

2. Custom Object with Text-to-CAD:
   "Create a cube that's 10 units wide"
   "Generate a smooth sphere with rounded edges"
   "Make a cylindrical pipe with ridges"

3. Hybrid Workflow:
   "Create a Lunuff character wearing armor"
   → Generates Lunuff base
   → Generates armor with text-to-CAD
   → Combine in Blender

4. Batch Generation:
   Multiple requests → each routed to appropriate tool
   → All exported in one session

SUPPORTED EXPORTS:
  • STL (3D printing ready)
  • BLEND (Blender native)
  • OBJ (universal format)
  • DAE (game engines)

All models are generated as manifold-verified geometry
optimized for 3D printing.
"""
        return help_text


def main():
    """Main entry point."""
    gen = UnifiedModelGenerator()

    print("\n" + "="*60)
    print("UNIFIED MODEL GENERATOR")
    print("="*60)

    print("\nAvailable Tools:")
    for tool_name, info in gen.get_available_tools().items():
        print(f"\n  ✓ {info['name']}")
        print(f"    Type: {info.get('type', 'N/A')}")
        print(f"    Best for: {info.get('best_for', 'N/A')}")

    print("\n" + "="*60)
    print("For more help, see the documentation or use get_help()")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
