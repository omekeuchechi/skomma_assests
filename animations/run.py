import bpy
import math


# ============================================================
# SKOMMA HUMANOID V1
# RUNNING ANIMATION
# ============================================================
#
# IMPORTANT
#
# This script works with the NEW SKOMMA ANIMATION LIBRARY.
#
# Existing animations:
#
#     Skomma_Idle
#     Skomma_Walk
#
# New animation:
#
#     Skomma_Run
#
# NLA structure:
#
#     Skomma_Idle
#     Skomma_Walk
#     Skomma_Run
#
# IMPORTANT:
#
# - Uses EXISTING skeleton
# - Uses EXISTING IK
# - Does NOT create bones
# - Does NOT create a GLB
# - Does NOT save Blender
# - Does NOT delete Idle
# - Does NOT delete Walk
# - Creates only Skomma_Run
# - Adds Run to its own NLA track
#
# ============================================================


print("")
print("======================================")
print("SKOMMA HUMANOID V1 - RUN ANIMATION")
print("======================================")
print("")


# ============================================================
# 1. FIND EXISTING SKOMMA RIG
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


# Fallback search

if rig is None:

    for obj in bpy.data.objects:

        if obj.type == 'ARMATURE':

            rig = obj
            break


if rig is None:

    raise RuntimeError(
        "No existing SKOMMA humanoid armature found."
    )


print("Existing rig:")
print("    ", rig.name)
print("")


# ============================================================
# 2. CHECK EXISTING ANIMATION LIBRARY
# ============================================================

idle_action = bpy.data.actions.get(
    "Skomma_Idle"
)

walk_action = bpy.data.actions.get(
    "Skomma_Walk"
)

old_run_action = bpy.data.actions.get(
    "Skomma_Run"
)


print("Animation library:")
print("--------------------------------------")


if idle_action:

    print("FOUND   : Skomma_Idle")

else:

    print("MISSING : Skomma_Idle")


if walk_action:

    print("FOUND   : Skomma_Walk")

else:

    print("MISSING : Skomma_Walk")


if old_run_action:

    print("FOUND   : Skomma_Run")

else:

    print("NEW     : Skomma_Run")


print("--------------------------------------")
print("")


# ============================================================
# 3. CHECK REQUIRED BONES
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


print("Checking skeleton:")
print("--------------------------------------")


for name in required_bones:

    if rig.pose.bones.get(name):

        print("FOUND   :", name)

    else:

        print("MISSING :", name)


print("--------------------------------------")
print("")


# ============================================================
# 4. GET BONE
# ============================================================

def get_bone(name):

    bone = rig.pose.bones.get(name)

    if bone is None:

        raise RuntimeError(
            "Required bone not found: " + name
        )

    return bone


# ============================================================
# 5. BODY BONES
# ============================================================

root = get_bone("Root")

hips = get_bone("Hips")

spine = get_bone("Spine")

chest = get_bone("Chest")

neck = get_bone("Neck")

head = get_bone("Head")


# ============================================================
# 6. ARM BONES
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
# 7. LEG BONES
# ============================================================

left_upper_leg = get_bone(
    "UpperLeg_L"
)

left_lower_leg = get_bone(
    "LowerLeg_L"
)


right_upper_leg = get_bone(
    "UpperLeg_R"
)

right_lower_leg = get_bone(
    "LowerLeg_R"
)


# ============================================================
# 8. IK CONTROLS
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
# 9. REMOVE ONLY OLD RUN ACTION
# ============================================================
#
# NEVER remove:
#
#     Skomma_Idle
#     Skomma_Walk
#
# ============================================================

if old_run_action:

    print("Removing old Skomma_Run action...")

    bpy.data.actions.remove(
        old_run_action
    )


# ============================================================
# 10. REMOVE ONLY OLD RUN NLA TRACK
# ============================================================

if rig.animation_data:

    for track in list(
        rig.animation_data.nla_tracks
    ):

        if track.name == "Skomma_Run":

            print(
                "Removing old Skomma_Run NLA track..."
            )

            rig.animation_data.nla_tracks.remove(
                track
            )


# ============================================================
# 11. CREATE RUN ACTION
# ============================================================

run_action = bpy.data.actions.new(
    "Skomma_Run"
)

run_action.use_fake_user = True


# ============================================================
# 12. MAKE SURE ANIMATION DATA EXISTS
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


# Temporarily make Run active
# so Blender accepts the keyframes.

rig.animation_data.action = run_action


# ============================================================
# 13. ANIMATION SETTINGS
# ============================================================

scene = bpy.context.scene

old_scene_start = scene.frame_start
old_scene_end = scene.frame_end


scene.render.fps = 30

scene.frame_start = 1
scene.frame_end = 19


# ============================================================
# 14. ROTATION HELPER
# ============================================================

