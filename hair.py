import bpy
import math

# ============================================================
# SKOMMA - MALE BLACK SPIKY HAIR
# Roblox / Blocky Anime-Inspired Style
# No Sculpting
# No Blender File Saving
# ============================================================


# ============================================================
# 1. CLEAN PREVIOUS HAIR
# ============================================================

if "Skomma_Hair" in bpy.data.collections:

    old_collection = bpy.data.collections["Skomma_Hair"]

    for obj in list(old_collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(old_collection)


# ============================================================
# 2. CREATE HAIR COLLECTION
# ============================================================

collection = bpy.data.collections.new(
    "Skomma_Hair"
)

bpy.context.scene.collection.children.link(
    collection
)


# ============================================================
# 3. BLACK HAIR MATERIAL
# ============================================================

BLACK_HAIR = bpy.data.materials.get(
    "Skomma_Black_Hair"
)

if BLACK_HAIR is None:

    BLACK_HAIR = bpy.data.materials.new(
        "Skomma_Black_Hair"
    )


BLACK_HAIR.use_nodes = True

bsdf = BLACK_HAIR.node_tree.nodes.get(
    "Principled BSDF"
)

if bsdf:

    bsdf.inputs["Base Color"].default_value = (
        0.008,
        0.008,
        0.008,
        1.0
    )

    bsdf.inputs["Roughness"].default_value = 0.58


# Viewport color
BLACK_HAIR.diffuse_color = (
    0.008,
    0.008,
    0.008,
    1.0
)


# ============================================================
# 4. HAIR ROOT
# ============================================================

bpy.ops.object.empty_add(
    type='PLAIN_AXES',
    location=(0, 0, 0)
)

hair_root = bpy.context.object

hair_root.name = "HairRoot"


# Move root into hair collection
for c in list(hair_root.users_collection):

    c.objects.unlink(hair_root)

collection.objects.link(hair_root)


# ============================================================
# 5. HELPER
# ============================================================

def move_to_collection(obj):

    for c in list(obj.users_collection):

        c.objects.unlink(obj)

    collection.objects.link(obj)


# ============================================================
# 6. BLOCK HAIR CREATOR
# ============================================================

def add_hair_block(
    name,
    location,
    dimensions,
    rotation=(0, 0, 0),
    bevel=0.08
):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    obj.dimensions = dimensions

    obj.rotation_euler = rotation

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )


    # --------------------------------------------------------
    # SOFT EDGES
    # --------------------------------------------------------

    bevel_modifier = obj.modifiers.new(
        "Hair_Soft_Edges",
        'BEVEL'
    )

    bevel_modifier.width = bevel
    bevel_modifier.segments = 3
    bevel_modifier.limit_method = 'ANGLE'


    # --------------------------------------------------------
    # MATERIAL
    # --------------------------------------------------------

    obj.data.materials.append(
        BLACK_HAIR
    )


    # --------------------------------------------------------
    # COLLECTION
    # --------------------------------------------------------

    move_to_collection(obj)


    # --------------------------------------------------------
    # PARENT
    # --------------------------------------------------------

    obj.parent = hair_root


    return obj


# ============================================================
# 7. SPIKE CREATOR
# ============================================================

def add_spike(
    name,
    location,
    scale,
    rotation=(0, 0, 0)
):

    bpy.ops.mesh.primitive_cone_add(
        vertices=6,
        radius1=1.0,
        radius2=0.12,
        depth=2.0,
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    obj.scale = scale

    obj.rotation_euler = rotation

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )


    # --------------------------------------------------------
    # SOFT EDGES
    # --------------------------------------------------------

    bevel_modifier = obj.modifiers.new(
        "Spike_Soft_Edges",
        'BEVEL'
    )

    bevel_modifier.width = 0.06
    bevel_modifier.segments = 2
    bevel_modifier.limit_method = 'ANGLE'


    # --------------------------------------------------------
    # MATERIAL
    # --------------------------------------------------------

    obj.data.materials.append(
        BLACK_HAIR
    )


    # --------------------------------------------------------
    # COLLECTION
    # --------------------------------------------------------

    move_to_collection(obj)


    # --------------------------------------------------------
    # PARENT
    # --------------------------------------------------------

    obj.parent = hair_root


    return obj


# ============================================================
# 8. MAIN HAIR MASS
# ============================================================

hair_mass = add_hair_block(
    "Hair_Main",
    (0, 0.02, 2.78),
    (1.70, 1.48, 0.55),
    rotation=(0, 0, 0),
    bevel=0.18
)


# ============================================================
# 9. FRONT HAIR MASS
# ============================================================

front_hair = add_hair_block(
    "Hair_Front",
    (0, -0.68, 2.66),
    (1.55, 0.42, 0.55),
    rotation=(math.radians(-8), 0, 0),
    bevel=0.13
)


# ============================================================
# 10. LEFT SIDE HAIR
# ============================================================

