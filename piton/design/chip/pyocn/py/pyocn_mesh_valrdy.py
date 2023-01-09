'''
==========================================================================
pyocn_mesh_valrdy.py
==========================================================================
Helper function that generates the pyocn_mesh_credit_ifc module.

Author : Yanghui Ou
  Date : Mar 18, 2020
'''
from __future__ import print_function

def print_module( x_tiles, y_tiles ):
  tmpl = '''
module pyocn_mesh_valrdy (
  input clk,
  input reset,
  input  [`DATA_WIDTH-1:0] in_dat [0:{n}],
  input                    in_val [0:{n}],
  output                   in_rdy [0:{n}],
  input  [`DATA_WIDTH-1:0] offchip_in_dat,
  input                    offchip_in_val,
  output                   offchip_in_rdy,
  output [`DATA_WIDTH-1:0] out_dat [0:{n}],
  output                   out_val [0:{n}],
  input                    out_rdy [0:{n}],
  output [`DATA_WIDTH-1:0] offchip_out_dat,
  output                   offchip_out_val,
  input                    offchip_out_rdy
);

pyocn_mesh_{x_tiles}x{y_tiles} noc(
  .clk     ( clk   ),
  .reset   ( reset ),
  .in___msg( in_dat ),
  .in___val( in_val ),
  .in___rdy( in_rdy ),
  .offchip_in__msg( offchip_in_dat ),
  .offchip_in__val( offchip_in_val ),
  .offchip_in__rdy( offchip_in_rdy ),
  .out__msg( out_dat ),
  .out__val( out_val ),
  .out__rdy( out_rdy ),
  .offchip_out__msg( offchip_out_dat ),
  .offchip_out__val( offchip_out_val ),
  .offchip_out__rdy( offchip_out_rdy )
);

endmodule
'''
  ntiles = x_tiles * y_tiles
  print( tmpl.format( x_tiles=x_tiles, y_tiles=y_tiles, n=ntiles-1 ) )
