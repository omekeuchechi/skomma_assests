import bpy
import math


# ============================================================
# SKOMMA HUMANOID V1
# ATTACK ANIMATION SYSTEM
# ============================================================
#
# Creates:
#
#     Skomma_Punch
#     Skomma_Kick
#
# NLA:
#
#     Skomma_Punch
#         └── Skomma_Punch
#
#     Skomma_Kick
#         └── Skomma_Kick
#
# Existing animations are preserved:
#
#     Skomma_Idle
#     Skomma_Walk
#     Skomma_Run
#     Skomma_Jump
#
#
# IMPORTANT:
#
# - Existing skeleton ONLY
# - Existing IK ONLY
# - No new bones
# - No new controls
# - No new GLB
# - No Blender file saving
#
# ============================================================


print("")
print("==============================================")
print("SKOMMA HUMANOID V1")
print("ATTACK ANIMATION SYSTEM")
print("==============================================")
print("")


# ============================================================
# 1. FIND EXISTING RIG
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
# 2. CREATE ANIMATION DATA
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


animation_data = rig.animation_data


# ============================================================
# 3. REMEMBER CURRENT ACTIVE ACTION
# ============================================================

original_action = animation_data.action


if original_action:

    print(
        "Original active Action:",
        original_action.name
    )

else:

    print("No active Action.")


print("")


# ============================================================
# 4. BONE FINDER
# ============================================================

def get_bone(name):

    bone = rig.pose.bones.get(name)

    if bone is None:

        raise RuntimeError(
            "Required bone not found: " + name
        )

    return bone


# ============================================================
# 5. EXISTING BODY BONES
# ============================================================

root = get_bone("Root")

hips = get_bone("Hips")

spine = get_bone("Spine")

chest = get_bone("Chest")

head = get_bone("Head")


# ============================================================
# 6. EXISTING IK CONTROLS
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
# 7. DELETE ONLY OLD ATTACK ANIMATIONS
# ============================================================
#
# We remove:
#
#     Skomma_Punch
#     Skomma_Kick
#
# Nothing else.
#
# ============================================================

attack_names = [
    "Skomma_Punch",
    "Skomma_Kick"
]


for animation_name in attack_names:

    # --------------------------------------------------------
    # Remove existing NLA strips
    # --------------------------------------------------------

    for track in list(
        animation_data.nla_tracks
    ):

        for strip in list(
            track.strips
        ):

            if (

                strip.name == animation_name

                or

                (
                    strip.action
                    and
                    strip.action.name == animation_name
                )

            ):

                track.strips.remove(
                    strip
                )


    # --------------------------------------------------------
    # Remove existing Action
    # --------------------------------------------------------

    old_action = bpy.data.actions.get(
        animation_name
    )


    if old_action:

        print(
            "Removing old Action:",
            animation_name
        )

        bpy.data.actions.remove(
            old_action
        )


# ============================================================
# 8. SAVE SCENE SETTINGS
# ============================================================

scene = bpy.context.scene

old_frame_start = scene.frame_start

old_frame_end = scene.frame_end

old_fps = scene.render.fps


scene.render.fps = 30


# ============================================================
# 9. KEYFRAME HELPERS
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
# 10. BODY POSE
# ============================================================

def body_pose(
    frame,

    root_x=0,
    root_y=0,
    root_z=0,

    hip_y=0,

    spine_y=0,

    chest_y=0,

    head_z=0
):

    key_location(
        root,
        frame,
        root_x,
        root_y,
        root_z
    )


    key_rotation(
        hips,
        frame,
        0,
        hip_y,
        0
    )


    key_rotation(
        spine,
        frame,
        0,
        spine_y,
        0
    )


    key_rotation(
        chest,
        frame,
        0,
        chest_y,
        0
    )


    key_rotation(
        head,
        frame,
        0,
        0,
        head_z
    )


# ============================================================
# 11. ARM POSE
# ============================================================

def arm_pose(
    frame,

    left_y=0,
    left_z=0,

    right_y=0,
    right_z=0
):

    key_location(
        hand_ik_l,
        frame,
        0,
        left_y,
        left_z
    )


    key_location(
        hand_ik_r,
        frame,
        0,
        right_y,
        right_z
    )


# ============================================================
# 12. LEG POSE
# ============================================================

