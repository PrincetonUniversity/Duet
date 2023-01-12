# get the path to the current dir
set DV_ROOT $::env(DV_ROOT)
set APP $::env(APP)
set generic_script_root [file dirname [file normalize [info script]]]

# bring yosys commands into tcl
yosys -import 

# read techmap libraries
read_verilog -lib [file join $generic_script_root adder.lib.v]
read_verilog -lib [file join $generic_script_root dual_port_ram.lib.v]
read_verilog -lib [file join $generic_script_root multiply.lib.v]

# read verilog sources
verilog_defaults -add -I${DV_ROOT}/design/chip/tile/prga/fabric/m2/include
verilog_defaults -add -I${DV_ROOT}/design/chip/tile/prga/app/${APP}/include
read_verilog -defer ${DV_ROOT}/design/chip/tile/prga/fabric/m2/rtl/prga_fifo_resizer.v
read_verilog -defer ${DV_ROOT}/design/chip/tile/prga/fabric/m2/rtl/prga_fifo_lookahead_buffer.v
read_verilog -defer ${DV_ROOT}/design/chip/tile/prga/fabric/m2/rtl/prga_fifo.v
read_verilog -defer -DPRGA_POSTPNR_NO_MEMINIT ${DV_ROOT}/design/chip/tile/prga/fabric/m2/rtl/prga_ram_1r1w.v
read_verilog -defer ${DV_ROOT}/design/chip/tile/prga/fabric/m2/rtl/prga_valrdy_buf.v

foreach f [glob -directory ${DV_ROOT}/design/chip/tile/prga/app/${APP}/rtl -- *.v] {
    read_verilog $f
}

# pre-process
hierarchy -check -top ${APP}

# synthesis
synth -flatten -noalumacc -run coarse

stat -width
async2sync

# print coarse synthesis report
stat -width

# memory map
memory_bram -rules [file join $generic_script_root bram.rule]
techmap -map [file join $generic_script_root memory.techmap.v]
stat -width

# map remaining memory operations to dff
opt -full
memory_map

# print memory map report
stat -width

# techmap onto library cells read with `read_verilog` above
techmap -map [file join $generic_script_root multiply.techmap.v]
techmap -map [file join $generic_script_root adder.techmap.v]
stat -width

# print techmap report
opt -full
stat -width

# LUT map
#   to LUT4 only, because adder cannot connect to LUT5/LUT6
techmap     ;# generic techmap onto basic logic elements
abc9 -luts 4:4
opt -full

# print LUT4 map report
stat -width

# now remap to LUT5/LUT6
#   the idea is to gather all LUT4s driving `adder` inputs, wrap them into a
#   submodule, set dont_touch to that submodule, remap the remaining logic to
#   LUT5/LUT6, then unwrap the submodule
splitnets -format _
select { */t:adder %x:+[a,b] */t:adder %d %a %c %x:+$lut %D }
submod -name saved_luts
select -clear
wbflip saved_luts
stat -width

#   remap
lut2mux
abc9 -luts 4:4,5:5,6:6
opt -full
stat -width

#   revert marker LUT4s
wbflip saved_luts
flatten
opt -full

# print final report
stat -width

# final check
check -noinit

# output
write_blif -conn -param ${APP}.eblif
