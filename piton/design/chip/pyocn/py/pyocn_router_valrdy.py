'''
==========================================================================
pyocn_mesh_valrdy.py
==========================================================================
Helper function that generates the pyocn_mesh_credit_ifc module.

Author : Yanghui Ou
  Date : Mar 18, 2020
'''

def print_module():
  tmpl = '''
module pyocn_router_valrdy (
  input clk,
  input reset,
  input  [`NOC_CHIPID_WIDTH-1:0] chipid,
  input  [`NOC_X_WIDTH-1     :0] pos_x,
  input  [`NOC_Y_WIDTH-1     :0] pos_y,
  input  [`DATA_WIDTH-1:0] in_N_dat,
  input                    in_N_val,
  output                   in_N_rdy,
  input  [`DATA_WIDTH-1:0] in_S_dat,
  input                    in_S_val,
  output                   in_S_rdy,
  input  [`DATA_WIDTH-1:0] in_W_dat,
  input                    in_W_val,
  output                   in_W_rdy,
  input  [`DATA_WIDTH-1:0] in_E_dat,
  input                    in_E_val,
  output                   in_E_rdy,
  input  [`DATA_WIDTH-1:0] in_P_dat,
  input                    in_P_val,
  output                   in_P_rdy,

  output [`DATA_WIDTH-1:0] out_N_dat,
  output                   out_N_val,
  input                    out_N_rdy,
  output [`DATA_WIDTH-1:0] out_S_dat,
  output                   out_S_val,
  input                    out_S_rdy,
  output [`DATA_WIDTH-1:0] out_W_dat,
  output                   out_W_val,
  input                    out_W_rdy,
  output [`DATA_WIDTH-1:0] out_E_dat,
  output                   out_E_val,
  input                    out_E_rdy,
  output [`DATA_WIDTH-1:0] out_P_dat,
  output                   out_P_val,
  input                    out_P_rdy

);

wire [`DATA_WIDTH-1:0] in_msg [0:4];
wire                   in_val [0:4];
wire                   in_rdy [0:4];
wire [`DATA_WIDTH-1:0] out_msg [0:4];
wire                   out_val [0:4];
wire                   out_rdy [0:4];

assign in_msg[0] = in_N_dat;
assign in_msg[1] = in_S_dat;
assign in_msg[2] = in_W_dat;
assign in_msg[3] = in_E_dat;
assign in_msg[4] = in_P_dat;

assign in_val[0] = in_N_val;
assign in_val[1] = in_S_val;
assign in_val[2] = in_W_val;
assign in_val[3] = in_E_val;
assign in_val[4] = in_P_val;

assign in_N_rdy = in_rdy[0];
assign in_S_rdy = in_rdy[1];
assign in_W_rdy = in_rdy[2];
assign in_E_rdy = in_rdy[3];
assign in_P_rdy = in_rdy[4];

assign out_N_dat = out_msg[0];
assign out_S_dat = out_msg[1];
assign out_W_dat = out_msg[2];
assign out_E_dat = out_msg[3];
assign out_P_dat = out_msg[4];

assign out_N_val = out_val[0];
assign out_S_val = out_val[1];
assign out_W_val = out_val[2];
assign out_E_val = out_val[3];
assign out_P_val = out_val[4];

assign out_rdy[0] = out_N_rdy;
assign out_rdy[1] = out_S_rdy;
assign out_rdy[2] = out_W_rdy;
assign out_rdy[3] = out_E_rdy;
assign out_rdy[4] = out_P_rdy;

pyocn_router router(
  .clk     ( clk   ),
  .reset   ( reset ),
  .pos     ( { chipid, pos_x, pos_y } ),
  .in___msg( in_msg ),
  .in___val( in_val ),
  .in___rdy( in_rdy ),
  .out__msg( out_msg ),
  .out__val( out_val ),
  .out__rdy( out_rdy )
);

endmodule
'''
  print( tmpl )

'''
Original interface:
    dynamic_node_top_wrap user_dynamic_network0
      (.clk(clk_gated),
       .reset_in(~rst_n_f),
       // dataIn (to input blocks)
       .dataIn_N(dyn0_dataIn_N),
       .dataIn_E(dyn0_dataIn_E),
       .dataIn_S(dyn0_dataIn_S),
       .dataIn_W(dyn0_dataIn_W),
       .dataIn_P(buffer_router_data_noc1),
       // validIn (to input blocks)
       .validIn_N(dyn0_validIn_N),
       .validIn_E(dyn0_validIn_E),
       .validIn_S(dyn0_validIn_S),
       .validIn_W(dyn0_validIn_W),
       .validIn_P(buffer_router_valid_noc1),
       // yummy (from nighboring input blocks)
       .yummyIn_N(dyn0_dNo_yummy),
       .yummyIn_E(dyn0_dEo_yummy),
       .yummyIn_S(dyn0_dSo_yummy),
       .yummyIn_W(dyn0_dWo_yummy),
       .yummyIn_P(buffer_router_yummy_noc1),
       // My Absolute Address
       .myLocX(config_coreid_x),
       .myLocY(config_coreid_y),
       .myChipID(config_chipid),
       //.ec_cfg(15'b0),//ec_dyn_cfg[14:0]),
       //.store_meter_partner_address_X(5'b0),
       //.store_meter_partner_address_Y(5'b0),
       // DataOut (from crossbar)
       .dataOut_N(dyn0_dNo),
       .dataOut_E(dyn0_dEo),
       .dataOut_S(dyn0_dSo),
       .dataOut_W(dyn0_dWo),
       .dataOut_P(router_buffer_data_noc1), //data output to processor
       // validOut (from crossbar)
       .validOut_N(dyn0_dNo_valid),
       .validOut_E(dyn0_dEo_valid),
       .validOut_S(dyn0_dSo_valid),
       .validOut_W(dyn0_dWo_valid),
       .validOut_P(router_buffer_data_val_noc1), //data valid to processor
       // yummyOut (to neighboring output blocks)
       .yummyOut_N(dyn0_yummyOut_N),
       .yummyOut_E(dyn0_yummyOut_E),
       .yummyOut_W(dyn0_yummyOut_W),
       .yummyOut_S(dyn0_yummyOut_S),
       .yummyOut_P(router_buffer_consumed_noc1), //yummy out to neighboring
       // thanksIn (to CGNO)
       .thanksIn_P(thanksIn_CGNO0));
       //.external_interrupt(),
       //.store_meter_ack_partner(),
       //.store_meter_ack_non_partner(),
       //.ec_out(ec_dyn0));
'''