def leg_pose(
    frame,

    left_y=0,
    left_z=0,

    right_y=0,
    right_z=0
):

    key_location(
        foot_ik_l,
        frame,
        0,
        left_y,
        left_z
    )


    key_location(
        foot_ik_r,
        frame,
        0,
        right_y,
        right_z
    )


# ============================================================
# 13. CREATE NLA TRACK + STRIP
# ============================================================

def add_nla_animation(
    action,
    start_frame,
    end_frame
):

    # --------------------------------------------------------
    # Create dedicated NLA track
    # --------------------------------------------------------

    track = animation_data.nla_tracks.new()

    track.name = action.name


    # --------------------------------------------------------
    # Create Action Clip
    # --------------------------------------------------------

    strip = track.strips.new(

        action.name,

        start_frame,

        action

    )


    # --------------------------------------------------------
    # Action range
    # --------------------------------------------------------

    strip.action_frame_start = (
        action.frame_start
    )

    strip.action_frame_end = (
        action.frame_end
    )


    # --------------------------------------------------------
    # NLA range
    # --------------------------------------------------------

    strip.frame_start = start_frame

    strip.frame_end = end_frame


    # --------------------------------------------------------
    # Attack is NOT looping
    # --------------------------------------------------------

    strip.repeat = 1.0


    # --------------------------------------------------------
    # Full animation replacement
    # --------------------------------------------------------

    strip.blend_type = 'REPLACE'

    strip.influence = 1.0

    strip.extrapolation = 'NOTHING'


    # --------------------------------------------------------
    # Select strip
    # --------------------------------------------------------

    strip.select = True


    return track, strip


# ============================================================
# 14. CREATE PUNCH ACTION
# ============================================================

print("")
print("Creating Skomma_Punch...")
print("")


punch_action = bpy.data.actions.new(
    "Skomma_Punch"
)


punch_action.use_fake_user = True


animation_data.action = punch_action


scene.frame_start = 1

scene.frame_end = 20


# ============================================================
# PUNCH FRAME 1
#
# NEUTRAL
# ============================================================

body_pose(

    1,

    0,
    0,
    0,

    0,
    0,
    0,

    0

)


arm_pose(

    1,

    0,
    0,

    0,
    0

)


leg_pose(

    1,

    0,
    0,

    0,
    0

)


# ============================================================
# PUNCH FRAME 4
#
# ANTICIPATION
#
# Right arm pulls backward.
# Body rotates slightly.
# ============================================================

body_pose(

    4,

    0,
    0,
    0,

    1.5,
    -1.0,
    -1.5,

    -0.5

)


arm_pose(

    4,

    # Left arm relaxed
    0.03,
    0,

    # Right arm pulled backward
    0.16,
    0.02

)


leg_pose(

    4,

    0,
    0,

    0,
    0

)


# ============================================================
# PUNCH FRAME 7
#
# EXTENSION
# ============================================================

body_pose(

    7,

    0,
    0,
    0,

    -1.5,
    1.0,
    1.5,

    0.5

)


arm_pose(

    7,

    # Left arm
    -0.02,
    0,

    # Right arm extending
    -0.20,
    0.02

)


# ============================================================
# PUNCH FRAME 10
#
# IMPACT
#
# Maximum extension.
# ============================================================

body_pose(

    10,

    0,
    -0.015,
    0.01,

    -2.0,
    1.5,
    2.0,

    1.0

)


arm_pose(

    10,

    -0.03,
    0,

    -0.28,
    0.03

)


# ============================================================
# PUNCH FRAME 13
#
# RETRACT
# ============================================================

body_pose(

    13,

    0,
    0,
    0,

    1.0,
    -0.5,
    -1.0,

    -0.5

)


arm_pose(

    13,

    0.02,
    0,

    0.12,
    0.01

)


# ============================================================
# PUNCH FRAME 16
#
# RECOVERY
# ============================================================

body_pose(

    16,

    0,
    0,
    0,

    0.3,
    -0.2,
    -0.3,

    0

)


arm_pose(

    16,

    0,
    0,

    0.03,
    0

)


# ============================================================
# PUNCH FRAME 20
#
# NEUTRAL
# ============================================================

body_pose(

    20,

    0,
    0,
    0,

    0,
    0,
    0,

    0

)


arm_pose(

    20,

    0,
    0,

    0,
    0

)


leg_pose(

    20,

    0,
    0,

    0,
    0

)


# ============================================================
# SMOOTH PUNCH
# ============================================================

