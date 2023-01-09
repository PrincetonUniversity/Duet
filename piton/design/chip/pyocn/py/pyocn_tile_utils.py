'''
==========================================================================
pyocn_tile_utils.py
==========================================================================
Helper functions for the tile module.

Author : Yanghui Ou
  Date : Mar 18, 2020
'''
from __future__ import print_function

#-------------------------------------------------------------------------
# str_tile_noc_ifcs
#-------------------------------------------------------------------------
# Returns the string for the tile - noc interface of the network
# configuration.

def str_tile_noc_ifcs():
  return '''
    // pyocn_config - str_tile_noc_ifcs

    input [`NOC_DATA_WIDTH-1:0]         dyn0_in_dat,
    input                               dyn0_in_val,
    output                              dyn0_in_rdy,

    input [`NOC_DATA_WIDTH-1:0]         dyn1_in_dat,
    input                               dyn1_in_val,
    output                              dyn1_in_rdy,

    input [`NOC_DATA_WIDTH-1:0]         dyn2_in_dat,
    input                               dyn2_in_val,
    output                              dyn2_in_rdy,

    output [`NOC_DATA_WIDTH-1:0]        dyn0_out_dat,
    output                              dyn0_out_val,
    input                               dyn0_out_rdy,

    output [`NOC_DATA_WIDTH-1:0]        dyn1_out_dat,
    output                              dyn1_out_val,
    input                               dyn1_out_rdy,

    output [`NOC_DATA_WIDTH-1:0]        dyn2_out_dat,
    output                              dyn2_out_val,
    input                               dyn2_out_rdy
'''

#-------------------------------------------------------------------------
# str_tile_noc_ifcs_connects
#-------------------------------------------------------------------------
# Returns the string that assigns the ports to the corresponding wires.

def str_tile_noc_ifcs_connects():
  return '''
    // pyocn_config - str_tile_noc_ifcs_connects

    assign dyn0_out_dat                = processor_router_data_noc1;
    assign dyn0_out_val                = processor_router_valid_noc1;
    assign router_processor_ready_noc1 = dyn0_out_rdy;

    assign dyn1_out_dat                = processor_router_data_noc2;
    assign dyn1_out_val                = processor_router_valid_noc2;
    assign router_processor_ready_noc2 = dyn1_out_rdy;

    assign dyn2_out_dat                = processor_router_data_noc3;
    assign dyn2_out_val                = processor_router_valid_noc3;
    assign router_processor_ready_noc3 = dyn2_out_rdy;

    assign buffer_processor_data_noc1  = dyn0_in_dat;
    assign buffer_processor_valid_noc1 = dyn0_in_val;
    assign dyn0_in_rdy                 = processor_router_ready_noc1;

    assign buffer_processor_data_noc2  = dyn1_in_dat;
    assign buffer_processor_valid_noc2 = dyn1_in_val;
    assign dyn1_in_rdy                 = processor_router_ready_noc2;

    assign buffer_processor_data_noc3  = dyn2_in_dat;
    assign buffer_processor_valid_noc3 = dyn2_in_val;
    assign dyn2_in_rdy                 = processor_router_ready_noc3;
'''

#-------------------------------------------------------------------------
# str_router_tile_noc_ifcs
#-------------------------------------------------------------------------
# Returns the string for the tile - noc interface of the router
# configuration.

