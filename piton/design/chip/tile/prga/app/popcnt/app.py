from prga import *
from prga.app import *
from prga.netlist import ModuleUtils, NetUtils, Const

import os, sys, logging

ctx = Context.unpickle(sys.argv[1])
ctx = AppContext.construct_from_arch_context(ctx)

yami = ctx.get_intf("yami_piton")

builder = ctx.build_kernel( "ppc",
        "rtl/ppc.v",
        do_generate_verilog = False, )

# port groups
builder.create_portgroup( "syscon", slave = True )

# other ports
builder.create_port("start_rdy",                1,  "output")
builder.create_port("start_vld",                1,  "input")
builder.create_port("len",                      32, "input")

builder.create_port("done_full",                1,  "input")
builder.create_port("done_wr",                  1,  "output")
builder.create_port("count",                    64, "output")

builder.create_port("irdy",                     1,  "output")
builder.create_port("ivld",                     1,  "input")
builder.create_port("idat",                     64, "input")

mk = builder.module

# create softregs interface
softregs = ctx.initialize_softregspace()
softregs.create_softreg("basic",        "addr",     width = 40) # will be promoted to hsr_plain
softregs.create_softreg("vldrdy_wr",    "len",      width = 32) # will be promoted to hsr_ififo_valrdy
softregs.create_softreg("hsr_ofifo",    "count",    width = 64)
softregs.log_summary()
ms = softregs.create_module(ctx)

# create top
mt = ctx.create_top( "popcnt" )

# instantiate stuff
ik  = ModuleUtils.instantiate( mt, mk,              "i_kernel" )
is_ = ModuleUtils.instantiate( mt, ms,              "i_softregs" )
im  = ModuleUtils.instantiate( mt, ctx.get_or_create_pipeldshim_yami(yami, 3), "i_ldshim" )

# connect groups
ctx.connect_portgroup( "syscon", mt, ik,  master_id = "app" )
ctx.connect_portgroup( "syscon", mt, is_, master_id = "app" )
ctx.connect_portgroup( "syscon", mt, im,  master_id = "app" )

ctx.connect_portgroup_buf( "rxi",    mt, is_ )
ctx.connect_portgroup_buf( "yami",   im, mt, slave_id = "i0" )

# connect soft registers
NetUtils.connect( is_.pins["var_addr_o"],       im.pins["cfg_addr"] )
NetUtils.connect( is_.pins["var_len_o"],        im.pins["cfg_len"] )
NetUtils.connect( is_.pins["var_len_o"],        ik.pins["len"] )
NetUtils.connect( is_.pins["var_len_vld"],      im.pins["cfg_start"] )
NetUtils.connect( is_.pins["var_len_vld"],      ik.pins["start_vld"] )
NetUtils.connect( ik.pins["start_rdy"],         is_.pins["var_len_rdy"] )

NetUtils.connect( im.pins["kvld"],              ik.pins["ivld"] )
NetUtils.connect( im.pins["kdata"],             ik.pins["idat"] )
NetUtils.connect( ik.pins["irdy"],              im.pins["krdy"] )

NetUtils.connect( ik.pins["done_wr"],           is_.pins["var_count_wr"] )
NetUtils.connect( ik.pins["count"],             is_.pins["var_count_i"] )
NetUtils.connect( is_.pins["var_count_full"],   ik.pins["done_full"] )

# generate verilog files
ctx.generate_verilog( "rtl", "include" )
