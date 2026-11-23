"""Hero shots for arjun-tank (plan §8). Every shot is labelled ILLUSTRATION in Remotion.

  .venv-blender/bin/python scripts/blender/arjun_hero.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

The tank is an Arjun Mk1A built from the real reference photos (PIB release 1757320: the side view and the dust
shot; PIB 14 Feb 2021 handover photos): a long hull with bolted side skirts, seven road wheels a side, rear drive
sprocket, raised front idler, the track-width mine plough, the low wedge-fronted turret with a long bustle, smoke
launcher clusters at its rear corners, the remote weapon station, two antennas, the long gun in a banded thermal
sleeve with its fume extractor, and the Army's stepped three-tone camouflage (green, cream, maroon-brown).
Sizes are the published ones rounded (hull about 7.7 m long, 3.9 m wide over the skirts, 2.3 m to the turret roof).
The engine bay (about 2.2 m long, 2.5 m wide, 1 m deep) is drawn, not measured: the room a powerpack sits in.

Shots (frames at 60 fps):
  bayopen (0-899)  open ~0:14-0:29 and landing ~9:20: the tank in the Thar from its side; the camera swings round to
                   the rear three-quarter and rises; the engine-deck covers lift away (420-600) and the bay is empty,
                   glowing caution yellow from inside (480-600); ends looking down into the room.
  thumb   (0)      the thumbnail base: rear three-quarter, low warm sun, the open bay glowing, bottom-right kept quiet.
Deterministic: fixed seeds, no simulation; labels come from Remotion.
"""
import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catapult_hero2 import (  # noqa: E402
    aim_cam, args, box, cyl, emit_socket, finish, haze, keys, light, mat, mesh_obj, pbr, render, setup, slab,
    smooth, track_cam, track_obj, world_hdri, _bsdf)
import ph_assets  # noqa: E402

YEL = (1.0, 0.62, 0.08)          # caution yellow light (linear)
SAND = (0.50, 0.33, 0.18)
# the Army's three-tone desert scheme, sampled from the PIB photos (sRGB -> linear)
CAMO = [(0.040, 0.15, 0.075), (0.52, 0.43, 0.28), (0.19, 0.06, 0.04)]

# engine bay box (hull coordinates: x forward, y left, z up; ground at z = 0)
BAY_X0, BAY_X1, BAY_Y, BAY_FLOOR, DECK_Z = -3.70, -1.50, 1.24, 0.60, 1.55