def str_router_tile_noc_ifcs():
  return '''
    // pyocn_config - str_tile_noc_ifcs

    // Dynamic network inputs 0
    input [`NOC_DATA_WIDTH-1:0]         dyn0_in_N_dat,
    input                               dyn0_in_N_val,
    output                              dyn0_in_N_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn0_in_S_dat,
    input                               dyn0_in_S_val,
    output                              dyn0_in_S_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn0_in_W_dat,
    input                               dyn0_in_W_val,
    output                              dyn0_in_W_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn0_in_E_dat,
    input                               dyn0_in_E_val,
    output                              dyn0_in_E_rdy,

    // Dynamic network inputs 1
    input [`NOC_DATA_WIDTH-1:0]         dyn1_in_N_dat,
    input                               dyn1_in_N_val,
    output                              dyn1_in_N_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn1_in_S_dat,
    input                               dyn1_in_S_val,
    output                              dyn1_in_S_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn1_in_W_dat,
    input                               dyn1_in_W_val,
    output                              dyn1_in_W_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn1_in_E_dat,
    input                               dyn1_in_E_val,
    output                              dyn1_in_E_rdy,

    // Dynamic network inputs 2
    input [`NOC_DATA_WIDTH-1:0]         dyn2_in_N_dat,
    input                               dyn2_in_N_val,
    output                              dyn2_in_N_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn2_in_S_dat,
    input                               dyn2_in_S_val,
    output                              dyn2_in_S_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn2_in_W_dat,
    input                               dyn2_in_W_val,
    output                              dyn2_in_W_rdy,
    input [`NOC_DATA_WIDTH-1:0]         dyn2_in_E_dat,
    input                               dyn2_in_E_val,
    output                              dyn2_in_E_rdy,

    // Dynamic network outputs 0
    output [`NOC_DATA_WIDTH-1:0]        dyn0_out_N_dat,
    output                              dyn0_out_N_val,
    input                               dyn0_out_N_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn0_out_S_dat,
    output                              dyn0_out_S_val,
    input                               dyn0_out_S_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn0_out_W_dat,
    output                              dyn0_out_W_val,
    input                               dyn0_out_W_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn0_out_E_dat,
    output                              dyn0_out_E_val,
    input                               dyn0_out_E_rdy,

    // Dynamic network outputs 1
    output [`NOC_DATA_WIDTH-1:0]        dyn1_out_N_dat,
    output                              dyn1_out_N_val,
    input                               dyn1_out_N_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn1_out_S_dat,
    output                              dyn1_out_S_val,
    input                               dyn1_out_S_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn1_out_W_dat,
    output                              dyn1_out_W_val,
    input                               dyn1_out_W_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn1_out_E_dat,
    output                              dyn1_out_E_val,
    input                               dyn1_out_E_rdy,

    // Dynamic network outputs 2
    output [`NOC_DATA_WIDTH-1:0]        dyn2_out_N_dat,
    output                              dyn2_out_N_val,
    input                               dyn2_out_N_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn2_out_S_dat,
    output                              dyn2_out_S_val,
    input                               dyn2_out_S_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn2_out_W_dat,
    output                              dyn2_out_W_val,
    input                               dyn2_out_W_rdy,
    output [`NOC_DATA_WIDTH-1:0]        dyn2_out_E_dat,
    output                              dyn2_out_E_val,
    input                               dyn2_out_E_rdy
'''

def define_wires_between_socket_and_core():
    return '''
    // This is for backend purpose:
    // North noc wires will go over core, generating huge wire delay
    // Thus for tall cores, we'll let the noc wire go through the core
    // We need to add input/output ports of NoC wires for IS and prga_ctrl core 
    wire [`NOC_DATA_WIDTH-1:0]         dyn0_in_N_dat_s2c;
    wire                               dyn0_in_N_val_s2c;
    wire                               dyn0_in_N_rdy_s2c;
    wire [`NOC_DATA_WIDTH-1:0]         dyn1_in_N_dat_s2c;
    wire                               dyn1_in_N_val_s2c;
    wire                               dyn1_in_N_rdy_s2c;
    wire [`NOC_DATA_WIDTH-1:0]         dyn2_in_N_dat_s2c;
    wire                               dyn2_in_N_val_s2c;
    wire                               dyn2_in_N_rdy_s2c;

    wire [`NOC_DATA_WIDTH-1:0]         dyn0_out_N_dat_s2c;
    wire                               dyn0_out_N_val_s2c;
    wire                               dyn0_out_N_rdy_s2c;
    wire [`NOC_DATA_WIDTH-1:0]         dyn1_out_N_dat_s2c;
    wire                               dyn1_out_N_val_s2c;
    wire                               dyn1_out_N_rdy_s2c;
    wire [`NOC_DATA_WIDTH-1:0]         dyn2_out_N_dat_s2c;
    wire                               dyn2_out_N_val_s2c;
    wire                               dyn2_out_N_rdy_s2c;
    '''

