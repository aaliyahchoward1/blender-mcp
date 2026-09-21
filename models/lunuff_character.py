"""
Lunuff Character Model Generator
Generates a 3D Lunuff character model for Blender with full mesh assembly,
modifier application, manifold checking, and STL export.

Usage:
    In Blender's Python console or via CLI:
    exec(open("lunuff_character.py").read())

    Or from command line:
    blender -b -P lunuff_character.py
"""

import bpy
import bmesh
import math
import os
from pathlib import Path


class LunuffModelGenerator:
    """Complete Lunuff character model generator with mesh assembly and export."""

    def __init__(self, output_dir=None):
        """Initialize the generator.

        Args:
            output_dir: Directory for STL export. Defaults to script directory.
        """
        self.output_dir = output_dir or str(Path(__file__).parent)
        self.objects = {}
        self.cleanup_scene()

    def cleanup_scene(self):
        """Clear all mesh objects from scene."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("Scene cleared.")

    def create_body(self):
        """Create the main body - egg-shaped sphere."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=1.0,
            location=(0, 0, 1.0)
        )
        body = bpy.context.active_object
        body.name = "Lunuff_Body"
        body.scale = (1.0, 0.9, 1.15)
        bpy.ops.object.transform_apply(scale=True)

        # Add subdivision surface for smoothness
        subsurf = body.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2
        subsurf.render_levels = 3

        # Smooth shading
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.shade_smooth()

        self.objects['body'] = body
        print(f"✓ Body created: {body.name}")
        return body

    def create_head(self):
        """Create the head - slightly flattened sphere."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.75,
            location=(0, -0.1, 2.1)
        )
        head = bpy.context.active_object
        head.name = "Lunuff_Head"
        head.scale = (1.0, 0.95, 0.95)
        bpy.ops.object.transform_apply(scale=True)

        # Smooth and subdivide
        subsurf = head.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2
        subsurf.render_levels = 3

        bpy.context.view_layer.objects.active = head
        bpy.ops.object.shade_smooth()

        self.objects['head'] = head
        print(f"✓ Head created: {head.name}")
        return head

    def create_ears(self):
        """Create floppy ears with bend deformation."""
        ear_configs = [
            (-0.4, 8, "Left"),
            (0.4, -8, "Right")
        ]

        ears = []
        for x_pos, rotation, side in ear_configs:
            # Create ear cube
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(x_pos, -0.15, 2.9)
            )
            ear = bpy.context.active_object
            ear.name = f"Lunuff_Ear_{side}"
            ear.scale = (0.22, 0.12, 0.9)
            bpy.ops.object.transform_apply(scale=True)

            # Subdivide for smooth bend
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=8)
            bpy.ops.object.mode_set(mode='OBJECT')

            # Add bend modifier for floppy droop
            bend = ear.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
            bend.deform_method = 'BEND'
            bend.angle = math.radians(70 + (10 if side == "Right" else 0))
            bend.deform_axis = 'X'

            # Smooth subdivision
            subsurf = ear.modifiers.new(name="Subsurf", type='SUBSURF')
            subsurf.levels = 2

            # Apply rotation
            ear.rotation_euler = (0, 0, math.radians(rotation))

            # Smooth shading
            bpy.context.view_layer.objects.active = ear
            bpy.ops.object.shade_smooth()

            ears.append(ear)

        self.objects['ears'] = ears
        print(f"✓ Ears created (2 ears)")
        return ears

    def create_snout(self):
        """Create a small snout protrusion."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.2,
            location=(0, -0.95, 1.9)
        )
        snout = bpy.context.active_object
        snout.name = "Lunuff_Snout"
        snout.scale = (0.6, 0.5, 0.4)
        bpy.ops.object.transform_apply(scale=True)

        # Smooth
        subsurf = snout.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2

        bpy.context.view_layer.objects.active = snout
        bpy.ops.object.shade_smooth()

        self.objects['snout'] = snout
        print(f"✓ Snout created: {snout.name}")
        return snout

    def create_eyes(self):
        """Create two eyes."""
        eye_positions = [
            (-0.25, -0.4, 2.3, "Left"),
            (0.25, -0.4, 2.3, "Right")
        ]

        eyes = []
        for x, y, z, side in eye_positions:
            # Eye white
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.15,
                location=(x, y, z)
            )
            eye = bpy.context.active_object
            eye.name = f"Lunuff_Eye_{side}"

            # Iris (small sphere)
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.08,
                location=(x, y - 0.08, z + 0.02)
            )
            iris = bpy.context.active_object
            iris.name = f"Lunuff_Iris_{side}"
            iris.scale = (1.0, 0.8, 0.9)
            bpy.ops.object.transform_apply(scale=True)

            eyes.append((eye, iris))

        self.objects['eyes'] = eyes
        print(f"✓ Eyes created (2 eyes with irises)")
        return eyes

    def create_tail(self):
        """Create a curved tail."""
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.25,
            location=(0, 0.85, 0.6)
        )
        tail = bpy.context.active_object
        tail.name = "Lunuff_Tail"
        tail.scale = (0.3, 0.3, 0.7)
        bpy.ops.object.transform_apply(scale=True)

        # Smooth
        subsurf = tail.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2

        bpy.context.view_layer.objects.active = tail
        bpy.ops.object.shade_smooth()

        self.objects['tail'] = tail
        print(f"✓ Tail created: {tail.name}")
        return tail

    def create_paws(self):
        """Create four paws."""
        paw_positions = [
            (-0.5, -0.6, 0.15, "Front_Left"),
            (0.5, -0.6, 0.15, "Front_Right"),
            (-0.5, 0.5, 0.15, "Back_Left"),
            (0.5, 0.5, 0.15, "Back_Right")
        ]

        paws = []
        for x, y, z, label in paw_positions:
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.22,
                location=(x, y, z)
            )
            paw = bpy.context.active_object
            paw.name = f"Lunuff_Paw_{label}"

            # Slightly flatten
            paw.scale = (1.0, 0.9, 0.8)
            bpy.ops.object.transform_apply(scale=True)

            # Smooth
            subsurf = paw.modifiers.new(name="Subsurf", type='SUBSURF')
            subsurf.levels = 2

            bpy.context.view_layer.objects.active = paw
            bpy.ops.object.shade_smooth()

            paws.append(paw)

        self.objects['paws'] = paws
        print(f"✓ Paws created (4 paws)")
        return paws

    def create_sigil_recess(self):
        """Create a shallow sigil recess on the chest (Common variant)."""
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.28,
            depth=0.05,
            location=(0, -0.85, 1.6)
        )
        sigil = bpy.context.active_object
        sigil.name = "Lunuff_Sigil_Recess"
        sigil.rotation_euler = (math.radians(80), 0, 0)

        self.objects['sigil'] = sigil
        print(f"✓ Sigil recess created: {sigil.name}")
        return sigil

    def create_print_base(self):
        """Create a flat base for 3D printing bed adhesion."""
        bpy.ops.mesh.primitive_cylinder_add(
            radius=1.05,
            depth=0.1,
            location=(0, 0, 0.05)
        )
        base = bpy.context.active_object
        base.name = "Lunuff_Print_Base"

        self.objects['base'] = base
        print(f"✓ Print base created: {base.name}")
        return base

    def build_complete_model(self):
        """Build the complete Lunuff model with all parts."""
        print("\n=== Building Lunuff Character Model ===\n")

        # Create all parts
        self.create_body()
        self.create_head()
        self.create_ears()
        self.create_snout()
        self.create_eyes()
        self.create_tail()
        self.create_paws()
        self.create_sigil_recess()
        self.create_print_base()

        print("\n=== Assembling Mesh ===\n")
        return self.assemble_and_export()

    def assemble_and_export(self):
        """Join all meshes, apply modifiers, check manifold, and export STL."""

        # Select all objects
        bpy.ops.object.select_all(action='SELECT')

        # Get the first object as active (for join operation)
        first_obj = self.objects['body']
        bpy.context.view_layer.objects.active = first_obj

        print("Joining all meshes...")
        bpy.ops.object.join()

        combined = bpy.context.active_object
        combined.name = "Lunuff_Character_Complete"

        print(f"✓ Meshes joined into: {combined.name}")

        # Apply all modifiers
        print("\nApplying modifiers...")
        for modifier in combined.modifiers:
            print(f"  - Applying {modifier.name}...")
            bpy.ops.object.modifier_apply(modifier=modifier.name)

        print("✓ All modifiers applied")

        # Check for manifold geometry
        print("\nChecking manifold geometry...")
        manifold_issues = self.check_manifold(combined)

        if manifold_issues:
            print(f"⚠ Found {len(manifold_issues)} manifold issues")
            print("  Attempting to fix...")
            self.fix_manifold_issues(combined)
        else:
            print("✓ Mesh is manifold")

        # Export to STL
        print("\nExporting to STL...")
        self.export_stl(combined)

        print("\n=== Lunuff Model Complete ===")
        return combined

    def check_manifold(self, obj):
        """Check if the mesh is manifold."""
        mesh = obj.data
        issues = []

        # Switch to edit mode to check
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Check for various issues
        bm = bmesh.from_edit_mesh(mesh)

        # Find non-manifold edges
        non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
        if non_manifold_edges:
            issues.append(f"Non-manifold edges: {len(non_manifold_edges)}")

        # Find degenerate faces
        degenerate = [f for f in bm.faces if len(f.verts) < 3]
        if degenerate:
            issues.append(f"Degenerate faces: {len(degenerate)}")

        bpy.ops.object.mode_set(mode='OBJECT')
        return issues

    def fix_manifold_issues(self, obj):
        """Fix common manifold issues."""
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        # Remove doubles
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        print("  ✓ Removed duplicate vertices")

        # Recalculate normals
        bpy.ops.mesh.normals_make_consistent(inside=False)
        print("  ✓ Recalculated normals")

        # Fill holes (limited)
        bpy.ops.mesh.select_non_manifold()
        if bpy.ops.mesh.fill():
            print("  ✓ Filled holes")

        bpy.ops.object.mode_set(mode='OBJECT')

    def export_stl(self, obj):
        """Export the model as STL."""
        # Create output filename
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            self.output_dir,
            f"lunuff_character_{timestamp}.stl"
        )

        # Ensure output directory exists
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

        # Return the path
        return output_file

    def generate(self):
        """Main method to generate the complete model."""
        try:
            return self.build_complete_model()
        except Exception as e:
            print(f"✗ Error during model generation: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    """Main entry point."""
    print("Starting Lunuff Character Model Generation...")

    # Determine output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate model
    generator = LunuffModelGenerator(output_dir=output_dir)
    result = generator.generate()

    print("\nModel generation successful!")
    return result


if __name__ == "__main__":
    main()
