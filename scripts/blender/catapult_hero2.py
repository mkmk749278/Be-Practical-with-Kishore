"""Hero shots for carrier-catapult, second build (owner, 2026-11-15: "3D shots: concentrate more and get the best").
Every shot is labelled ILLUSTRATION in Remotion (the catapult and cutaways also SIMPLIFIED).

  .venv-blender/bin/python scripts/blender/catapult_hero2.py --shot NAME --out DIR --frames a-b --step 2 [--w --h]

Why a second build: the first (catapult_hero.py) was plain primitives in flat light on a void-like plate; it read as
a slide, not a film. This build uses scanned CC0 materials (Poly Haven, scripts/blender/ph_assets.py), HDRI light,
bevelled edges, haze with light shafts, depth of field and real motion blur (every motion is keyframed, so Cycles
sees it between frames). Timings of the four rebuilt shots are kept, so the Remotion offsets still land on the words.

Shots (frames at 60 fps):
  deckrun  (0-329)  S17: the pilot's seat on a carrier deck: the run along the deck, the deck curves up the ski-jump
                         and ends in the sky (the lip passes under the camera at about 250).
  rampjet  (0-389)  S24-25: behind a jet at the foot of the ramp, loaded (tanks and missiles under the wings); the
                         engines spool from 0, the afterburners light at 240 ("its own engines"), it rolls at 255 and
                         climbs off the ramp (lip at about 370). A generic jet, no markings.
  catapult (0-599)  S50: the 1961 steam catapult in a sectioned deck: twin slotted cylinders under the slot; steam
                         fires the pistons (150-330) and the shuttle drags a 1950s straight-winged jet by its bridle.
  drum     (0-959)  S52-56, S70-72: a riveted boiler water drum with its rows of generating tubes rising into the
                         dark; cracks glow one by one (60-300); steel bands come down and ratchet tight (420, 560, 700).
  room     (0-599)  S73-75: a Bourdon gauge on its pigtail; the needle swings into the red (150-260) and holds; the
                         camera pulls back through the hazy boiler room.
  store    (0-959)  S120-125: a motor generator in cutaway, others behind; the rotor spins up (0-420), its copper glows;
                         at 600 the energy is pulled out in three seconds (600-780), a pulse runs along the bus.
Deterministic: fixed seeds, no simulation; labels come from Remotion.
"""
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ph_assets  # noqa: E402

FPS = 60


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", default="deckrun")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="0-0")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--bounces", type=int, default=8)
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--noblur", action="store_true")
    ap.add_argument("--gpu", action="store_true", help="render on the NVIDIA GPU with OptiX (Modal; PLAYBOOK §14.1)")
    ap.add_argument("--noise", type=float, default=0.02, help="adaptive sampling noise threshold")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


# ---------------------------------------------------------------- timing helpers
def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def keys(f, ks):
    if f <= ks[0][0]:
        return ks[0][1]
    for (f0, v0), (f1, v1) in zip(ks, ks[1:]):
        if f <= f1:
            t = smooth((f - f0) / (f1 - f0))
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * t for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * t
    return ks[-1][1]


# ---------------------------------------------------------------- materials
def _bsdf(m):
    return m.node_tree.nodes["Principled BSDF"]


