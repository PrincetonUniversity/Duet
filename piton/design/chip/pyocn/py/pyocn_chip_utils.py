'''
==========================================================================
pyocn_chip_utils.py
==========================================================================
Helper functions for the chip module.

Author : Yanghui Ou
  Date : Mar 15, 2020
'''
from __future__ import print_function

#-------------------------------------------------------------------------
# print_tile_noc_wires
#-------------------------------------------------------------------------
# Instantiate wires between tiles and the network.

def print_tile_noc_wires( x_tiles, y_tiles ):
  ntiles = x_tiles * y_tiles
  print( '// pyocn_config - print_tile_noc_wires( {}, {} )'.format( x_tiles, y_tiles ) )

  # Wires connecting to the pyocn

  for i in range(1, 4):
    print( 'wire [`DATA_WIDTH-1:0] noc{}_tile_vr_dat [0:{}];'.format( i, ntiles-1 ) )
    print( 'wire                   noc{}_tile_vr_val [0:{}];'.format( i, ntiles-1 ) )
    print( 'wire                   noc{}_tile_vr_rdy [0:{}];'.format( i, ntiles-1 ) )

    print( 'wire [`DATA_WIDTH-1:0] noc{}_offchip_vr_dat;'.format( i ) )
    print( 'wire                   noc{}_offchip_vr_val;'.format( i ) )
    print( 'wire                   noc{}_offchip_vr_rdy;'.format( i ) )

  # Wires connecting tiles and pyocn

  for i in range(1, 4):
    print( 'wire [`DATA_WIDTH-1:0] tile_noc{}_vr_dat [0:{}];'.format( i, ntiles-1 ) )
    print( 'wire                   tile_noc{}_vr_val [0:{}];'.format( i, ntiles-1 ) )
    print( 'wire                   tile_noc{}_vr_rdy [0:{}];'.format( i, ntiles-1 ) )

  # Offchip wires

  for i in range(1, 4):
    print( 'wire [`DATA_WIDTH-1:0] offchip_noc{}_vr_dat;'.format( i ) )
    print( 'wire                   offchip_noc{}_vr_val;'.format( i ) )
    print( 'wire                   offchip_noc{}_vr_rdy;'.format( i ) )

#-------------------------------------------------------------------------
# str_proc_oram
#-------------------------------------------------------------------------
# The assign statements that connect the chip to the oram. Line 530.
# TODO: revisit this, might not be correct...

def str_proc_oram():
  return '''
  // pyocn_config - str_proc_oram

  assign chip_intf_noc2_data  = noc2_offchip_vr_dat;
  assign chip_intf_noc2_valid = noc2_offchip_vr_val;
  assign noc2_offchip_vr_rdy  = chip_intf_noc2_rdy;

'''

#-------------------------------------------------------------------------
# str_processor_offchip_noc1
#-------------------------------------------------------------------------
# The assign statements that connect the chip to the offchip. Line 551.
# TODO: revisit this, might not be correct...

def str_processor_offchip_noc1():
  return '''
  // pyocn_config - str_processor_offchip_noc1

  assign chip_intf_noc1_data  = noc1_offchip_vr_dat;
  assign chip_intf_noc1_valid = noc1_offchip_vr_val;
  assign noc1_offchip_vr_rdy  = chip_intf_noc1_rdy;
'''

#-------------------------------------------------------------------------
# str_processor_offchip_noc3
#-------------------------------------------------------------------------
# The assign statements that connect the chip to the offchip. Line 551.
# TODO: revisit this, might not be correct...

def str_processor_offchip_noc3():
  return '''
  // pyocn_config - str_processor_offchip_noc3

  assign chip_intf_noc3_data  = noc3_offchip_vr_dat;
  assign chip_intf_noc3_valid = noc3_offchip_vr_val;
  assign noc3_offchip_vr_rdy  = chip_intf_noc3_rdy;
'''

#-------------------------------------------------------------------------
# str_offchip_out
#-------------------------------------------------------------------------
# The assign statements that connect the oram to the offchip. Line 569.
# TODO: revisit this, might not be correct...