def feed_through_connection():
    return '''
    assign  dyn0_in_N_dat_s2c   =  dyn0_in_N_dat;
    assign  dyn0_in_N_val_s2c   =  dyn0_in_N_val;
    assign  dyn0_in_N_rdy   =  dyn0_in_N_rdy_s2c;
    assign  dyn1_in_N_dat_s2c   =  dyn1_in_N_dat;
    assign  dyn1_in_N_val_s2c   =  dyn1_in_N_val;
    assign  dyn1_in_N_rdy   =  dyn1_in_N_rdy_s2c;
    assign  dyn2_in_N_dat_s2c   =  dyn2_in_N_dat;
    assign  dyn2_in_N_val_s2c   =  dyn2_in_N_val;
    assign  dyn2_in_N_rdy   =  dyn2_in_N_rdy_s2c;
                              
    assign  dyn0_out_N_dat  =  dyn0_out_N_dat_s2c;
    assign  dyn0_out_N_val  =  dyn0_out_N_val_s2c;
    assign  dyn0_out_N_rdy_s2c  =  dyn0_out_N_rdy;
    assign  dyn1_out_N_dat  =  dyn1_out_N_dat_s2c;
    assign  dyn1_out_N_val  =  dyn1_out_N_val_s2c;
    assign  dyn1_out_N_rdy_s2c  =  dyn1_out_N_rdy;
    assign  dyn2_out_N_dat  =  dyn2_out_N_dat_s2c;
    assign  dyn2_out_N_val  =  dyn2_out_N_val_s2c;
    assign  dyn2_out_N_rdy_s2c  =  dyn2_out_N_rdy;
    '''

