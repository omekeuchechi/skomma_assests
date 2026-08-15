import bpy
import math


# ============================================================
# SKOMMA HUMANOID V1
# WALKING ANIMATION
# ============================================================
#
# IMPORTANT:
#
# - Uses EXISTING Skomma humanoid skeleton
# - Does NOT create new bones
# - Does NOT create a new GLB
# - Does NOT save the Blender file
# - Preserves existing Skomma_Idle animation
# - Creates Skomma_Walk as a SEPARATE action
# - Existing IK system is preserved
#
# ANIMATIONS:
#
#     Skomma_Idle
#     Skomma_Walk
#
# Both actions remain inside the same Blender scene.
#
# ============================================================


print("")
print("======================================")
print("SKOMMA HUMANOID V1 - WALK ANIMATION")
print("======================================")
print("")


# ============================================================
# 1. FIND EXISTING ARMATURE
# ============================================================

rig = None

possible_names = [
    "Skomma_Rig",
    "skomma_humanoid_v1",
    "Skomma_Humanoid",
    "Skomma_Humanoid_v1",
    "SkommaHumanoid",
    "Humanoid",
    "Armature"
]


for name in possible_names:

    obj = bpy.data.objects.get(name)

    if obj and obj.type == 'ARMATURE':

        rig = obj
        break


# Search all armatures if needed

if rig is None:

    for obj in bpy.data.objects:

        if obj.type == 'ARMATURE':

            rig = obj
            break


if rig is None:

    raise RuntimeError(
        "No existing SKOMMA humanoid armature found."
    )


print("Existing armature:")
print("   ", rig.name)
print("")


# ============================================================
# 2. CHECK EXISTING IDLE ANIMATION
# ============================================================

idle_action = bpy.data.actions.get(
    "Skomma_Idle"
)


if idle_action:

    print("Existing Idle animation FOUND:")
    print("    Skomma_Idle")
    print("")

else:

    print("WARNING:")
    print("    Skomma_Idle was not found.")
    print("")


# ============================================================
# 3. REMEMBER CURRENT ACTIVE ACTION
# ============================================================

original_action = None


if rig.animation_data:

    original_action = rig.animation_data.action


if original_action:

    print("Current active animation:")
    print("    ", original_action.name)
    print("")

else:

    print("No active animation currently assigned.")
    print("")


# ============================================================
# 4. CHECK REQUIRED BONES
# ============================================================

required_bones = [

    "Root",

    "Hips",
    "Spine",
    "Chest",
    "Neck",
    "Head",

    "UpperArm_L",
    "LowerArm_L",
    "Hand_L",

    "UpperArm_R",
    "LowerArm_R",
    "Hand_R",

    "UpperLeg_L",
    "LowerLeg_L",

    "UpperLeg_R",
    "LowerLeg_R",

    "Hand_IK_L",
    "Hand_IK_R",

    "Foot_IK_L",
    "Foot_IK_R"

]


print("Checking skeleton...")
print("--------------------------------------")


for bone_name in required_bones:

    if rig.pose.bones.get(bone_name):

        print("FOUND   :", bone_name)

    else:

        print("MISSING :", bone_name)


print("--------------------------------------")
print("")


# ============================================================
# 5. GET POSE BONE
# ============================================================

def get_bone(name):

    bone = rig.pose.bones.get(name)

    if bone is None:

        raise RuntimeError(
            "Required bone not found: " + name
        )

    return bone


# ============================================================
# 6. GET BONES
# ============================================================

root = get_bone("Root")

hips = get_bone("Hips")

spine = get_bone("Spine")

chest = get_bone("Chest")

neck = get_bone("Neck")

head = get_bone("Head")


# ============================================================
# LEFT ARM
# ============================================================

left_upper_arm = get_bone(
    "UpperArm_L"
)

left_forearm = get_bone(
    "LowerArm_L"
)

left_hand = get_bone(
    "Hand_L"
)


# ============================================================
# RIGHT ARM
# ============================================================

right_upper_arm = get_bone(
    "UpperArm_R"
)

right_forearm = get_bone(
    "LowerArm_R"
)

right_hand = get_bone(
    "Hand_R"
)


# ============================================================
# LEFT LEG
# ============================================================

left_upper_leg = get_bone(
    "UpperLeg_L"
)

left_lower_leg = get_bone(
    "LowerLeg_L"
)


# ============================================================
# RIGHT LEG
# ============================================================

right_upper_leg = get_bone(
    "UpperLeg_R"
)

right_lower_leg = get_bone(
    "LowerLeg_R"
)


# ============================================================
# IK CONTROLS
# ============================================================

hand_ik_l = get_bone(
    "Hand_IK_L"
)

hand_ik_r = get_bone(
    "Hand_IK_R"
)

foot_ik_l = get_bone(
    "Foot_IK_L"
)