def str_offchip_out():
  return '''
  // pyocn_config - str_offchip_out

  assign offchip_noc1_vr_dat = intf_chip_noc1_data;
  assign offchip_noc1_vr_val = intf_chip_noc1_valid;
  assign intf_chip_noc1_rdy  = offchip_noc1_vr_rdy;

  assign offchip_noc2_vr_dat = intf_chip_noc2_data;
  assign offchip_noc2_vr_val = intf_chip_noc2_valid;
  assign intf_chip_noc2_rdy  = offchip_noc2_vr_rdy;

  assign offchip_noc3_vr_dat = intf_chip_noc3_data;
  assign offchip_noc3_vr_val = intf_chip_noc3_valid;
  assign intf_chip_noc3_rdy  = offchip_noc3_vr_rdy;
'''

#-------------------------------------------------------------------------
# print_pyocn_instances
#-------------------------------------------------------------------------
# Instantiate the pyocn modules.

def print_pyocn_instances():
  tmpl = '''\
  // pyocn_config - print_pyocn_instances - pyocn_noc{i}

  pyocn_mesh_valrdy pyocn_noc{i}(
    .clk            ( clk_muxed         ),
    .reset          ( ~rst_n_inter_sync ),
    .in_dat         ( tile_noc{i}_vr_dat    ),
    .in_val         ( tile_noc{i}_vr_val    ),
    .in_rdy         ( tile_noc{i}_vr_rdy    ),
    .offchip_in_dat ( offchip_noc{i}_vr_dat ),
    .offchip_in_val ( offchip_noc{i}_vr_val ),
    .offchip_in_rdy ( offchip_noc{i}_vr_rdy ),
    .out_dat        ( noc{i}_tile_vr_dat    ),
    .out_val        ( noc{i}_tile_vr_val    ),
    .out_rdy        ( noc{i}_tile_vr_rdy    ),
    .offchip_out_dat( noc{i}_offchip_vr_dat ),
    .offchip_out_val( noc{i}_offchip_vr_val ),
    .offchip_out_rdy( noc{i}_offchip_vr_rdy )
  );

'''
  for i in range(1, 4):
    print( tmpl.format( i=i ) )

#-------------------------------------------------------------------------
# str_tile_template
#-------------------------------------------------------------------------
# Instantiate the tile modules.

def str_tile_template( y, x, x_tiles, tile_type ):
  tmpl = '''\
  // pyocn_config - str_tile_template( {y}, {x} )

  tile #(
    .TILE_TYPE( {tile_type} )
  ) tile{fid} (
    .clk              ( clk_muxed        ),
    .rst_n            ( rst_n_inter_sync ),
    .clk_en           ( ctap_clk_en_inter[{fid}] && clk_en_inter ),
    .default_chipid   ( 14'd0  ), // the first chip
    .default_coreid_x ( 8'd{x} ),
    .default_coreid_y ( 8'd{y} ),
    .flat_tileid      ( `JTAG_FLATID_WIDTH'd{fid} ),

`ifdef PITON_ARIANE
    .debug_req_i         ( debug_req_i[{fid}]   ),
    .unavailable_o       ( unavailable_o[{fid}] ),
    .timer_irq_i         ( timer_irq_i[{fid}]   ),
    .ipi_i               ( ipi_i[{fid}]         ),
    .irq_i               ( irq_i[{fid}*2 +: 2]  ),
`endif

    // ucb from tiles to jtag
    .tile_jtag_ucb_val   ( tile0_jtag_ucb_val  ),
    .tile_jtag_ucb_data  ( tile0_jtag_ucb_data ),
    // ucb from jtag to tiles
    .jtag_tiles_ucb_val  ( jtag_tiles_ucb_val  ),
    .jtag_tiles_ucb_data ( jtag_tiles_ucb_data ),

    .dyn0_in_dat       ( noc1_tile_vr_dat[{fid}] ),
    .dyn0_in_val       ( noc1_tile_vr_val[{fid}] ),
    .dyn0_in_rdy       ( noc1_tile_vr_rdy[{fid}] ),
    .dyn0_out_dat      ( tile_noc1_vr_dat[{fid}] ),
    .dyn0_out_val      ( tile_noc1_vr_val[{fid}] ),
    .dyn0_out_rdy      ( tile_noc1_vr_rdy[{fid}] ),

    .dyn1_in_dat       ( noc2_tile_vr_dat[{fid}] ),
    .dyn1_in_val       ( noc2_tile_vr_val[{fid}] ),
    .dyn1_in_rdy       ( noc2_tile_vr_rdy[{fid}] ),
    .dyn1_out_dat      ( tile_noc2_vr_dat[{fid}] ),
    .dyn1_out_val      ( tile_noc2_vr_val[{fid}] ),
    .dyn1_out_rdy      ( tile_noc2_vr_rdy[{fid}] ),

    .dyn2_in_dat       ( noc3_tile_vr_dat[{fid}] ),
    .dyn2_in_val       ( noc3_tile_vr_val[{fid}] ),
    .dyn2_in_rdy       ( noc3_tile_vr_rdy[{fid}] ),
    .dyn2_out_dat      ( tile_noc3_vr_dat[{fid}] ),
    .dyn2_out_val      ( tile_noc3_vr_val[{fid}] ),
    .dyn2_out_rdy      ( tile_noc3_vr_rdy[{fid}] )
  );

'''

  flat_id   = x + y*x_tiles
  return tmpl.format( x=x, y=y, fid=flat_id, tile_type=tile_type )

