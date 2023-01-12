from prga import *
from prga.netlist import Module, ModuleUtils, NetUtils, PortDirection

from itertools import product, chain
import os, sys

N = 8                       # No. of Grady'18 per CLB
CFG_WIDTH, PHIT_WIDTH = 1, 8
SA_WIDTH, SA_HEIGHT = 8, 8
SA_XCNT, SA_YCNT = 4, 8
NUM_IOB_PER_TILE = 16
MUL_WIDTH = 40
MM_COL = 2                  # memory/multiplier column

FBRC_WIDTH, FBRC_HEIGHT = SA_XCNT * SA_WIDTH + 2, SA_YCNT * SA_HEIGHT + 2

import logging
logger = logging.getLogger("prga")
logger.setLevel(logging.DEBUG)

try:
    ctx = Context.unpickle("ctx.tmp.pkl")

except FileNotFoundError:
    ctx = Context()

    # ============================================================================
    # -- Routing Resources -------------------------------------------------------
    # ============================================================================
    glb_clk = ctx.create_global("clk", is_clock = True)
    glb_clk.bind( (SA_XCNT * SA_WIDTH + 1, (SA_YCNT // 2) * SA_HEIGHT + 1), 0)
    l1 = ctx.create_segment('L1', 20, 1)
    l4 = ctx.create_segment('L4', 20, 4)

    # ============================================================================
    # -- Primitives --------------------------------------------------------------
    # ============================================================================

    # multi-mode memory: 512x32b, 1K16b, and 2K8b
    memory = ctx.create_multimode_memory(9, 32, addr_width = 11)

    # ============================================================================
    # -- Blocks ------------------------------------------------------------------
    # ============================================================================

    # -- IOB ---------------------------------------------------------------------
    builder = ctx.build_io_block("prga_iob")
    o = builder.create_input("outpad", 1)
    i = builder.create_output("inpad", 1)
    builder.connect(builder.instances['io'].pins['inpad'], i)
    builder.connect(o, builder.instances['io'].pins['outpad'])
    iob = builder.commit()

    # -- CLB ---------------------------------------------------------------------
    prim = ctx.primitives["grady18"]
    builder = ctx.build_logic_block("prga_clb")
    clk = builder.create_global(glb_clk, Orientation.south)
    ce = builder.create_input("ce", 1, Orientation.west)
    in_ = builder.create_input("in", (N // 2) * len(prim.ports["in"]), Orientation.west)
    out = builder.create_output("out", N * len(prim.ports["out"]), Orientation.west)
    cin = builder.create_input("cin", 1, Orientation.south)
    xbar_i, xbar_o = list(in_), []
    for i, inst in enumerate(builder.instantiate(prim, "i_slice", N)):
        builder.connect(clk, inst.pins['clk'])
        builder.connect(ce, inst.pins['ce'])
        builder.connect(inst.pins['out'], out[i * (l := len(prim.ports["out"])):(i + 1) * l])
        builder.connect(cin, inst.pins["cin"], vpr_pack_patterns = ["carrychain"])
        xbar_i.extend(inst.pins["out"])
        xbar_o.extend(inst.pins["in"])
        cin = inst.pins["cout"]
    builder.connect(cin, builder.create_output("cout", 1, Orientation.north), vpr_pack_patterns = ["carrychain"])
    # crossbar: 50% connectivity
    for (i, ipin), (o, opin) in product(enumerate(xbar_i), enumerate(xbar_o)):
        if i % 2 == o % 2:
            builder.connect(ipin, opin)
    clb = builder.commit()

    ctx.create_tunnel("carrychain", clb.ports["cout"], clb.ports["cin"], (0, -1))

    # -- BRAM --------------------------------------------------------------------
    builder = ctx.build_logic_block("prga_bram", 1, 2)
    inst = builder.instantiate(memory, "i_ram")
    builder.connect(
            builder.create_global(glb_clk, Orientation.south),
            inst.pins["clk"])
    builder.connect(
            builder.create_input("we", len(inst.pins["we"]), Orientation.west, (0, 0)),
            inst.pins["we"])
    for y in range(2):
        for p in ["raddr", "waddr", "din"]:
            bits = [b for i, b in enumerate(inst.pins[p]) if i % 2 == y]
            builder.connect(
                    builder.create_input("{}x{}".format(p, y), len(bits), Orientation.west, (0, y)),
                    bits)
        bits = [b for i, b in enumerate(inst.pins["dout"]) if i % 2 == y]
        builder.connect(bits,
                builder.create_output("doutx{}".format(y), len(bits), Orientation.west, (0, y)))

    bram = builder.commit()

    # -- Multiplier --------------------------------------------------------------
    builder = ctx.build_logic_block("prga_bmul", 1, 2)
    clk = builder.create_global(glb_clk, Orientation.south)
    ce = builder.create_input("ce", 1, Orientation.west, (0, 0))
    inst = builder.instantiate(ctx.create_multiplier(MUL_WIDTH, name="prga_prim_mul"), "i_mul")
    ffs = builder.instantiate(ctx.primitives["dffe"], "i_x_f", len(inst.pins["x"]))
    for y in range(2):
        for p in ["a", "b"]:
            bits = [b for i, b in enumerate(inst.pins[p]) if i % 2 == y]
            builder.connect(
                    builder.create_input("{}x{}".format(p, y), len(bits), Orientation.west, (0, y)),
                    bits)
        xbits, fbits = [], []
        for i, b in enumerate(inst.pins["x"]):
            if i % 2 == y:
                xbits.append(b)
                fbits.append(ffs[i].pins["Q"])
                builder.connect(clk, ffs[i].pins["C"])
                builder.connect(ce, ffs[i].pins["E"])
                builder.connect(b, ffs[i].pins["D"], vpr_pack_patterns = ["mul_x2f"])
        builder.connect(xbits,
                o := builder.create_output("x{}".format(y), len(xbits), Orientation.west, (0, y)))
        builder.connect(fbits, o)

    bmul = builder.commit()

    # ============================================================================
    # -- Tiles -------------------------------------------------------------------
    # ============================================================================
    iotile = ctx.build_tile(iob, NUM_IOB_PER_TILE,
            name = "prga_t_iob",
            edge = OrientationTuple(False, east = True),
            ).fill( (.5, .5) ).auto_connect().commit()
    clbtile = ctx.build_tile(clb,
            name = "prga_t_clb",
            ).fill( (0.15, 0.2) ).auto_connect().commit()
    bramtile = ctx.build_tile(bram,
            name = "prga_t_bram",
            ).fill( (0.15, 0.2) ).auto_connect().commit()
    bmultile = ctx.build_tile(bmul,
            name = "prga_t_bmul",
            ).fill( (0.15, 0.2) ).auto_connect().commit()

    # ============================================================================
    # -- Subarrays ---------------------------------------------------------------
    # ============================================================================
    pattern = SwitchBoxPattern.cycle_free(fill_corners = [Corner.northwest, Corner.southwest])

    # -- Single-Tile Arrays ------------------------------------------------------
    builder = ctx.build_array("prga_a_iob", 1, 1, set_as_top = False,
            edge = OrientationTuple(False, east = True))
    builder.instantiate(iotile, (0, 0))
    iosta = builder.fill( pattern ).auto_connect().commit()

    builder = ctx.build_array("prga_a_clb", 1, 1, set_as_top = False)
    builder.instantiate(clbtile, (0, 0))
    clbsta = builder.fill( pattern ).auto_connect().commit()

    builder = ctx.build_array("prga_a_bram", 1, 2, set_as_top = False)
    builder.instantiate(bramtile, (0, 0))
    bramsta = builder.fill( pattern ).auto_connect().commit()

    builder = ctx.build_array("prga_a_bmul", 1, 2, set_as_top = False)
    builder.instantiate(bmultile, (0, 0))
    bmulsta = builder.fill( pattern ).auto_connect().commit()

    # -- Subarray Type A (Left Mega Column) --------------------------------------
    builder = ctx.build_array("prga_region_left", SA_WIDTH, SA_HEIGHT, set_as_top = False)
    for x, y in product(range(builder.width), range(builder.height)):
        if x == SA_WIDTH - 1 and y == 0:
            # reserved for router
            pass
        elif x == MM_COL:               # column 2
            if y % bramsta.height == 0:
                builder.instantiate(bramsta, (x, y))
        elif x == SA_WIDTH - MM_COL:    # column 6
            if y % bmulsta.height == 0:
                builder.instantiate(bmulsta, (x, y))
        else:
            builder.instantiate(clbsta, (x, y))
    left = builder.fill( pattern ).auto_connect().commit()

    # -- Subarray Type B (Right Mega Column) -------------------------------------
    builder = ctx.build_array("prga_region_right", SA_WIDTH + 1, SA_HEIGHT,
            set_as_top = False, edge = OrientationTuple(False, east = True))
    for x, y in product(range(builder.width), range(builder.height)):
        if x == SA_WIDTH - 1 and y == 0:
            # reserved for router
            pass
        elif x == MM_COL:
            if y % bramsta.height == 0:
                builder.instantiate(bramsta, (x, y))
        elif x == SA_WIDTH:
            builder.instantiate(iosta, (x, y))
        else:
            builder.instantiate(clbsta, (x, y))
    right = builder.fill( pattern ).auto_connect().commit()

    # ============================================================================
    # -- Fabric ------------------------------------------------------------------
    # ============================================================================
    builder = ctx.build_array("prga_fabric", FBRC_WIDTH, FBRC_HEIGHT, set_as_top = True)
    for y in range(SA_YCNT):
        for x in range(SA_XCNT - 1):
            builder.instantiate(left, (1 + x * SA_WIDTH, 1 + y * SA_HEIGHT))
        builder.instantiate(right, (1 + (SA_XCNT - 1) * SA_WIDTH, 1 + y * SA_HEIGHT))
    fabric = builder.auto_connect().commit()

    # ============================================================================
    # -- Abstract Flow -----------------------------------------------------------
    # ============================================================================
    Flow(
        VPRArchGeneration("vpr/arch.xml"),
        VPR_RRG_Generation("vpr/rrg.xml"),
        YosysScriptsCollection("syn"),
        ).run(ctx)

    # ============================================================================
    # -- Pickle Context ----------------------------------------------------------
    # ============================================================================

    ctx.pickle("ctx.tmp.pkl")

# ============================================================================
# -- Design views ------------------------------------------------------------
# ============================================================================

Flow(Materialization('pktchain',
    phit_width = PHIT_WIDTH,
    chain_width = CFG_WIDTH,
    router_fifo_depth_log2 = 7,  # 128x8b (32 frames) router FIFO
    )).run(ctx)

# ============================================================================
# -- Configuration Chain Injection -------------------------------------------
# ============================================================================
def iter_instances(module):
    if module.name == "prga_t_clb":
        yield module.instances[0]
        yield module.instances[Orientation.west, 0]
    elif module.name == "prga_t_iob":
        for i in range(NUM_IOB_PER_TILE):
            yield module.instances[i]
        yield module.instances[Orientation.west, 0]
    elif module.name == "prga_t_bram":
        yield module.instances[0]
        yield module.instances[Orientation.west, 1]
        yield module.instances[Orientation.west, 0]
    elif module.name == "prga_t_bmul":
        yield module.instances[0]
        yield module.instances[Orientation.west, 1]
        yield module.instances[Orientation.west, 0]
    elif module.name.startswith( "prga_a_" ):
        for y in range(module.height):
            yield module.instances[(0, y), Corner.southwest]
            if y == 0: yield module.instances[0, y]
            yield module.instances[(0, y), Corner.northwest]
    elif module.name.startswith( "prga_region_" ):
        # for y in range(module.height):
        #     for x in reversed(range(module.width - 1)):
        #         if i := module.instances.get( (x, y) ): yield i
        #         if i := module.instances.get( ((x, y), Corner.southwest) ): yield i
        #     for x in range(module.width - 1):
        #         if i := module.instances.get( ((x, y), Corner.northwest) ): yield i
        # for y in reversed(range(module.height)):
        #     if i := module.instances.get( ((module.width - 1, y), Corner.northwest) ): yield i
        #     if i := module.instances.get(  (module.width - 1, y) ): yield i
        #     if i := module.instances.get( ((module.width - 1, y), Corner.southwest) ): yield i
        for y in range(module.height):
            if y % 2 == 0:
                for x in reversed(range(module.width - 1)):
                    if x == SA_WIDTH - 1 and y == 0:
                        yield module.instances[(x, y), Corner.southwest]
                        yield module.instances[(x, y), Corner.northwest]
                    if i := module.instances.get( (x, y) ): yield i
            else:
                for x in range(module.width - 1):
                    if i := module.instances.get( (x, y) ): yield i
        for y in reversed(range(module.height)):
            if module.width == SA_WIDTH and y == 0:
                yield module.instances[     (module.width - 1, y), Corner.southwest]
                yield module.instances[     (module.width - 1, y), Corner.northwest]
            if i := module.instances.get(   (module.width - 1, y) ): yield i
        yield Pktchain.TERMINATE_LEAF
    elif module.name == "prga_fabric":
        for x in reversed(range(SA_XCNT // 2)):
            # upper half
            # going up
            for y in range(SA_YCNT // 2, SA_YCNT):
                yield module.instances[1 + (2 * x + 1) * SA_WIDTH, 1 + y * SA_HEIGHT]
            # going down
            for y in reversed(range(SA_YCNT // 2, SA_YCNT)):
                yield module.instances[1 + (2 * x + 0) * SA_WIDTH, 1 + y * SA_HEIGHT]
            # wrap up branch chain
            yield Pktchain.TERMINATE_BRANCH
            # lower half
            # going down
            for y in reversed(range(SA_YCNT // 2)):
                yield module.instances[1 + (2 * x + 1) * SA_WIDTH, 1 + y * SA_HEIGHT]
            # going down
            for y in range(SA_YCNT // 2):
                yield module.instances[1 + (2 * x + 0) * SA_WIDTH, 1 + y * SA_HEIGHT]
            # wrap up branch chain
            yield Pktchain.TERMINATE_BRANCH
    else:
        for i in module.instances.values():
            yield i

Flow(
        Translation(),
        SwitchPathAnnotation(),
        ProgCircuitryInsertion(iter_instances = iter_instances),
        ).run(ctx)

# ============================================================================
# -- Build System ------------------------------------------------------------
# ============================================================================
Flow(
        Pktchain.BuildSystemRXIYAMI("constraints/io.pads",
            fabric_wrapper = "prga_fabric_wrap",
            prog_be_in_wrapper = True,
            piton = True,
            num_yami = 2,
            use_fake_clkgen = True,
            ),
    ).run(ctx)

v = VerilogCollection("rtl", "include")
v._process_module(ctx, ctx.database[ModuleView.design, "prga_yami_tri_transducer"])
v._process_module(ctx, ctx.database[ModuleView.design, "prga_axi4lite_sri_transducer"])
v._process_module(ctx, ctx.database[ModuleView.design, "prga_sri_demux"])

Flow( v ).run(ctx)

# generate Flists
with open("include/Flist.include", "w") as f:
    f.write("+incdir+.")

with open("rtl/Flist.ctrl", "w") as f:
    stack = [ ctx.system_top ]
    visited = set([ctx.system_top.key,
        ctx.database[ModuleView.design, "prga_fabric_wrap"].key])
    f.write("prga_yami_tri_transducer.v\n")
    f.write("prga_axi4lite_sri_transducer.v\n")
    f.write("prga_sri_demux.v\n")
    while stack:
        m = stack.pop()
        for i in m.instances.values():
            if i.model.key in visited:
                continue
            visited.add(i.model.key)
            f.write(i.model.name + ".v\n")
            stack.append( i.model )

with open("rtl/Flist.fabric", "w") as f:
    stack = [ ctx.database[ModuleView.design, "prga_fabric_wrap"] ]
    visited = set()
    f.write("prga_fabric_wrap.v\n")
    while stack:
        m = stack.pop()
        for i in m.instances.values():
            if i.model.key in visited:
                continue
            visited.add(i.model.key)
            f.write(i.model.name + ".v\n")
            stack.append( i.model )

ctx.pickle("ctx.pkl")