foot_ik_r = get_bone(
    "Foot_IK_R"
)


# ============================================================
# 7. REMOVE ONLY OLD WALK ACTION
# ============================================================
#
# IMPORTANT:
#
# We ONLY remove Skomma_Walk.
#
# Skomma_Idle is NEVER removed.
#
# ============================================================

old_walk = bpy.data.actions.get(
    "Skomma_Walk"
)


if old_walk:

    print("Removing previous Skomma_Walk...")

    bpy.data.actions.remove(
        old_walk
    )


# ============================================================
# 8. CREATE NEW WALK ACTION
# ============================================================

action = bpy.data.actions.new(
    "Skomma_Walk"
)


action.use_fake_user = True


# ============================================================
# 9. TEMPORARILY ASSIGN WALK ACTION
# ============================================================
#
# We need the action assigned while inserting keyframes.
#
# IMPORTANT:
#
# At the END of this script we restore the previous
# animation, so Idle is NOT lost.
#
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


rig.animation_data.action = action


print("")
print("Creating:")
print("    Skomma_Walk")
print("")


# ============================================================
# 10. ANIMATION SETTINGS
# ============================================================

scene = bpy.context.scene

scene.render.fps = 30


# Do NOT permanently destroy the user's scene range.

old_scene_start = scene.frame_start
old_scene_end = scene.frame_end


scene.frame_start = 1
scene.frame_end = 25


# ============================================================
# 11. ROTATION HELPER
# ============================================================

def key_rotation(
    bone,
    frame,
    x=0,
    y=0,
    z=0
):

    if bone is None:
        return


    bone.rotation_mode = 'XYZ'


    bone.rotation_euler = (

        math.radians(x),

        math.radians(y),

        math.radians(z)

    )


    bone.keyframe_insert(

        data_path="rotation_euler",

        frame=frame,

        group=bone.name

    )


# ============================================================
# 12. LOCATION HELPER
# ============================================================

def key_location(
    bone,
    frame,
    x=0,
    y=0,
    z=0
):

    if bone is None:
        return


    bone.location = (

        x,
        y,
        z

    )


    bone.keyframe_insert(

        data_path="location",

        frame=frame,

        group=bone.name

    )


# ============================================================
# 13. BODY
# ============================================================

def neutral_body(frame):


    key_rotation(
        root,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        hips,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        spine,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        chest,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        neck,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        head,
        frame,
        0,
        0,
        0
    )


# ============================================================
# 14. WALK POSE
# ============================================================

def walk_pose(

    frame,

    left_foot_y,
    left_foot_z,

    right_foot_y,
    right_foot_z,

    left_hand_y,
    right_hand_y,

    hip_x=0,
    hip_y=0,
    hip_z=0,

    torso_y=0,

    head_z=0
):


    # ========================================================
    # BODY BOB
    # ========================================================

    key_location(
        root,
        frame,
        hip_x,
        hip_y,
        hip_z
    )


    # ========================================================
    # HIPS
    # ========================================================

    key_rotation(
        hips,
        frame,
        0,
        torso_y,
        0
    )


    # ========================================================
    # SPINE
    # ========================================================

    key_rotation(
        spine,
        frame,
        0,
        -torso_y * 0.35,
        0
    )


    # ========================================================
    # CHEST
    # ========================================================

    key_rotation(
        chest,
        frame,
        0,
        -torso_y * 0.25,
        0
    )


    # ========================================================
    # HEAD
    # ========================================================

    key_rotation(
        head,
        frame,
        0,
        0,
        head_z
    )


    # ========================================================
    # LEFT FOOT IK
    # ========================================================

    key_location(
        foot_ik_l,
        frame,
        0,
        left_foot_y,
        left_foot_z
    )


    # ========================================================
    # RIGHT FOOT IK
    # ========================================================

    key_location(
        foot_ik_r,
        frame,
        0,
        right_foot_y,
        right_foot_z
    )


    # ========================================================
    # LEFT HAND IK
    # ========================================================

    key_location(
        hand_ik_l,
        frame,
        0,
        left_hand_y,
        0
    )


    # ========================================================
    # RIGHT HAND IK
    # ========================================================

    key_location(
        hand_ik_r,
        frame,
        0,
        right_hand_y,
        0
    )


# ============================================================
# 15. FRAME 1
# ============================================================

neutral_body(1)


walk_pose(

    1,

    -0.22,
    0.00,

    0.18,
    0.00,

    0.10,
    -0.10,

    0,
    0,
    0.00,

    -2.0,

    -1.0

)


# ============================================================
# 16. FRAME 4
# ============================================================

walk_pose(

    4,

    -0.16,
    0.035,

    0.12,
    0.00,

    0.07,
    -0.07,

    0,
    0,
    0.025,

    -1.0,

    -0.5

)


# ============================================================
# 17. FRAME 7
# ============================================================