#-------------------------------------------------------------------------
# print_router_tile_wiring
#-------------------------------------------------------------------------
# Generate tile wiring for the router config.
#
# Coordinate system:
# 0 ------------------> x
#  | (0, 0)  (1, 0)
#  | (0, 1)  (1, 1)
#  | ...
#  |
#  | (0, 6)  (1, 6)
#  v
# y

def print_router_tile_wiring( x_tiles, y_tiles ):

  print( '  // pyocn_chip_utils.print_router_tile_wiring\n' )

  for x in range( x_tiles ):
    for y in range( y_tiles ):
      for idx in range( 3 ):

        # Wire N -> S
        if y >= 1:
          print( f'''
  wire [`DATA_WIDTH-1:0] tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_dat;
  wire                   tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_val;
  wire                   tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_rdy;
''' )

        # Wire S -> N
        if y < y_tiles - 1:
          print( f'''
  wire [`DATA_WIDTH-1:0] tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_dat;
  wire                   tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_val;
  wire                   tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_rdy;
''' )

        # Wire E -> W
        if x < x_tiles - 1:
          print( f'''
  wire [`DATA_WIDTH-1:0] tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_dat;
  wire                   tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_val;
  wire                   tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_rdy;
''' )

        # Wire W -> E
        if x >= 1:
          print( f'''
  wire [`DATA_WIDTH-1:0] tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_dat;
  wire                   tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_val;
  wire                   tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_rdy;
''' )

#-------------------------------------------------------------------------
# str_router_tile_template
#-------------------------------------------------------------------------
# Instantiate the tile modules for the router configuration.

