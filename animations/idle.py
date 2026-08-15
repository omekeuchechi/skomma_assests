import bpy
import math


# ============================================================
# SKOMMA HUMANOID V1
# NORMAL STANDING IDLE ANIMATION
# ============================================================
#
# IMPORTANT:
#
# - Uses EXISTING Skomma_Rig
# - Uses EXISTING bones
# - Does NOT create new bones
# - Does NOT create a new GLB
# - Does NOT save the Blender file
#
# ARM POSITION:
#
# - Hands remain close to body
# - No T-POSE
# - No extra downward arm rotation
# - Existing skeleton rest position is preserved
#
# ANIMATION:
#
# - Normal standing
# - Subtle breathing
# - Small chest movement
# - Small spine movement
# - Small head movement
# - Arms remain relaxed
# - Hands remain beside body
# - Smooth 60-frame loop
#
# Blender 3.3 LTS
#
# ============================================================


print("")
print("======================================")
print("SKOMMA NORMAL STANDING IDLE")
print("======================================")
print("")


# ============================================================
# 1. FIND EXISTING SKOMMA RIG
# ============================================================

rig = bpy.data.objects.get("Skomma_Rig")


if rig is None:

    raise RuntimeError(
        "Skomma_Rig was not found. "
        "Run the SKOMMA humanoid skeleton script first."
    )


if rig.type != 'ARMATURE':

    raise RuntimeError(
        "Skomma_Rig exists but it is not an armature."
    )


print("Rig found:")
print("   ", rig.name)
print("")


# ============================================================
# 2. PRINT EXISTING BONES
# ============================================================

print("Existing bones:")
print("--------------------------------------")

for bone in rig.data.bones:

    print("   ", bone.name)

print("--------------------------------------")
print("")


# ============================================================
# 3. BONE FINDER
# ============================================================

def find_bone(names):

    for name in names:

        bone = rig.pose.bones.get(name)

        if bone:

            return bone

    return None


# ============================================================
# 4. MAIN BODY BONES
# ============================================================

root = find_bone([
    "Root"
])


hips = find_bone([
    "Hips"
])


spine = find_bone([
    "Spine"
])


chest = find_bone([
    "Chest"
])


neck = find_bone([
    "Neck"
])


head = find_bone([
    "Head"
])


# ============================================================
# 5. ARM BONES
# ============================================================

upper_arm_l = find_bone([
    "UpperArm_L"
])


lower_arm_l = find_bone([
    "LowerArm_L"
])


hand_l = find_bone([
    "Hand_L"
])


upper_arm_r = find_bone([
    "UpperArm_R"
])


lower_arm_r = find_bone([
    "LowerArm_R"
])


hand_r = find_bone([
    "Hand_R"
])


# ============================================================
# 6. LEG BONES
# ============================================================

upper_leg_l = find_bone([
    "UpperLeg_L"
])


lower_leg_l = find_bone([
    "LowerLeg_L"
])


foot_l = find_bone([
    "Foot_L"
])


upper_leg_r = find_bone([
    "UpperLeg_R"
])


lower_leg_r = find_bone([
    "LowerLeg_R"
])


foot_r = find_bone([
    "Foot_R"
])


# ============================================================
# 7. DISPLAY BONE STATUS
# ============================================================

bones = {

    "Root": root,
    "Hips": hips,
    "Spine": spine,
    "Chest": chest,
    "Neck": neck,
    "Head": head,

    "UpperArm_L": upper_arm_l,
    "LowerArm_L": lower_arm_l,
    "Hand_L": hand_l,

    "UpperArm_R": upper_arm_r,
    "LowerArm_R": lower_arm_r,
    "Hand_R": hand_r,

    "UpperLeg_L": upper_leg_l,
    "LowerLeg_L": lower_leg_l,
    "Foot_L": foot_l,

    "UpperLeg_R": upper_leg_r,
    "LowerLeg_R": lower_leg_r,
    "Foot_R": foot_r
}


