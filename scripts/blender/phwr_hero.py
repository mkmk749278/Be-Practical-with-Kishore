"""Hero shots for phwr-700 (plan §8). Every shot is labelled ILLUSTRATION in Remotion.

  .venv-blender/bin/python scripts/blender/phwr_hero.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

The reactor face of a 220 MWe pressurised heavy-water reactor (RAPS-2 class): 306 coolant channels on a square
lattice inside a circle (lattice pitch 228.6 mm), each ending in a steel end fitting that stands out from the end
shield, with its feeder pipe bending away (top half up, bottom half down) into the feeder forest. Sizes are drawn,
not measured: end fittings about 0.11 m across and 0.9 m proud of the face. The shielded flask is a drawn machine,
painted caution yellow as the plan's thumbnail asks, on a floor carriage; it is not a copy of any one real flask.

Shots (frames at 60 fps):
  face  (0-599)  cold open, first frame = the thumbnail's subject: a slow push across the 306 end fittings in a dim
                 vault, warm key light; the flask glides in along its rails (240-470) and locks on one end fitting
                 near the centre: the clamp ring turns and seats at 480 (the clunk, 480), a settle of 6 mm.
  thumb (0)      the thumbnail base: three-quarter on the face with the flask locked on, bottom-right kept quiet.
Deterministic: fixed seeds, no simulation; labels come from Remotion.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catapult_hero2 import (  # noqa: E402
    aim_cam, args, box, cyl, finish, haze, keys, light, mat, pbr, render, setup, sphere, torus, track_cam, track_obj,
    world_hdri)

YEL = (0.95, 0.55, 0.03)        # caution yellow paint (linear)
PITCH = 0.2286                  # lattice pitch, m
CZ = 3.6                        # height of the core centre above the floor, m
FIT_L, FIT_R = 0.90, 0.055      # end fitting length out of the face and radius, m
# the end fitting the flask locks on: one step left of centre, one step up (a real one, not the dead centre)
TARGET = (-0.5 * PITCH, CZ + 0.5 * PITCH)


def lattice():
    """306 channel centres (x, z): the 306 lattice points nearest the core centre on a half-offset square grid."""
    pts = [((i + 0.5) * PITCH, (j + 0.5) * PITCH) for i in range(-12, 12) for j in range(-12, 12)]
    pts.sort(key=lambda p: (round(math.hypot(*p), 6), p[1], p[0]))
    return [(x, CZ + z) for x, z in pts[:306]]


def linked(name, src, loc, rot=(0, 0, 0)):
    """a linked duplicate (shares the mesh) so 306 fittings cost one mesh"""
    o = bpy.data.objects.new(name, src.data)
    bpy.context.collection.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    for md in src.modifiers:
        n = o.modifiers.new(md.name, md.type)
        if md.type == "BEVEL":
            n.width, n.segments, n.limit_method = md.width, md.segments, md.limit_method
    return o


def end_fitting_proto(m_steel, m_dark):
    """one end fitting along -y from the face: hub collar, body, the closure plug ring, the feeder coupling"""
    parts = [
        cyl("ef_collar", (0, -0.06, 0), FIT_R * 1.55, 0.12, m_steel, rot=(math.pi / 2, 0, 0), verts=32, bevel=0.006),
        cyl("ef_body", (0, -0.12 - FIT_L / 2, 0), FIT_R, FIT_L, m_steel, rot=(math.pi / 2, 0, 0), verts=32,
            bevel=0.004),
        cyl("ef_cap", (0, -0.12 - FIT_L - 0.05, 0), FIT_R * 1.18, 0.10, m_steel, rot=(math.pi / 2, 0, 0), verts=32,
            bevel=0.008),
        cyl("ef_plug", (0, -0.12 - FIT_L - 0.105, 0), FIT_R * 0.70, 0.02, m_dark, rot=(math.pi / 2, 0, 0), verts=24),
        cyl("ef_coupling", (0.04, -0.42, 0), 0.026, 0.09, m_steel, rot=(0, math.pi / 2, 0), verts=16, bevel=0.003),
    ]
    for o in parts:
        for md in list(o.modifiers):
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[1]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)   # bake each part's pose first
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = "ef_proto"
    return o


def feeder_curve(name, x, z, up, m):
    """the feeder pipe from the fitting's coupling: out a little, then a smooth bend up (or down) and away"""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.017
    cu.bevel_resolution = 2
    cu.resolution_u = 8
    sp = cu.splines.new("BEZIER")
    s = 1 if up else -1
    pts = [(x + 0.06, -0.42, z + s * 0.10), (x + 0.075, -0.30, z + s * 0.32), (x + 0.08, -0.20, CZ + s * 3.6)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def build_face(a):
    sc, cam = setup(a, exposure=0.0)
    world_hdri(sc, "machine_shop_02", strength=0.28, rot=1.2, bg_strength=0.0)   # lights the reflections only

    m_face = pbr("endshield", "metal_plate_02", scale=1.6, tint=(0.62, 0.60, 0.56), rough=(0.25, 0.75), metal=1.0,
                 grime=0.35)
    m_steel = mat("fitting", (0.62, 0.60, 0.57), 0.33, metal=1.0)
    m_feeder = mat("feeder", (0.30, 0.29, 0.27), 0.45, metal=1.0)
    m_dark = mat("plugdark", (0.05, 0.05, 0.05), 0.5, metal=0.6)
    m_conc = pbr("vault", "concrete_floor_worn_001", scale=2.5, tint=(0.22, 0.20, 0.18), grime=0.5)   # 26 NOV: a dim vault
    m_floor = pbr("floor", "concrete_floor_worn_001", scale=3.0, tint=(0.20, 0.19, 0.17), grime=0.5)
    # caution-yellow paint over steel: the plate's own scan gives the paint its wear and roughness
    # caution yellow on steel (AgX lifts and pales yellows: a deeper base reads as caution yellow); 26 NOV: the scanned
    # look pass tried a scanned plate (read as rust); the hard key and haze now carry the shape
    m_yel = mat("flask", (0.72, 0.30, 0.0), 0.55, coat=0.15)   # the scanned plate turned it brown: solid paint, the key light gives it form
    m_black = mat("black", (0.02, 0.02, 0.02), 0.45, metal=0.3)
    m_rail = mat("rail", (0.30, 0.30, 0.30), 0.3, metal=1.0)

    # the vault: floor, end-shield wall, side walls, the face plate
    box("floor", (0, -6, 0), (24, 16, 0.2), m_floor)
    box("wall", (0, 0.35, 5), (24, 0.5, 10), m_conc)
    box("wallL", (-7.5, -5, 5), (0.5, 12, 10), m_conc)
    box("wallR", (7.5, -5, 5), (0.5, 12, 10), m_conc)
    cyl("faceplate", (0, 0.04, CZ), 2.55, 0.16, m_face, rot=(math.pi / 2, 0, 0), verts=128, bevel=0.02)
    torus("facering", (0, -0.05, CZ), 2.60, 0.06, m_steel, rot=(math.pi / 2, 0, 0))

    proto = end_fitting_proto(m_steel, m_dark)
    pts = lattice()
    for k, (x, z) in enumerate(pts):
        linked(f"ef{k:03d}", proto, (x, 0, z))
        feeder_curve(f"fd{k:03d}", x, z, z >= CZ, m_feeder)
    proto.location = (100, 100, -100)       # the prototype parks out of sight

    # the flask: yellow body on a carriage with rails to the face
    tx, tz = TARGET
    flask = bpy.data.objects.new("flask", None)
    bpy.context.collection.objects.link(flask)
    body = cyl("fl_body", (0, -1.55, 0), 0.62, 2.4, m_yel, rot=(math.pi / 2, 0, 0), verts=96, bevel=0.03)
    nose = cyl("fl_nose", (0, -0.25, 0), 0.30, 0.42, m_yel, rot=(math.pi / 2, 0, 0), verts=64, bevel=0.02)
    snout = cyl("fl_snout", (0, 0.02, 0), 0.10, 0.18, m_steel, rot=(math.pi / 2, 0, 0), verts=48, bevel=0.01)
    bands = [torus(f"fl_band{i}", (0, y, 0), 0.63, 0.025, m_black, rot=(math.pi / 2, 0, 0))
             for i, y in enumerate((-0.6, -1.55, -2.5))]
    back = cyl("fl_back", (0, -2.8, 0), 0.50, 0.12, m_black, rot=(math.pi / 2, 0, 0), verts=64, bevel=0.01)
    hazard = []
    for i in range(16):
        ang = i * 2 * math.pi / 16
        hazard.append(box(f"fl_hz{i}", (0.625 * math.cos(ang), -0.52, 0.625 * math.sin(ang)), (0.24, 0.16, 0.02),
                          m_black if i % 2 else m_yel, rot=(0, -ang + math.pi / 2, 0)))
    clamp = torus("fl_clamp", (0, -0.03, 0), 0.13, 0.03, m_black, rot=(math.pi / 2, 0, 0))
    lugs = [box(f"fl_lug{i}", (0.13 * math.cos(i * math.pi / 2), -0.03, 0.13 * math.sin(i * math.pi / 2)),
                (0.05, 0.06, 0.05), m_steel, bevel=0.005) for i in range(4)]
    carriage = box("fl_cradle", (0, -1.55, -0.72), (1.0, 2.2, 0.22), m_yel, bevel=0.02)
    legs = [box(f"fl_leg{i}", (sx * 0.42, sy, -(tz + 0.72) / 2 + 0.05), (0.16, 0.16, tz - 0.72 - 0.25), m_black,
                bevel=0.01) for i, (sx, sy) in enumerate([(-1, -0.6), (1, -0.6), (-1, -2.5), (1, -2.5)])]
    shoes = [box(f"fl_shoe{i}", (sx * 0.5, sy, -tz + 0.2), (0.34, 0.5, 0.14), m_yel, bevel=0.01)
             for i, (sx, sy) in enumerate([(-1, -0.6), (1, -0.6), (-1, -2.5), (1, -2.5)])]
    cables = cyl("fl_cable", (0.75, -2.9, -tz + 0.12), 0.05, 4.0, m_black, rot=(math.pi / 2, 0, 0), verts=16)
    for o in [body, nose, snout, *bands, *hazard, back, clamp, *lugs, carriage, *legs, *shoes, cables]:
        o.parent = flask
    for i, o in enumerate(lugs):   # the lugs ride the clamp ring: in its local frame they sit in its xy plane
        o.parent = clamp
        o.location = (0.13 * math.cos(i * math.pi / 2), 0.13 * math.sin(i * math.pi / 2), 0)
        o.rotation_euler = (-math.pi / 2, 0, 0)
    clamp_pivot = clamp
    for side in (-0.5, 0.5):
        box(f"rail{side}", (tx + side, -3.4, 0.13), (0.10, 6.6, 0.06), m_rail)

    # light: a warm key from high left draws shafts in thin haze; a cool fill; a rim on the fittings
    # 26 NOV look pass (bench frames read flat and bright): the room falls to dark, one hard warm key draws shafts
    light("SPOT", (-4.5, -6.5, 8.5), (0, 0, CZ), 16000, (1.0, 0.74, 0.48), size=0.25, spot=26)
    light("AREA", (5.5, -5.5, 3.0), (0, 0, CZ), 220, (0.55, 0.70, 1.0), size=4.0)
    light("AREA", (0, -1.5, 8.6), (0, 0, CZ), 120, (1.0, 0.9, 0.8), size=3.0)
    light("SPOT", (2.5, -3.0, 0.4), (tx, -1.0, tz), 1400, (1.0, 0.82, 0.55), size=0.2, spot=30)
    light("AREA", (0, -8.0, 4.0), (0, 0, CZ), 160, (1.0, 0.95, 0.88), size=6.0)   # a soft wall for the steel to mirror
    # the engineer for scale: far left at a console, hard hat and coverall, soft in the depth of field
    m_cov = mat("coverall", (0.02, 0.025, 0.035), 0.9)   # 26 NOV: a silhouette, never a lit toy figure
    m_hat = mat("hardhat", (0.55, 0.55, 0.52), 0.35, coat=0.4)
    m_skin = mat("skin", (0.06, 0.035, 0.02), 0.6)
    ex, ey, ez = -3.4, -0.9, 2.0   # 26 NOV: on the fuelling bridge at the face's left edge, inside the opening frames
    m_grate = mat("grate", (0.12, 0.12, 0.12), 0.5, metal=0.8)
    box("platform", (ex + 0.3, ey, ez - 0.05), (1.8, 1.6, 0.1), m_grate)
    box("rail_top", (ex + 0.3, ey - 0.8, ez + 1.0), (1.8, 0.05, 0.05), m_rail)
    for px in (-0.6, 0.3, 1.2):
        box(f"post{px}", (ex + px, ey - 0.8, ez + 0.5), (0.05, 0.05, 1.0), m_rail)
    box("pillar", (ex + 0.3, ey, ez / 2 - 0.1), (0.25, 0.25, ez - 0.1), m_rail)
    for o in (cyl("eng_legs", (ex, ey, ez + 0.45), 0.16, 0.9, m_cov, verts=24),
              cyl("eng_body", (ex, ey, ez + 1.25), 0.21, 0.72, m_cov, verts=24, bevel=0.05),
              sphere("eng_head", (ex, ey, ez + 1.72), 0.11, m_skin),
              sphere("eng_hat", (ex, ey, ez + 1.78), 0.13, m_hat, scale=(1, 1, 0.62)),
              cyl("eng_armL", (ex + 0.14, ey + 0.18, ez + 1.22), 0.06, 0.55, m_cov, rot=(math.radians(60), 0, 0), verts=16),
              cyl("eng_armR", (ex - 0.14, ey + 0.18, ez + 1.22), 0.06, 0.55, m_cov, rot=(math.radians(60), 0, 0), verts=16)):
        o.rotation_euler[2] += math.radians(20)   # turned toward the face
    box("console", (ex - 0.7, ey + 0.5, ez + 0.5), (1.2, 0.5, 1.0), mat("console", (0.22, 0.22, 0.21), 0.5), bevel=0.02)
    box("screen", (ex - 0.7, ey + 0.27, ez + 1.25), (0.9, 0.05, 0.5), mat("screen", (0.02, 0.02, 0.02), 0.2,
        emit=(0.55, 0.85, 1.0), strength=0.8))
    haze((0, -5, 4.5), (14, 10, 9), 0.02, color=(1.0, 0.95, 0.9))

    SEAT, LOCK = 470, 480
    approach = [(0, -4.0), (240, -4.0), (SEAT, -FIT_L - 0.29), (LOCK, -FIT_L - 0.29)]

    def frame(f):
        y = keys(f, approach)
        settle = 0.006 * math.exp(-max(0, f - LOCK) / 6) * math.sin(max(0, f - LOCK) * 0.9) if f >= LOCK else 0
        flask.location = (tx, y + settle, tz)
        clamp_pivot.rotation_euler = (math.pi / 2, keys(f, [(SEAT, 0.0), (LOCK, math.radians(45))]), 0)
        if a.shot == "thumb":
            aim_cam(cam, (2.9, -2.9, 3.4), (tx - 0.8, -0.5, tz + 0.1), 24, fstop=7.1)
            return
        # the push across the face, then round to the side so the snout is seen meeting its fitting at the lock
        loc = keys(f, [(0, (-3.0, -5.4, 5.0)), (260, (1.2, -6.0, 5.6)), (440, (2.4, -2.2, tz + 0.55)),
                       (599, (2.1, -1.75, tz + 0.40))])
        aim = keys(f, [(0, (-0.6, 0, CZ + 0.3)), (260, (0.2, -1.2, CZ)), (440, (tx, -1.05, tz)),
                       (599, (tx, -1.05, tz))])
        lens = keys(f, [(0, 30), (440, 30), (599, 34)])
        aim_cam(cam, loc, aim, lens, fstop=4.0)

    render(sc, a, frame, track_cam(cam) + track_obj(flask, props=("location",))
           + track_obj(clamp_pivot, props=("rotation_euler",)))


SHOTS = {"face": build_face, "thumb": build_face}


def main():
    a = args()
    if a.shot not in SHOTS:
        sys.exit(f"unknown shot {a.shot}")
    SHOTS[a.shot](a)


if __name__ == "__main__":
    main()
