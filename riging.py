import bpy
import math


# ============================================================
# SKOMMA - MALE HUMANOID SKELETON RIG
# ============================================================
#
# SKOMMA HUMANOID V1
#
# IMPORTANT:
#
# - Normal standing rest pose
# - Arms are DOWN beside the body
# - NOT T-POSE
# - Hands stay close to the torso
# - Existing modular avatar system compatible
# - ARM IK
# - LEG IK
# - Elbow poles
# - Knee poles
# - No animation
# - No GLB export
# - No Blender file saving
#
# Blender 3.3 LTS
#
# ============================================================


print("")
print("======================================")
print("SKOMMA MALE HUMANOID RIG")
print("NORMAL STANDING REST POSE")
print("======================================")
print("")


# ============================================================
# 1. CLEAN PREVIOUS SKOMMA RIG
# ============================================================

old_collection = bpy.data.collections.get("Skomma_Rig")

if old_collection:

    for obj in list(old_collection.objects):

        bpy.data.objects.remove(
            obj,
            do_unlink=True
        )

    bpy.data.collections.remove(
        old_collection
    )


# Also remove any old rig object outside the collection

old_rig = bpy.data.objects.get("Skomma_Rig")

if old_rig:

    bpy.data.objects.remove(
        old_rig,
        do_unlink=True
    )


# ============================================================
# 2. CREATE RIG COLLECTION
# ============================================================

rig_collection = bpy.data.collections.new(
    "Skomma_Rig"
)

bpy.context.scene.collection.children.link(
    rig_collection
)


# ============================================================
# 3. CREATE ARMATURE
# ============================================================

bpy.ops.object.armature_add(
    location=(0, 0, 0)
)

rig = bpy.context.object

rig.name = "Skomma_Rig"

rig.data.name = "Skomma_Humanoid_v1"

rig.show_in_front = True

rig.data.display_type = 'BBONE'


# ============================================================
# RIG METADATA
# ============================================================

rig["rig_type"] = "humanoid"

rig["rig_gender"] = "male"

rig["rig_version"] = "skomma_humanoid_v1"

rig["inverse_kinematics"] = True


# ============================================================
# MOVE RIG INTO SKOMMA COLLECTION
# ============================================================

for c in list(rig.users_collection):

    c.objects.unlink(rig)

rig_collection.objects.link(rig)


# ============================================================
# 4. REMOVE DEFAULT BONE
# ============================================================

bpy.context.view_layer.objects.active = rig

bpy.ops.object.mode_set(
    mode='EDIT'
)

edit_bones = rig.data.edit_bones


for bone in list(edit_bones):

    edit_bones.remove(bone)


# ============================================================
# 5. BONE CREATOR
# ============================================================

def create_bone(
    name,
    head,
    tail,
    parent=None,
    use_connect=False
):

    bone = edit_bones.new(name)

    bone.head = head

    bone.tail = tail

    if parent:

        bone.parent = edit_bones.get(
            parent
        )

    bone.use_connect = use_connect

    return bone


# ============================================================
# 6. ROOT
# ============================================================

create_bone(
    "Root",
    (0, 0, 0),
    (0, 0, 0.25)
)


# ============================================================
# 7. HIPS
# ============================================================

create_bone(
    "Hips",
    (0, 0, 0.25),
    (0, 0, 0.75),
    "Root"
)


# ============================================================
# 8. SPINE
# ============================================================

create_bone(
    "Spine",
    (0, 0, 0.75),
    (0, 0, 1.25),
    "Hips",
    True
)


# ============================================================
# 9. CHEST
# ============================================================

create_bone(
    "Chest",
    (0, 0, 1.25),
    (0, 0, 1.75),
    "Spine",
    True
)


# ============================================================
# 10. NECK
# ============================================================

create_bone(
    "Neck",
    (0, 0, 1.75),
    (0, 0, 1.98),
    "Chest",
    True
)


# ============================================================
# 11. HEAD
# ============================================================

create_bone(
    "Head",
    (0, 0, 1.98),
    (0, 0, 2.80),
    "Neck",
    True
)


# ============================================================
# 12. LEFT ARM
#
# NORMAL STANDING POSITION
#
# The arm is placed DOWN beside the body.
#
# Shoulder
#    |
#    |
#   Elbow
#    |
#    |
#   Hand
#
# NOT T-POSE
# ============================================================


# LEFT UPPER ARM