# Return the string for the instantiation of the socket
# in tile module. It just directly coneects the noc ports.
# Only used when PITON_SOCKET is defined
def str_router_tile_noc_direct_connect():
  return '''
    // pyocn_router_config - str_router_tile_noc_direct_connect

    // Dynamic network inputs 0
    .dyn0_in_N_dat                      (dyn0_in_N_dat_s2c),
    .dyn0_in_N_val                      (dyn0_in_N_val_s2c),
    .dyn0_in_N_rdy                      (dyn0_in_N_rdy_s2c),
    .dyn0_in_S_dat                      (dyn0_in_S_dat),
    .dyn0_in_S_val                      (dyn0_in_S_val),
    .dyn0_in_S_rdy                      (dyn0_in_S_rdy),
    .dyn0_in_W_dat                      (dyn0_in_W_dat),
    .dyn0_in_W_val                      (dyn0_in_W_val),
    .dyn0_in_W_rdy                      (dyn0_in_W_rdy),
    .dyn0_in_E_dat                      (dyn0_in_E_dat),
    .dyn0_in_E_val                      (dyn0_in_E_val),
    .dyn0_in_E_rdy                      (dyn0_in_E_rdy),
                                                     
                                       
    // Dynamic network inputs 1
    .dyn1_in_N_dat                      (dyn1_in_N_dat_s2c),
    .dyn1_in_N_val                      (dyn1_in_N_val_s2c),
    .dyn1_in_N_rdy                      (dyn1_in_N_rdy_s2c),
    .dyn1_in_S_dat                      (dyn1_in_S_dat),
    .dyn1_in_S_val                      (dyn1_in_S_val),
    .dyn1_in_S_rdy                      (dyn1_in_S_rdy),
    .dyn1_in_W_dat                      (dyn1_in_W_dat),
    .dyn1_in_W_val                      (dyn1_in_W_val),
    .dyn1_in_W_rdy                      (dyn1_in_W_rdy),
    .dyn1_in_E_dat                      (dyn1_in_E_dat),
    .dyn1_in_E_val                      (dyn1_in_E_val),
    .dyn1_in_E_rdy                      (dyn1_in_E_rdy),
                                                     
                                       
    // Dynamic network inputs 2
    .dyn2_in_N_dat                      (dyn2_in_N_dat_s2c),
    .dyn2_in_N_val                      (dyn2_in_N_val_s2c),
    .dyn2_in_N_rdy                      (dyn2_in_N_rdy_s2c),
    .dyn2_in_S_dat                      (dyn2_in_S_dat),
    .dyn2_in_S_val                      (dyn2_in_S_val),
    .dyn2_in_S_rdy                      (dyn2_in_S_rdy),
    .dyn2_in_W_dat                      (dyn2_in_W_dat),
    .dyn2_in_W_val                      (dyn2_in_W_val),
    .dyn2_in_W_rdy                      (dyn2_in_W_rdy),
    .dyn2_in_E_dat                      (dyn2_in_E_dat),
    .dyn2_in_E_val                      (dyn2_in_E_val),
    .dyn2_in_E_rdy                      (dyn2_in_E_rdy),
                                                      
                                       
    // Dynamic network outputs 0
    .dyn0_out_N_dat                     (dyn0_out_N_dat_s2c),
    .dyn0_out_N_val                     (dyn0_out_N_val_s2c),
    .dyn0_out_N_rdy                     (dyn0_out_N_rdy_s2c),
    .dyn0_out_S_dat                     (dyn0_out_S_dat),
    .dyn0_out_S_val                     (dyn0_out_S_val),
    .dyn0_out_S_rdy                     (dyn0_out_S_rdy),
    .dyn0_out_W_dat                     (dyn0_out_W_dat),
    .dyn0_out_W_val                     (dyn0_out_W_val),
    .dyn0_out_W_rdy                     (dyn0_out_W_rdy),
    .dyn0_out_E_dat                     (dyn0_out_E_dat),
    .dyn0_out_E_val                     (dyn0_out_E_val),
    .dyn0_out_E_rdy                     (dyn0_out_E_rdy),
                                                     
                                        
    // Dynamic network outputs 1
    .dyn1_out_N_dat                     (dyn1_out_N_dat_s2c),
    .dyn1_out_N_val                     (dyn1_out_N_val_s2c),
    .dyn1_out_N_rdy                     (dyn1_out_N_rdy_s2c),
    .dyn1_out_S_dat                     (dyn1_out_S_dat),
    .dyn1_out_S_val                     (dyn1_out_S_val),
    .dyn1_out_S_rdy                     (dyn1_out_S_rdy),
    .dyn1_out_W_dat                     (dyn1_out_W_dat),
    .dyn1_out_W_val                     (dyn1_out_W_val),
    .dyn1_out_W_rdy                     (dyn1_out_W_rdy),
    .dyn1_out_E_dat                     (dyn1_out_E_dat),
    .dyn1_out_E_val                     (dyn1_out_E_val),
    .dyn1_out_E_rdy                     (dyn1_out_E_rdy),
                                                     
                                        
    // Dynamic network outputs 2
    .dyn2_out_N_dat                     (dyn2_out_N_dat_s2c),
    .dyn2_out_N_val                     (dyn2_out_N_val_s2c),
    .dyn2_out_N_rdy                     (dyn2_out_N_rdy_s2c),
    .dyn2_out_S_dat                     (dyn2_out_S_dat),
    .dyn2_out_S_val                     (dyn2_out_S_val),
    .dyn2_out_S_rdy                     (dyn2_out_S_rdy),
    .dyn2_out_W_dat                     (dyn2_out_W_dat),
    .dyn2_out_W_val                     (dyn2_out_W_val),
    .dyn2_out_W_rdy                     (dyn2_out_W_rdy),
    .dyn2_out_E_dat                     (dyn2_out_E_dat),
    .dyn2_out_E_val                     (dyn2_out_E_val),
    .dyn2_out_E_rdy                     (dyn2_out_E_rdy)
'''