# ---------------------------------------------------------------- materials
def camo_mat(name, root, dust=0.55, rough=0.62):
    """stepped camouflage: Chebychev Voronoi cells in the tank's own coordinates (one pattern across all parts),
    three flat colours, a sand dust layer heavier low down, a faint plate normal."""
    files = ph_assets.texture("metal_plate_02")
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt, p = m.node_tree, _bsdf(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    tc.object = root
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.05, 1.6, 1.4)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    vo = nt.nodes.new("ShaderNodeTexVoronoi")
    vo.distance = "CHEBYCHEV"
    vo.inputs["Scale"].default_value = 1.0
    vo.inputs["Randomness"].default_value = 0.85
    nt.links.new(mp.outputs["Vector"], vo.inputs["Vector"])
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(vo.outputs["Color"], sep.inputs["Color"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.interpolation = "CONSTANT"
    els = cr.color_ramp.elements
    els[0].position, els[0].color = 0.0, (*CAMO[0], 1)
    els[1].position, els[1].color = 0.42, (*CAMO[1], 1)
    e3 = els.new(0.74)
    e3.color = (*CAMO[2], 1)
    nt.links.new(sep.outputs["Red"], cr.inputs["Fac"])
    col = cr.outputs["Color"]
    if dust:
        sz = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sz.inputs["Vector"])
        zr = nt.nodes.new("ShaderNodeMapRange")
        zr.inputs["From Min"].default_value, zr.inputs["From Max"].default_value = 0.2, 1.6
        zr.inputs["To Min"].default_value, zr.inputs["To Max"].default_value = dust, dust * 0.18
        nt.links.new(sz.outputs["Z"], zr.inputs["Value"])
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 3.0
        nz.inputs["Detail"].default_value = 8
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        nt.links.new(zr.outputs["Result"], mul.inputs[0])
        nr = nt.nodes.new("ShaderNodeMapRange")
        nr.inputs["From Min"].default_value, nr.inputs["From Max"].default_value = 0.35, 0.7
        nt.links.new(nz.outputs["Fac"], nr.inputs["Value"])
        nt.links.new(nr.outputs["Result"], mul.inputs[1])
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        nt.links.new(mul.outputs["Value"], mx.inputs["Factor"])
        nt.links.new(col, mx.inputs[6])
        mx.inputs[7].default_value = (*SAND, 1)
        col = mx.outputs[2]
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.25
    ao.samples = 8
    ar = nt.nodes.new("ShaderNodeMapRange")
    ar.inputs["To Min"].default_value, ar.inputs["To Max"].default_value = 0.45, 1.0
    nt.links.new(ao.outputs["AO"], ar.inputs["Value"])
    gm = nt.nodes.new("ShaderNodeMix")
    gm.data_type = "RGBA"
    gm.blend_type = "MULTIPLY"
    gm.inputs["Factor"].default_value = 1.0
    nt.links.new(col, gm.inputs[6])
    gc = nt.nodes.new("ShaderNodeCombineColor")
    for k in ("Red", "Green", "Blue"):
        nt.links.new(ar.outputs["Result"], gc.inputs[k])
    nt.links.new(gc.outputs["Color"], gm.inputs[7])
    col = gm.outputs[2]
    nt.links.new(col, p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = 0.0
    if "nor" in files:
        im = nt.nodes.new("ShaderNodeTexImage")
        im.image = bpy.data.images.load(files["nor"], check_existing=True)
        im.image.colorspace_settings.name = "Non-Color"
        im.projection = "BOX"
        im.projection_blend = 0.3
        m2 = nt.nodes.new("ShaderNodeMapping")
        m2.inputs["Scale"].default_value = (0.8, 0.8, 0.8)
        nt.links.new(tc.outputs["Object"], m2.inputs["Vector"])
        nt.links.new(m2.outputs["Vector"], im.inputs["Vector"])
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = 0.25
        nt.links.new(im.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    return m


def ground_mat():
    """Thar sand, with the tank's own two track ruts running out behind it"""
    m = pbr("sand", "aerial_sand", scale=9.0, tint=(1.0, 0.76, 0.50), rough=(0.75, 1.0), nor=0.5, grime=0.22)
    nt, p = m.node_tree, _bsdf(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    # rut mask: |(|y| - 1.62)| < 0.32 and x < -3.6 (behind the tank), fading out far behind
    ay = nt.nodes.new("ShaderNodeMath")
    ay.operation = "ABSOLUTE"
    nt.links.new(sep.outputs["Y"], ay.inputs[0])
    d = nt.nodes.new("ShaderNodeMath")
    d.operation = "SUBTRACT"
    nt.links.new(ay.outputs["Value"], d.inputs[0])
    d.inputs[1].default_value = 1.62
    ad = nt.nodes.new("ShaderNodeMath")
    ad.operation = "ABSOLUTE"
    nt.links.new(d.outputs["Value"], ad.inputs[0])
    band = nt.nodes.new("ShaderNodeMapRange")
    band.inputs["From Min"].default_value, band.inputs["From Max"].default_value = 0.26, 0.36
    band.inputs["To Min"].default_value, band.inputs["To Max"].default_value = 1.0, 0.0
    nt.links.new(ad.outputs["Value"], band.inputs["Value"])
    bx = nt.nodes.new("ShaderNodeMapRange")
    bx.inputs["From Min"].default_value, bx.inputs["From Max"].default_value = -3.4, -4.2
    nt.links.new(sep.outputs["X"], bx.inputs["Value"])
    far = nt.nodes.new("ShaderNodeMapRange")
    far.inputs["From Min"].default_value, far.inputs["From Max"].default_value = -25, -70
    far.inputs["To Min"].default_value, far.inputs["To Max"].default_value = 1.0, 0.0
    nt.links.new(sep.outputs["X"], far.inputs["Value"])
    m1 = nt.nodes.new("ShaderNodeMath")
    m1.operation = "MULTIPLY"
    nt.links.new(band.outputs["Result"], m1.inputs[0])
    nt.links.new(bx.outputs["Result"], m1.inputs[1])
    m2 = nt.nodes.new("ShaderNodeMath")
    m2.operation = "MULTIPLY"
    nt.links.new(m1.outputs["Value"], m2.inputs[0])
    nt.links.new(far.outputs["Result"], m2.inputs[1])
    # track-link ribs inside the ruts
    rib = nt.nodes.new("ShaderNodeTexWave")
    rib.wave_type = "BANDS"
    rib.bands_direction = "X"
    rib.inputs["Scale"].default_value = 0.6
    rib.inputs["Distortion"].default_value = 1.5
    nt.links.new(tc.outputs["Object"], rib.inputs["Vector"])
    rr = nt.nodes.new("ShaderNodeMapRange")
    rr.inputs["To Min"].default_value, rr.inputs["To Max"].default_value = 0.55, 0.8
    nt.links.new(rib.outputs["Fac"], rr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    nt.links.new(m2.outputs["Value"], mix.inputs["Factor"])
    base = p.inputs["Base Color"].links[0].from_socket
    nt.links.new(base, mix.inputs[6])
    cc = nt.nodes.new("ShaderNodeCombineColor")
    for k in ("Red", "Green", "Blue"):
        nt.links.new(rr.outputs["Result"], cc.inputs[k])
    nt.links.new(cc.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], p.inputs["Base Color"])
    return m


# ---------------------------------------------------------------- geometry helpers
def prism_xz(name, profile, y0, y1, m, bevel=0.0):
    """a side profile [(x, z)] (counter-clockwise seen from +y) extruded between y0 and y1"""
    n = len(profile)
    verts = [(x, y0, z) for x, z in profile] + [(x, y1, z) for x, z in profile]
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    faces += [((k + 1) % n, k, n + k, n + (k + 1) % n) for k in range(n)]
    return finish(mesh_obj(name, verts, faces, m), bevel)


def frustum(name, bot, z0, top, z1, m, bevel=0.0):
    """two outlines (same count, counter-clockwise from above) joined: a sloped-sided block"""
    n = len(bot)
    verts = [(x, y, z0) for x, y in bot] + [(x, y, z1) for x, y in top]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    faces += [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    return finish(mesh_obj(name, verts, faces, m), bevel)


def hide_tree(o, hidden):
    o.hide_render = hidden
    for c in o.children:
        hide_tree(c, hidden)


def link_to(objs, root):
    for o in objs:
        if o.parent is None and o is not root:
            o.parent = root
    return objs


def track_path():
    """the track loop in (x, z) for one side, resampled to equal steps"""
    pts = []
    sp, sr = (-3.45, 0.62), 0.36
    idl, ir = (3.28, 0.70), 0.33
    pts += [(2.40, 0.035), (-2.55, 0.035)]
    for k in range(0, 21):                                   # round the sprocket (rear), bottom-rear to top
        a = math.radians(250 - k * 8)
        pts.append((sp[0] + sr * math.cos(a), sp[1] + sr * math.sin(a)))
    pts += [(-2.0, 1.03), (0.0, 1.05), (2.0, 1.04)]
    for k in range(0, 21):                                   # round the idler (front), top to lower-front
        a = math.radians(90 - k * 8)
        pts.append((idl[0] + ir * math.cos(a), idl[1] + ir * math.sin(a)))
    pts.append((2.40, 0.035))
    # resample
    out, step, acc = [], 0.165, 0.0
    for (a, b) in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        t = acc
        while t < seg:
            u = t / seg
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, math.atan2(b[1] - a[1], b[0] - a[0])))
            t += step
        acc = t - seg
    return out


# ---------------------------------------------------------------- the tank
def build_arjun(root, bay_open=True):
    """the Arjun Mk1A, parented to `root` (an empty at the hull's origin). Returns dict of parts to animate."""
    paint = camo_mat("camo", root)
    paint_clean = camo_mat("camo_turret", root, dust=0.28)
    steel = pbr("bay_steel", "metal_plate", scale=1.2, tint=(0.42, 0.44, 0.40), rough=(0.35, 0.7), metal=0.6, nor=0.6)
    dark = mat("dark_steel", (0.035, 0.035, 0.032), 0.55, metal=0.7)
    rubber = mat("rubber", (0.02, 0.02, 0.02), 0.85)
    link_m = camo_mat("track", root, dust=0.9, rough=0.8)
    wheel_m = mat("wheel", (0.30, 0.12, 0.05), 0.7)
    glass_m = mat("optic", (0.01, 0.02, 0.03), 0.05, metal=0.2, coat=1.0)
    red_m = mat("red", (0.6, 0.02, 0.02), 0.5)
    parts = {}
    objs = []

    # hull: lower body between the tracks, upper body over them, glacis
    lower = prism_xz("hull_lower", [(-3.80, 0.50), (3.05, 0.50), (3.80, 1.00), (-3.80, 1.00)], -1.25, 1.25, paint, 0.02)
    upper = prism_xz("hull_upper", [(-3.86, 0.98), (3.72, 0.98), (3.86, 1.08), (2.50, DECK_Z), (-3.86, DECK_Z)],
                     -1.86, 1.86, paint, 0.03)
    objs.append(upper)
    if bay_open:
        bpy.ops.object.select_all(action="DESELECT")
        lower.select_set(True)
        upper.select_set(True)
        bpy.context.view_layer.objects.active = upper
        bpy.ops.object.join()
        hull = upper
        hull.name = "hull"
        bpy.ops.mesh.primitive_cube_add(size=1)
        c = bpy.context.object
        c.name = "bay_cut"
        c.location = ((BAY_X0 + BAY_X1) / 2, 0, (BAY_FLOOR + DECK_Z + 0.3) / 2)
        c.scale = (BAY_X1 - BAY_X0, 2 * BAY_Y, DECK_Z + 0.3 - BAY_FLOOR)
        c.data.materials.append(steel)
        c.hide_render = True
        c.display_type = "WIRE"
        b = hull.modifiers.new("bay", "BOOLEAN")
        b.object = c
        b.operation = "DIFFERENCE"
        b.solver = "EXACT"
        b.use_self = True
        b.material_mode = "TRANSFER"
        hull.modifiers.move(len(hull.modifiers) - 1, 0)
        objs.append(c)
    else:
        objs.append(lower)
    # rear plate details: two exhaust grilles, stowage bins, tow hooks
    for s in (-1, 1):
        objs.append(box(f"exhaust_{s}", (-3.90, s * 1.15, 1.22), (0.05, 0.62, 0.32), dark, bevel=0.01))
        for k in range(5):
            objs.append(box(f"exh_slat_{s}_{k}", (-3.93, s * 1.15, 1.10 + k * 0.06), (0.02, 0.6, 0.015), paint))
        objs.append(cyl(f"tow_{s}", (-3.95, s * 0.6, 0.78), 0.06, 0.12, dark, rot=(0, math.pi / 2, 0)))
    objs.append(box("rear_bin", (-3.95, 0, 1.30), (0.12, 0.9, 0.3), paint, bevel=0.015))
    # headlights and glacis details
    for s in (-1, 1):
        objs.append(cyl(f"lamp_{s}", (3.30, s * 1.55, 1.30), 0.07, 0.10, glass_m, rot=(0, math.radians(70), 0)))
    objs.append(box("driver_hatch", (2.15, 0.6, DECK_Z + 0.02), (0.6, 0.55, 0.05), paint, bevel=0.01))
    objs.append(cyl("driver_periscope", (2.45, 0.6, DECK_Z + 0.06), 0.06, 0.08, glass_m))

    # side skirts: six bolted panels a side
    edges = [-3.72, -2.55, -1.40, -0.25, 0.90, 2.05, 3.30]
    for s in (-1, 1):
        for i, (a0, a1) in enumerate(zip(edges, edges[1:])):
            z0 = 0.66 if i < 5 else 0.78
            p = box(f"skirt_{s}_{i}", ((a0 + a1) / 2, s * 1.92, (z0 + 1.40) / 2), (a1 - a0 - 0.03, 0.07, 1.40 - z0),
                    paint, bevel=0.012)
            objs.append(p)
            for bx in (a0 + 0.12, a1 - 0.12):
                for bz in (z0 + 0.1, 1.30):
                    objs.append(cyl(f"bolt_{s}_{i}_{bx:.2f}_{bz:.2f}", (bx, s * 1.96, bz), 0.025, 0.03, dark,
                                    rot=(math.pi / 2, 0, 0), verts=12))
        # mudguard over the idler
        objs.append(box(f"fender_{s}", (3.50, s * 1.62, 1.08), (0.6, 0.62, 0.04), paint, rot=(0, math.radians(-14), 0)))

    # running gear: 7 twin road wheels, sprocket, idler, 3 return rollers; track links
    wx = [2.35, 1.55, 0.75, -0.05, -0.85, -1.65, -2.45]
    wheels = []
    for s in (-1, 1):
        for i, x in enumerate(wx):
            for off in (-0.17, 0.17):
                w = cyl(f"wheel_{s}_{i}_{off}", (x, s * 1.62 + off, 0.41), 0.37, 0.16, wheel_m, rot=(math.pi / 2, 0, 0),
                        verts=48, bevel=0.03)
                objs.append(w)
                wheels.append(w)
                objs.append(cyl(f"hub_{s}_{i}_{off}", (x, s * 1.62 + off * 1.55, 0.41), 0.13, 0.06, dark,
                                rot=(math.pi / 2, 0, 0), verts=24))
                objs.append(cyl(f"tyre_{s}_{i}_{off}", (x, s * 1.62 + off, 0.41), 0.385, 0.12, rubber,
                                rot=(math.pi / 2, 0, 0), verts=48))
        objs.append(cyl(f"sprocket_{s}", (-3.45, s * 1.62, 0.62), 0.33, 0.34, dark, rot=(math.pi / 2, 0, 0), verts=24,
                        bevel=0.02))
        objs.append(cyl(f"idler_{s}", (3.28, s * 1.62, 0.70), 0.30, 0.30, wheel_m, rot=(math.pi / 2, 0, 0), verts=48,
                        bevel=0.02))
        for x in (1.6, -0.2, -2.0):
            objs.append(cyl(f"roller_{s}_{x}", (x, s * 1.62, 0.93), 0.09, 0.4, dark, rot=(math.pi / 2, 0, 0)))
    bpy.ops.mesh.primitive_cube_add(size=1)
    proto = bpy.context.object
    proto.scale = (0.15, 0.64, 0.07)
    bpy.ops.object.transform_apply(scale=True)
    proto.data.materials.append(link_m)
    finish(proto, 0.012)
    proto.hide_render = True
    objs.append(proto)
    for s in (-1, 1):
        for k, (x, z, ang) in enumerate(track_path()):
            o = bpy.data.objects.new(f"link_{s}_{k}", proto.data)
            bpy.context.collection.objects.link(o)
            o.location = (x, s * 1.62, z)
            o.rotation_euler = (0, -ang, 0)
            objs.append(o)

    # mine plough (Mk1A, track width): arms and a toothed blade in front of each track
    for s in (-1, 1):
        objs.append(box(f"plough_arm_{s}", (3.95, s * 1.45, 0.82), (0.9, 0.12, 0.14), paint,
                        rot=(0, math.radians(18), 0), bevel=0.01))
        blade = box(f"plough_blade_{s}", (4.45, s * 1.6, 0.35), (0.12, 0.85, 0.5), paint, rot=(0, math.radians(-25), 0),
                    bevel=0.015)
        objs.append(blade)
        for k in range(5):
            objs.append(box(f"tooth_{s}_{k}", (4.62, s * 1.6 + (k - 2) * 0.17, 0.12), (0.28, 0.05, 0.06), red_m,
                            rot=(0, math.radians(30), 0)))
    objs.append(box("plough_beam", (4.05, 0, 0.75), (0.14, 2.8, 0.16), paint, bevel=0.015))

    # turret
    tur = bpy.data.objects.new("turret", None)
    bpy.context.collection.objects.link(tur)
    tur.location = (0.35, 0, DECK_Z)
    tur.parent = root
    bot = [(2.35, -0.55), (2.35, 0.55), (1.75, 1.62), (-2.35, 1.62), (-2.65, 1.35), (-2.65, -1.35), (-2.35, -1.62),
           (1.75, -1.62)]
    top = [(1.55, -0.42), (1.55, 0.42), (1.20, 1.42), (-2.30, 1.50), (-2.55, 1.25), (-2.55, -1.25), (-2.30, -1.50),
           (1.20, -1.42)]
    shell = frustum("turret_shell", bot, 0.02, top, 0.74, paint_clean, bevel=0.03)
    shell.parent = tur
    tparts = [shell]
    # add-on armour wedges either side of the gun, panel seams as thin strips
    for s in (-1, 1):
        w = frustum(f"wedge_{s}", [(2.55, s * 0.42), (1.6, s * 1.3), (1.2, s * 1.3), (1.2, s * 0.42)][::s], 0.18,
                    [(1.95, s * 0.42), (1.35, s * 1.0), (1.1, s * 1.0), (1.1, s * 0.42)][::s], 0.66, paint_clean, 0.02)
        w.parent = tur
        tparts.append(w)
        for k in range(4):
            sm = box(f"seam_{s}_{k}", (1.1 - k * 0.95, s * 1.56, 0.42), (0.02, 0.03, 0.6), dark)
            sm.parent = tur
            tparts.append(sm)
        # smoke grenade launchers: a cluster of 6 tubes at each rear corner
        for k in range(6):
            t = cyl(f"smoke_{s}_{k}", (-2.2 + (k % 3) * 0.17, s * (1.62 - (k // 3) * 0.16), 0.98), 0.065, 0.36, dark,
                    rot=(math.radians(-35) * s, math.radians(-10), 0), verts=16)
            t.parent = tur
            tparts.append(t)
        ant = cyl(f"antenna_{s}", (-2.25, s * 1.15, 2.05), 0.012, 2.6, dark, verts=8)
        ant.parent = tur
        tip = cyl(f"antenna_tip_{s}", (-2.25, s * 1.15, 3.30), 0.02, 0.16, red_m, verts=8)
        tip.parent = tur
        tparts += [ant, tip]
    for p in [box("bustle_box", (-1.9, -0.55, 0.86), (0.7, 0.75, 0.24), paint_clean, bevel=0.02),
              cyl("bustle_can", (-2.35, 0.55, 0.95), 0.22, 0.5, paint_clean, rot=(math.pi / 2, 0, 0), bevel=0.02),
              box("cmdr_sight_base", (0.2, -0.65, 0.84), (0.35, 0.35, 0.22), paint_clean, bevel=0.015),
              box("cmdr_sight_head", (0.2, -0.65, 1.05), (0.42, 0.36, 0.26), dark, bevel=0.02),
              box("cmdr_sight_glass", (0.42, -0.65, 1.05), (0.02, 0.26, 0.14), glass_m),
              cyl("cmdr_hatch", (-0.7, -0.75, 0.78), 0.36, 0.08, paint_clean, bevel=0.01),
              cyl("loader_hatch", (-0.6, 0.8, 0.77), 0.32, 0.06, paint_clean, bevel=0.01),
              box("gunner_sight", (1.05, 0.95, 0.82), (0.45, 0.32, 0.2), dark, bevel=0.02),
              box("rcws_base", (-0.2, 0.15, 0.86), (0.55, 0.5, 0.24), paint_clean, bevel=0.02),
              box("rcws_body", (-0.15, 0.15, 1.12), (0.5, 0.38, 0.3), dark, bevel=0.02),
              cyl("rcws_mg", (0.35, 0.15, 1.16), 0.025, 1.0, dark, rot=(0, math.pi / 2, 0), verts=12)]:
        p.parent = tur
        tparts.append(p)

    # stowage basket round the bustle: rails on posts
    for s in (-1, 1):
        for x in (-2.8, -2.1, -1.4):
            pst = cyl(f"post_{s}_{x}", (x, s * 1.72, 0.55), 0.015, 0.4, dark, verts=8)
            pst.parent = tur
            tparts.append(pst)
        for z in (0.42, 0.72):
            rl = cyl(f"rail_{s}_{z}", (-2.1, s * 1.72, z), 0.015, 1.5, dark, rot=(0, math.pi / 2, 0), verts=8)
            rl.parent = tur
            tparts.append(rl)
        bag = box(f"bag_{s}", (-2.1, s * 1.68, 0.5), (1.3, 0.12, 0.28), mat(f"canvas_{s}", (0.18, 0.15, 0.08), 0.9),
                  bevel=0.04)
        bag.parent = tur
        tparts.append(bag)

    # gun: mantlet, sleeved barrel, fume extractor, muzzle reference sensor; on a trunnion for elevation
    gun = bpy.data.objects.new("gun", None)
    bpy.context.collection.objects.link(gun)
    gun.parent = tur
    gun.location = (1.9, 0, 0.42)
    mant = box("mantlet", (0.55, 0, 0), (0.7, 0.75, 0.5), dark, bevel=0.04)
    mant.parent = gun
    gparts = [mant]
    sleeve = [(0.9, 1.3, 0.145), (1.3, 2.7, 0.135), (2.7, 3.5, 0.185), (3.5, 5.4, 0.13), (5.4, 6.95, 0.115)]
    for i, (a0, a1, r) in enumerate(sleeve):
        c = cyl(f"barrel_{i}", ((a0 + a1) / 2, 0, 0), r, a1 - a0, paint_clean, rot=(0, math.pi / 2, 0), verts=40,
                bevel=0.01)
        c.parent = gun
        gparts.append(c)
        band = cyl(f"band_{i}", (a1, 0, 0), r + 0.012, 0.05, dark, rot=(0, math.pi / 2, 0), verts=40)
        band.parent = gun
        gparts.append(band)
    mz = cyl("muzzle", (7.0, 0, 0), 0.09, 0.12, dark, rot=(0, math.pi / 2, 0))
    mrs = box("mrs", (6.9, 0, 0.17), (0.12, 0.08, 0.12), dark)
    mz.parent = gun
    mrs.parent = gun
    gparts += [mz, mrs]

    # the bay: mounts with bolt holes, the final-drive flanges, pipe ends and cut cable ends on the firewall
    bay = []
    if bay_open:
        for x in (-2.05, -3.25):
            for y in (-0.72, 0.72):
                m_ = box(f"mount_{x}_{y}", (x, y, BAY_FLOOR + 0.09), (0.32, 0.26, 0.18), steel, bevel=0.015)
                bay.append(m_)
                for dx in (-0.08, 0.08):
                    bay.append(cyl(f"mhole_{x}_{y}_{dx}", (x + dx, y, BAY_FLOOR + 0.185), 0.035, 0.012, dark, verts=16))
        for s in (-1, 1):
            fl = cyl(f"final_drive_{s}", (-3.42, s * (BAY_Y - 0.03), 0.80), 0.20, 0.08, steel, rot=(math.pi / 2, 0, 0),
                     bevel=0.01)
            bay.append(fl)
            for k in range(8):
                a = k / 8 * math.tau
                bay.append(cyl(f"fd_bolt_{s}_{k}", (-3.42 + 0.15 * math.cos(a), s * (BAY_Y - 0.075),
                                                     0.80 + 0.15 * math.sin(a)), 0.018, 0.02, dark,
                               rot=(math.pi / 2, 0, 0), verts=8))
            bay.append(cyl(f"fd_hole_{s}", (-3.42, s * (BAY_Y - 0.07), 0.80), 0.09, 0.02, dark, rot=(math.pi / 2, 0, 0)))
            # air-intake duct mouths, top corners of the firewall
            bay.append(box(f"intake_{s}", (BAY_X1 - 0.02, s * 0.85, 1.32), (0.04, 0.5, 0.26), dark))
        for i, (y, z, r) in enumerate([(-0.35, 0.95, 0.07), (-0.15, 0.95, 0.07), (0.25, 1.05, 0.055),
                                       (0.45, 0.82, 0.045), (0.0, 1.25, 0.09)]):
            pipe = cyl(f"pipe_{i}", (BAY_X1 - 0.12, y, z), r, 0.24, steel, rot=(0, math.pi / 2, 0), bevel=0.008)
            bay.append(pipe)
            bay.append(cyl(f"pipe_end_{i}", (BAY_X1 - 0.245, y, z), r * 0.72, 0.012, dark, rot=(0, math.pi / 2, 0)))
        for k in range(3):
            bay.append(cyl(f"cable_{k}", (BAY_X1 - 0.18, -0.85 + k * 0.07, 0.75), 0.022, 0.36, rubber,
                           rot=(0, math.radians(80), 0), verts=12))
        bay.append(box("firewall_rib", (BAY_X1 - 0.03, 0, 1.05), (0.05, 2.3, 0.06), steel))
        bay.append(box("floor_rib", ((BAY_X0 + BAY_X1) / 2, 0, BAY_FLOOR + 0.02), (2.1, 0.08, 0.04), steel))
        objs += bay

    # deck seams and bolts, sponson stowage, lifting eyes
    for x in (-1.25, 0.9, 2.2):
        objs.append(box(f"deck_seam_{x}", (x, 0, DECK_Z + 0.004), (0.02, 3.6, 0.012), dark))
    for s in (-1, 1):
        objs.append(box(f"deck_edge_{s}", (-0.6, s * 1.52, DECK_Z + 0.004), (6.4, 0.02, 0.012), dark))
        for k in range(12):
            objs.append(cyl(f"deck_bolt_{s}_{k}", (-3.6 + k * 0.55, s * 1.62, DECK_Z + 0.01), 0.022, 0.02, dark,
                            verts=10))
        # tools on the sponson: a shovel, a crowbar, a tow cable along the hull edge
        objs.append(box(f"shovel_{s}", (1.2, s * 1.72, DECK_Z + 0.03), (1.1, 0.05, 0.03), dark))
        objs.append(box(f"shovel_blade_{s}", (1.85, s * 1.72, DECK_Z + 0.03), (0.28, 0.2, 0.025), dark))
        objs.append(cyl(f"crowbar_{s}", (-0.3, s * 1.76, DECK_Z + 0.03), 0.02, 1.5, dark, rot=(0, math.pi / 2, 0),
                        verts=10))
        objs.append(cyl(f"cable_{s}", (0.5, s * 1.81, DECK_Z - 0.06), 0.03, 5.6, dark, rot=(0, math.pi / 2, 0),
                        verts=10))
        objs.append(cyl(f"lift_eye_{s}", (2.6, s * 1.4, DECK_Z + 0.05), 0.05, 0.03, dark, rot=(math.pi / 2, 0, 0),
                        verts=12))
    if bay_open:
        n_bay = len(bay)
        # the room's walls: ribs, a cable tray, coolant lines with clamps along the side walls
        for s in (-1, 1):
            for x in (-2.2, -2.9):
                bay.append(box(f"rib_{s}_{x}", (x, s * (BAY_Y - 0.02), (BAY_FLOOR + DECK_Z) / 2), (0.06, 0.04, 0.9),
                               steel))
            bay.append(box(f"tray_{s}", ((BAY_X0 + BAY_X1) / 2, s * (BAY_Y - 0.06), 1.25), (2.0, 0.1, 0.03), steel))
            for k in range(4):
                bay.append(cyl(f"wire_{s}_{k}", ((BAY_X0 + BAY_X1) / 2, s * (BAY_Y - 0.05 - k * 0.022), 1.28), 0.011,
                               2.0, rubber, rot=(0, math.pi / 2, 0), verts=8))
            bay.append(cyl(f"coolant_{s}", ((BAY_X0 + BAY_X1) / 2 + 0.2, s * (BAY_Y - 0.09), 0.92), 0.045, 1.6,
                           steel, rot=(0, math.pi / 2, 0), verts=16))
            for k in range(3):
                bay.append(cyl(f"clamp_{s}_{k}", (-3.0 + k * 0.6, s * (BAY_Y - 0.09), 0.92), 0.055, 0.04, dark,
                               rot=(0, math.pi / 2, 0), verts=16))
            bay.append(cyl(f"coolant_end_{s}", (-1.68 + 0.2 - 2.0 * 0.0, s * (BAY_Y - 0.09), 0.92), 0.032, 0.012,
                           dark, rot=(0, math.pi / 2, 0), verts=16))
        objs += bay[n_bay:]

    # engine-deck covers: two grille plates over the bay (they lift away in `bayopen`)
    covers = []
    for i, (a0, a1) in enumerate([(BAY_X0, -2.62), (-2.58, BAY_X1)]):
        cv = bpy.data.objects.new(f"cover_{i}", None)
        bpy.context.collection.objects.link(cv)
        cv.location = ((a0 + a1) / 2, 0, DECK_Z + 0.03)
        cv.parent = root
        plate = box(f"cover_plate_{i}", (0, 0, 0), (a1 - a0 + 0.06, 2 * BAY_Y + 0.16, 0.05), paint, bevel=0.01)
        plate.parent = cv
        plate.location = (0, 0, 0)
        for k in range(9):
            sl = box(f"louvre_{i}_{k}", (0, -0.95 + k * 0.237, 0.035), (a1 - a0 - 0.25, 0.09, 0.025), dark)
            sl.parent = cv
            sl.location = (0, -0.95 + k * 0.237, 0.035)
        for (bx, by) in [(-0.95, -1.2), (0.95, -1.2), (-0.95, 1.2), (0.95, 1.2)]:
            bt = cyl(f"cbolt_{i}_{bx}_{by}", (0, 0, 0), 0.03, 0.03, dark, verts=12)
            bt.parent = cv
            bt.location = (bx * (a1 - a0) / 2.2, by, 0.03)
        covers.append(cv)

    link_to(objs, root)
    parts.update(turret=tur, gun=gun, covers=covers, wheels=wheels, bay=bay)
    return parts


def dunes(ground_m):
    """the Thar: flat hard sand round the tank, low dunes rising beyond 25 m"""
    n, size = 160, 600.0
    verts, faces = [], []
    rnd = random.Random(7)
    waves = [(rnd.uniform(0, math.tau), rnd.uniform(0.012, 0.04), rnd.uniform(0, math.tau), rnd.uniform(1.0, 4.5))
             for _ in range(7)]
    for j in range(n + 1):
        for i in range(n + 1):
            x = -size / 2 + size * i / n
            y = -size / 2 + size * j / n
            r = math.hypot(x, y)
            h = sum(a * math.sin(k * (x * math.cos(d) + y * math.sin(d)) + ph) for d, k, ph, a in waves)
            h = (h + 6) * smooth((r - 25) / 90)
            verts.append((x, y, h - 0.02))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + 1, a + n + 2, a + n + 1))
    g = mesh_obj("ground", verts, faces, ground_m)
    for p in g.data.polygons:
        p.use_smooth = True
    # fine near-field ground for crisp sand at the tank
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    near = bpy.context.object
    near.name = "ground_near"
    near.data.materials.append(ground_m)
    return g, near


def thar_scene(a, exposure=0.0, sun_elev=18.0, sun_az=-35.0):
    sc, cam = setup(a, exposure)
    world_hdri(sc, "kloofendal_43d_clear_puresky", strength=0.55, rot=math.radians(40), color=(1.0, 0.93, 0.85))
    sun = light("SUN", (0, 0, 10), None, 4.2, (1.0, 0.74, 0.48), size=math.radians(1.2))
    sun.rotation_euler = (math.radians(90 - sun_elev), 0, math.radians(sun_az))
    root = bpy.data.objects.new("arjun", None)
    bpy.context.collection.objects.link(root)
    gm = ground_mat()
    dunes(gm)
    return sc, cam, root, sun


def bay_light(root, strength):
    """the glow from inside the empty room: an area light on the floor facing up, two low fill points, thin haze"""
    l1 = light("AREA", (-1.75, 0, 0.95), (-3.3, 0, 0.7), strength, YEL, size=1.8)
    l1.data.shape = "RECTANGLE"
    l1.data.size, l1.data.size_y = 0.5, 2.0
    l2 = light("POINT", (-3.45, 0.85, 0.75), None, strength * 0.06, YEL, size=0.15)
    l3 = light("POINT", (-2.6, -0.95, 0.70), None, strength * 0.06, YEL, size=0.15)
    # light linking: the bay lights reach only the hull and the room's own parts, never the sand
    rc = bpy.data.collections.new("bay_receivers")
    for o in bpy.data.objects:
        if o.type == "MESH" and (o.name == "hull" or o.name.split("_")[0] in (
                "mount", "mhole", "final", "fd", "intake", "pipe", "cable", "firewall", "floor", "rib", "tray",
                "wire", "coolant", "clamp", "exhaust", "exh", "rear", "deck", "turret", "wedge", "bustle")):
            rc.objects.link(o)
    hz = haze((-2.6, 0, DECK_Z + 0.25), (2.2, 2.5, 1.4), 0.012, (1.0, 0.8, 0.5), name="bay_haze")
    rc.objects.link(hz)
    for l in (l1, l2, l3):
        l.light_linking.receiver_collection = rc
    for o in (l1, l2, l3, hz):
        o.parent = root
    return [l1, l2, l3], hz


# ---------------------------------------------------------------- shots
def build_bayopen(a):
    sc, cam, root, sun = thar_scene(a)
    parts = build_arjun(root, bay_open=True)
    parts["gun"].rotation_euler = (0, math.radians(-2.5), 0)
    lights, hz = bay_light(root, 0.0)
    vol = hz.data.materials[0].node_tree.nodes["Principled Volume"].inputs["Density"]

    def frame(f):
        aim_cam(cam,
                keys(f, [(0, (6.5, 14.5, 2.0)), (300, (-2.0, 15.5, 3.0)), (600, (-10.5, 8.5, 5.2)),
                         (900, (-7.2, 4.2, 6.6))]),
                keys(f, [(0, (0.2, 0, 1.45)), (300, (-1.2, 0, 1.35)), (600, (-2.4, 0, 1.2)), (900, (-2.65, 0, 0.9))]),
                keys(f, [(0, 32.0), (600, 38.0), (900, 34.0)]), fstop=8.0)
        for i, cv in enumerate(parts["covers"]):
            t0 = 420 + i * 40
            lift = smooth((f - t0) / 150)
            cv.location = (cv.location[0], (0.6 + 2.8 * lift) * (1 if i else -1) * lift, DECK_Z + 0.03 + 3.2 * lift)
            cv.rotation_euler = (math.radians(35) * lift * (1 if i else -1), math.radians(-12) * lift, 0)
            hide_tree(cv, f > t0 + 150)
        g = smooth((f - 470) / 120)
        for k, l in enumerate(lights):
            l.data.energy = (320 if k == 0 else 25) * g
        vol.default_value = 0.012 * g

    tracked = track_cam(cam) + track_obj(*parts["covers"], props=("location", "rotation_euler"))
    tracked += [(l.data, "energy") for l in lights] + [(vol, "default_value")]
    render(sc, a, frame, tracked)


def build_thumb(a):
    sc, cam, root, sun = thar_scene(a, exposure=0.1, sun_elev=11.0, sun_az=-55.0)
    parts = build_arjun(root, bay_open=True)
    parts["gun"].rotation_euler = (0, math.radians(-3), 0)
    parts["turret"].rotation_euler = (0, 0, math.radians(-22))
    for cv in parts["covers"]:
        hide_tree(cv, True)
    lights, hz = bay_light(root, 1.0)
    lights[0].data.energy = 340
    for l in lights[1:]:
        l.data.energy = 28

    def frame(f):
        aim_cam(cam, (-9.0, 6.6, 4.9), (-1.2, 0.0, 1.0), 27.0, fstop=11.0)

    render(sc, a, frame, track_cam(cam))


SHOTS = {"bayopen": build_bayopen, "thumb": build_thumb}


def main():
    a = args()
    if a.shot not in SHOTS:
        sys.exit(f"unknown shot {a.shot}")
    SHOTS[a.shot](a)


if __name__ == "__main__":
    main()
