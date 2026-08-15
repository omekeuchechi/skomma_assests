import bpy
import math

# ============================================================
# SKOMMA MALE HANDS - BLACK SUIT
# Blender 3.3 LTS
#
# HANDS ONLY
# Separate modular asset
# NO BLENDER FILE SAVING
# ============================================================

COLLECTION_NAME = "Skomma_Hands"

# ============================================================
# CLEAN OLD HANDS
# ============================================================

if COLLECTION_NAME in bpy.data.collections:

    old_collection = bpy.data.collections[COLLECTION_NAME]

    for obj in list(old_collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(old_collection)

# ============================================================
# COLLECTION
# ============================================================

collection = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(collection)

# ============================================================
# MATERIALS
# ============================================================

def create_material(name, color, roughness=0.65):

    material = bpy.data.materials.get(name)

    if material is None:
        material = bpy.data.materials.new(name)

    material.use_nodes = True

    bsdf = material.node_tree.nodes.get("Principled BSDF")

    if bsdf:
        bsdf.inputs["Base Color"].default_value = (
            color[0],
            color[1],
            color[2],
            1
        )

        bsdf.inputs["Roughness"].default_value = roughness

    return material


SUIT = create_material(
    "Skomma_Suit_Black",
    (0.008, 0.009, 0.012),
    0.58
)

SKIN = create_material(
    "Skomma_Skin_Light",
    (0.72, 0.42, 0.25),
    0.72
)

# ============================================================
# ROOT
# ============================================================

bpy.ops.object.empty_add(
    type='PLAIN_AXES',
    location=(0, 0, 0)
)

hands_root = bpy.context.object
hands_root.name = "HandsRoot"

for c in list(hands_root.users_collection):
    c.objects.unlink(hands_root)

collection.objects.link(hands_root)

# ============================================================
# HELPERS
# ============================================================

def move_to_collection(obj):

    for c in list(obj.users_collection):
        c.objects.unlink(obj)

    collection.objects.link(obj)


def add_block(
    name,
    location,
    dimensions,
    material,
    bevel=0.08,
    segments=4
):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    modifier = obj.modifiers.new(
        "RoundedEdges",
        'BEVEL'
    )

    modifier.width = bevel
    modifier.segments = segments
    modifier.limit_method = 'ANGLE'

    obj.data.materials.append(material)

    move_to_collection(obj)

    obj.parent = hands_root

    return obj


def add_sphere(
    name,
    location,
    scale,
    material
):

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16,
        ring_count=10,
        location=location
    )

    obj = bpy.context.object
    obj.name = name
    obj.scale = scale

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    obj.data.materials.append(material)

    move_to_collection(obj)

    obj.parent = hands_root

    return obj

# ============================================================
# LEFT CUFF
# ============================================================

left_cuff = add_block(
    "Left_Suit_Cuff",
    (-1.30, 0, 1.35),
    (0.36, 0.46, 0.25),
    SUIT,
    0.06,
    3
)

# ============================================================
# LEFT PALM
# ============================================================

left_palm = add_block(
    "Left_Palm",
    (-1.30, -0.02, 1.02),
    (0.42, 0.34, 0.55),
    SKIN,
    0.13,
    5
)

# ============================================================
# LEFT THUMB
# ============================================================

left_thumb = add_sphere(
    "Left_Thumb",
    (-1.53, -0.17, 1.03),
    (0.13, 0.16, 0.23),
    SKIN
)

left_thumb.rotation_euler[1] = math.radians(-25)

# ============================================================
# LEFT FINGERS
# ============================================================

for i, x in enumerate([-1.44, -1.34, -1.24, -1.14]):

    finger = add_block(
        "Left_Finger_" + str(i + 1),
        (x, -0.04, 0.70),
        (0.075, 0.12, 0.34),
        SKIN,
        0.035,
        3
    )

# ============================================================
# RIGHT CUFF
# ============================================================

right_cuff = add_block(
    "Right_Suit_Cuff",
    (1.30, 0, 1.35),
    (0.36, 0.46, 0.25),
    SUIT,
    0.06,
    3
)

# ============================================================
# RIGHT PALM
# ============================================================

right_palm = add_block(
    "Right_Palm",
    (1.30, -0.02, 1.02),
    (0.42, 0.34, 0.55),
    SKIN,
    0.13,
    5
)

# ============================================================
# RIGHT THUMB
# ============================================================

right_thumb = add_sphere(
    "Right_Thumb",
    (1.53, -0.17, 1.03),
    (0.13, 0.16, 0.23),
    SKIN
)

right_thumb.rotation_euler[1] = math.radians(25)

# ============================================================
# RIGHT FINGERS
# ============================================================

for i, x in enumerate([1.14, 1.24, 1.34, 1.44]):

    finger = add_block(
        "Right_Finger_" + str(i + 1),
        (x, -0.04, 0.70),
        (0.075, 0.12, 0.34),
        SKIN,
        0.035,
        3
    )

# ============================================================
# SOCKETS
# ============================================================

for name, location in [
    ("LeftHandSocket", (-1.30, 0, 1.52)),
    ("RightHandSocket", (1.30, 0, 1.52))
]:

    socket = bpy.data.objects.new(name, None)
    socket.empty_display_type = 'PLAIN_AXES'
    socket.location = location

    collection.objects.link(socket)
    socket.parent = hands_root

# ============================================================
# METADATA
# ============================================================

hands_root["asset_type"] = "avatar_hands"
hands_root["asset_gender"] = "male"
hands_root["asset_style"] = "blocky_shaped"
hands_root["asset_clothing"] = "black_suit"
hands_root["asset_name"] = "Skomma_Hands_Male_Black_Suit_01"
hands_root["compatible_skeleton"] = "skomma_humanoid_v1"

# ============================================================
# SMOOTH
# ============================================================

for obj in collection.objects:

    if obj.type == 'MESH':

        for polygon in obj.data.polygons:
            polygon.use_smooth = True

bpy.ops.object.select_all(action='DESELECT')

hands_root.select_set(True)

bpy.context.view_layer.objects.active = hands_root

print("BLACK SUIT HANDS CREATED")
print("NO BLENDER FILE SAVED")