def str_router_inst( id ):
    return f'''

wire [`NOC_DATA_WIDTH-1:0]    router_buffer_vr_noc{id+1}_dat;
wire                          router_buffer_vr_noc{id+1}_val;
wire                          router_buffer_vr_noc{id+1}_rdy;

pyocn_router_valrdy pyocn_router{id} (
  .clk     ( clk_gated ),
  .reset   ( ~rst_n_f  ),
  .chipid  ( config_chipid   ),
  .pos_x   ( config_coreid_x ),
  .pos_y   ( config_coreid_y ),

  // input
  .in_N_dat( dyn{id}_in_N_dat ),
  .in_N_val( dyn{id}_in_N_val ),
  .in_N_rdy( dyn{id}_in_N_rdy ),
  .in_S_dat( dyn{id}_in_S_dat ),
  .in_S_val( dyn{id}_in_S_val ),
  .in_S_rdy( dyn{id}_in_S_rdy ),
  .in_W_dat( dyn{id}_in_W_dat ),
  .in_W_val( dyn{id}_in_W_val ),
  .in_W_rdy( dyn{id}_in_W_rdy ),
  .in_E_dat( dyn{id}_in_E_dat ),
  .in_E_val( dyn{id}_in_E_val ),
  .in_E_rdy( dyn{id}_in_E_rdy ),
  .in_P_dat( merger_buffer_vr_noc{id+1}_dat ),
  .in_P_val( merger_buffer_vr_noc{id+1}_val ),
  .in_P_rdy( merger_buffer_vr_noc{id+1}_rdy ),

  // output
  .out_N_dat( dyn{id}_out_N_dat ),
  .out_N_val( dyn{id}_out_N_val ),
  .out_N_rdy( dyn{id}_out_N_rdy ),
  .out_S_dat( dyn{id}_out_S_dat ),
  .out_S_val( dyn{id}_out_S_val ),
  .out_S_rdy( dyn{id}_out_S_rdy ),
  .out_W_dat( dyn{id}_out_W_dat ),
  .out_W_val( dyn{id}_out_W_val ),
  .out_W_rdy( dyn{id}_out_W_rdy ),
  .out_E_dat( dyn{id}_out_E_dat ),
  .out_E_val( dyn{id}_out_E_val ),
  .out_E_rdy( dyn{id}_out_E_rdy ),
  .out_P_dat( router_buffer_vr_noc{id+1}_dat ),
  .out_P_val( router_buffer_vr_noc{id+1}_val ),
  .out_P_rdy( router_buffer_vr_noc{id+1}_rdy )
);

sync_fifo_vr #(
    .DATA_WIDTH (`NOC_DATA_WIDTH),
    .FIFO_DEPTH (2)
) pyocn_router_{id}_output_queue (
    .clk                    ( clk_gated                        ),
    .rst_n                  ( rst_n_f                          ),

    .enqueue_vr_dat         ( router_buffer_vr_noc{id+1}_dat   ),
    .enqueue_vr_val         ( router_buffer_vr_noc{id+1}_val   ),
    .enqueue_vr_rdy         ( router_buffer_vr_noc{id+1}_rdy   ),

    .dequeue_vr_dat         ( buffer_splitter_vr_noc{id+1}_dat ),
    .dequeue_vr_val         ( buffer_splitter_vr_noc{id+1}_val ),
    .dequeue_vr_rdy         ( buffer_splitter_vr_noc{id+1}_rdy )
);

'''

'''
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
