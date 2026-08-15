import bpy
import math


# ============================================================
# SKOMMA HUMANOID V1
# JUMP ANIMATION + NLA ORGANIZATION
# ============================================================
#
# IMPORTANT
#
# EXISTING:
#
#     Skomma_Idle
#     Skomma_Walk
#     Skomma_Run
#
# NEW:
#
#     Skomma_Jump
#
# NLA:
#
#     Skomma_Idle
#     Skomma_Walk
#     Skomma_Run
#     Skomma_Jump
#
# Each animation has:
#
#     ACTION
#        +
#     NLA STRIP
#
# No new skeleton.
# No new bones.
# No new controls.
# No new GLB.
#
# ============================================================


print("")
print("==============================================")
print("SKOMMA HUMANOID V1")
print("JUMP + NLA ANIMATION SYSTEM")
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
print("   ", rig.name)
print("")


# ============================================================
# 2. VERIFY EXISTING ANIMATIONS
# ============================================================

print("Existing Skomma animations:")
print("----------------------------------------------")


for animation_name in [
    "Skomma_Idle",
    "Skomma_Walk",
    "Skomma_Run"
]:

    act = bpy.data.actions.get(animation_name)

    if act:

        print("FOUND   :", animation_name)

    else:

        print("MISSING :", animation_name)


print("----------------------------------------------")
print("")


# ============================================================
# 3. CREATE ANIMATION DATA IF NEEDED
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


# ============================================================
# 4. REMEMBER CURRENT ACTIVE ACTION
# ============================================================

original_action = rig.animation_data.action


if original_action:

    print(
        "Original active action:",
        original_action.name
    )

else:

    print("No original active action.")


print("")


# ============================================================
# 5. BONE FINDER
# ============================================================

def get_bone(name):

    bone = rig.pose.bones.get(name)

    if bone is None:

        raise RuntimeError(
            "Required bone not found: " + name
        )

    return bone


# ============================================================
# 6. EXISTING BONES
# ============================================================

root = get_bone("Root")

hips = get_bone("Hips")

spine = get_bone("Spine")

chest = get_bone("Chest")

neck = get_bone("Neck")

head = get_bone("Head")


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
# 7. REMOVE OLD JUMP ACTION
# ============================================================
#
# ONLY Skomma_Jump is replaced.
#
# Idle / Walk / Run are untouched.
#
# ============================================================

old_jump = bpy.data.actions.get(
    "Skomma_Jump"
)


if old_jump:

    print("Removing old Skomma_Jump action.")

    bpy.data.actions.remove(
        old_jump
    )


# ============================================================
# 8. REMOVE OLD JUMP NLA STRIPS
# ============================================================
#
# This prevents duplicate Jump strips when the script
# is run multiple times.
#
# ============================================================

for track in list(
    rig.animation_data.nla_tracks
):

    for strip in list(track.strips):

        if (
            strip.name == "Skomma_Jump"
            or
            (
                strip.action
                and
                strip.action.name == "Skomma_Jump"
            )
        ):

            print(
                "Removing old Jump NLA strip."
            )

            track.strips.remove(
                strip
            )


# ============================================================
# 9. CREATE JUMP ACTION
# ============================================================

action = bpy.data.actions.new(
    "Skomma_Jump"
)

action.use_fake_user = True


print("")
print("Created Action:")
print("    Skomma_Jump")
print("")


# ============================================================
# 10. TEMPORARILY MAKE JUMP ACTIVE
# ============================================================
#
# We need an active Action while inserting keyframes.
#
# AFTER keyframing:
#
#     action -> removed from active slot
#     action -> placed into NLA
#
# ============================================================

rig.animation_data.action = action


# ============================================================
# 11. SCENE SETTINGS
# ============================================================

scene = bpy.context.scene

old_scene_start = scene.frame_start
old_scene_end = scene.frame_end
old_fps = scene.render.fps


scene.render.fps = 30

scene.frame_start = 1

scene.frame_end = 36


# ============================================================
# 12. ROTATION HELPER
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
# 13. LOCATION HELPER
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
# 14. BODY POSE
# ============================================================