left_side = add_hair_block(
    "Hair_Left_Side",
    (-0.78, -0.05, 2.55),
    (0.40, 1.15, 0.70),
    rotation=(0, math.radians(-8), 0),
    bevel=0.12
)


# ============================================================
# 11. RIGHT SIDE HAIR
# ============================================================

right_side = add_hair_block(
    "Hair_Right_Side",
    (0.78, -0.05, 2.55),
    (0.40, 1.15, 0.70),
    rotation=(0, math.radians(8), 0),
    bevel=0.12
)


# ============================================================
# 12. FRONT CENTER SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Center",
    (0, -0.82, 2.95),
    (0.30, 0.25, 0.58),
    rotation=(
        math.radians(-18),
        0,
        0
    )
)


# ============================================================
# 13. FRONT LEFT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Front_Left",
    (-0.32, -0.78, 2.92),
    (0.28, 0.23, 0.52),
    rotation=(
        math.radians(-15),
        math.radians(-8),
        math.radians(-10)
    )
)


# ============================================================
# 14. FRONT RIGHT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Front_Right",
    (0.32, -0.78, 2.92),
    (0.28, 0.23, 0.52),
    rotation=(
        math.radians(-15),
        math.radians(8),
        math.radians(10)
    )
)


# ============================================================
# 15. TOP CENTER SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Top_Center",
    (0, 0.02, 3.20),
    (0.34, 0.30, 0.65),
    rotation=(
        math.radians(4),
        0,
        0
    )
)


# ============================================================
# 16. TOP LEFT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Top_Left",
    (-0.43, 0.02, 3.12),
    (0.30, 0.28, 0.58),
    rotation=(
        math.radians(2),
        math.radians(-12),
        math.radians(-8)
    )
)


# ============================================================
# 17. TOP RIGHT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Top_Right",
    (0.43, 0.02, 3.12),
    (0.30, 0.28, 0.58),
    rotation=(
        math.radians(2),
        math.radians(12),
        math.radians(8)
    )
)


# ============================================================
# 18. BACK LEFT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Back_Left",
    (-0.55, 0.55, 3.00),
    (0.30, 0.28, 0.55),
    rotation=(
        math.radians(18),
        math.radians(-12),
        math.radians(-8)
    )
)


# ============================================================
# 19. BACK RIGHT SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Back_Right",
    (0.55, 0.55, 3.00),
    (0.30, 0.28, 0.55),
    rotation=(
        math.radians(18),
        math.radians(12),
        math.radians(8)
    )
)


# ============================================================
# 20. BACK CENTER SPIKE
# ============================================================

add_spike(
    "Hair_Spike_Back_Center",
    (0, 0.65, 3.03),
    (0.34, 0.30, 0.62),
    rotation=(
        math.radians(20),
        0,
        0
    )
)


# ============================================================
# 21. HAIR SOCKET
# ============================================================

bpy.ops.object.empty_add(
    type='PLAIN_AXES',
    location=(0, 0, 2.92)
)

hair_socket = bpy.context.object

hair_socket.name = "HairSocket"

move_to_collection(
    hair_socket
)

hair_socket.parent = hair_root


# ============================================================
# 22. METADATA
# ============================================================

hair_root["asset_type"] = "avatar_hair"

hair_root["asset_category"] = "hair"

hair_root["asset_gender"] = "male"

hair_root["asset_style"] = (
    "blocky_spiky_anime_inspired"
)

hair_root["asset_color"] = "black"

hair_root["asset_sculpting"] = "none"

hair_root["asset_name"] = (
    "Skomma_Hair_Black_Spiky_Male_01"
)

hair_root["asset_version"] = "1.0"

hair_root["compatible_skeleton"] = (
    "skomma_humanoid_v1"
)

hair_root["hair_socket"] = "HairSocket"


# ============================================================
# 23. SMOOTH SHADING
# ============================================================

for obj in collection.objects:

    if obj.type == 'MESH':

        for polygon in obj.data.polygons:

            polygon.use_smooth = True


# ============================================================
# 24. SELECT HAIR ROOT
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

hair_root.select_set(True)

bpy.context.view_layer.objects.active = hair_root


# ============================================================
# 25. FINISHED
# ============================================================

print("")
print("======================================")
print("SKOMMA BLACK SPIKY MALE HAIR")
print("======================================")
print("")

print("Style:")
print("    Blocky")
print("    Anime Inspired")
print("    Spiky")
print("    Roblox Style")
print("    Black")
print("    No Sculpting")
print("")

print("Hair Root:")
print("    HairRoot")
print("")

print("Hair Socket:")
print("    HairSocket")
print("")

print("Collection:")
print("    Skomma_Hair")
print("")

print("Asset:")
print("    Skomma_Hair_Black_Spiky_Male_01")
print("")

print("Blender file was NOT saved.")
print("")

print("======================================")