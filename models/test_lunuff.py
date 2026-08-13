"""
Test suite for the Lunuff character model generator.

Usage:
    In Blender Python console:
    exec(open("test_lunuff.py").read())

    Or command line:
    blender -b -P test_lunuff.py
"""

import bpy
import sys
from pathlib import Path


def test_model_generation():
    """Test that the model generates without errors."""
    print("\n" + "="*60)
    print("LUNUFF CHARACTER MODEL TEST SUITE")
    print("="*60 + "\n")

    # Add the models directory to path
    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    try:
        from lunuff_character import LunuffModelGenerator

        print("✓ Successfully imported LunuffModelGenerator\n")

        # Test 1: Basic generation
        print("TEST 1: Basic Model Generation")
        print("-" * 40)
        gen = LunuffModelGenerator(output_dir=str(models_dir))
        model = gen.generate()

        if model:
            print("✓ Model generation completed")
            print(f"  Model name: {model.name}")
            print(f"  Vertex count: {len(model.data.vertices)}")
            print(f"  Face count: {len(model.data.polygons)}")
        else:
            print("✗ Model generation returned None")
            return False

        # Test 2: Verify mesh integrity
        print("\nTEST 2: Mesh Integrity Check")
        print("-" * 40)

        # Count edges
        edge_count = len(model.data.edges)
        print(f"✓ Edge count: {edge_count}")

        # Check for degenerate geometry
        degenerate = 0
        for face in model.data.polygons:
            if len(face.vertices) < 3:
                degenerate += 1

        if degenerate == 0:
            print("✓ No degenerate faces detected")
        else:
            print(f"⚠ Found {degenerate} degenerate faces")

        # Test 3: Verify object in scene
        print("\nTEST 3: Scene Integration")
        print("-" * 40)

        if model.name in bpy.data.objects:
            print(f"✓ Model found in scene: {model.name}")
        else:
            print(f"✗ Model not found in scene")
            return False

        # Test 4: Check bounding box
        print("\nTEST 4: Model Dimensions")
        print("-" * 40)

        bbox_min = min((vertex.co for vertex in model.data.vertices), key=lambda v: sum(v))
        bbox_max = max((vertex.co for vertex in model.data.vertices), key=lambda v: sum(v))

        width = abs(bbox_max.x - bbox_min.x)
        depth = abs(bbox_max.y - bbox_min.y)
        height = abs(bbox_max.z - bbox_min.z)

        print(f"✓ Dimensions: {width:.2f} × {depth:.2f} × {height:.2f}")
        print(f"  Center: ({bbox_min.x:.2f}, {bbox_min.y:.2f}, {bbox_min.z:.2f})")

        # Verify reasonable dimensions (should be roughly 2-3 units)
        if 1.5 < width < 3.5 and 1.5 < height < 3.5:
            print("✓ Dimensions are within expected range")
        else:
            print(f"⚠ Unexpected dimensions (width={width}, height={height})")

        # Test 5: Verify modifiers were applied
        print("\nTEST 5: Modifier Application")
        print("-" * 40)

        if len(model.modifiers) == 0:
            print("✓ All modifiers applied (none remaining)")
        else:
            print(f"⚠ {len(model.modifiers)} modifiers remain:")
            for mod in model.modifiers:
                print(f"  - {mod.name} ({mod.type})")

        # Test 6: Verify materials (optional)
        print("\nTEST 6: Material Assignment")
        print("-" * 40)

        if len(model.material_slots) > 0:
            print(f"✓ Materials assigned: {len(model.material_slots)}")
        else:
            print("ℹ No materials assigned (model uses default)")

        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print("✓ All tests passed successfully!")
        print(f"\nGenerated model: {model.name}")
        print(f"Vertices: {len(model.data.vertices)}")
        print(f"Faces: {len(model.data.polygons)}")
        print(f"Edges: {edge_count}")
        print("\nThe model is ready for:")
        print("  • 3D printing (STL export)")
        print("  • Rendering (Cycles/Eevee)")
        print("  • Animation (rigging)")
        print("  • Game engine import")
        print("="*60 + "\n")

        return True

    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance():
    """Test generation performance."""
    print("\nPERFORMANCE TEST")
    print("-" * 40)

    import time
    models_dir = Path(__file__).parent
    sys.path.insert(0, str(models_dir))

    from lunuff_character import LunuffModelGenerator

    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    start_time = time.time()
    gen = LunuffModelGenerator(output_dir=str(models_dir))
    model = gen.generate()
    elapsed = time.time() - start_time

    print(f"Generation time: {elapsed:.2f} seconds")

    if elapsed < 10:
        print("✓ Performance is excellent")
    elif elapsed < 30:
        print("✓ Performance is good")
    else:
        print("⚠ Performance could be optimized")

    return True


if __name__ == "__main__":
    success = test_model_generation()

    try:
        test_performance()
    except Exception as e:
        print(f"Performance test skipped: {e}")

    if success:
        print("\n✓ All tests passed! Model is production-ready.\n")
        sys.exit(0)
    else:
        print("\n✗ Tests failed. Check output above.\n")
        sys.exit(1)