create_bone(
    "UpperArm_L",

    # Shoulder
    (-0.58, 0, 1.65),

    # Elbow
    (-0.62, 0, 1.32),

    "Chest"
)


# LEFT LOWER ARM

create_bone(
    "LowerArm_L",

    # Elbow
    (-0.62, 0, 1.32),

    # Wrist
    (-0.64, 0, 0.98),

    "UpperArm_L",

    True
)


# LEFT HAND

create_bone(
    "Hand_L",

    # Wrist
    (-0.64, 0, 0.98),

    # Hand extends slightly downward
    (-0.64, 0, 0.78),

    "LowerArm_L",

    True
)


# ============================================================
# 13. RIGHT ARM
#
# NORMAL STANDING POSITION
# ============================================================


# RIGHT UPPER ARM

create_bone(
    "UpperArm_R",

    # Shoulder
    (0.58, 0, 1.65),

    # Elbow
    (0.62, 0, 1.32),

    "Chest"
)


# RIGHT LOWER ARM

create_bone(
    "LowerArm_R",

    # Elbow
    (0.62, 0, 1.32),

    # Wrist
    (0.64, 0, 0.98),

    "UpperArm_R",

    True
)


# RIGHT HAND

create_bone(
    "Hand_R",

    # Wrist
    (0.64, 0, 0.98),

    # Hand extends slightly downward
    (0.64, 0, 0.78),

    "LowerArm_R",

    True
)


# ============================================================
# 14. LEFT LEG
# ============================================================

create_bone(
    "UpperLeg_L",

    (-0.30, 0, 0.70),

    (-0.30, 0, 0.05),

    "Hips"
)


create_bone(
    "LowerLeg_L",

    (-0.30, 0, 0.05),

    (-0.30, 0, -0.75),

    "UpperLeg_L",

    True
)


create_bone(
    "Foot_L",

    (-0.30, 0, -0.75),

    (-0.30, -0.35, -0.75),

    "LowerLeg_L",

    True
)


# ============================================================
# 15. RIGHT LEG
# ============================================================

create_bone(
    "UpperLeg_R",

    (0.30, 0, 0.70),

    (0.30, 0, 0.05),

    "Hips"
)


create_bone(
    "LowerLeg_R",

    (0.30, 0, 0.05),

    (0.30, 0, -0.75),

    "UpperLeg_R",

    True
)


create_bone(
    "Foot_R",

    (0.30, 0, -0.75),

    (0.30, -0.35, -0.75),

    "LowerLeg_R",

    True
)


# ============================================================
# 16. ARM IK CONTROL BONES
# ============================================================
#
# IMPORTANT:
#
# These are now CLOSE TO THE BODY.
#
# They are positioned at the actual hand locations.
# ============================================================


# LEFT HAND IK

hand_ik_l = create_bone(
    "Hand_IK_L",

    (-0.64, 0, 0.78),

    (-0.64, 0, 0.98),

    "Root"
)

hand_ik_l.use_deform = False


# RIGHT HAND IK

hand_ik_r = create_bone(
    "Hand_IK_R",

    (0.64, 0, 0.78),

    (0.64, 0, 0.98),

    "Root"
)

hand_ik_r.use_deform = False


# ============================================================
# 17. FOOT IK
# ============================================================


foot_ik_l = create_bone(
    "Foot_IK_L",

    (-0.30, -0.35, -0.75),

    (-0.30, -0.35, -0.50),

    "Root"
)

foot_ik_l.use_deform = False


foot_ik_r = create_bone(
    "Foot_IK_R",

    (0.30, -0.35, -0.75),

    (0.30, -0.35, -0.50),

    "Root"
)

foot_ik_r.use_deform = False


# ============================================================
# 18. ELBOW POLE BONES
#
# Positioned slightly IN FRONT of the body.
#
# They are no longer far away from the character.
# ============================================================


elbow_l = create_bone(
    "Elbow_Pole_L",

    (-0.72, -0.55, 1.32),

    (-0.72, -0.55, 1.55),

    "Root"
)

elbow_l.use_deform = False


elbow_r = create_bone(
    "Elbow_Pole_R",

    (0.72, -0.55, 1.32),

    (0.72, -0.55, 1.55),

    "Root"
)

elbow_r.use_deform = False


# ============================================================
# 19. KNEE POLE BONES
# ============================================================


knee_l = create_bone(
    "Knee_Pole_L",

    (-0.30, -0.65, 0.05),

    (-0.30, -0.65, 0.30),

    "Root"
)