for fcurve in punch_action.fcurves:

    for keyframe in fcurve.keyframe_points:

        keyframe.interpolation = 'BEZIER'


# ============================================================
# PUNCH METADATA
# ============================================================

punch_action.frame_start = 1

punch_action.frame_end = 20


punch_action["animation_type"] = "attack"

punch_action["attack_type"] = "punch"

punch_action["character"] = "skomma_humanoid_v1"

punch_action["animation_style"] = "blocky_humanoid"

punch_action["loop"] = False

punch_action["fps"] = 30

punch_action["frame_length"] = 20

punch_action["uses_existing_ik"] = True

punch_action["creates_new_bones"] = False

punch_action["creates_new_controls"] = False

punch_action["creates_new_glb"] = False


# ============================================================
# REMOVE FROM ACTIVE ACTION
# ============================================================

animation_data.action = None


# ============================================================
# ADD PUNCH TO NLA
# ============================================================

punch_track, punch_strip = add_nla_animation(

    punch_action,

    1,
    20

)


print("Punch added to NLA.")


# ============================================================
# 15. CREATE KICK ACTION
# ============================================================

print("")
print("Creating Skomma_Kick...")
print("")


kick_action = bpy.data.actions.new(
    "Skomma_Kick"
)


kick_action.use_fake_user = True


animation_data.action = kick_action


scene.frame_start = 1

scene.frame_end = 24


# ============================================================
# KICK FRAME 1
#
# NEUTRAL
# ============================================================

body_pose(

    1,

    0,
    0,
    0,

    0,
    0,
    0,

    0

)


arm_pose(

    1,

    0,
    0,

    0,
    0

)


leg_pose(

    1,

    0,
    0,

    0,
    0

)


# ============================================================
# KICK FRAME 5
#
# PREPARATION
#
# Body leans slightly back.
# ============================================================

body_pose(

    5,

    0,
    0,
    0,

    -2.0,
    2.0,
    2.0,

    -0.5

)


arm_pose(

    5,

    0.08,
    0.02,

    -0.08,
    0.02

)


leg_pose(

    5,

    0.03,
    0,

    0.10,
    0.02

)


# ============================================================
# KICK FRAME 8
#
# CHAMBER
#
# Right leg comes forward/up.
# ============================================================

body_pose(

    8,

    0,
    0,
    0,

    -3.0,
    2.5,
    2.0,

    -1.0

)


arm_pose(

    8,

    0.10,
    0.04,

    -0.10,
    0.04

)


leg_pose(

    8,

    -0.02,
    0.05,

    -0.08,
    0.22

)


# ============================================================
# KICK FRAME 12
#
# EXTENSION
# ============================================================

body_pose(

    12,

    0,
    -0.01,
    0.02,

    -2.0,
    1.5,
    1.5,

    -0.5

)


arm_pose(

    12,

    0.12,
    0.05,

    -0.12,
    0.05

)


leg_pose(

    12,

    -0.04,
    0.04,

    -0.30,
    0.12

)


# ============================================================
# KICK FRAME 14
#
# IMPACT
#
# Maximum extension.
# ============================================================

body_pose(

    14,

    0,
    -0.015,
    0.02,

    -2.5,
    1.5,
    1.5,

    -0.5

)


arm_pose(

    14,

    0.14,
    0.05,

    -0.14,
    0.05

)


leg_pose(

    14,

    -0.05,
    0.03,

    -0.38,
    0.10

)


# ============================================================
# KICK FRAME 17
#
# RETRACT
# ============================================================

body_pose(

    17,

    0,
    0,
    0,

    1.5,
    -1.0,
    -1.0,

    0.5

)


arm_pose(

    17,

    0.05,
    0.01,

    -0.05,
    0.01

)


leg_pose(

    17,

    0.02,
    0,

    0.08,
    0.08

)


# ============================================================
# KICK FRAME 20
#
# RECOVERY
# ============================================================

body_pose(

    20,

    0,
    0,
    0,

    0.5,
    -0.3,
    -0.5,

    0

)


arm_pose(

    20,

    0.02,
    0,

    -0.02,
    0

)


leg_pose(

    20,

    0,
    0,

    0,
    0

)


# ============================================================
# KICK FRAME 24
#
# NEUTRAL
# ============================================================

body_pose(

    24,

    0,
    0,
    0,

    0,
    0,
    0,

    0

)


arm_pose(

    24,

    0,
    0,

    0,
    0

)


