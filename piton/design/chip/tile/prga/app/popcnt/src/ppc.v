module ppc (
    input wire              clk
    , input wire            rst_n

    , output wire           start_rdy
    , input wire            start_vld
    , input wire [31:0]     len         // number of 64b inputs

    , input wire            done_full
    , output wire           done_wr
    , output reg [63:0]     count       // total number of bits set

    , input wire            ivld
    , input wire [63:0]     idat
    , output wire           irdy
    );

    // count per element
    reg         elem_vld;
    reg [63:0]  elem;
    wire [7:0]  elem_cnt;

    always @(posedge clk) begin
        if (~rst_n) begin
            elem_vld    <= 1'b0;
            elem        <= 64'h0;
        end else if (ivld && irdy) begin
            elem_vld    <= 1'b1;
            elem        <= idat;
        end else begin
            elem_vld    <= 1'b0;
        end
    end

    // FSM
    localparam  STATE_WIDTH     = 2;
    localparam  STATE_RESET     = 2'h0,
                STATE_IDLE      = 2'h1,
                STATE_WORKING   = 2'h2,
                STATE_DONE      = 2'h3;

    reg [STATE_WIDTH-1:0]   state, state_next;
    reg                     elem_vld_f;
    reg [7:0]               elem_cnt_f;
    reg [31:0]              left;

    always @(posedge clk) begin
        if (~rst_n) begin
            state       <= STATE_RESET;
            elem_vld_f  <= 1'b0;
            elem_cnt_f  <= 8'h0;
            left        <= 32'h0;
            count       <= 64'h0;
        end else begin
            state       <= state_next;
            elem_vld_f  <= elem_vld;
            elem_cnt_f  <= elem_cnt;

            if (start_rdy && start_vld)
                left    <= len;
            else if (ivld && irdy)
                left    <= left - 1;

            if (start_rdy && start_vld)
                count   <= 64'h0;
            else if (elem_vld_f)
                count   <= count + elem_cnt_f;
        end
    end

    always @* begin
        state_next  = state;

        case (state)
            STATE_RESET:
                state_next = STATE_IDLE;

            STATE_IDLE:
                if (start_rdy && start_vld)
                    state_next = STATE_WORKING;

            STATE_WORKING:
                if (left == 1 && ivld && irdy)
                    state_next = STATE_DONE;

            STATE_DONE:
                if (!done_full && done_wr)
                    state_next = STATE_IDLE;
        endcase
    end

    assign start_rdy = state == STATE_IDLE;
    assign done_wr = state == STATE_DONE && !elem_vld && !elem_vld_f;
    assign irdy = state == STATE_WORKING;

    // popcount sum tree
    // lvl 0: nibble count

    reg [2:0]   partial0    [15:0];

    genvar i0;
    generate
        for (i0 = 0; i0 < 16; i0 = i0 + 1) begin
            always @* begin
                partial0[i0] = 3'd0;

                case (elem[i0 * 4 +: 4])
                    4'b0000:
                        partial0[i0] = 3'd0;
                    4'b0001,
                    4'b0010,
                    4'b0100,
                    4'b1000:
                        partial0[i0] = 3'd1;
                    4'b0111,
                    4'b1011,
                    4'b1101,
                    4'b1110:
                        partial0[i0] = 3'd3;
                    4'b1111:
                        partial0[i0] = 3'd4;
                    default:
                        partial0[i0] = 3'd2;
                endcase
            end
        end
    endgenerate

    // lvl 1: half-word count
    wire [3:0]  partial1    [7:0];

    genvar i1;
    generate
        for (i1 = 0; i1 < 8; i1 = i1 + 1) begin
            assign  partial1[i1] = partial0[i1 * 2] + partial0[i1 * 2 + 1];
        end
    endgenerate

    // lvl 2: word count
    wire [4:0]  partial2    [3:0];

    genvar i2;
    generate
        for (i2 = 0; i2 < 4; i2 = i2 + 1) begin
            assign  partial2[i2] = partial1[i2 * 2] + partial1[i2 * 2 + 1];
        end
    endgenerate

    // lvl 3: double-word count
    wire [5:0]  partial3    [1:0];

    genvar i3;
    generate
        for (i3 = 0; i3 < 2; i3 = i3 + 1) begin
            assign  partial3[i3] = partial2[i3 * 2] + partial2[i3 * 2 + 1];
        end
    endgenerate

    // lvl 4: final (quad-word) count
    assign elem_cnt = partial3[0] + partial3[1];

endmodule