def body_pose(
    frame,

    root_z=0,

    hip_y=0,

    spine_y=0,

    chest_y=0,

    head_z=0
):

    key_location(
        root,
        frame,
        0,
        0,
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
# 15. LEG POSE
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
# 16. ARM POSE
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
# 17. COMPLETE JUMP POSE
# ============================================================

def jump_pose(

    frame,

    root_z,

    hip_y,

    spine_y,

    chest_y,

    head_z,

    left_foot_y,
    left_foot_z,

    right_foot_y,
    right_foot_z,

    left_hand_y,
    left_hand_z,

    right_hand_y,
    right_hand_z

):

    body_pose(

        frame,

        root_z,

        hip_y,

        spine_y,

        chest_y,

        head_z

    )


    leg_pose(

        frame,

        left_foot_y,
        left_foot_z,

        right_foot_y,
        right_foot_z

    )


    arm_pose(

        frame,

        left_hand_y,
        left_hand_z,

        right_hand_y,
        right_hand_z

    )


# ============================================================
# 18. JUMP ANIMATION
# ============================================================


# ------------------------------------------------------------
# FRAME 1
# NEUTRAL
# ------------------------------------------------------------

jump_pose(

    1,

    0.00,

    0,
    0,
    0,

    0,

    0,
    0,

    0,
    0,

    0,
    0,

    0,
    0

)


# ------------------------------------------------------------
# FRAME 5
# ANTICIPATION
# ------------------------------------------------------------

jump_pose(

    5,

    -0.10,

    -2.0,
    2.0,
    3.0,

    -1.0,

    0,
    0,

    0,
    0,

    0.12,
    -0.05,

    -0.12,
    -0.05

)


# ------------------------------------------------------------
# FRAME 8
# DEEP CROUCH
# ------------------------------------------------------------

jump_pose(

    8,

    -0.22,

    -4.0,
    3.0,
    4.0,

    -2.0,

    0,
    0,

    0,
    0,

    0.18,
    -0.10,

    -0.18,
    -0.10

)


# ------------------------------------------------------------
# FRAME 10
# TAKEOFF
# ------------------------------------------------------------

jump_pose(

    10,

    0.05,

    2.0,
    -2.0,
    -2.0,

    1.0,

    0,
    0.10,

    0,
    0.10,

    -0.08,
    0.18,

    0.08,
    0.18

)


# ------------------------------------------------------------
# FRAME 13
# AIRBORNE
# ------------------------------------------------------------

jump_pose(

    13,

    0.38,

    0,
    -1.0,
    -1.0,

    0.5,

    0,
    0.28,

    0,
    0.28,

    -0.04,
    0.28,

    0.04,
    0.28

)


# ------------------------------------------------------------
# FRAME 17
# APEX
# ------------------------------------------------------------

jump_pose(

    17,

    0.50,

    0,
    0,
    0,

    -0.5,

    0,
    0.32,

    0,
    0.32,

    -0.02,
    0.24,

    0.02,
    0.24

)


# ------------------------------------------------------------
# FRAME 21
# FALLING
# ------------------------------------------------------------

jump_pose(

    21,

    0.32,

    1.0,
    1.0,
    1.0,

    0.5,

    0,
    0.18,

    0,
    0.18,

    0.04,
    0.15,

    -0.04,
    0.15

)


# ------------------------------------------------------------
# FRAME 24
# LANDING
# ------------------------------------------------------------

jump_pose(

    24,

    0.02,

    -2.0,
    2.0,
    2.0,

    -1.0,

    0,
    0,

    0,
    0,

    0.10,
    0.04,

    -0.10,
    0.04

)


# ------------------------------------------------------------
# FRAME 27
# IMPACT
# ------------------------------------------------------------

jump_pose(

    27,

    -0.12,

    -3.0,
    2.0,
    3.0,

    -1.0,

    0,
    0,

    0,
    0,

    0.06,
    0,

    -0.06,
    0

)


# ------------------------------------------------------------
# FRAME 32
# RECOVERY
# ------------------------------------------------------------

jump_pose(

    32,

    0.03,

    1.0,
    -0.5,
    -0.5,

    0.5,

    0,
    0,

    0,
    0,

    0.02,
    0,

    -0.02,
    0

)


# ------------------------------------------------------------
# FRAME 36
# NEUTRAL
# ------------------------------------------------------------

jump_pose(

    36,

    0.00,

    0,
    0,
    0,

    0,

    0,
    0,

    0,
    0,

    0,
    0,

    0,
    0

)


# ============================================================
# 19. SMOOTH INTERPOLATION
# ============================================================

for fcurve in action.fcurves:

    for keyframe in fcurve.keyframe_points:

        keyframe.interpolation = 'BEZIER'


# ============================================================
# 20. ACTION METADATA
# ============================================================

action.frame_start = 1

action.frame_end = 36

action["animation_type"] = "jump"

action["character"] = "skomma_humanoid_v1"

action["animation_style"] = "blocky_humanoid"

action["loop"] = False

action["fps"] = 30

action["frame_length"] = 36

action["uses_existing_ik"] = True

action["creates_new_bones"] = False

action["creates_new_controls"] = False

action["creates_new_glb"] = False


# ============================================================
# 21. IMPORTANT
#
# REMOVE ACTION FROM ACTIVE SLOT
# ============================================================
#
# The Jump Action now exists independently.
#
# We do NOT leave it in:
#
#     animation_data.action
#
# because we want it controlled through NLA.
#
# ============================================================

rig.animation_data.action = None


# ============================================================
# 22. CREATE NLA TRACK
# ============================================================
#
# One dedicated track for Jump.
#
# ============================================================

jump_track = rig.animation_data.nla_tracks.new()

jump_track.name = "Skomma_Jump"


# ============================================================
# 23. CREATE NLA STRIP
# ============================================================
#
# This is the critical part.
#
# The Action is now actually inserted into the NLA.
#
# ============================================================

jump_strip = jump_track.strips.new(

    "Skomma_Jump",

    1,

    action

)


# ============================================================
# 24. NLA STRIP SETTINGS
# ============================================================

jump_strip.action_frame_start = 1

jump_strip.action_frame_end = 36

jump_strip.frame_start = 1

jump_strip.frame_end = 36


# Jump should NOT loop.

jump_strip.repeat = 1.0


# Replace animation underneath.

jump_strip.blend_type = 'REPLACE'


# Full influence.

jump_strip.influence = 1.0


# Hold nothing after jump.

jump_strip.extrapolation = 'NOTHING'


# ============================================================
# 25. ORGANIZE EXISTING SKOMMA ACTIONS
# ============================================================
#
# Make sure Idle / Walk / Run also have NLA tracks.
#
# IMPORTANT:
#
# If a track already exists, we do NOT create another one.
#
# If a strip already exists, we do NOT duplicate it.
#
# ============================================================

existing_animation_names = [

    "Skomma_Idle",
    "Skomma_Walk",
    "Skomma_Run"

]


def find_nla_track(name):

    for track in rig.animation_data.nla_tracks:

        if track.name == name:

            return track

    return None


def find_nla_strip(action_name):

    for track in rig.animation_data.nla_tracks:

        for strip in track.strips:

            if (

                strip.name == action_name

                or

                (
                    strip.action
                    and
                    strip.action.name == action_name
                )

            ):

                return strip

    return None


for animation_name in existing_animation_names:

    act = bpy.data.actions.get(
        animation_name
    )


    if act is None:

        continue


    existing_strip = find_nla_strip(
        animation_name
    )


    if existing_strip:

        print(
            "NLA already contains:",
            animation_name
        )

        continue


    track = find_nla_track(
        animation_name
    )


    if track is None:

        track = rig.animation_data.nla_tracks.new()

        track.name = animation_name


    strip = track.strips.new(

        animation_name,

        1,

        act

    )


    strip.action_frame_start = act.frame_start

    strip.action_frame_end = act.frame_end

    strip.frame_start = 1

    strip.frame_end = (
        1 +
        (
            act.frame_end -
            act.frame_start
        )
    )


    strip.blend_type = 'REPLACE'

    strip.influence = 1.0


    print(
        "Added to NLA:",
        animation_name
    )


# ============================================================
# 26. MUTE ALL LIBRARY TRACKS
# ============================================================
#
# IMPORTANT:
#
# These animations are a LIBRARY.
#
# We don't want Idle + Walk + Run + Jump all playing
# on top of each other.
#
# Therefore:
#
#     Idle  -> muted
#     Walk  -> muted
#     Run   -> muted
#     Jump  -> ACTIVE
#
# This makes Jump immediately visible.
#
# ============================================================

for track in rig.animation_data.nla_tracks:

    if track.name.startswith("Skomma_"):

        track.mute = True


jump_track.mute = False


# ============================================================
# 27. SELECT JUMP STRIP
# ============================================================

for track in rig.animation_data.nla_tracks:

    for strip in track.strips:

        strip.select = False


jump_strip.select = True


# ============================================================
# 28. RESTORE SCENE SETTINGS
# ============================================================

scene.frame_start = old_scene_start

scene.frame_end = old_scene_end

scene.render.fps = old_fps


scene.frame_set(1)


# ============================================================
# 29. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 30. PRINT NLA LIBRARY
# ============================================================

print("")
print("==============================================")
print("SKOMMA NLA ANIMATION LIBRARY")
print("==============================================")
print("")


for track in rig.animation_data.nla_tracks:

    if track.name.startswith("Skomma_"):

        print("TRACK:")
        print("    ", track.name)

        for strip in track.strips:

            if strip.action:

                print(
                    "        STRIP:",
                    strip.name,
                    "->",
                    strip.action.name
                )

        print(
            "        MUTED:",
            track.mute
        )

        print("")


# ============================================================
# 31. FINAL INFORMATION
# ============================================================

print("")
print("==============================================")
print("SKOMMA JUMP COMPLETE")
print("==============================================")
print("")

print("Action:")
print("    Skomma_Jump")
print("")

print("NLA Track:")
print("    Skomma_Jump")
print("")

print("NLA Strip:")
print("    Skomma_Jump")
print("")

print("Existing:")
print("    Skomma_Idle")
print("    Skomma_Walk")
print("    Skomma_Run")
print("")

print("Jump:")
print("    NON-LOOPING")
print("    36 frames")
print("    30 FPS")
print("")

print("Skeleton:")
print("    EXISTING ONLY")
print("")

print("New bones:")
print("    NONE")
print("")

print("New controls:")
print("    NONE")
print("")

print("New GLB:")
print("    NONE")
print("")

print("NLA:")
print("    ORGANIZED")
print("")

print("==============================================")