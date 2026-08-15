import bpy

# ============================================================
# SKOMMA - MALE GREEN TROUSER LEGS
# Slim Blocky Legs - No Feet - No Sculpting
# ============================================================

if "Skomma_Legs" in bpy.data.collections:

    old_collection = bpy.data.collections["Skomma_Legs"]

    for obj in list(old_collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(old_collection)


collection = bpy.data.collections.new("Skomma_Legs")
bpy.context.scene.collection.children.link(collection)


# ============================================================
# GREEN MATERIAL
# ============================================================

GREEN = bpy.data.materials.get("Skomma_Green_Cloth")

if GREEN is None:
    GREEN = bpy.data.materials.new("Skomma_Green_Cloth")

GREEN.use_nodes = True

bsdf = GREEN.node_tree.nodes.get("Principled BSDF")

if bsdf:

    bsdf.inputs["Base Color"].default_value = (
        0.04,
        0.45,
        0.10,
        1.0
    )

    bsdf.inputs["Roughness"].default_value = 0.72

GREEN.diffuse_color = (
    0.04,
    0.45,
    0.10,
    1.0
)


# ============================================================
# LEG CREATOR
# ============================================================

def add_leg(name, location):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.object
    obj.name = name

    obj.dimensions = (
        0.35,
        0.35,
        1.20
    )

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    bevel = obj.modifiers.new(
        "Soft_Block_Edges",
        'BEVEL'
    )

    bevel.width = 0.08
    bevel.segments = 3

    obj.data.materials.append(GREEN)

    for c in list(obj.users_collection):
        c.objects.unlink(obj)

    collection.objects.link(obj)


# ============================================================
# LEGS
# ============================================================

add_leg(
    "Left_Leg",
    (-0.30, 0, 0.35)
)

add_leg(
    "Right_Leg",
    (0.30, 0, 0.35)
)


print("SKOMMA GREEN TROUSER LEGS CREATED")
print("Blender file NOT saved")