def key_rotation(
    bone,
    frame,
    x=0,
    y=0,
    z=0
):

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
# 15. LOCATION HELPER
# ============================================================

def key_location(
    bone,
    frame,
    x=0,
    y=0,
    z=0
):

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
# 16. RUN POSE
# ============================================================
#
# The run uses EXISTING IK.
#
# Feet:
#     larger stride
#     higher lift
#
# Hands:
#     stronger forward/back swing
#     still close to body
#
# Body:
#     forward lean
#     stronger bounce
#
# ============================================================

def run_pose(

    frame,

    left_foot_y,
    left_foot_z,

    right_foot_y,
    right_foot_z,

    left_hand_y,
    right_hand_y,

    body_z=0,

    hip_rotation=0,

    torso_lean=0,

    head_rotation=0
):


    # ========================================================
    # ROOT
    # ========================================================

    key_location(
        root,
        frame,
        0,
        0,
        body_z
    )


    # ========================================================
    # HIPS
    # ========================================================

    key_rotation(
        hips,
        frame,
        torso_lean,
        hip_rotation,
        0
    )


    # ========================================================
    # SPINE
    # ========================================================

    key_rotation(
        spine,
        frame,
        torso_lean * 0.35,
        -hip_rotation * 0.30,
        0
    )


    # ========================================================
    # CHEST
    # ========================================================

    key_rotation(
        chest,
        frame,
        torso_lean * 0.25,
        -hip_rotation * 0.20,
        0
    )


    # ========================================================
    # NECK
    # ========================================================

    key_rotation(
        neck,
        frame,
        -torso_lean * 0.15,
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
        head_rotation
    )


    # ========================================================
    # LEFT FOOT
    # ========================================================

    key_location(
        foot_ik_l,
        frame,
        0,
        left_foot_y,
        left_foot_z
    )


    # ========================================================
    # RIGHT FOOT
    # ========================================================

    key_location(
        foot_ik_r,
        frame,
        0,
        right_foot_y,
        right_foot_z
    )


    # ========================================================
    # LEFT HAND
    # ========================================================

    key_location(
        hand_ik_l,
        frame,
        0,
        left_hand_y,
        0
    )


    # ========================================================
    # RIGHT HAND
    # ========================================================

    key_location(
        hand_ik_r,
        frame,
        0,
        right_hand_y,
        0
    )


# ============================================================
# 17. RUN CYCLE
# ============================================================
#
# 19 frames
#
# 1  = Left contact
# 4  = Left push
# 7  = Right passing
# 10 = Right contact
# 13 = Right push
# 16 = Left passing
# 19 = Left contact
#
# ============================================================


# ============================================================
# FRAME 1
# LEFT FOOT FORWARD
# RIGHT FOOT BACK
# ============================================================

run_pose(

    1,

    # Left foot
    -0.34,
    0.00,

    # Right foot
    0.28,
    0.00,

    # Left hand
    0.17,

    # Right hand
    -0.17,

    # Body
    0.00,

    # Hip rotation
    -3.0,

    # Forward lean
    -4.0,

    # Head
    -1.0

)


# ============================================================
# FRAME 4
# LEFT PUSH
# ============================================================

run_pose(

    4,

    -0.20,
    0.08,

    0.10,
    0.03,

    0.10,
    -0.10,

    0.045,

    -1.5,

    -4.5,

    -0.5

)


# ============================================================
# FRAME 7
# PASSING
# ============================================================

run_pose(

    7,

    -0.03,
    0.15,

    -0.02,
    0.08,

    0.00,
    0.00,

    0.085,

    0,

    -5.0,

    0.5

)


# ============================================================
# FRAME 10
# RIGHT FOOT FORWARD
# ============================================================

run_pose(

    10,

    0.28,
    0.00,

    -0.34,
    0.00,

    -0.17,
    0.17,

    0.00,

    3.0,

    -4.0,

    1.0

)


# ============================================================
# FRAME 13
# RIGHT PUSH
# ============================================================

run_pose(

    13,

    0.10,
    0.03,

    -0.20,
    0.08,

    -0.10,
    0.10,

    0.045,

    1.5,

    -4.5,

    0.5

)


# ============================================================
# FRAME 16
# PASSING
# ============================================================

run_pose(

    16,

    0.02,
    0.08,

    0.03,
    0.15,

    0.00,
    0.00,

    0.085,

    0,

    -5.0,

    -0.5

)


# ============================================================
# FRAME 19
# SAME AS FRAME 1
# ============================================================

run_pose(

    19,

    -0.34,
    0.00,

    0.28,
    0.00,

    0.17,
    -0.17,

    0.00,

    -3.0,

    -4.0,

    -1.0

)


# ============================================================
# 18. SMOOTH CURVES
# ============================================================