def str_router_tile_template( y, x, y_tiles, x_tiles, tile_type ):
  flat_id  = x + y*x_tiles

  tmpl     = f'''\
  // pyocn_config - str_router_tile_template( {y}, {x} )
'''
  for idx in range(3):

    # North

    # Offchip - idx+1 because those wires are 1 based indexing
    if x == 0 and y == 0:
      north_in = f'''
    .dyn{idx}_in_N_dat( intf_chip_noc{idx+1}_data  ),
    .dyn{idx}_in_N_val( intf_chip_noc{idx+1}_valid ),
    .dyn{idx}_in_N_rdy( intf_chip_noc{idx+1}_rdy   ),'''

      north_out = f'''
    .dyn{idx}_out_N_dat( chip_intf_noc{idx+1}_data  ),
    .dyn{idx}_out_N_val( chip_intf_noc{idx+1}_valid ),
    .dyn{idx}_out_N_rdy( chip_intf_noc{idx+1}_rdy   ),'''

    elif y >= 1:
      north_in = f'''
    .dyn{idx}_in_N_dat( tile_{y-1}_{x}_S_tile_{y}_{x}_N_dyn{idx}_dat ),
    .dyn{idx}_in_N_val( tile_{y-1}_{x}_S_tile_{y}_{x}_N_dyn{idx}_val ),
    .dyn{idx}_in_N_rdy( tile_{y-1}_{x}_S_tile_{y}_{x}_N_dyn{idx}_rdy ),'''

      north_out = f'''
    .dyn{idx}_out_N_dat( tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_dat ),
    .dyn{idx}_out_N_val( tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_val ),
    .dyn{idx}_out_N_rdy( tile_{y}_{x}_N_tile_{y-1}_{x}_S_dyn{idx}_rdy ),'''

    else:
      north_in = f'''
    .dyn{idx}_in_N_dat( `DATA_WIDTH'b0 ),
    .dyn{idx}_in_N_val( 1'b0           ),
    .dyn{idx}_in_N_rdy(                ),'''

      north_out = f'''
    .dyn{idx}_out_N_dat(      ),
    .dyn{idx}_out_N_val(      ),
    .dyn{idx}_out_N_rdy( 1'b0 ),'''

    # South

    if y < y_tiles-1:
      south_in = f'''
    .dyn{idx}_in_S_dat( tile_{y+1}_{x}_N_tile_{y}_{x}_S_dyn{idx}_dat ),
    .dyn{idx}_in_S_val( tile_{y+1}_{x}_N_tile_{y}_{x}_S_dyn{idx}_val ),
    .dyn{idx}_in_S_rdy( tile_{y+1}_{x}_N_tile_{y}_{x}_S_dyn{idx}_rdy ),'''

      south_out = f'''
    .dyn{idx}_out_S_dat( tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_dat ),
    .dyn{idx}_out_S_val( tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_val ),
    .dyn{idx}_out_S_rdy( tile_{y}_{x}_S_tile_{y+1}_{x}_N_dyn{idx}_rdy ),'''

    else:
      south_in = f'''
    .dyn{idx}_in_S_dat( `DATA_WIDTH'b0 ),
    .dyn{idx}_in_S_val( 1'b0           ),
    .dyn{idx}_in_S_rdy(                ),'''

      south_out = f'''
    .dyn{idx}_out_S_dat(      ),
    .dyn{idx}_out_S_val(      ),
    .dyn{idx}_out_S_rdy( 1'b0 ),'''

    # West

    if x >= 1:
      west_in = f'''
    .dyn{idx}_in_W_dat( tile_{y}_{x-1}_E_tile_{y}_{x}_W_dyn{idx}_dat ),
    .dyn{idx}_in_W_val( tile_{y}_{x-1}_E_tile_{y}_{x}_W_dyn{idx}_val ),
    .dyn{idx}_in_W_rdy( tile_{y}_{x-1}_E_tile_{y}_{x}_W_dyn{idx}_rdy ),'''

      west_out = f'''
    .dyn{idx}_out_W_dat( tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_dat ),
    .dyn{idx}_out_W_val( tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_val ),
    .dyn{idx}_out_W_rdy( tile_{y}_{x}_W_tile_{y}_{x-1}_E_dyn{idx}_rdy ),'''

    else:
      west_in = f'''
    .dyn{idx}_in_W_dat( `DATA_WIDTH'b0 ),
    .dyn{idx}_in_W_val( 1'b0           ),
    .dyn{idx}_in_W_rdy(                ),'''

      west_out = f'''
    .dyn{idx}_out_W_dat(      ),
    .dyn{idx}_out_W_val(      ),
    .dyn{idx}_out_W_rdy( 1'b0 ),'''

    # East

    if x < x_tiles - 1:
      east_in = f'''
    .dyn{idx}_in_E_dat( tile_{y}_{x+1}_W_tile_{y}_{x}_E_dyn{idx}_dat ),
    .dyn{idx}_in_E_val( tile_{y}_{x+1}_W_tile_{y}_{x}_E_dyn{idx}_val ),
    .dyn{idx}_in_E_rdy( tile_{y}_{x+1}_W_tile_{y}_{x}_E_dyn{idx}_rdy ),'''

      east_out = f'''
    .dyn{idx}_out_E_dat( tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_dat ),
    .dyn{idx}_out_E_val( tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_val ),
    .dyn{idx}_out_E_rdy( tile_{y}_{x}_E_tile_{y}_{x+1}_W_dyn{idx}_rdy )'''

    else:
      east_in = f'''
    .dyn{idx}_in_E_dat( `DATA_WIDTH'b0 ),
    .dyn{idx}_in_E_val( 1'b0           ),
    .dyn{idx}_in_E_rdy(                ),'''

      east_out = f'''
    .dyn{idx}_out_E_dat(      ),
    .dyn{idx}_out_E_val(      ),
    .dyn{idx}_out_E_rdy( 1'b0 )'''

    tmpl += north_in
    tmpl += south_in
    tmpl += west_in
    tmpl += east_in
    tmpl += north_out
    tmpl += south_out
    tmpl += west_out
    tmpl += east_out

    if idx != 2:
      tmpl += ','

  tmpl += '\n'
  return tmpl

if __name__ == '__main__':
  for y in range( 2 ):
    for x in range( 2 ):
      print( str_router_tile_template( y, x, 2, 2, '`SPARC_TILE' ) )
