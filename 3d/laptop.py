# Рендер первого экрана портфолио: ноутбук открывается, камера влетает в экран.
# Запуск: blender -b -P laptop.py -- [preview]
import bpy, math, sys, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "video", "hero")
PREVIEW = "preview" in sys.argv
FRAMES = 150

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, FRAMES
sc.render.fps = 30

def srgb(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def mat(name, color, metal=0.0, rough=0.4, emit=None, strength=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m

def box(name, size, loc, material, bevel=0.03, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = o.modifiers.new("bevel", "BEVEL")
        mod.width, mod.segments = bevel, 4
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent:
        o.parent = parent
    return o

alu = mat("alu", (0.11, 0.115, 0.13), metal=0.85, rough=0.32)
dark = mat("keys", (0.012, 0.013, 0.016), rough=0.55)
pad = mat("pad", (0.07, 0.075, 0.085), metal=0.6, rough=0.25)
bezel = mat("bezel", (0.005, 0.005, 0.007), rough=0.2)
logo = mat("logo", (0, 0, 0), emit=(srgb(124), srgb(240), srgb(180)), strength=4)

# Корпус: перед смотрит в -Y, петля сзади (y = +1.1)
BW, BD, BH = 3.2, 2.2, 0.12
box("base", (BW, BD, BH), (0, 0, BH / 2), alu, 0.04)
# Клавиатура: массив клавиш
bpy.ops.mesh.primitive_cube_add(location=(-1.27, 0.75, BH + 0.004))
k = bpy.context.object
k.scale = (0.095, 0.095, 0.01)
bpy.ops.object.transform_apply(scale=True)
k.data.materials.append(dark)
a1 = k.modifiers.new("ax", "ARRAY"); a1.count = 13; a1.relative_offset_displace = (1.21, 0, 0)
a2 = k.modifiers.new("ay", "ARRAY"); a2.count = 5; a2.relative_offset_displace = (0, -1.21, 0)
box("trackpad", (1.1, 0.68, 0.006), (0, -0.62, BH + 0.001), pad, 0.01)

# Крышка с осью вращения на петле
bpy.ops.object.empty_add(location=(0, BD / 2 - 0.02, BH))
hinge = bpy.context.object
hinge.name = "hinge"
LW, LL, LT = 3.18, 2.12, 0.05
box("lid", (LW, LL, LT), (0, -LL / 2, LT / 2 + 0.004), alu, 0.03, hinge)
box("bezel", (LW - 0.06, LL - 0.06, 0.004), (0, -LL / 2, 0.003), bezel, 0.01, hinge)
# Логотип на крышке
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=0.14, fill_type="NGON", location=(0, -LL / 2, LT + 0.006))
lg = bpy.context.object
lg.data.materials.append(logo)
lg.parent = hinge

# Экран: плоскость на внутренней стороне крышки, нормаль вниз (-Z)
SW, SH = 2.96, 1.85
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -LL / 2 - 0.02, -0.0015), rotation=(math.pi, 0, 0))
scr = bpy.context.object
scr.name = "screen"
scr.scale = (SW, SH, 1)
bpy.ops.object.transform_apply(scale=True)
scr.parent = hinge
sm = bpy.data.materials.new("screen")
sm.use_nodes = True
nt = sm.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(os.path.join(HERE, "screen.png"))
em = nt.nodes.new("ShaderNodeEmission")
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(tex.outputs["Color"], em.inputs["Color"])
nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
scr.data.materials.append(sm)

# Анимация крышки: закрыта -> открыта на 100 градусов
OPEN = -math.radians(100)
hinge.rotation_euler = (0, 0, 0); hinge.keyframe_insert("rotation_euler", frame=8)
hinge.rotation_euler = (OPEN, 0, 0); hinge.keyframe_insert("rotation_euler", frame=70)
# Яркость экрана разгорается при открытии
em.inputs["Strength"].default_value = 0.0; em.inputs["Strength"].keyframe_insert("default_value", frame=25)
em.inputs["Strength"].default_value = 1.0; em.inputs["Strength"].keyframe_insert("default_value", frame=75)

# Центр и нормаль экрана в открытом положении
hinge.rotation_euler = (OPEN, 0, 0)
bpy.context.view_layer.update()
poly = scr.data.polygons[0]
center = scr.matrix_world @ poly.center
normal = (scr.matrix_world.to_3x3() @ poly.normal).normalized()
print("CENTER", tuple(center), "NORMAL", tuple(normal))

# Камера смотрит на цель, цель плавно переезжает с корпуса на центр экрана
bpy.ops.object.empty_add(location=(0, 0, 0.5))
tgt = bpy.context.object
tgt.keyframe_insert("location", frame=1)
tgt.location = center
tgt.keyframe_insert("location", frame=105)

bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 50
con = cam.constraints.new("TRACK_TO")
con.target = tgt
con.track_axis, con.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
END_D = 3.35
keys = [
    (1, Vector((6.2, -6.8, 4.6))),
    (60, Vector((3.0, -7.4, 3.0))),
    (105, center + normal * 6.5),
    (FRAMES, center + normal * END_D),
]
for f, p in keys:
    cam.location = p
    cam.keyframe_insert("location", frame=f)
for o in (hinge, tgt, cam):
    if o.animation_data and o.animation_data.action:
        try:
            for fc in o.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"; kp.easing = "AUTO"
        except AttributeError:
            pass

# Свет: холодный контровой и мятный, мягкий верхний
def light(name, loc, energy, color, size):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.color, d.size = energy, color, size
    o = bpy.data.objects.new(name, d)
    sc.collection.objects.link(o)
    o.location = loc
    c = o.constraints.new("TRACK_TO"); c.target = tgt
    c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
light("key", (4, -4, 6), 220, (1, 1, 1), 5)
light("rimBlue", (-5, 4, 3), 1400, (0.42, 0.62, 1.0), 3)
light("rimMint", (5, 4, 2), 900, (0.45, 0.95, 0.7), 3)

# Пол и фон в цвет сайта
bg = tuple(srgb(c) for c in (13, 15, 20))
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
bpy.context.object.data.materials.append(mat("floor", bg, rough=0.55))
w = bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
bgn = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bgn.inputs["Color"].default_value = (*bg, 1)

# Рендер
try:
    sc.render.engine = "BLENDER_EEVEE"
except TypeError as e:
    print(e); sc.render.engine = "BLENDER_EEVEE_NEXT"
try:
    sc.eevee.taa_render_samples = 96 if not PREVIEW else 8
    sc.eevee.use_raytracing = True
except AttributeError:
    pass
sc.view_settings.view_transform = "Standard"
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 95
os.makedirs(OUT, exist_ok=True)
if PREVIEW:
    for f in (1, 40, 70, 105, 130, FRAMES):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(HERE, f"prev_{f:03d}.jpg")
        bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(OUT, "f")
    bpy.ops.render.render(animation=True)
print("DONE")