def mat(name, color, rough, metal=0.0, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = _bsdf(m)
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


def emit_socket(m):
    return _bsdf(m).inputs["Emission Strength"]


def pbr(name, asset, scale=1.0, tint=(1, 1, 1), rough=(0.0, 1.0), metal=0.0, nor=1.0, emit=None, grime=0.0,
        coords="Object", blend=0.25, streaks=0.0):
    """A Poly Haven texture set, box-projected from object (or generated) coordinates, `scale` metres per tile."""
    files = ph_assets.texture(asset)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt, p = m.node_tree, _bsdf(m)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1 / scale, 1 / scale, 1 / scale)
    nt.links.new(tc.outputs[coords], mp.inputs["Vector"])

    def img(key, noncolor):
        n = nt.nodes.new("ShaderNodeTexImage")
        n.image = bpy.data.images.load(files[key], check_existing=True)
        if noncolor:
            n.image.colorspace_settings.name = "Non-Color"
        n.projection = "BOX"
        n.projection_blend = blend
        nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
        return n

    d = img("diff", False)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 1.0
    nt.links.new(d.outputs["Color"], mix.inputs[6])
    mix.inputs[7].default_value = (*tint, 1)
    col = mix.outputs[2]
    if grime:
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 0.6
        nz.inputs["Detail"].default_value = 6
        nt.links.new(tc.outputs[coords], nz.inputs["Vector"])
        ramp = nt.nodes.new("ShaderNodeMapRange")
        ramp.inputs["From Min"].default_value = 0.45
        ramp.inputs["From Max"].default_value = 0.75
        ramp.inputs["To Min"].default_value = 1.0
        ramp.inputs["To Max"].default_value = 1.0 - grime
        g = nt.nodes.new("ShaderNodeMix")
        g.data_type = "RGBA"
        g.blend_type = "MULTIPLY"
        g.inputs["Factor"].default_value = 1.0
        nt.links.new(col, g.inputs[6])
        cr = nt.nodes.new("ShaderNodeCombineColor")
        for k in ("Red", "Green", "Blue"):
            nt.links.new(ramp.outputs["Result"], cr.inputs[k])
        nt.links.new(nz.outputs["Fac"], ramp.inputs["Value"])
        nt.links.new(cr.outputs["Color"], g.inputs[7])
        col = g.outputs[2]
    if streaks:
        # tyre and exhaust streaks along x (a flight deck's rubber marks)
        sm = nt.nodes.new("ShaderNodeMapping")
        sm.inputs["Scale"].default_value = (0.04, 1.6, 1.0)
        nt.links.new(tc.outputs[coords], sm.inputs["Vector"])
        sn = nt.nodes.new("ShaderNodeTexNoise")
        sn.inputs["Scale"].default_value = 1.0
        sn.inputs["Detail"].default_value = 8
        nt.links.new(sm.outputs["Vector"], sn.inputs["Vector"])
        sr = nt.nodes.new("ShaderNodeMapRange")
        sr.inputs["From Min"].default_value = 0.5
        sr.inputs["From Max"].default_value = 0.72
        sr.inputs["To Min"].default_value = 1.0
        sr.inputs["To Max"].default_value = 1.0 - streaks
        nt.links.new(sn.outputs["Fac"], sr.inputs["Value"])
        cs = nt.nodes.new("ShaderNodeCombineColor")
        for k in ("Red", "Green", "Blue"):
            nt.links.new(sr.outputs["Result"], cs.inputs[k])
        g2 = nt.nodes.new("ShaderNodeMix")
        g2.data_type = "RGBA"
        g2.blend_type = "MULTIPLY"
        g2.inputs["Factor"].default_value = 1.0
        nt.links.new(col, g2.inputs[6])
        nt.links.new(cs.outputs["Color"], g2.inputs[7])
        col = g2.outputs[2]
    nt.links.new(col, p.inputs["Base Color"])
    if "rough" in files:
        r = img("rough", True)
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = rough
        nt.links.new(r.outputs["Color"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], p.inputs["Roughness"])
    if "metal" in files and metal is None:
        nt.links.new(img("metal", True).outputs["Color"], p.inputs["Metallic"])
    else:
        p.inputs["Metallic"].default_value = metal or 0.0
    if "nor" in files and nor:
        n = img("nor", True)
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = nor
        nt.links.new(n.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = 0.0
    return m


def glass(name="glass"):
    m = mat(name, (1, 1, 1), 0.02)
    _bsdf(m).inputs["Transmission Weight"].default_value = 1.0
    _bsdf(m).inputs["IOR"].default_value = 1.5
    return m


def flame_mat(name, color, strength):
    """an afterburner/steam glow: emission that fades to transparent at grazing angles (soft edges)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.85
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lw.outputs["Facing"], mx.inputs["Fac"])
    nt.links.new(em.outputs["Emission"], mx.inputs[1])
    nt.links.new(tr.outputs["BSDF"], mx.inputs[2])
    nt.links.new(mx.outputs["Shader"], out.inputs["Surface"])
    m.blend_method = "BLEND"
    return m, em.inputs["Strength"]


def haze(loc, size, density, color=(1, 1, 1), name="haze"):
    """a box of thin haze so lights draw shafts (kept to the shot's volume for render time)"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(_bsdf(m))
    v = nt.nodes.new("ShaderNodeVolumePrincipled")
    v.inputs["Density"].default_value = density
    v.inputs["Color"].default_value = (*color, 1)
    v.inputs["Anisotropy"].default_value = 0.35
    nt.links.new(v.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    o.data.materials.append(m)
    o.visible_shadow = False
    return o


# ---------------------------------------------------------------- scene helpers
def setup(a, exposure=0.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = getattr(a, "noise", 0.02)
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    if getattr(a, "gpu", False):
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == "OPTIX"
        if not any(d.use for d in prefs.devices):
            raise SystemExit("no OptiX device found")
        sc.cycles.device = "GPU"
        sc.cycles.denoiser = "OPTIX"
    sc.cycles.max_bounces = a.bounces
    sc.cycles.transparent_max_bounces = 16
    sc.cycles.volume_bounces = 1
    sc.cycles.volume_step_rate = 4.0
    sc.cycles.sample_clamp_indirect = 8.0
    sc.cycles.blur_glossy = 1.0
    sc.cycles.seed = 5
    sc.render.fps = FPS
    sc.render.resolution_x, sc.render.resolution_y = a.w, a.h
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "16"
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = exposure
    sc.render.use_motion_blur = not a.noblur
    sc.render.motion_blur_shutter = 0.5
    if a.threads:
        sc.render.threads_mode = "FIXED"
        sc.render.threads = a.threads
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    cam.data.clip_end = 20000
    cam.data.sensor_width = 36
    sc.camera = cam
    return sc, cam


def world_hdri(sc, asset, strength=1.0, rot=0.0, color=None, bg_strength=None):
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(ph_assets.hdri(asset), check_existing=True)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, rot)
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    if color:
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        mx.blend_type = "MULTIPLY"
        mx.inputs["Factor"].default_value = 1.0
        nt.links.new(env.outputs["Color"], mx.inputs[6])
        mx.inputs[7].default_value = (*color, 1)
        nt.links.new(mx.outputs[2], bg.inputs["Color"])
    else:
        nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    if bg_strength is not None:
        # the camera sees a different strength from the lighting (a dark room lit by its HDRI)
        lp = nt.nodes.new("ShaderNodeLightPath")
        bg2 = nt.nodes.new("ShaderNodeBackground")
        bg2.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1)
        bg2.inputs["Strength"].default_value = bg_strength
        nt.links.new(bg.inputs["Color"].links[0].from_socket, bg2.inputs["Color"])
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
        nt.links.new(bg.outputs["Background"], mx.inputs[1])
        nt.links.new(bg2.outputs["Background"], mx.inputs[2])
        nt.links.new(mx.outputs["Shader"], nt.nodes["World Output"].inputs["Surface"])


def light(kind, loc, aim, energy, color, size=1.0, spot=None):
    bpy.ops.object.light_add(type=kind, location=loc)
    l = bpy.context.object
    l.data.energy = energy
    l.data.color = color
    if kind == "AREA":
        l.data.size = size
    elif kind in ("POINT", "SPOT"):
        l.data.shadow_soft_size = size
    elif kind == "SUN":
        l.data.angle = size
    if kind == "SPOT" and spot:
        l.data.spot_size = math.radians(spot)
        l.data.spot_blend = 0.6
    if aim:
        l.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return l


def aim_cam(cam, loc, aim, lens, fstop=None, roll=0.0):
    cam.location = loc
    q = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y")
    e = q.to_euler()
    if roll:
        from mathutils import Quaternion
        q = q @ Quaternion((0, 0, 1), roll)
        e = q.to_euler()
    cam.rotation_euler = e
    cam.data.lens = lens
    if fstop:
        cam.data.dof.use_dof = True
        cam.data.dof.aperture_fstop = fstop
        cam.data.dof.focus_distance = (Vector(aim) - Vector(loc)).length
    else:
        cam.data.dof.use_dof = False


def finish(o, bevel=0.0, smooth_angle=None, segs=2):
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL")
        b.width = bevel
        b.segments = segs
        b.limit_method = "ANGLE"
    if smooth_angle is not None:
        for p in o.data.polygons:
            p.use_smooth = True
        o.data.set_sharp_from_angle(angle=math.radians(smooth_angle))
    return o


def box(name, loc, size, m, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    return finish(o, bevel)


def cyl(name, loc, r, depth, m, rot=(0, 0, 0), verts=64, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    return finish(o, bevel, 35)


def torus(name, loc, R, r, m, rot=(0, 0, 0), seg=96):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=seg,
                                     minor_segments=12)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(m)
    return finish(o, 0, 60)


def sphere(name, loc, r, m, scale=(1, 1, 1), seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(m)
    return finish(o, 0, 60)


def parent(child, par):
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()
    return child


def cutter(loc, size):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    c = bpy.context.object
    c.scale = size
    c.hide_render = True
    c.display_type = "WIRE"
    return c


def boolean(o, c, op="DIFFERENCE"):
    b = o.modifiers.new("cut", "BOOLEAN")
    b.object = c
    b.operation = op
    b.solver = "EXACT"
    # keep the bevel after the cut so the cut edges are softened too
    if "bevel" in o.modifiers:
        o.modifiers.move(len(o.modifiers) - 1, 0)
    return o


def mesh_obj(name, verts, faces, m):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def loft(name, stations, m, segs=40):
    """a smooth body of revolution-like shape: stations = [(x, half-width, half-height, z-centre)]"""
    verts, faces = [], []
    for (x, ry, rz, zc) in stations:
        for k in range(segs):
            t = k / segs * math.tau
            verts.append((x, ry * math.cos(t), zc + rz * math.sin(t)))
    n = len(stations)
    for i in range(n - 1):
        for k in range(segs):
            a, b = i * segs + k, i * segs + (k + 1) % segs
            faces.append((a, b, b + segs, a + segs))
    verts += [(stations[0][0], 0, stations[0][3]), (stations[-1][0], 0, stations[-1][3])]
    c0, c1 = len(verts) - 2, len(verts) - 1
    for k in range(segs):
        faces.append((c0, (k + 1) % segs, k))
        faces.append((c1, (n - 1) * segs + k, (n - 1) * segs + (k + 1) % segs))
    o = mesh_obj(name, verts, faces, m)
    return finish(o, 0, 50)


def slab(name, outline, z0, z1, m, bevel=0.0):
    """an extruded polygon (outline in xy, counter-clockwise) between heights z0 and z1"""
    n = len(outline)
    verts = [(x, y, z0) for x, y in outline] + [(x, y, z1) for x, y in outline]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    faces += [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    return finish(mesh_obj(name, verts, faces, m), bevel)


def wing(name, outline_xy, thick, m, z=0.0, dihedral=0.0, side=1):
    """a thin lifting surface from a planform (x, y>=0), mirrored by `side`"""
    pts = [(x, side * y) for x, y in outline_xy]
    if side < 0:
        pts = pts[::-1]
    o = slab(name, pts, z - thick / 2, z + thick / 2, m)
    o.rotation_euler = (side * math.radians(dihedral), 0, 0)
    return finish(o, thick * 0.45, None, 3)


# ---------------------------------------------------------------- render: keyframe every motion, then render
def render(sc, a, frame_fn, tracked):
    """frame_fn(f) sets the scene for frame f; tracked = [(datablock, data_path)] gets a key on every frame, so
    Cycles' motion blur sees the motion between frames."""
    lo, hi = map(int, a.frames.split("-"))
    for f in range(lo - 2, hi + 3):
        frame_fn(f)
        for blk, path in tracked:
            blk.keyframe_insert(path, frame=f)
    os.makedirs(a.out, exist_ok=True)
    for f in range(lo, hi + 1, a.step):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(a.out, f"{a.shot}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"frame {f}", flush=True)


def track_obj(*objs, props=("location", "rotation_euler", "scale")):
    return [(o, p) for o in objs for p in props]


def track_cam(cam):
    return track_obj(cam, props=("location", "rotation_euler")) + [(cam.data, "lens"), (cam.data.dof, "focus_distance")]


# ================================================================ the carrier deck and the ski-jump
RAMP_L, RAMP_H = 56.0, 7.0   # drawn: a 56 m ramp rising 7 m (exit slope about 14 degrees; not stated on screen)


def zr(x):
    if x <= 0:
        return 0.0
    if x >= RAMP_L:
        return RAMP_H
    return RAMP_H * (x / RAMP_L) ** 2


def slope(x):
    return 0.0 if x <= 0 or x >= RAMP_L else 2 * RAMP_H * x / RAMP_L ** 2


def deck_width(x):
    # the flight deck narrows towards the bow
    return 26.0 if x < -60 else 26.0 - 10.0 * smooth((x + 60) / (RAMP_L + 60))


def follow_strip(name, x0, x1, y0, y1, m, lift=0.012, step=0.5):
    """a flat strip on the deck surface (markings), following the ramp's curve"""
    xs, x = [], x0
    while x < x1:
        xs.append(x)
        x += step
    xs.append(x1)
    verts, faces = [], []
    for i, x in enumerate(xs):
        verts += [(x, y0, zr(x) + lift), (x, y1, zr(x) + lift)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    return mesh_obj(name, verts, faces, m)


def edge_strip(name, x0, x1, side, inset, width, m, lift=0.012, step=1.0):
    """a marking that keeps `inset` metres inside the (narrowing) deck edge"""
    xs, x = [], x0
    while x < x1:
        xs.append(x)
        x += step
    xs.append(x1)
    verts, faces = [], []
    for i, x in enumerate(xs):
        e = deck_width(x) / 2 - inset
        y0, y1 = sorted((side * e, side * (e - width)))
        verts += [(x, y0, zr(x) + lift), (x, y1, zr(x) + lift)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    return mesh_obj(name, verts, faces, m)


def lead_line(name, xa, ya, xb, x1, m, w=0.15, lift=0.03, step=1.0):
    """a take-off lead line from (xa, ya) curving in to the centre line at xb, then straight to x1"""
    xs, x = [], xa
    while x < x1:
        xs.append(x)
        x += step
    xs.append(x1)
    verts, faces = [], []
    for i, x in enumerate(xs):
        yc = ya * (1 - smooth((x - xa) / (xb - xa)))
        verts += [(x, yc - w, zr(x) + lift), (x, yc + w, zr(x) + lift)]
        if i:
            a = 2 * (i - 1)
            faces.append((a, a + 2, a + 3, a + 1))
    return mesh_obj(name, verts, faces, m)


def build_carrier(sc):
    """the deck, the ramp, the island, the hull sides and the sea (shared by deckrun and rampjet)"""
    world_hdri(sc, "kloofendal_48d_partly_cloudy_puresky", 1.0, rot=math.radians(200))
    sun = light("SUN", (0, 0, 50), None, 4.5, (1.0, 0.95, 0.86), size=math.radians(1.2))
    sun.rotation_euler = (math.radians(52), 0, math.radians(-145))
    deck_m = pbr("deck", "concrete_floor_worn_001", 2.5, tint=(0.2, 0.21, 0.22), rough=(0.65, 0.95), nor=1.4, grime=0.45,
                 streaks=0.55)
    hull_m = pbr("hull", "painted_metal_shutter", 4.0, tint=(0.55, 0.58, 0.6), rough=(0.45, 0.8), nor=0.4, grime=0.3)
    # the deck: a grid that follows the ramp
    xs = [x for x in range(-260, 0, 4)] + [k * 0.5 for k in range(int(RAMP_L * 2) + 1)]
    ny = 10
    verts, faces = [], []
    for i, x in enumerate(xs):
        w = deck_width(x)
        for j in range(ny + 1):
            verts.append((x, -w / 2 + w * j / ny, zr(x)))
        if i:
            for j in range(ny):
                a, b = (i - 1) * (ny + 1) + j, i * (ny + 1) + j
                faces.append((a, b, b + 1, a + 1))
    deck = mesh_obj("deck", verts, faces, deck_m)
    sol = deck.modifiers.new("thick", "SOLIDIFY")
    sol.thickness = 0.6
    sol.offset = -1
    # hull sides: from the deck edge down to the sea, flaring out a little; and the bow face under the lip
    for side in (-1, 1):
        verts, faces = [], []
        for i, x in enumerate(xs):
            w = deck_width(x) / 2
            verts += [(x, side * w, zr(x) - 0.6), (x, side * (w - 1.8), -22.0)]
            if i:
                a = 2 * (i - 1)
                faces.append((a, a + 2, a + 3, a + 1) if side > 0 else (a, a + 1, a + 3, a + 2))
        mesh_obj(f"hull{side}", verts, faces, hull_m)
    w = deck_width(RAMP_L) / 2
    mesh_obj("bow", [(RAMP_L, -w, RAMP_H - 0.6), (RAMP_L, w, RAMP_H - 0.6), (RAMP_L - 6, w - 1.8, -22),
                     (RAMP_L - 6, -w + 1.8, -22)], [(0, 1, 2, 3)], hull_m)
    # deck-edge lip and safety-net frames along both sides
    rail_m = mat("rail", (0.2, 0.21, 0.22), 0.5, metal=0.6)
    for side in (-1, 1):
        for x in range(-250, int(RAMP_L), 3):
            yy = side * (deck_width(x) / 2 + 0.25)
            box(f"post{side}_{x}", (x, yy, zr(x) + 0.35), (0.06, 0.06, 0.7), rail_m)
        follow_strip(f"lip{side}", -255, RAMP_L, side * deck_width(0) / 2 - 0.0, side * deck_width(0) / 2, rail_m)
    # markings: the take-off line (yellow), the centre dashes (white), the deck-edge lines (white)
    white = mat("white", (0.78, 0.78, 0.74), 0.55)
    yellow = mat("yellow", (0.85, 0.62, 0.08), 0.5)
    red = mat("red", (0.55, 0.06, 0.04), 0.55)
    for k, x in enumerate(range(-240, -30, 9)):
        follow_strip(f"dash{k}", x, x + 4.5, -0.18, 0.18, white, lift=0.02)
    # two take-off positions, their lead lines curving in to the centre before the ramp
    lead_line("lead1", -200, -6.5, -25, RAMP_L - 0.5, yellow)
    lead_line("lead2", -120, 6.0, -15, -14, yellow, lift=0.045)   # not coplanar with lead1 (Cycles renders that black)
    for side in (-1, 1):
        edge_strip(f"edge{side}", -250, RAMP_L - 0.5, side, 0.9, 0.25, white)
    follow_strip("lipband", RAMP_L - 1.2, RAMP_L - 0.2, -8, 8, red)
    # the take-off restraint marks near the ramp foot (dark rectangles across the deck)
    for k in range(3):
        follow_strip(f"chock{k}", -44 + k * 0.9, -43.6 + k * 0.9, -1.6, 1.6, yellow)
    # the island on the starboard side
    isl_m = pbr("island", "painted_metal_shutter", 3.0, tint=(0.62, 0.64, 0.66), rough=(0.4, 0.75), nor=0.3, grime=0.25)
    glass_dark = mat("bridgeglass", (0.02, 0.03, 0.04), 0.05, metal=0.2)
    IX, IY = -62.0, 17.0
    box("island0", (IX, IY + 0.5, 9), (40, 8, 18), isl_m, bevel=0.15)
    box("island1", (IX + 2, IY, 21), (26, 7, 6), isl_m, bevel=0.15)
    box("bridge", (IX + 15.2, IY - 0.4, 22.4), (1.0, 6.6, 1.6), glass_dark)
    box("island2", (IX - 2, IY - 0.2, 27), (12, 5.5, 6), isl_m, bevel=0.1)
    cyl("mast", (IX - 2, IY - 0.2, 36), 0.6, 14, rail_m, verts=16)
    box("yard", (IX - 2, IY - 0.2, 39), (0.4, 7, 0.3), rail_m)
    for k in range(4):
        box(f"radar{k}", (IX - 6 + k * 5, IY - 3.6, 15 + (k % 2) * 6), (2.6, 0.3, 2.6), rail_m, bevel=0.05)
    # the sea: an ocean surface well below the deck, out to the horizon
    bpy.ops.mesh.primitive_plane_add(size=10)
    sea = bpy.context.object
    sea.location = (0, 0, -22)
    oc = sea.modifiers.new("ocean", "OCEAN")
    oc.geometry_mode = "GENERATE"
    oc.size = 1.0
    oc.spatial_size = 300
    oc.resolution = 14
    oc.repeat_x = oc.repeat_y = 12
    oc.wave_scale = 1.2
    oc.choppiness = 0.9
    oc.wind_velocity = 14
    oc.random_seed = 3
    sea.location = (-1800 + 300, -1800 + 0, -22)
    sea_m = mat("sea", (0.012, 0.035, 0.05), 0.08)
    _bsdf(sea_m).inputs["Specular IOR Level"].default_value = 0.6
    sea.data.materials.append(sea_m)
    return {"sea": sea, "ocean": oc}


def build_deckrun(a):
    sc, cam = setup(a, exposure=0.1)
    env = build_carrier(sc)
    cam.data.sensor_width = 36

    # the run: a take-off roll that accelerates; the eye 3.6 m above the deck (a pilot's seat), up the ramp, off the lip
    def pos(f):
        t = max(0.0, f) / 330.0
        return -70.0 + (RAMP_L + 70.0 + 40.0) * (0.55 * t + 0.45 * t * t)

    def frame(f):
        x = pos(f)
        if x <= RAMP_L:
            z = zr(x) + 3.6
            pitch = math.atan(slope(x))
        else:
            dx = x - RAMP_L
            pitch = math.atan(slope(RAMP_L - 0.01)) + 0.004 * dx
            z = RAMP_H + 3.6 + dx * math.tan(pitch)
        look = 0.03 + 0.10 * smooth((x - RAMP_L + 20) / 50)       # the eye lifts to the sky at the lip
        aim = (x + 30 * math.cos(pitch + look), 0.4, z + 30 * math.sin(pitch + look))
        aim_cam(cam, (x, -0.6, z), aim, 24)
        # a little seat shake that grows with speed
        cam.location.z += 0.03 * math.sin(f * 1.9) * min(1.0, f / 200)
        env["ocean"].time = f / FPS

    render(sc, a, frame, track_cam(cam) + [(env["ocean"], "time")])


# ---------------------------------------------------------------- a generic modern jet (no markings)
def modern_jet(name, loaded=True):
    body = pbr(f"{name}_skin", "metal_plate_02", 1.2, tint=(0.55, 0.58, 0.62), rough=(0.35, 0.6), nor=0.25, grime=0.15)
    dark = mat(f"{name}_dark", (0.03, 0.03, 0.035), 0.45, metal=0.7)
    can = mat(f"{name}_canopy", (0.04, 0.05, 0.06), 0.03, metal=0.6, coat=1.0)
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    parts = []
    # fuselage: nose at +x, tail at 0 (15 m long), centre line at z 0
    st = [(15.2, 0.02, 0.02, 0.1), (14.2, 0.35, 0.35, 0.05), (12.5, 0.6, 0.62, 0.05), (10.5, 0.75, 0.8, 0.15),
          (8.5, 1.1, 0.85, 0.1), (6.0, 1.45, 0.8, 0.0), (3.5, 1.45, 0.75, 0.0), (1.2, 1.25, 0.7, 0.0),
          (0.0, 1.15, 0.62, 0.0)]
    parts.append(loft(f"{name}_fus", st, body))
    parts.append(sphere(f"{name}_cnp", (10.9, 0, 0.75), 1.0, can, scale=(2.2, 0.48, 0.5)))
    # delta wing (y >= 0 planform), canards, fin
    dw = [(7.5, 0.9), (1.0, 5.4), (0.2, 5.4), (0.3, 0.9)]
    for s in (1, -1):
        parts.append(wing(f"{name}_wing{s}", dw, 0.16, body, z=-0.25, dihedral=-2, side=s))
        parts.append(wing(f"{name}_can{s}", [(10.2, 0.6), (8.9, 2.3), (8.4, 2.3), (8.6, 0.6)], 0.08, body, z=0.35, side=s))
    fin = slab(f"{name}_fin", [(4.5, 0), (0.6, 0), (-0.3, 0.0), (1.5, 0.0)], -0.07, 0.07, body)
    fin.data.vertices[0].co = (4.6, -0.07, 0.6)
    # the fin as an extruded profile in the xz plane
    bpy.data.objects.remove(fin, do_unlink=True)
    prof = [(4.8, 0.6), (0.4, 0.6), (-0.4, 3.9), (1.3, 3.9)]
    verts = [(x, -0.07, z) for x, z in prof] + [(x, 0.07, z) for x, z in prof]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    parts.append(finish(mesh_obj(f"{name}_fin", verts, faces, body), 0.05, None, 3))
    # two engines: nozzles with petals ring, the turbine face dark, the glow disc and the flame
    glow = mat(f"{name}_glow", (0.1, 0.05, 0.02), 0.4, emit=(1.0, 0.45, 0.12), strength=0.0)
    flame, flame_s = flame_mat(f"{name}_flame", (1.0, 0.42, 0.12), 0.0)
    flames = []
    for s in (1, -1):
        y = s * 0.55
        n = cyl(f"{name}_noz{s}", (-0.45, y, -0.05), 0.47, 1.0, dark, rot=(0, math.pi / 2, 0), verts=48)
        sol = n.modifiers.new("shell", "SOLIDIFY")
        sol.thickness = 0.05
        parts.append(n)
        parts.append(torus(f"{name}_lip{s}", (-0.95, y, -0.05), 0.47, 0.04, dark, rot=(0, math.pi / 2, 0)))
        parts.append(cyl(f"{name}_core{s}", (-0.3, y, -0.05), 0.42, 0.05, glow, rot=(0, math.pi / 2, 0), verts=48))
        bpy.ops.mesh.primitive_cone_add(radius1=0.4, radius2=0.04, depth=4.0, location=(-2.9, y, -0.05),
                                        rotation=(0, -math.pi / 2, 0), vertices=48)
        fl = bpy.context.object
        fl.name = f"{name}_flame{s}"
        fl.data.materials.append(flame)
        fl.visible_shadow = False
        for p in fl.data.polygons:
            p.use_smooth = True
        flames.append(fl)
        parts.append(fl)
    # landing gear (short legs and wheels) so it sits on the deck
    gear = mat(f"{name}_gear", (0.5, 0.5, 0.5), 0.4, metal=0.8)
    tyre = mat(f"{name}_tyre", (0.02, 0.02, 0.02), 0.8)
    for (x, y) in ((12.0, 0.0), (5.2, 1.7), (5.2, -1.7)):
        parts.append(cyl(f"{name}_leg{x}{y}", (x, y, -1.2), 0.07, 1.4, gear, verts=12))
        parts.append(cyl(f"{name}_wheel{x}{y}", (x, y, -1.95), 0.38, 0.28, tyre, rot=(math.pi / 2, 0, 0), verts=32))
    if loaded:
        store = mat(f"{name}_store", (0.55, 0.56, 0.55), 0.45, metal=0.3)
        for s in (1, -1):
            parts.append(sphere(f"{name}_tank{s}", (4.6, s * 2.6, -0.95), 0.42, store, scale=(5.2, 1, 1)))
            parts.append(box(f"{name}_pyl{s}", (4.6, s * 2.6, -0.5), (1.6, 0.08, 0.35), store))
            for k, yy in enumerate((3.9, 4.8)):
                parts.append(cyl(f"{name}_msl{s}{k}", (3.6, s * yy, -0.62), 0.11, 3.0, store, rot=(0, math.pi / 2, 0), verts=16))
        parts.append(sphere(f"{name}_ctank", (6.0, 0, -1.2), 0.5, store, scale=(5.0, 1, 1)))
    for p in parts:
        parent(p, root)
    return root, glow, flame_s, flames


def build_rampjet(a):
    sc, cam = setup(a, exposure=0.0)
    env = build_carrier(sc)
    jet, glow, flame_s, flames = modern_jet("jet", loaded=True)
    x0 = -46.0                      # the jet waits at the restraint line, nose to the ramp
    H_GEAR = 2.33                   # wheel bottom to fuselage centre

    def jx(f):
        t = max(0.0, (f - 255) / FPS)        # rolls at 255; about 0.5 g along the deck, then up the ramp
        return x0 + 0.5 * 9.0 * t * t + 2.0 * t

    def frame(f):
        x = jx(f)
        tail = x
        mid = x + 7.5
        if mid <= RAMP_L:
            pitch = math.atan(slope(mid))
            z = zr(mid) + H_GEAR
        else:
            dx = mid - RAMP_L
            pitch = math.atan(slope(RAMP_L - 0.01)) + 0.006 * dx
            z = RAMP_H + H_GEAR + dx * math.tan(pitch)
        jet.location = (mid - 7.5 * math.cos(pitch), 0, z - 7.5 * math.sin(pitch))
        jet.rotation_euler = (0, -pitch, 0)
        # engines: spool up from the start, afterburner at 240 ("with its own engines"), a flicker on the flame
        spool = smooth(f / 120)
        ab = smooth((f - 240) / 14)
        emit_socket(glow).default_value = 3.0 * spool + 30.0 * ab
        flame_s.default_value = (0.4 * spool + 9.0 * ab) * (1 + 0.08 * math.sin(f * 2.7))
        for fl in flames:
            fl.scale = (1, 1, 0.25 + 0.75 * ab + 0.04 * math.sin(f * 3.1))
        # camera: low behind and left of the jet, creeping in; it lets the jet go up the ramp, tilting to follow
        cx = keys(f, [(0, x0 - 24.0), (250, x0 - 19.0), (389, x0 - 14.0)])
        cz = 1.9 + 0.006 * max(0, f - 250)
        target = (max(x + 4.0, x0 + 4.0), 0.0, z - 0.3)
        aim_cam(cam, (cx, -5.2, cz), target, keys(f, [(0, 40.0), (389, 34.0)]), fstop=4.0)
        env["ocean"].time = f / FPS

    tracked = track_cam(cam) + track_obj(jet, props=("location", "rotation_euler")) + [(env["ocean"], "time")]
    tracked += [(emit_socket(glow), "default_value"), (flame_s, "default_value")]
    tracked += track_obj(*flames, props=("scale",))
    render(sc, a, frame, tracked)


# ================================================================ 1961: the steam catapult
def sea_hawk(name):
    """a 1950s straight-winged naval jet of the Sea Hawk's period (no markings): fuselage, wings, tailplane on fin"""
    body = pbr(f"{name}_skin", "metal_plate_02", 1.0, tint=(0.3, 0.33, 0.36), rough=(0.4, 0.7), nor=0.2, grime=0.2)
    can = mat(f"{name}_canopy", (0.05, 0.06, 0.07), 0.03, metal=0.5, coat=1.0)
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    st = [(12.2, 0.05, 0.05, 0.0), (11.4, 0.5, 0.55, 0.0), (9.5, 0.8, 0.85, 0.05), (7.0, 0.95, 0.95, 0.0),
          (4.0, 0.9, 0.85, 0.0), (1.5, 0.55, 0.6, 0.15), (0.0, 0.3, 0.35, 0.25)]
    parts = [loft(f"{name}_fus", st, body), sphere(f"{name}_cnp", (9.2, 0, 0.8), 1.0, can, scale=(1.6, 0.48, 0.52))]
    for s in (1, -1):
        parts.append(wing(f"{name}_w{s}", [(8.6, 0.8), (7.9, 6.0), (6.5, 6.0), (5.6, 0.8)], 0.2, body, z=-0.2, side=s))
        parts.append(wing(f"{name}_t{s}", [(1.8, 0.0), (1.4, 2.4), (0.6, 2.4), (0.3, 0.0)], 0.08, body, z=2.0, side=s))
    prof = [(2.6, 0.4), (0.4, 0.4), (0.2, 2.1), (1.6, 2.1)]
    verts = [(x, -0.06, z) for x, z in prof] + [(x, 0.06, z) for x, z in prof]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    parts.append(finish(mesh_obj(f"{name}_fin", verts, faces, body), 0.04, None, 3))
    for p in parts:
        parent(p, root)
    return root


def build_catapult(a):
    sc, cam = setup(a, exposure=-0.2)
    world_hdri(sc, "industrial_pipe_and_valve_01", 0.25, rot=1.2, bg_strength=0.0)
    LEN = 24.0
    floor = pbr("plate", "metal_plate", 1.2, tint=(0.35, 0.36, 0.38), rough=(0.35, 0.7), metal=1.0, nor=0.8, grime=0.4)
    bpy.ops.mesh.primitive_plane_add(size=120, location=(LEN / 2, 0, 0))
    bpy.context.object.data.materials.append(floor)
    deck_m = pbr("deck61", "concrete_floor_worn_001", 2.0, tint=(0.33, 0.34, 0.35), rough=(0.65, 0.95), nor=1.0, grime=0.3)
    beam_m = pbr("beam", "rusty_painted_metal", 1.5, tint=(0.8, 0.8, 0.8), rough=(0.4, 0.85), nor=0.6)
    cut_m = mat("cutface", (0.62, 0.12, 0.06), 0.55)          # the cutaway convention: cut faces in red
    steel = pbr("cylsteel", "metal_plate_02", 0.8, tint=(0.75, 0.77, 0.8), rough=(0.12, 0.3), metal=1.0, nor=0.15)
    brass = mat("brass", (0.78, 0.56, 0.26), 0.25, metal=1.0)
    dark = mat("darksteel", (0.05, 0.05, 0.055), 0.45, metal=0.8)
    # the deck section: a thick plate with the slot, cut on the near side, standing on frames and girders
    DZ = 3.2
    for side, (y0, y1) in (("L", (-4.5, -0.07)), ("R", (0.07, 5.5))):
        d = box(f"deck{side}", (LEN / 2, (y0 + y1) / 2, DZ), (LEN + 6, y1 - y0, 0.3), deck_m, bevel=0.01)
    box("deckcutL", (LEN / 2, -4.55, DZ), (LEN + 6, 0.1, 0.3), cut_m)
    for k in range(9):
        x = -2 + k * 3.6
        box(f"frame{k}", (x, 0.5, 1.6), (0.25, 9.6, 2.9), beam_m, bevel=0.02)
        box(f"frameflange{k}", (x, 0.5, 0.1), (0.6, 9.6, 0.15), beam_m, bevel=0.01)
    for y in (-3.6, 3.6):
        box(f"girder{y}", (LEN / 2, y, 2.9), (LEN + 6, 0.25, 0.4), beam_m, bevel=0.02)
    # twin cylinders under the slot (the slot's sealing strip on top), cut open on the near side
    tubes = []
    for k, y in enumerate((-0.32, 0.32)):
        t = cyl(f"tube{k}", (LEN / 2, y, 2.55), 0.27, LEN, steel, rot=(0, math.pi / 2, 0), verts=64)
        s = t.modifiers.new("shell", "SOLIDIFY")
        s.thickness = 0.035
        tubes.append(t)
    cc = cutter((LEN / 2, -0.32, 2.85), (LEN + 2, 0.7, 0.5))
    boolean(tubes[0], cc)
    cc2 = cutter((LEN / 2, 0.32, 2.85), (LEN + 2, 0.5, 0.36))
    boolean(tubes[1], cc2)
    for k in range(int(LEN / 1.2) + 1):
        x = k * 1.2
        for y in (-0.32, 0.32):
            box(f"clamp{k}{y}", (x, y, 2.55), (0.12, 0.66, 0.66), dark, bevel=0.01)
    # the steam inlet: the launch valve and a pipe from the boiler at the aft end
    pipe_m = pbr("pipe", "rusty_metal_02", 0.6, tint=(0.55, 0.5, 0.45), rough=(0.4, 0.8), metal=0.8, nor=0.6)
    cyl("inlet", (-1.2, 0, 2.55), 0.45, 1.6, pipe_m, rot=(0, math.pi / 2, 0), bevel=0.02)
    cyl("valve", (-1.2, 0, 3.0), 0.35, 0.5, brass, bevel=0.02)
    cyl("steampipe", (-1.2, -2.5, 1.6), 0.22, 5.0, pipe_m, rot=(math.pi / 2, 0, 0))
    # the water brake at the bow end
    cyl("brake", (LEN + 0.6, 0, 2.55), 0.5, 1.6, dark, rot=(0, math.pi / 2, 0), bevel=0.03)
    # pistons, the shuttle that rides in the slot, the bridle up to the jet
    pist_root = bpy.data.objects.new("pistons", None)
    bpy.context.collection.objects.link(pist_root)
    pist_root.location = (1.0, 0, 2.55)
    for k, y in enumerate((-0.32, 0.32)):
        p = cyl(f"piston{k}", (1.0, y, 2.55), 0.25, 1.3, brass, rot=(0, math.pi / 2, 0), verts=48, bevel=0.02)
        parent(p, pist_root)
        sp = cyl(f"spear{k}", (2.0, y, 2.55), 0.1, 0.9, steel, rot=(0, math.pi / 2, 0), verts=24)
        parent(sp, pist_root)
    sh = box("shuttle", (1.2, 0, 3.45), (1.3, 0.12, 0.35), brass, bevel=0.02)
    parent(sh, pist_root)
    hook = box("shuttlehook", (1.4, 0, 3.6), (0.3, 0.3, 0.2), dark, bevel=0.02)
    parent(hook, pist_root)
    # the steam behind each piston: an amber, softly glowing column that grows with the stroke
    steam_m, steam_s = flame_mat("steam", (1.0, 0.72, 0.42), 0.0)
    steams = []
    for k, y in enumerate((-0.32, 0.32)):
        s = cyl(f"steam{k}", (0.5, y, 2.55), 0.24, 1.0, steam_m, rot=(0, math.pi / 2, 0), verts=48)
        s.visible_shadow = False
        steams.append(s)
    steam_light = light("POINT", (0.5, -0.4, 2.7), None, 0.0, (1.0, 0.65, 0.35), size=0.3)
    jet = sea_hawk("jet")
    # the bridle: two cables from the shuttle hook to the jet's belly hooks
    br_m = mat("bridle", (0.12, 0.12, 0.12), 0.5, metal=0.6)
    bridles = []
    for s in (1, -1):
        b = cyl(f"bridle{s}", (0, 0, 0), 0.03, 1.0, br_m, verts=8)
        bridles.append((b, s))
    # light: a hard key down the length (a hangar lamp), cool fill, a warm rim from the far end; haze for the beams
    light("SPOT", (LEN / 2 - 6, -9, 12), (LEN / 2, 0, 2.5), 9000, (1.0, 0.86, 0.7), size=0.4, spot=55)
    light("AREA", (LEN / 2 + 6, 9, 7), (LEN / 2, 0, 2.5), 1200, (0.65, 0.78, 1.0), size=8)
    light("AREA", (LEN + 8, -2, 4), (LEN / 2, 0, 2.5), 1500, (1.0, 0.7, 0.45), size=4)
    haze((LEN / 2, 0, 5), (LEN + 30, 30, 12), 0.006)

    def frame(f):
        t = smooth((f - 150) / 180)
        x = 1.0 + (LEN - 3.0) * (t ** 1.6)
        pist_root.location.x = x
        for s, (yy) in zip(steams, (-0.32, 0.32)):
            L = max(0.05, x - 0.45)
            s.scale = (1, 1, L)
            s.location = (0.0 + L / 2 - 0.05, yy, 2.55)
        k = smooth((f - 130) / 25) * (1 - 0.6 * smooth((f - 360) / 120))
        steam_s.default_value = 6.0 * k
        steam_light.data.energy = 160 * k
        steam_light.location.x = max(0.5, x - 1.0)
        jx = x + 0.4
        jet.location = (jx - 5.0, 0, DZ + 0.15 + 2.1)
        for b, s in bridles:
            a0 = Vector((x + 0.6, 0, 3.65))
            a1 = Vector((jx + 0.4, s * 0.7, DZ + 0.15 + 1.5))
            mid = (a0 + a1) / 2
            b.location = mid
            b.rotation_euler = (a1 - a0).to_track_quat("Z", "Y").to_euler()
            b.scale = (1, 1, (a1 - a0).length)
        cx = keys(f, [(0, 0.5), (150, 2.5), (330, LEN - 6.0), (599, LEN - 4.0)])
        aim_cam(cam, (cx - 5.0, -8.8, 6.6), (cx + 1.6, 0, 2.7), 30, fstop=5.6)

    tracked = track_cam(cam) + track_obj(pist_root, jet, props=("location",)) + track_obj(*steams, props=("location", "scale"))
    tracked += track_obj(*[b for b, _ in bridles]) + [(steam_s, "default_value"), (steam_light.data, "energy"),
                                                      (steam_light, "location")]
    render(sc, a, frame, tracked)


# ================================================================ 1970: the boiler drum
def crack_curve(name, m, pts, r=0.006):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def build_drum(a):
    sc, cam = setup(a, exposure=-0.1)
    world_hdri(sc, "boiler_room", 0.35, rot=0.5, bg_strength=0.0)
    grate = pbr("grate", "metal_grate_rusty", 1.0, tint=(0.45, 0.42, 0.4), rough=(0.4, 0.9), metal=0.9, nor=1.0)
    bpy.ops.mesh.primitive_plane_add(size=40)
    bpy.context.object.data.materials.append(grate)
    iron = pbr("drumsteel", "rusty_metal_02", 1.4, tint=(0.32, 0.29, 0.27), rough=(0.35, 0.85), metal=0.9, nor=0.7, grime=0.4)
    dark = pbr("saddle", "rusty_painted_metal", 1.0, tint=(0.35, 0.33, 0.32), rough=(0.5, 0.9), nor=0.5)
    tube_m = pbr("tubes", "metal_plate_02", 0.5, tint=(0.35, 0.33, 0.3), rough=(0.3, 0.7), metal=1.0, nor=0.3, grime=0.5)
    R, LEN, ZC = 0.75, 4.0, 1.6
    cyl("drum", (0, 0, ZC), R, LEN, iron, rot=(0, math.pi / 2, 0), verts=128)
    for s in (-1, 1):
        sphere(f"end{s}", (s * LEN / 2, 0, ZC), R, iron, scale=(0.42, 1, 1), seg=64)
        cyl(f"manhole{s}", (s * (LEN / 2 + 0.28), 0, ZC), 0.24, 0.08, dark, rot=(0, math.pi / 2, 0), bevel=0.01)
        box(f"saddle{s}", (s * 1.35, 0, 0.5), (0.45, 1.5, 1.0), dark, bevel=0.03)
    # lap seams: a raised strap with two rows of rivets round the drum, and one long seam along the top
    rivet = mat("rivet", (0.09, 0.08, 0.075), 0.45, metal=1.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, segments=10, ring_count=6)
    proto = bpy.context.object
    proto.data.materials.append(rivet)
    for p in proto.data.polygons:
        p.use_smooth = True
    me = proto.data
    bpy.data.objects.remove(proto, do_unlink=True)
    n_r = 0
    for sx in (-1.0, 0.0, 1.0):
        bpy.ops.mesh.primitive_cylinder_add(radius=R + 0.012, depth=0.16, location=(sx, 0, ZC), rotation=(0, math.pi / 2, 0),
                                            vertices=128)
        bpy.context.object.data.materials.append(iron)
        for row in (-0.05, 0.05):
            for j in range(56):
                t = j / 56 * math.tau
                o = bpy.data.objects.new(f"rv{n_r}", me)
                o.location = (sx + row, (R + 0.016) * math.cos(t), ZC + (R + 0.016) * math.sin(t))
                bpy.context.collection.objects.link(o)
                n_r += 1
    # the generating tubes: rows of tubes leaving the top of the drum and rising, bending away, into the dark
    random.seed(7)
    for row in range(4):
        ang = math.radians(70 + row * 9)
        for k in range(34):
            x = -1.85 + k * 0.112 + (0.056 if row % 2 else 0)
            y0, z0 = R * math.cos(ang), ZC + R * math.sin(ang)
            cu = bpy.data.curves.new(f"tb{row}_{k}", "CURVE")
            cu.dimensions = "3D"
            cu.bevel_depth = 0.026
            cu.bevel_resolution = 3
            sp = cu.splines.new("BEZIER")
            sp.bezier_points.add(1)
            p0, p1 = sp.bezier_points
            p0.co = (x, y0, z0)
            p0.handle_left = (x, y0 - 0.1, z0 - 0.3)
            p0.handle_right = (x, y0 + 0.15, z0 + 0.6)
            top = (x, 1.6 + row * 0.25, 6.5 + random.uniform(-0.2, 0.2))
            p1.co = top
            p1.handle_left = (x, top[1] - 0.6, top[2] - 1.5)
            p1.handle_right = (x, top[1] + 0.3, top[2] + 0.8)
            o = bpy.data.objects.new(cu.name, cu)
            bpy.context.collection.objects.link(o)
            o.data.materials.append(tube_m)
    # the cracks: hairlines on the drum's front face, glowing hot one after another
    crack_m = [mat(f"crack{k}", (0.05, 0.02, 0.01), 0.5, emit=(1.0, 0.33, 0.07), strength=0.0) for k in range(7)]
    crack_l = []
    random.seed(4)
    for k in range(7):
        x = -1.5 + k * 0.48 + random.uniform(-0.1, 0.1)
        t = math.radians(random.uniform(-30, 25))
        pts, xx, tt = [], x, t
        for s in range(22):
            tt += 0.022 + random.uniform(-0.012, 0.012)
            xx += random.uniform(-0.016, 0.016)
            pts.append((xx, -(R + 0.003) * math.cos(tt), ZC + (R + 0.003) * math.sin(tt)))
        crack_curve(f"crack{k}", crack_m[k], pts, r=0.0045)
        mid = pts[len(pts) // 2]
        crack_l.append(light("POINT", (mid[0], mid[1] - 0.12, mid[2]), None, 0.0, (1.0, 0.4, 0.12), size=0.05))
    # the bands: heavy straps with a bolted clamp; each comes down and ratchets tight
    band_m = pbr("band", "metal_plate_02", 0.5, tint=(0.75, 0.76, 0.78), rough=(0.2, 0.45), metal=1.0, nor=0.2)
    bands = []
    for k, bx in enumerate((-1.1, 0.0, 1.1)):
        b = cyl(f"band{k}", (bx, 0, ZC), R + 0.04, 0.17, band_m, rot=(0, math.pi / 2, 0), verts=128, bevel=0.006)
        inner = cyl(f"bandhole{k}", (bx, 0, ZC), R + 0.006, 0.4, band_m, rot=(0, math.pi / 2, 0), verts=128)
        inner.hide_render = True
        inner.display_type = "WIRE"
        boolean(b, inner)
        parent(inner, b)
        c = box(f"clamp{k}", (bx, 0, ZC + R + 0.1), (0.26, 0.24, 0.12), dark, bevel=0.01)
        parent(c, b)
        for dy in (-0.07, 0.07):
            parent(cyl(f"bolt{k}{dy}", (bx, dy, ZC + R + 0.19), 0.025, 0.12, band_m, verts=12), b)
        bands.append(b)
    # light: a caged work lamp above (warm, hard), a cool fill from an open hatch, haze
    light("SPOT", (-1.6, -2.4, 4.6), (0, 0, ZC), 2600, (1.0, 0.78, 0.5), size=0.15, spot=60)
    light("AREA", (3.5, -3.5, 2.2), (0, 0, ZC), 260, (0.6, 0.72, 1.0), size=3)
    light("AREA", (0, 4, 3), (0, 0, ZC), 300, (1.0, 0.65, 0.4), size=5)
    haze((0, 0, 3), (14, 12, 8), 0.02)
    starts = (420, 560, 700)

    def frame(f):
        for k in range(7):
            e = smooth((f - 60 - 34 * k) / 20) * (1 - 0.7 * smooth((f - starts[0] + 40) / 60))
            flick = 1 + 0.12 * math.sin(f * 0.7 + k)
            emit_socket(crack_m[k]).default_value = 14.0 * e * flick
            crack_l[k].data.energy = 6.0 * e * flick
        for k, b in enumerate(bands):
            s0 = starts[k]
            drop = 1 - smooth((f - s0) / 60)
            tight = sum(smooth((f - s0 - 60 - 18 * c) / 6) for c in range(3)) / 3
            sc_ = 1.22 - 0.22 * tight
            b.location.z = ZC + 2.8 * drop
            b.scale = (1, sc_, sc_)
        x = keys(f, [(0, -1.9), (400, -0.7), (959, 0.4)])
        aim_cam(cam, (x, -4.3, 2.25), (x * 0.5, 0, ZC - 0.05), 40, fstop=4.0)

    tracked = track_cam(cam) + track_obj(*bands, props=("location", "scale"))
    tracked += [(emit_socket(m), "default_value") for m in crack_m] + [(l.data, "energy") for l in crack_l]
    render(sc, a, frame, tracked)


# ================================================================ 1970: the one gauge in the boiler room
def build_room(a):
    sc, cam = setup(a, exposure=0.1)
    world_hdri(sc, "boiler_room", 0.3, rot=2.0, bg_strength=0.0)
    wall = pbr("wall", "rusty_painted_metal", 2.0, tint=(0.55, 0.52, 0.48), rough=(0.5, 0.9), nor=0.6, grime=0.4)
    floor = pbr("floor", "metal_grate_rusty", 1.0, tint=(0.4, 0.38, 0.36), rough=(0.4, 0.9), metal=0.9, nor=1.0)
    face_m = pbr("boilerface", "green_metal_rust", 1.6, tint=(0.55, 0.6, 0.55), rough=(0.45, 0.85), nor=0.6, grime=0.35)
    pipe = pbr("pipe", "rusty_metal_02", 0.8, tint=(0.5, 0.46, 0.42), rough=(0.35, 0.8), metal=0.85, nor=0.5)
    lag = mat("lagging", (0.55, 0.52, 0.46), 0.95)        # pipe lagging (cloth wrap)
    brass = mat("gbrass", (0.8, 0.6, 0.3), 0.22, metal=1.0)
    face = mat("gface", (0.88, 0.86, 0.8), 0.4)
    redm = mat("gred", (0.75, 0.05, 0.03), 0.45)
    blk = mat("gblack", (0.015, 0.015, 0.015), 0.35)
    bpy.ops.mesh.primitive_plane_add(size=1)
    fl = bpy.context.object
    fl.scale = (16, 12, 1)
    fl.data.materials.append(floor)
    box("back", (0, 5.6, 3.5), (16, 0.2, 7), wall)
    box("left", (-8, 0, 3.5), (0.2, 12, 7), wall)
    box("right", (8, 0, 3.5), (0.2, 12, 7), wall)
    box("ceiling", (0, 0, 7), (16, 12, 0.2), wall)
    # the boiler's front: riveted plates, a furnace door, the gauge on its own pipe
    box("boiler", (0, 4.0, 2.7), (6.4, 2.6, 5.4), face_m, bevel=0.04)
    for k in range(3):
        box(f"door{k}", (-1.8 + k * 1.8, 2.66, 1.2), (1.1, 0.12, 0.9), pipe, bevel=0.03)
        cyl(f"latch{k}", (-1.4 + k * 1.8, 2.58, 1.2), 0.06, 0.1, brass, rot=(math.pi / 2, 0, 0))
    for zz in (0.3, 2.2, 4.1, 5.3):
        for j in range(30):
            sphere(f"r{zz}{j}", (-3.1 + j * 0.214, 2.68, zz), 0.03, blk, seg=8)
    # pipes: overhead runs with flanges, lagged risers, a valve wheel
    for k in range(5):
        y = -4 + k * 1.9
        cyl(f"run{k}", (0, y, 6.3 - 0.18 * k), 0.15 + 0.02 * (k % 2), 16, pipe if k % 2 else lag, rot=(0, math.pi / 2, 0), verts=24)
        for j in range(5):
            cyl(f"fl{k}{j}", (-6 + j * 3, y, 6.3 - 0.18 * k), 0.24, 0.08, pipe, rot=(0, math.pi / 2, 0), verts=24)
    cyl("riser", (-2.6, 2.6, 3.4), 0.2, 7, lag, verts=24)
    cyl("riser2", (2.9, 2.6, 3.4), 0.14, 7, pipe, verts=24)
    torus("wheel", (2.9, 2.4, 2.3), 0.32, 0.03, brass, rot=(math.pi / 2, 0, 0), seg=48)
    # the gauge: a 30 cm Bourdon gauge, brass bezel, glass, white dial, red sector, needle; on a pigtail siphon
    gx, gy, gz = 0.9, 2.2, 2.6
    G = 0.3
    cyl("stem", (gx, gy + 0.25, gz - 0.55), 0.03, 0.8, brass, verts=16)
    torus("pigtail", (gx, gy + 0.25, gz - 0.32), 0.07, 0.022, brass, rot=(0, math.pi / 2, 0), seg=24)
    cyl("case", (gx, gy + 0.08, gz), G + 0.03, 0.12, pipe, rot=(math.pi / 2, 0, 0), bevel=0.01)
    torus("bezel", (gx, gy, gz), G + 0.015, 0.03, brass, rot=(math.pi / 2, 0, 0))
    cyl("dial", (gx, gy + 0.02, gz), G, 0.01, face, rot=(math.pi / 2, 0, 0))
    gl = sphere("glass", (gx, gy - 0.005, gz), G, glass(), scale=(1, 0.08, 1))
    gl.visible_shadow = False
    for k in range(41):
        t = math.radians(225 - k * 6.75)
        big = k % 5 == 0
        L = 0.05 if big else 0.025
        box(f"tick{k}", (gx + (G - 0.03 - L / 2) * math.cos(t), gy + 0.012, gz + (G - 0.03 - L / 2) * math.sin(t)),
            (L, 0.002, 0.008 if big else 0.004), blk, rot=(0, -t, 0))
    for k in range(18):
        t = math.radians(-14 - k * 2.3)
        box(f"red{k}", (gx + (G - 0.07) * math.cos(t), gy + 0.013, gz + (G - 0.07) * math.sin(t)), (0.05, 0.002, 0.02), redm,
            rot=(0, -t, 0))
    hub = bpy.data.objects.new("hub", None)
    bpy.context.collection.objects.link(hub)
    hub.location = (gx, gy + 0.004, gz)
    nd = box("needle", (gx + 0.11, gy + 0.004, gz), (0.25, 0.004, 0.014), blk)
    parent(nd, hub)
    parent(box("tailw", (gx - 0.04, gy + 0.004, gz), (0.07, 0.004, 0.03), blk), hub)
    cyl("cap", (gx, gy, gz), 0.02, 0.012, brass, rot=(math.pi / 2, 0, 0))
    # light: one bulb in a cage over the gauge, a cold shaft through a hatch, haze
    bulb = light("POINT", (0.5, 1.4, 4.8), None, 900, (1.0, 0.7, 0.4), size=0.06)
    sphere("bulbglass", (0.5, 1.4, 4.8), 0.07, mat("bulbm", (1, 0.8, 0.5), 0.2, emit=(1, 0.72, 0.42), strength=40))
    light("SPOT", (-5, -2, 6.8), (-2.5, 2, 0), 5000, (0.62, 0.74, 1.0), size=0.3, spot=22)
    gl_fill = light("AREA", (2.5, -1.0, 2.6), (gx, gy, gz), 40, (1.0, 0.85, 0.65), size=0.8)
    gl_fill.visible_glossy = False         # it showed as a white square on the gauge glass
    haze((0, 0, 3.5), (16, 12, 7), 0.03)

    def frame(f):
        ang = keys(f, [(0, 150.0), (150, 140.0), (260, -32.0), (599, -34.0)])
        ang += 1.4 * math.sin(f * 0.9) * smooth((f - 200) / 40) * (1 - smooth((f - 330) / 60))
        hub.rotation_euler = (0, -math.radians(ang), 0)
        loc = keys(f, [(0, (gx + 0.05, gy - 0.95, gz + 0.02)), (300, (gx, gy - 1.1, gz)), (599, (-3.4, -4.6, 2.9))])
        aim = keys(f, [(0, (gx, gy, gz)), (300, (gx, gy, gz)), (599, (0.5, 3.0, 2.3))])
        aim_cam(cam, loc, aim, keys(f, [(0, 55.0), (300, 50.0), (599, 24.0)]), fstop=keys(f, [(0, 2.0), (300, 2.8), (599, 8.0)]))

    tracked = track_cam(cam) + track_obj(hub, props=("rotation_euler",)) + [(cam.data.dof, "aperture_fstop")]
    render(sc, a, frame, tracked)


# ================================================================ today: the energy store (motor generators)
def motor_generator(name, loc, cut, mats):
    shell_m, dark, copper, glow, cut_m = mats
    x0, y0, z0 = loc
    box(f"{name}_skid", (x0, y0, z0 + 0.15), (4.8, 2.5, 0.3), dark, bevel=0.03)
    for dx in (-1.6, 1.6):
        box(f"{name}_saddle{dx}", (x0 + dx, y0, z0 + 0.55), (0.4, 2.0, 0.65), dark, bevel=0.03)
    h = cyl(f"{name}_housing", (x0, y0, z0 + 1.45), 1.15, 3.9, shell_m, rot=(0, math.pi / 2, 0), verts=128, bevel=0.02)
    s = h.modifiers.new("shell", "SOLIDIFY")
    s.thickness = 0.07
    h.modifiers.move(len(h.modifiers) - 1, 0)
    for k in range(9):           # cooling ribs round the housing
        torus(f"{name}_rib{k}", (x0 - 1.6 + k * 0.4, y0, z0 + 1.45), 1.17, 0.025, shell_m, rot=(0, math.pi / 2, 0))
    for sx in (-1, 1):
        cyl(f"{name}_endcap{sx}", (x0 + sx * 2.0, y0, z0 + 1.45), 1.0, 0.18, dark, rot=(0, math.pi / 2, 0), bevel=0.03)
    parts_cut = [h]
    if cut:
        c = cutter((x0 + 0.2, y0 - 0.95, z0 + 2.35), (3.5, 1.9, 1.95))
        boolean(h, c)
        # the red faces of the cut: a thin ring sector drawn where the housing was cut
        for k in range(10):
            w = torus(f"{name}_wind{k}", (x0 - 1.45 + k * 0.32, y0, z0 + 1.45), 0.97, 0.07, copper, rot=(0, math.pi / 2, 0))
            boolean(w, c)
        for k in range(9):
            boolean(torus(f"{name}_rib{k}c", (x0 - 1.6 + k * 0.4, y0, z0 + 1.45), 1.17, 0.03, cut_m, rot=(0, math.pi / 2, 0)), c,
                    "INTERSECT")
    cyl(f"{name}_shaft", (x0, y0, z0 + 1.45), 0.13, 4.8, dark, rot=(0, math.pi / 2, 0), verts=32)
    pivot = bpy.data.objects.new(f"{name}_pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = (x0, y0, z0 + 1.45)
    for k in range(6):
        d = cyl(f"{name}_disc{k}", (x0 - 1.25 + k * 0.5, y0, z0 + 1.45), 0.82, 0.34, shell_m, rot=(0, math.pi / 2, 0), verts=96,
                bevel=0.02)
        parent(d, pivot)
        parent(torus(f"{name}_ring{k}", (x0 - 1.25 + k * 0.5, y0, z0 + 1.45), 0.84, 0.05, copper, rot=(0, math.pi / 2, 0)), pivot)
        for j in range(24):
            t = j / 24 * math.tau
            mg = box(f"{name}_mag{k}_{j}", (x0 - 1.25 + k * 0.5, y0 + 0.79 * math.cos(t), z0 + 1.45 + 0.79 * math.sin(t)),
                     (0.3, 0.1, 0.07), glow if j % 6 == 0 else dark, rot=(t, 0, 0))
            parent(mg, pivot)
    return pivot


def build_store(a):
    sc, cam = setup(a, exposure=-0.1)
    world_hdri(sc, "machine_shop_02", 0.2, rot=1.0, bg_strength=0.0)
    floor = pbr("plate", "metal_plate", 1.2, tint=(0.32, 0.33, 0.35), rough=(0.3, 0.7), metal=1.0, nor=0.8, grime=0.4)
    bpy.ops.mesh.primitive_plane_add(size=80)
    bpy.context.object.data.materials.append(floor)
    shell_m = pbr("hsteel", "painted_metal_shutter", 1.0, tint=(0.62, 0.65, 0.68), rough=(0.25, 0.55), metal=0.3, nor=0.25)
    dark = pbr("dark", "metal_plate_02", 0.8, tint=(0.08, 0.08, 0.09), rough=(0.3, 0.6), metal=0.9, nor=0.3)
    copper = mat("copper", (0.75, 0.38, 0.17), 0.25, metal=1.0, emit=(1.0, 0.45, 0.12), strength=0.0)
    glow = mat("magglow", (0.8, 0.5, 0.2), 0.3, metal=0.5, emit=(1.0, 0.6, 0.2), strength=0.0)
    cut_m = mat("cutface", (0.62, 0.12, 0.06), 0.55)
    mats = (shell_m, dark, copper, glow, cut_m)
    hero = motor_generator("mg0", (0, 0, 0), True, mats)
    others = [motor_generator(f"mg{k}", (-1.0 + 6.2 * k, 7.6, 0), False, mats) for k in (1, 2)]
    bus_m = mat("bus", (0.06, 0.06, 0.07), 0.45, emit=(1.0, 0.7, 0.25), strength=0.0)
    cyl("bus", (5.0, 0, 0.28), 0.17, 10, bus_m, rot=(0, math.pi / 2, 0), verts=24)
    cyl("bus2", (5.0, 0.5, 0.28), 0.17, 10, dark, rot=(0, math.pi / 2, 0), verts=24)
    glow_l = light("POINT", (0.2, -0.6, 1.5), None, 0.0, (1.0, 0.55, 0.2), size=0.6)
    light("SPOT", (-5, -7, 8), (0, 0, 1.4), 7000, (1.0, 0.86, 0.68), size=0.3, spot=45)
    light("AREA", (6, -5, 3), (0, 0, 1.4), 700, (0.65, 0.78, 1.0), size=4)
    light("AREA", (0, 13, 6), (0, 0, 1.4), 1400, (1.0, 0.75, 0.5), size=10)
    haze((2, 3, 4), (26, 24, 9), 0.01)

    def speed(f):
        up = smooth(f / 420)
        out = 0.55 * smooth((f - 600) / 180)
        back = 0.55 * smooth((f - 820) / 140)
        return 1.6 * up * (1 - out + back)

    cache = {}

    def angle(f):
        if f in cache:
            return cache[f]
        s = 0.0
        for k in range(0, max(0, int(f))):
            s += speed(k) / FPS
        cache[f] = s * math.tau
        return cache[f]

    def frame(f):
        hero.rotation_euler = (angle(f), 0, 0)
        for o in others:
            o.rotation_euler = (angle(f) * 0.97 + 1.0, 0, 0)
        e = speed(f) / 1.6
        emit_socket(copper).default_value = 3.0 * e
        emit_socket(glow).default_value = 9.0 * e
        glow_l.data.energy = 120 * e
        pulse = smooth((f - 600) / 30) * (1 - smooth((f - 700) / 80))
        emit_socket(bus_m).default_value = 16 * pulse
        x = keys(f, [(0, -6.0), (959, -3.2)])
        aim_cam(cam, (x, -6.4 + 0.0012 * f, 2.9 - 0.0006 * f), (0.3, 0, 1.45), 35, fstop=3.2)

    tracked = track_cam(cam) + track_obj(hero, *others, props=("rotation_euler",))
    tracked += [(emit_socket(copper), "default_value"), (emit_socket(glow), "default_value"),
                (emit_socket(bus_m), "default_value"), (glow_l.data, "energy")]
    render(sc, a, frame, tracked)


SHOTS = {"deckrun": build_deckrun, "rampjet": build_rampjet, "catapult": build_catapult, "drum": build_drum,
         "room": build_room, "store": build_store}


def main():
    a = args()
    if a.shot not in SHOTS:
        sys.exit(f"unknown shot {a.shot}")
    SHOTS[a.shot](a)


if __name__ == "__main__":
    main()