knee_l.use_deform = False


knee_r = create_bone(
    "Knee_Pole_R",

    (0.30, -0.65, 0.05),

    (0.30, -0.65, 0.30),

    "Root"
)

knee_r.use_deform = False


# ============================================================
# 20. FINISH EDIT MODE
# ============================================================

bpy.ops.object.mode_set(
    mode='POSE'
)


# ============================================================
# 21. LEFT ARM IK
# ============================================================

pose_bone = rig.pose.bones[
    "LowerArm_L"
]

ik = pose_bone.constraints.new(
    'IK'
)

ik.name = "Left_Arm_IK"

ik.target = rig

ik.subtarget = "Hand_IK_L"

ik.pole_target = rig

ik.pole_subtarget = "Elbow_Pole_L"

ik.chain_count = 2

ik.influence = 1.0


# ============================================================
# 22. RIGHT ARM IK
# ============================================================

pose_bone = rig.pose.bones[
    "LowerArm_R"
]

ik = pose_bone.constraints.new(
    'IK'
)

ik.name = "Right_Arm_IK"

ik.target = rig

ik.subtarget = "Hand_IK_R"

ik.pole_target = rig

ik.pole_subtarget = "Elbow_Pole_R"

ik.chain_count = 2

ik.influence = 1.0


# ============================================================
# 23. LEFT LEG IK
# ============================================================

pose_bone = rig.pose.bones[
    "LowerLeg_L"
]

ik = pose_bone.constraints.new(
    'IK'
)

ik.name = "Left_Leg_IK"

ik.target = rig

ik.subtarget = "Foot_IK_L"

ik.pole_target = rig

ik.pole_subtarget = "Knee_Pole_L"

ik.chain_count = 2

ik.influence = 1.0


# ============================================================
# 24. RIGHT LEG IK
# ============================================================

pose_bone = rig.pose.bones[
    "LowerLeg_R"
]

ik = pose_bone.constraints.new(
    'IK'
)

ik.name = "Right_Leg_IK"

ik.target = rig

ik.subtarget = "Foot_IK_R"

ik.pole_target = rig

ik.pole_subtarget = "Knee_Pole_R"

ik.chain_count = 2

ik.influence = 1.0


# ============================================================
# 25. FINISH POSE MODE
# ============================================================

bpy.ops.object.mode_set(
    mode='OBJECT'
)


# ============================================================
# 26. BODY PART PARENTING HELPER
# ============================================================

def parent_object_to_bone(
    obj,
    bone_name
):

    if obj is None:
        return

    obj.parent = rig

    obj.parent_type = 'BONE'

    obj.parent_bone = bone_name


# ============================================================
# 27. HEAD
# ============================================================

head_collection = bpy.data.collections.get(
    "Skomma_Head"
)

if head_collection:

    for obj in head_collection.objects:

        if obj.name == "HeadRoot":

            parent_object_to_bone(
                obj,
                "Head"
            )


# ============================================================
# 28. BODY
# ============================================================

body_collection = bpy.data.collections.get(
    "Skomma_Body"
)

if body_collection:

    for obj in body_collection.objects:

        if obj.type != 'EMPTY':

            parent_object_to_bone(
                obj,
                "Chest"
            )


# ============================================================
# 29. HANDS
# ============================================================

hand_collection = bpy.data.collections.get(
    "Skomma_Hands"
)

if hand_collection:

    for obj in hand_collection.objects:

        if "Left" in obj.name:

            parent_object_to_bone(
                obj,
                "Hand_L"
            )

        elif "Right" in obj.name:

            parent_object_to_bone(
                obj,
                "Hand_R"
            )


# ============================================================
# 30. LEGS
# ============================================================

leg_collection = bpy.data.collections.get(
    "Skomma_Legs"
)

if leg_collection:

    for obj in leg_collection.objects:

        if "Left" in obj.name:

            parent_object_to_bone(
                obj,
                "LowerLeg_L"
            )

        elif "Right" in obj.name:

            parent_object_to_bone(
                obj,
                "LowerLeg_R"
            )


# ============================================================
# 31. SHOES
# ============================================================

shoe_collection = bpy.data.collections.get(
    "Skomma_Shoes"
)

if shoe_collection:

    for obj in shoe_collection.objects:

        if "Left" in obj.name:

            parent_object_to_bone(
                obj,
                "Foot_L"
            )

        elif "Right" in obj.name:

            parent_object_to_bone(
                obj,
                "Foot_R"
            )


