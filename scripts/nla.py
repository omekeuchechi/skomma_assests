import bpy


# ============================================================
# SKOMMA ANIMATION LIBRARY ORGANIZER
# ============================================================
#
# PURPOSE:
#
# Organize existing animation Actions into NLA tracks.
#
# EXISTING ACTIONS:
#
#     Skomma_Idle
#     Skomma_Walk
#
# RESULT:
#
#     Skomma_Idle
#     Skomma_Walk
#
# appear as separate NLA animation tracks.
#
# IMPORTANT:
#
# - Does NOT create bones
# - Does NOT create skeleton
# - Does NOT create GLB
# - Does NOT delete animations
# - Does NOT save Blender file
#
# ============================================================


print("")
print("======================================")
print("SKOMMA ANIMATION LIBRARY")
print("======================================")
print("")


# ============================================================
# 1. FIND SKOMMA RIG
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


# Fallback: find any armature

if rig is None:

    for obj in bpy.data.objects:

        if obj.type == 'ARMATURE':

            rig = obj
            break


if rig is None:

    raise RuntimeError(
        "No existing SKOMMA armature was found."
    )


print("Rig found:")
print("   ", rig.name)
print("")


# ============================================================
# 2. FIND EXISTING ACTIONS
# ============================================================

idle_action = bpy.data.actions.get(
    "Skomma_Idle"
)

walk_action = bpy.data.actions.get(
    "Skomma_Walk"
)


if idle_action:

    print("FOUND:")
    print("    Skomma_Idle")

else:

    print("MISSING:")
    print("    Skomma_Idle")


if walk_action:

    print("FOUND:")
    print("    Skomma_Walk")

else:

    print("MISSING:")
    print("    Skomma_Walk")


print("")


# ============================================================
# 3. REQUIRE ACTIONS
# ============================================================

if idle_action is None:

    raise RuntimeError(
        "Skomma_Idle does not exist."
    )


if walk_action is None:

    raise RuntimeError(
        "Skomma_Walk does not exist."
    )


# ============================================================
# 4. CREATE ANIMATION DATA
# ============================================================

if rig.animation_data is None:

    rig.animation_data_create()


# ============================================================
# 5. REMOVE ONLY OLD SKOMMA NLA TRACKS
# ============================================================
#
# IMPORTANT:
#
# We only remove tracks created by this organizer.
#
# We do NOT remove Actions.
#
# ============================================================

for track in list(rig.animation_data.nla_tracks):

    if track.name in [
        "Skomma_Idle",
        "Skomma_Walk"
    ]:

        rig.animation_data.nla_tracks.remove(
            track
        )


# ============================================================
# 6. CLEAR ACTIVE ACTION
# ============================================================
#
# NLA will now control the animation.
#
# The Actions themselves remain safely stored in:
#
# bpy.data.actions
#
# ============================================================

rig.animation_data.action = None


# ============================================================
# 7. CREATE IDLE TRACK
# ============================================================

idle_track = rig.animation_data.nla_tracks.new()

idle_track.name = "Skomma_Idle"


idle_strip = idle_track.strips.new(
    "Skomma_Idle",
    1,
    idle_action
)


# ============================================================
# 8. SET IDLE STRIP RANGE
# ============================================================

idle_start = idle_action.frame_start
idle_end = idle_action.frame_end

idle_strip.action_frame_start = idle_start
idle_strip.action_frame_end = idle_end

idle_strip.frame_start = 1
idle_strip.frame_end = (
    1 + (idle_end - idle_start)
)


# Loop Idle

idle_strip.repeat = 1.0


# ============================================================
# 9. CREATE WALK TRACK
# ============================================================

walk_track = rig.animation_data.nla_tracks.new()

walk_track.name = "Skomma_Walk"


walk_strip = walk_track.strips.new(
    "Skomma_Walk",
    1,
    walk_action
)


# ============================================================
# 10. SET WALK STRIP RANGE
# ============================================================

walk_start = walk_action.frame_start
walk_end = walk_action.frame_end

walk_strip.action_frame_start = walk_start
walk_strip.action_frame_end = walk_end

walk_strip.frame_start = 1
walk_strip.frame_end = (
    1 + (walk_end - walk_start)
)


# ============================================================
# 11. LOOP WALK
# ============================================================

walk_strip.repeat = 1.0


# ============================================================
# 12. DEFAULT TO IDLE
# ============================================================
#
# Idle is visible.
#
# Walk exists but is muted.
#
# ============================================================

idle_track.mute = False
idle_track.is_solo = True

walk_track.mute = True
walk_track.is_solo = False


# ============================================================
# 13. ACTION METADATA
# ============================================================

idle_action["animation_type"] = "idle"
idle_action["character"] = "skomma_humanoid_v1"
idle_action["loop"] = True
idle_action["fps"] = 30
idle_action["creates_new_bones"] = False
idle_action["creates_new_glb"] = False


walk_action["animation_type"] = "walk"
walk_action["character"] = "skomma_humanoid_v1"
walk_action["loop"] = True
walk_action["fps"] = 30
walk_action["creates_new_bones"] = False
walk_action["creates_new_glb"] = False


# ============================================================
# 14. SET SCENE
# ============================================================

scene = bpy.context.scene

scene.frame_start = 1

scene.frame_end = 60

scene.frame_set(1)


# ============================================================
# 15. SELECT RIG
# ============================================================

bpy.ops.object.select_all(
    action='DESELECT'
)

rig.select_set(True)

bpy.context.view_layer.objects.active = rig


# ============================================================
# 16. VERIFY
# ============================================================

print("")
print("======================================")
print("SKOMMA ANIMATION LIBRARY")
print("======================================")
print("")

print("Actions:")
print("    ", idle_action.name)
print("    ", walk_action.name)
print("")

print("NLA Tracks:")
print("    ", idle_track.name)
print("    ", walk_track.name)
print("")

print("Default:")
print("    Skomma_Idle")
print("")

print("Walk:")
print("    Skomma_Walk")
print("    Available but muted")
print("")

print("Skeleton:")
print("    EXISTING")
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