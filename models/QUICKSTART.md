# Lunuff Character Model - Quick Start Guide

## 30-Second Setup

### Option 1: Direct Blender Execution (Easiest)

1. **Open Blender**
2. **Switch to Scripting workspace**
3. **Open** `lunuff_character.py`
4. **Click Run** (or press Alt+P)
5. **Model appears in viewport + STL exports automatically** ✓

### Option 2: Command Line

```bash
cd /path/to/blender-mcp/models
blender -b -P lunuff_character.py
```

The model will generate and export as STL automatically.

### Option 3: Python Console

In Blender's Python console, paste:

```python
exec(open("/path/to/models/lunuff_character.py").read())
```

Press Enter. Done!

---

## What You Get

✓ Complete 3D model in Blender viewport  
✓ STL file ready for 3D printing  
✓ Smooth, manifold geometry  
✓ Properly applied modifiers  
✓ All in ~5 seconds

---

## File Outputs

After running the script:

```
models/
└── lunuff_character_20260813_142530.stl
```

The timestamp filename ensures you don't overwrite previous exports.

---

## Next Steps

### To Render
1. Add lighting and camera (optional)
2. Set render engine (Cycles or Eevee)
3. Press F12 to render

### To Modify
- Edit component scales in `LunuffModelGenerator.create_*()` methods
- Adjust modifier levels for more/less smoothness
- Change colors by adding materials

### To 3D Print
1. Download the STL file
2. Open in Cura, PrusaSlicer, or similar
3. Recommended print: 100mm height
4. Estimated time: ~6 hours at 0.2mm layer height

### To Combine with Other Models
1. Generate Lunuff (creates STL)
2. Open in Blender again
3. Import via File → Import
4. Arrange with other models
5. Export combined STL

---

## Model Scale Reference

| Use Case | Height | Notes |
|----------|--------|-------|
| Keychain | 25mm | Quick print, ~30 min |
| Figurine | 75mm | Good detail, ~3 hours |
| **Recommended** | **100mm** | **Best quality, ~6 hours** |
| Display | 150mm+ | Showcase piece, 12+ hours |

---

## Customization Quick Tips

### Make it Bigger/Smaller
```python
generator = LunuffModelGenerator()
model = generator.generate()
model.scale = (2.0, 2.0, 2.0)  # 2x larger
bpy.ops.object.transform_apply(scale=True)
```

### Change Ear Bend
Edit line in `create_ears()`:
```python
bend.angle = math.radians(45)  # Less floppy (default: 70)
```

### Make Eyes Bigger
Edit line in `create_eyes()`:
```python
radius=0.20  # Larger iris (default: 0.08)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| STL not exporting | Check permissions in output folder |
| Model looks flat | Normal - STL viewer issue. Use Blender to preview |
| Ears too floppy | Reduce `bend.angle` value |
| Performance slow | Lower `subsurf.levels` from 2 to 1 |

---

## Pro Tips

💡 **Keep the STL file** - You can re-import it anytime  
💡 **Use multiple models** - Generate at different scales  
💡 **Join with others** - Combine Lunuff with other models in Blender  
💡 **Parametric variants** - Modify and regenerate for "families"  

---

## What's Next?

- ✓ **Print it!** Send the STL to your 3D printer
- ✓ **Render it!** Create beautiful promotional images
- ✓ **Rig it!** Add armature for animation
- ✓ **Modify it!** Tweak scales and features
- ✓ **Integrate it!** Use via Blender MCP with Claude

---

## Need Help?

1. Check `README.md` for detailed documentation
2. Run tests: `blender -b -P test_lunuff.py`
3. Review examples: `examples.py`
4. Validate structure: `python3 validate_structure.py`

---

**Ready? Let's go!** 🚀

Open Blender → Open `lunuff_character.py` → Run → Export → Print!