# ============================================================
# 32. HAIR
# ============================================================

hair_collection = bpy.data.collections.get(
    "Skomma_Hair"
)

if hair_collection:

    for obj in hair_collection.objects:

        parent_object_to_bone(
            obj,
            "Head"
        )


# ============================================================
# 33. DISPLAY CONTROL CREATOR
# ============================================================

def create_control(
    name,
    location,
    display_type='CUBE',
    size=0.15
):

    empty = bpy.data.objects.new(
        name,
        None
    )

    empty.empty_display_type = display_type

    empty.empty_display_size = size

    empty.location = location

    rig_collection.objects.link(
        empty
    )

    return empty


# ============================================================
# 34. HAND CONTROLS
# ============================================================
#
# CLOSE TO BODY
# ============================================================


hand_control_l = create_control(
    "CTRL_Hand_L",

    (-0.64, 0, 0.78),

    'CUBE',

    0.12
)


hand_control_r = create_control(
    "CTRL_Hand_R",

    (0.64, 0, 0.78),

    'CUBE',

    0.12
)


# ============================================================
# 35. FOOT CONTROLS
# ============================================================


foot_control_l = create_control(
    "CTRL_Foot_L",

    (-0.30, -0.35, -0.75),

    'CUBE',

    0.16
)


foot_control_r = create_control(
    "CTRL_Foot_R",

    (0.30, -0.35, -0.75),

    'CUBE',

    0.16
)


# ============================================================
# 36. ELBOW CONTROLS
# ============================================================


create_control(
    "CTRL_Elbow_L",

    (-0.72, -0.55, 1.32),

    'SPHERE',

    0.10
)


create_control(
    "CTRL_Elbow_R",

    (0.72, -0.55, 1.32),

    'SPHERE',

    0.10
)


# ============================================================
# 37. KNEE CONTROLS
# ============================================================


create_control(
    "CTRL_Knee_L",

    (-0.30, -0.65, 0.05),

    'SPHERE',

    0.10
)


create_control(
    "CTRL_Knee_R",

    (0.30, -0.65, 0.05),

    'SPHERE',

    0.10
)


# ============================================================
# 38. RIG METADATA
# ============================================================

rig["asset_type"] = "avatar_rig"

rig["asset_category"] = "humanoid_skeleton"

rig["asset_gender"] = "male"

rig["asset_style"] = "skomma_blocky"

rig["asset_version"] = "1.0"

rig["compatible_skeleton"] = (
    "skomma_humanoid_v1"
)

rig["ik_enabled"] = True

rig["arm_ik"] = True

rig["leg_ik"] = True

rig["modular_avatar"] = True

rig["female_compatible_structure"] = True

rig["rest_pose"] = "normal_standing"

rig["arms_rest_pose"] = "down_beside_body"


# ============================================================
# 39. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 40. FINAL INFORMATION
# ============================================================

print("")
print("======================================")
print("SKOMMA HUMANOID V1 CREATED")
print("======================================")
print("")

print("Rest Pose:")
print("    NORMAL STANDING")
print("")

print("Arms:")
print("    DOWN BESIDE BODY")
print("    NOT T-POSE")
print("")

print("Hands:")
print("    CLOSE TO BODY")
print("    RELAXED POSITION")
print("")

print("Left Arm:")
print("    UpperArm_L")
print("    LowerArm_L")
print("    Hand_L")
print("")

print("Right Arm:")
print("    UpperArm_R")
print("    LowerArm_R")
print("    Hand_R")
print("")

print("Legs:")
print("    UpperLeg_L")
print("    LowerLeg_L")
print("    Foot_L")
print("    UpperLeg_R")
print("    LowerLeg_R")
print("    Foot_R")
print("")

print("======================================")
print("INVERSE KINEMATICS")
print("======================================")
print("")

print("Left Arm:")
print("    Hand_IK_L")
print("    Elbow_Pole_L")
print("")

print("Right Arm:")
print("    Hand_IK_R")
print("    Elbow_Pole_R")
print("")

print("Left Leg:")
print("    Foot_IK_L")
print("    Knee_Pole_L")
print("")

print("Right Leg:")
print("    Foot_IK_R")
print("    Knee_Pole_R")
print("")

print("======================================")
print("NO BLENDER FILE SAVED")
print("NO GLB CREATED")
print("======================================")