if run_action.fcurves:

    for fcurve in run_action.fcurves:

        for keyframe in fcurve.keyframe_points:

            keyframe.interpolation = 'BEZIER'


# ============================================================
# 19. MAKE ACTION LOOP
# ============================================================

for fcurve in run_action.fcurves:

    # Remove previous cycles modifiers if any

    for modifier in list(
        fcurve.modifiers
    ):

        if modifier.type == 'CYCLES':

            fcurve.modifiers.remove(
                modifier
            )

    fcurve.modifiers.new(
        type='CYCLES'
    )


# ============================================================
# 20. RUN ACTION INFORMATION
# ============================================================

run_action.frame_start = 1

run_action.frame_end = 19


run_action["animation_type"] = "run"

run_action["character"] = (
    "skomma_humanoid_v1"
)

run_action["animation_style"] = (
    "blocky_humanoid"
)

run_action["loop"] = True

run_action["fps"] = 30

run_action["frame_length"] = 19

run_action["uses_existing_ik"] = True

run_action["creates_new_bones"] = False

run_action["creates_new_glb"] = False


# ============================================================
# 21. CREATE NLA TRACK
# ============================================================
#
# IMPORTANT:
#
# This is the NEW animation-library structure.
#
# Existing:
#
#     Skomma_Idle
#     Skomma_Walk
#
# New:
#
#     Skomma_Run
#
# ============================================================

run_track = rig.animation_data.nla_tracks.new()

run_track.name = "Skomma_Run"


# ============================================================
# 22. CREATE RUN STRIP
# ============================================================

run_strip = run_track.strips.new(

    "Skomma_Run",

    1,

    run_action

)


# ============================================================
# 23. CONFIGURE RUN STRIP
# ============================================================

run_strip.action_frame_start = 1

run_strip.action_frame_end = 19

run_strip.frame_start = 1

run_strip.frame_end = 19

run_strip.repeat = 1.0


# ============================================================
# 24. RUN SHOULD NOT REPLACE IDLE
# ============================================================
#
# IMPORTANT:
#
# Idle remains the default animation.
#
# Walk remains available.
#
# Run is added but muted.
#
# ============================================================

run_track.mute = True

run_track.is_solo = False


# ============================================================
# 25. KEEP EXISTING IDLE DEFAULT
# ============================================================

if rig.animation_data:

    for track in rig.animation_data.nla_tracks:

        if track.name == "Skomma_Idle":

            track.mute = False

            track.is_solo = True

        elif track.name == "Skomma_Walk":

            track.mute = True

            track.is_solo = False

        elif track.name == "Skomma_Run":

            track.mute = True

            track.is_solo = False


# ============================================================
# 26. REMOVE ACTIVE ACTION
# ============================================================
#
# NLA is now responsible for playback.
#
# ============================================================

rig.animation_data.action = None


# ============================================================
# 27. RESTORE SCENE RANGE
# ============================================================

scene.frame_start = old_scene_start

scene.frame_end = old_scene_end

scene.frame_set(1)


# ============================================================
# 28. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 29. VERIFY ANIMATION LIBRARY
# ============================================================

print("")
print("======================================")
print("SKOMMA ANIMATION LIBRARY")
print("======================================")
print("")


print("Actions:")
print("--------------------------------------")


for action in bpy.data.actions:

    if action.name.startswith(
        "Skomma_"
    ):

        print(
            "FOUND:",
            action.name
        )


print("--------------------------------------")
print("")


print("NLA Tracks:")
print("--------------------------------------")


for track in rig.animation_data.nla_tracks:

    print(
        "TRACK:",
        track.name
    )

    for strip in track.strips:

        print(
            "    STRIP:",
            strip.name
        )


print("--------------------------------------")
print("")


# ============================================================
# 30. FINAL
# ============================================================

print("======================================")
print("SKOMMA RUN ANIMATION COMPLETE")
print("======================================")
print("")

print("Created:")
print("    Skomma_Run")
print("")

print("Existing animations:")
print("    Skomma_Idle  -> PRESERVED")
print("    Skomma_Walk  -> PRESERVED")
print("")

print("NLA:")
print("    Skomma_Idle")
print("    Skomma_Walk")
print("    Skomma_Run")
print("")

print("Default:")
print("    Skomma_Idle")
print("")

print("Run:")
print("    CREATED")
print("    MUTED BY DEFAULT")
print("")

print("Run cycle:")
print("    19 frames")
print("    30 FPS")
print("    LOOPING")
print("")

print("Movement:")
print("    Larger stride")
print("    Higher foot lift")
print("    Faster arm swing")
print("    Stronger body bounce")
print("    Forward running lean")
print("")

print("Skeleton:")
print("    EXISTING ONLY")
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