walk_pose(

    7,

    -0.02,
    0.11,

    0.02,
    0.04,

    0.02,
    -0.02,

    0,
    0,
    0.055,

    0,

    0.5

)


# ============================================================
# 18. FRAME 10
# ============================================================

walk_pose(

    10,

    0.16,
    0.025,

    -0.12,
    0.07,

    -0.07,
    0.07,

    0,
    0,
    0.025,

    1.0,

    0.5

)


# ============================================================
# 19. FRAME 13
# ============================================================

walk_pose(

    13,

    0.18,
    0.00,

    -0.22,
    0.00,

    -0.10,
    0.10,

    0,
    0,
    0.00,

    2.0,

    1.0

)


# ============================================================
# 20. FRAME 16
# ============================================================

walk_pose(

    16,

    0.12,
    0.00,

    -0.16,
    0.035,

    -0.07,
    0.07,

    0,
    0,
    0.025,

    1.0,

    0.5

)


# ============================================================
# 21. FRAME 19
# ============================================================

walk_pose(

    19,

    0.02,
    0.04,

    -0.02,
    0.11,

    -0.02,
    0.02,

    0,
    0,
    0.055,

    0,

    -0.5

)


# ============================================================
# 22. FRAME 22
# ============================================================

walk_pose(

    22,

    -0.12,
    0.07,

    0.16,
    0.025,

    0.07,
    -0.07,

    0,
    0,
    0.025,

    -1.0,

    -0.5

)


# ============================================================
# 23. FRAME 25
# ============================================================

walk_pose(

    25,

    -0.22,
    0.00,

    0.18,
    0.00,

    0.10,
    -0.10,

    0,
    0,
    0.00,

    -2.0,

    -1.0

)


# ============================================================
# 24. SMOOTH WALK
# ============================================================

if action.fcurves:

    for fcurve in action.fcurves:

        for keyframe in fcurve.keyframe_points:

            keyframe.interpolation = 'BEZIER'


# ============================================================
# 25. MAKE WALK LOOP
# ============================================================

for fcurve in action.fcurves:

    fcurve.modifiers.new(
        type='CYCLES'
    )


# ============================================================
# 26. ACTION INFORMATION
# ============================================================

action.frame_start = 1

action.frame_end = 25


action["animation_type"] = "walk"

action["character"] = "skomma_humanoid_v1"

action["animation_style"] = "blocky_humanoid"

action["loop"] = True

action["fps"] = 30

action["frame_length"] = 25

action["uses_existing_ik"] = True

action["creates_new_bones"] = False

action["creates_new_glb"] = False


# ============================================================
# 27. RESTORE ORIGINAL ACTION
# ============================================================
#
# THIS IS THE IMPORTANT FIX.
#
# Skomma_Walk has been created and stored.
#
# We now put the previous animation back as the
# ACTIVE animation.
#
# If Skomma_Idle was active before, it becomes active again.
#
# ============================================================

if original_action:

    rig.animation_data.action = original_action

    print("")
    print("Restored original active animation:")
    print("    ", original_action.name)
    print("")

elif idle_action:

    rig.animation_data.action = idle_action

    print("")
    print("Restored Skomma_Idle as active animation.")
    print("")

else:

    # No previous action existed.
    #
    # Leave Walk available but don't delete it.

    rig.animation_data.action = action

    print("")
    print("No previous animation existed.")
    print("Skomma_Walk remains active.")
    print("")


# ============================================================
# 28. RESTORE SCENE RANGE
# ============================================================

scene.frame_start = old_scene_start

scene.frame_end = old_scene_end


# ============================================================
# 29. SET FRAME
# ============================================================

scene.frame_set(1)


# ============================================================
# 30. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 31. VERIFY ANIMATIONS
# ============================================================

print("")
print("======================================")
print("AVAILABLE SKOMMA ANIMATIONS")
print("======================================")
print("")


for act in bpy.data.actions:

    if act.name.startswith("Skomma_"):

        print(
            "FOUND:",
            act.name
        )


# ============================================================
# 32. FINAL INFORMATION
# ============================================================

print("")
print("======================================")
print("SKOMMA WALK ANIMATION COMPLETE")
print("======================================")
print("")

print("Created:")
print("    Skomma_Walk")
print("")

print("Existing animation:")
print("    Skomma_Idle")
print("    PRESERVED")
print("")

print("Walk frames:")
print("    1 - 25")
print("")

print("FPS:")
print("    30")
print("")

print("Loop:")
print("    YES")
print("")

print("IK:")
print("    Existing IK")
print("")

print("Skeleton:")
print("    Existing skeleton ONLY")
print("")

print("New bones:")
print("    NONE")
print("")

print("New GLB:")
print("    NONE")
print("")

print("Blender file:")
print("    NOT SAVED")
print("")

print("======================================")