leg_pose(

    24,

    0,
    0,

    0,
    0

)


# ============================================================
# SMOOTH KICK
# ============================================================

for fcurve in kick_action.fcurves:

    for keyframe in fcurve.keyframe_points:

        keyframe.interpolation = 'BEZIER'


# ============================================================
# KICK METADATA
# ============================================================

kick_action.frame_start = 1

kick_action.frame_end = 24


kick_action["animation_type"] = "attack"

kick_action["attack_type"] = "kick"

kick_action["character"] = "skomma_humanoid_v1"

kick_action["animation_style"] = "blocky_humanoid"

kick_action["loop"] = False

kick_action["fps"] = 30

kick_action["frame_length"] = 24

kick_action["uses_existing_ik"] = True

kick_action["creates_new_bones"] = False

kick_action["creates_new_controls"] = False

kick_action["creates_new_glb"] = False


# ============================================================
# REMOVE FROM ACTIVE ACTION
# ============================================================

animation_data.action = None


# ============================================================
# ADD KICK TO NLA
# ============================================================

kick_track, kick_strip = add_nla_animation(

    kick_action,

    1,
    24

)


print("Kick added to NLA.")


# ============================================================
# 16. MUTE ATTACK TRACKS AFTER CREATION
# ============================================================
#
# The animations are stored in the NLA library but are not
# automatically playing on top of the character.
#
# This is important.
#
# Your game can later activate:
#
#     Punch
# OR
#     Kick
#
# ============================================================

punch_track.mute = True

kick_track.mute = True


punch_strip.select = False

kick_strip.select = False


# ============================================================
# 17. RESTORE ORIGINAL ACTION
# ============================================================
#
# Do NOT leave Punch or Kick in the active Action slot.
#
# Existing animation system remains untouched.
#
# ============================================================

animation_data.action = original_action


# ============================================================
# 18. RESTORE SCENE SETTINGS
# ============================================================

scene.frame_start = old_frame_start

scene.frame_end = old_frame_end

scene.render.fps = old_fps


scene.frame_set(
    old_frame_start
)


# ============================================================
# 19. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 20. VERIFY ACTIONS
# ============================================================

print("")
print("==============================================")
print("SKOMMA ATTACK ANIMATION LIBRARY")
print("==============================================")
print("")


for animation_name in [

    "Skomma_Idle",
    "Skomma_Walk",
    "Skomma_Run",
    "Skomma_Jump",
    "Skomma_Punch",
    "Skomma_Kick"

]:

    action = bpy.data.actions.get(
        animation_name
    )


    if action:

        print(
            "ACTION FOUND:",
            animation_name
        )

    else:

        print(
            "ACTION MISSING:",
            animation_name
        )


# ============================================================
# 21. VERIFY NLA
# ============================================================

print("")
print("==============================================")
print("SKOMMA NLA STRUCTURE")
print("==============================================")
print("")


for track in animation_data.nla_tracks:

    if not track.name.startswith(
        "Skomma_"
    ):

        continue


    print(
        "TRACK:",
        track.name
    )


    for strip in track.strips:

        action_name = "None"


        if strip.action:

            action_name = (
                strip.action.name
            )


        print(
            "    STRIP:",
            strip.name,
            "->",
            action_name
        )


    print("")


# ============================================================
# 22. FINAL INFORMATION
# ============================================================

print("")
print("==============================================")
print("SKOMMA ATTACK SYSTEM COMPLETE")
print("==============================================")
print("")

print("Created Actions:")
print("    Skomma_Punch")
print("    Skomma_Kick")
print("")

print("NLA Tracks:")
print("    Skomma_Punch")
print("    Skomma_Kick")
print("")

print("Punch:")
print("    20 frames")
print("    30 FPS")
print("    NON-LOOPING")
print("")

print("Kick:")
print("    24 frames")
print("    30 FPS")
print("    NON-LOOPING")
print("")

print("Existing animations preserved:")
print("    Skomma_Idle")
print("    Skomma_Walk")
print("    Skomma_Run")
print("    Skomma_Jump")
print("")

print("Skeleton:")
print("    EXISTING ONLY")
print("")

print("Bones created:")
print("    NONE")
print("")

print("Controls created:")
print("    NONE")
print("")

print("GLB created:")
print("    NONE")
print("")

print("Blender file saved:")
print("    NO")
print("")

print("==============================================")