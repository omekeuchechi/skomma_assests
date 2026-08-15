import bpy

# ============================================================
# SKOMMA - MALE BLACK SHOES
# Blocky Shoe Format
# No Sculpting
# No Blender File Saving
# ============================================================


# ============================================================
# 1. CLEAN PREVIOUS SHOES
# ============================================================

if "Skomma_Shoes" in bpy.data.collections:

    old_collection = bpy.data.collections["Skomma_Shoes"]

    for obj in list(old_collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(old_collection)


# ============================================================
# 2. CREATE COLLECTION
# ============================================================

collection = bpy.data.collections.new(
    "Skomma_Shoes"
)

bpy.context.scene.collection.children.link(
    collection
)


# ============================================================
# 3. BLACK SHOE MATERIAL
# ============================================================

BLACK = bpy.data.materials.get(
    "Skomma_Black_Shoes"
)

# Create material if it doesn't exist
if BLACK is None:

    BLACK = bpy.data.materials.new(
        "Skomma_Black_Shoes"
    )


# ============================================================
# IMPORTANT
# ALWAYS ENABLE NODES
# ============================================================

BLACK.use_nodes = True


# ============================================================
# GET PRINCIPLED BSDF
# ============================================================

bsdf = BLACK.node_tree.nodes.get(
    "Principled BSDF"
)


# ============================================================
# FORCE BLACK COLOR
# ============================================================

if bsdf:

    bsdf.inputs["Base Color"].default_value = (
        0.005,
        0.005,
        0.005,
        1.0
    )

    bsdf.inputs["Roughness"].default_value = 0.62


# Also set viewport color
BLACK.diffuse_color = (
    0.005,
    0.005,
    0.005,
    1.0
)


# ============================================================
# 4. SHOE CREATOR
# ============================================================

def add_shoe(
    name,
    location
):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.object

    obj.name = name


    # ========================================================
    # SHOE DIMENSIONS
    #
    # X = WIDTH
    # Y = LENGTH / DEPTH
    # Z = HEIGHT
    # ========================================================

    obj.dimensions = (
        0.48,
        0.82,
        0.30
    )


    # Apply dimensions
    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )


    # ========================================================
    # ROUNDED SHOE EDGES
    # ========================================================

    bevel = obj.modifiers.new(
        "Shoe_Soft_Edges",
        'BEVEL'
    )

    bevel.width = 0.10
    bevel.segments = 4

    bevel.limit_method = 'ANGLE'


    # ========================================================
    # ADD BLACK MATERIAL
    # ========================================================

    obj.data.materials.clear()

    obj.data.materials.append(
        BLACK
    )


    # ========================================================
    # MOVE TO SKOMMA SHOES COLLECTION
    # ========================================================

    for c in list(obj.users_collection):

        c.objects.unlink(obj)

    collection.objects.link(obj)


# ============================================================
# 5. LEFT SHOE
# ============================================================

add_shoe(
    "Left_Shoe",
    (-0.30, -0.24, -0.12)
)


# ============================================================
# 6. RIGHT SHOE
# ============================================================

add_shoe(
    "Right_Shoe",
    (0.30, -0.24, -0.12)
)


# ============================================================
# 7. FINISHED
# ============================================================

print("")
print("======================================")
print("SKOMMA BLACK MALE SHOES")
print("======================================")
print("")

print("Style:")
print("    Blocky Shoe")
print("    Male")
print("    Black")
print("    No Sculpting")
print("    No Feet Geometry")
print("")

print("Shoe Dimensions:")
print("    Width:  0.48")
print("    Depth:  0.82")
print("    Height: 0.30")
print("")

print("Left Shoe:")
print("    Left_Shoe")
print("")

print("Right Shoe:")
print("    Right_Shoe")
print("")

print("Collection:")
print("    Skomma_Shoes")
print("")

print("Material:")
print("    Skomma_Black_Shoes")
print("    Forced Black")
print("")

print("Blender file was NOT saved.")
print("")

print("======================================")