print("Bone mapping:")
print("--------------------------------------")

for name, bone in bones.items():

    if bone:

        print("FOUND   :", name)

    else:

        print("MISSING :", name)

print("--------------------------------------")
print("")


# ============================================================
# 8. CREATE / REPLACE IDLE ACTION
# ============================================================

old_action = bpy.data.actions.get(
    "Skomma_Idle"
)


if old_action:

    bpy.data.actions.remove(
        old_action
    )


action = bpy.data.actions.new(
    "Skomma_Idle"
)


# ============================================================
# 9. ASSIGN ACTION TO RIG
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


rig.animation_data.action = action


action.use_fake_user = True


# ============================================================
# 10. ANIMATION SETTINGS
# ============================================================

scene = bpy.context.scene

scene.frame_start = 1

scene.frame_end = 60

scene.render.fps = 30


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
# 13. RESET BODY TO REST ROTATION
# ============================================================
#
# IMPORTANT:
#
# We DO NOT rotate the arms into position.
#
# Your new skeleton already has the arms close
# to the body.
#
# Therefore:
#
#     UpperArm = 0
#     LowerArm = 0
#     Hand     = 0
#
# This preserves the skeleton's standing position.
#
# ============================================================

def normal_standing(frame):


    # ========================================================
    # ROOT
    # ========================================================

    key_rotation(
        root,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # HIPS
    # ========================================================

    key_rotation(
        hips,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # SPINE
    # ========================================================

    key_rotation(
        spine,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # CHEST
    # ========================================================

    key_rotation(
        chest,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # NECK
    # ========================================================

    key_rotation(
        neck,
        frame,
        0,
        0,
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
        0
    )


    # ========================================================
    # LEFT ARM
    #
    # DO NOT MOVE THE ARM.
    #
    # The skeleton rest position already places
    # the arm beside the body.
    # ========================================================

    key_rotation(
        upper_arm_l,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        lower_arm_l,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        hand_l,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # RIGHT ARM
    # ========================================================

    key_rotation(
        upper_arm_r,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        lower_arm_r,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        hand_r,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # LEFT LEG
    # ========================================================

    key_rotation(
        upper_leg_l,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        lower_leg_l,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        foot_l,
        frame,
        0,
        0,
        0
    )


    # ========================================================
    # RIGHT LEG
    # ========================================================

    key_rotation(
        upper_leg_r,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        lower_leg_r,
        frame,
        0,
        0,
        0
    )


    key_rotation(
        foot_r,
        frame,
        0,
        0,
        0
    )


# ============================================================
# 14. FRAME 1
# ============================================================

normal_standing(1)


# ============================================================
# 15. FRAME 15
#
# SMALL INHALE
# ============================================================

key_rotation(
    spine,
    15,
    -1.2,
    0,
    0
)


key_rotation(
    chest,
    15,
    -1.8,
    0,
    0
)


# Small shoulder movement
#
# IMPORTANT:
# Only very small movement.
#
# The arms remain beside the body.

key_rotation(
    upper_arm_l,
    15,
    0,
    0,
    -1.0
)


key_rotation(
    upper_arm_r,
    15,
    0,
    0,
    1.0
)


# ============================================================
# 16. FRAME 30
#
# RETURN TO NORMAL
# ============================================================

normal_standing(30)


# ============================================================
# 17. FRAME 45
#
# SECOND SMALL INHALE
# ============================================================

key_rotation(
    spine,
    45,
    -1.2,
    0,
    0
)


key_rotation(
    chest,
    45,
    -1.8,
    0,
    0
)


key_rotation(
    upper_arm_l,
    45,
    0,
    0,
    -1.0
)


key_rotation(
    upper_arm_r,
    45,
    0,
    0,
    1.0
)


# ============================================================
# 18. FRAME 60
#
# RETURN TO EXACT FRAME 1
# ============================================================

normal_standing(60)


# ============================================================
# 19. NATURAL HEAD MOVEMENT
# ============================================================

if head:


    # --------------------------------------------------------
    # FRAME 1
    # --------------------------------------------------------

    key_rotation(
        head,
        1,
        0,
        0,
        -1.0
    )


    # --------------------------------------------------------
    # FRAME 15
    # --------------------------------------------------------

    key_rotation(
        head,
        15,
        0.5,
        0,
        -0.3
    )


    # --------------------------------------------------------
    # FRAME 30
    # --------------------------------------------------------

    key_rotation(
        head,
        30,
        0,
        0,
        1.0
    )


    # --------------------------------------------------------
    # FRAME 45
    # --------------------------------------------------------

    key_rotation(
        head,
        45,
        -0.5,
        0,
        0.3
    )


    # --------------------------------------------------------
    # FRAME 60
    # --------------------------------------------------------

    key_rotation(
        head,
        60,
        0,
        0,
        -1.0
    )


# ============================================================
# 20. SUBTLE NECK MOVEMENT
# ============================================================

if neck:


    key_rotation(
        neck,
        1,
        0,
        0,
        0
    )


    key_rotation(
        neck,
        30,
        0,
        0,
        0.4
    )


    key_rotation(
        neck,
        60,
        0,
        0,
        0
    )


# ============================================================
# 21. SUBTLE HIPS MOVEMENT
# ============================================================
#
# Very small movement.
#
# This prevents the character from looking completely
# frozen while standing.
#
# ============================================================

if hips:


    key_rotation(
        hips,
        1,
        0,
        0,
        0
    )


    key_rotation(
        hips,
        30,
        0,
        0,
        -0.25
    )


    key_rotation(
        hips,
        60,
        0,
        0,
        0
    )


# ============================================================
# 22. MAKE ALL KEYFRAMES SMOOTH
# ============================================================

if action.fcurves:

    for fcurve in action.fcurves:

        for keyframe in fcurve.keyframe_points:

            keyframe.interpolation = 'BEZIER'


# ============================================================
# 23. MAKE ANIMATION LOOP
# ============================================================

if action.fcurves:

    for fcurve in action.fcurves:

        modifier = fcurve.modifiers.new(
            type='CYCLES'
        )


# ============================================================
# 24. FRAME SET
# ============================================================

scene.frame_set(1)


# ============================================================
# 25. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 26. FINISHED
# ============================================================

print("")
print("======================================")
print("SKOMMA IDLE ANIMATION COMPLETE")
print("======================================")
print("")

print("Animation:")
print("    Skomma_Idle")
print("")

print("Frames:")
print("    1 - 60")
print("")

print("FPS:")
print("    30")
print("")

print("Character:")
print("    Normal Standing")
print("")

print("======================================")
print("ARM POSITION")
print("======================================")
print("")

print("Left Arm:")
print("    Beside body")
print("    No T-Pose")
print("")

print("Right Arm:")
print("    Beside body")
print("    No T-Pose")
print("")

print("Hands:")
print("    Close to body")
print("    Relaxed")
print("    No finger animation")
print("")

print("======================================")
print("ANIMATION")
print("======================================")
print("")

print("Breathing:")
print("    Subtle")
print("")

print("Chest:")
print("    Small movement")
print("")

print("Spine:")
print("    Small movement")
print("")

print("Head:")
print("    Small natural movement")
print("")

print("Hips:")
print("    Very small natural movement")
print("")

print("======================================")
print("SKELETON")
print("======================================")
print("")

print("Existing skeleton:")
print("    YES")

print("New bones:")
print("    NONE")

print("IK:")
print("    Existing IK preserved")

print("New GLB:")
print("    NONE")

print("Blender file saved:")
print("    NO")

print("")
print("======================================")
print("DONE")
print("======================================")