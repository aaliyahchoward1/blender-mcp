"""
Example usage patterns for the Lunuff character model generator.

These examples demonstrate different ways to use the Lunuff model
generation system in various contexts.
"""

# Example 1: Basic Generation (Blender Console)
# ===============================================
"""
# In Blender's Python console, simply run:
exec(open("lunuff_character.py").read())

# This will:
# 1. Generate the complete 3D model
# 2. Assemble all meshes
# 3. Apply modifiers
# 4. Export as STL to the same directory
"""


# Example 2: Programmatic Generation with Python
# ================================================
def example_programmatic_generation():
    """Generate Lunuff programmatically with custom settings."""
    import sys
    from pathlib import Path

    # Add models directory to path
    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    # Create generator with custom output directory
    custom_output = "/path/to/output/models"
    generator = LunuffModelGenerator(output_dir=custom_output)

    # Generate the model
    model = generator.generate()

    print(f"Generated model: {model.name}")
    print(f"Vertices: {len(model.data.vertices)}")
    print(f"Faces: {len(model.data.polygons)}")

    return model


# Example 3: Batch Generation
# ============================
def example_batch_generation(num_models=3):
    """Generate multiple Lunuff models."""
    import sys
    from pathlib import Path

    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    models = []
    for i in range(num_models):
        print(f"\nGenerating Lunuff {i+1}/{num_models}...")

        generator = LunuffModelGenerator()
        model = generator.generate()
        models.append(model)

        print(f"✓ Generated {model.name}")

    return models


# Example 4: With Scale Variations
# =================================
def example_scaled_models():
    """Generate Lunuff models at different scales."""
    import bpy
    import sys
    from pathlib import Path

    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    scales = [0.5, 1.0, 2.0]  # Small, medium, large
    models = {}

    for scale in scales:
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Generate model
        generator = LunuffModelGenerator()
        model = generator.generate()

        # Apply scale
        model.scale = (scale, scale, scale)
        bpy.ops.object.transform_apply(scale=True)

        models[f"scale_{scale}"] = model
        print(f"✓ Generated Lunuff at scale {scale}x")

    return models


# Example 5: Using MCP Integration
# ==================================
def example_mcp_usage():
    """Generate Lunuff using MCP integration."""
    import sys
    from pathlib import Path

    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from mcp_lunuff_integration import LunuffMCPTool

    tool = LunuffMCPTool()

    # Get model information
    print("Lunuff Model Information:")
    info = tool.get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    # Generate model with options
    options = {
        'auto_export': True,
        'scale': 1.5
    }

    result = tool.generate_lunuff(options)
    print(f"\nGeneration Result: {result}")

    return result


# Example 6: Command Line Execution
# ==================================
"""
# Generate from command line:
blender -b -P lunuff_character.py

# This will:
# 1. Run Blender in background mode (no GUI)
# 2. Execute the script
# 3. Export STL
# 4. Exit automatically

# With custom output directory:
cd /path/to/output && blender -b -P /path/to/lunuff_character.py
"""


# Example 7: Integration with Rendering
# =======================================
def example_with_rendering():
    """Generate Lunuff and set up for rendering."""
    import bpy
    import sys
    from pathlib import Path

    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    # Generate model
    generator = LunuffModelGenerator()
    model = generator.generate()

    # Add lighting
    bpy.ops.object.light_add(
        type='SUN',
        location=(5, 5, 10)
    )

    # Add camera
    bpy.ops.object.camera_add(
        location=(0, -5, 2)
    )
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera

    # Set up rendering
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128

    print("✓ Model set up for rendering")
    print(f"✓ Camera positioned at {camera.location}")

    return model


# Example 8: Export Variations
# =============================
def example_export_formats():
    """Generate Lunuff and export in multiple formats."""
    import bpy
    import sys
    from pathlib import Path

    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    # Generate model
    generator = LunuffModelGenerator()
    model = generator.generate()

    # Export as STL (already done in generate)
    print(f"✓ Exported as STL")

    # Export as OBJ
    bpy.ops.object.select_all(action='DESELECT')
    model.select_set(True)
    bpy.context.view_layer.objects.active = model

    obj_path = str(models_dir / "lunuff_character.obj")
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True
    )
    print(f"✓ Exported as OBJ: {obj_path}")

    # Export as Collada (DAE)
    dae_path = str(models_dir / "lunuff_character.dae")
    bpy.ops.wm.collada_export(
        filepath=dae_path,
        selected=True
    )
    print(f"✓ Exported as Collada: {dae_path}")

    return model


# Example 9: Process Flow Diagram
# ================================
"""
Lunuff Generation Process Flow:

1. Scene Initialization
   ↓
2. Component Creation (in parallel concept)
   ├─ Body
   ├─ Head
   ├─ Ears
   ├─ Snout
   ├─ Eyes
   ├─ Tail
   ├─ Paws
   ├─ Sigil Recess
   └─ Print Base
   ↓
3. Modifier Application
   ├─ Subdivision Surface (Smooth)
   ├─ Shade Smooth
   └─ Bend (Ears only)
   ↓
4. Mesh Assembly
   ├─ Join All Objects
   ├─ Apply Modifiers
   └─ Clean Geometry
   ↓
5. Manifold Verification
   ├─ Check Non-manifold Edges
   ├─ Check Degenerate Faces
   └─ Auto-repair if needed
   ↓
6. Export
   └─ STL with Timestamp
"""


# Example 10: Testing and Validation
# ====================================
"""
Run the test suite:
blender -b -P test_lunuff.py

This will:
1. Generate the model
2. Verify mesh integrity
3. Check scene integration
4. Validate dimensions
5. Test modifier application
6. Measure performance
7. Report all results
"""


def run_all_examples():
    """Run (conceptually) all examples."""
    print("="*60)
    print("LUNUFF CHARACTER MODEL - USAGE EXAMPLES")
    print("="*60)

    examples = [
        ("Basic Generation", lambda: None),  # Already shown in console
        ("Programmatic Generation", example_programmatic_generation),
        ("Batch Generation", lambda: example_batch_generation(2)),
        ("Scaled Models", example_scaled_models),
        ("MCP Integration", example_mcp_usage),
        ("With Rendering", example_with_rendering),
        ("Export Formats", example_export_formats),
    ]

    for name, func in examples:
        print(f"\n{name}:")
        print("-" * 40)
        if callable(func) and func != (lambda: None):
            try:
                result = func()
                print(f"✓ {name} completed successfully")
            except Exception as e:
                print(f"⚠ {name} skipped (requires Blender context)")


if __name__ == "__main__":
    run_all_examples()
    print("\nFor more examples, see this file's docstrings.")
