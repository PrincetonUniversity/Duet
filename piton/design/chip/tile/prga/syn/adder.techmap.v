module \$add (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;
    localparam  LAST = Y_WIDTH-1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [LAST:0] Y;

    wire _TECHMAP_FAIL_ = Y_WIDTH <= 2;

    wire [LAST:0] A_buf, B_buf;
    \$pos #(.A_SIGNED(A_SIGNED), .A_WIDTH(A_WIDTH), .Y_WIDTH(Y_WIDTH)) A_conv (.A(A), .Y(A_buf));
    \$pos #(.A_SIGNED(B_SIGNED), .A_WIDTH(B_WIDTH), .Y_WIDTH(Y_WIDTH)) B_conv (.A(B), .Y(B_buf));

    wire [LAST:1] CARRY;

    // VTR flagship architecture assumes cin is tied to ground if not connected
    adder cc_first (.a(A_buf[0]), .b(B_buf[0]), .sumout(Y[0]), .cout(CARRY[1]));

    genvar i;
    generate for (i = 1; i < LAST; i = i + 1) begin
        adder cc (.a(A_buf[i]), .b(B_buf[i]), .cin(CARRY[i]), .sumout(Y[i]), .cout(CARRY[i+1]));
    end endgenerate

    adder cc_last  (.a(A_buf[LAST]), .b(B_buf[LAST]), .cin(CARRY[LAST]), .sumout(Y[LAST]));

endmodule

module \$sub (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;
    localparam  LAST = Y_WIDTH-1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [LAST:0] Y;

    wire _TECHMAP_FAIL_ = Y_WIDTH <= 2;

    wire [LAST:0] A_buf, B_buf;
    \$pos #(.A_SIGNED(A_SIGNED), .A_WIDTH(A_WIDTH), .Y_WIDTH(Y_WIDTH)) A_conv (.A(A), .Y(A_buf));
    \$pos #(.A_SIGNED(B_SIGNED), .A_WIDTH(B_WIDTH), .Y_WIDTH(Y_WIDTH)) B_conv (.A(B), .Y(B_buf));

    wire [LAST:0] CARRY;

    adder cc_zero (.a(1'b0), .b(1'b1), .cout(CARRY[0]));

    genvar i;
    generate for (i = 0; i < LAST; i = i + 1) begin
        adder cc (.a(A_buf[i]), .b(~B_buf[i]), .cin(CARRY[i]), .sumout(Y[i]), .cout(CARRY[i+1]));
    end endgenerate

    adder cc_last (.a(A_buf[LAST]), .b(B_buf[LAST]), .cin(CARRY[LAST]), .sumout(Y[LAST]));

endmodule

module _cmp_ (A, B, Y);
    // calculates A - B, set Y to 1'b1 if A < B
    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output Y;

    localparam  Z_WIDTH = (A_WIDTH > B_WIDTH ? A_WIDTH : B_WIDTH) + (A_SIGNED != B_SIGNED ? 1 : 0); 
    wire [Z_WIDTH-1:0] A_buf, B_buf;
    \$pos #(.A_SIGNED(A_SIGNED), .A_WIDTH(A_WIDTH), .Y_WIDTH(Z_WIDTH)) A_conv (.A(A), .Y(A_buf));
    \$pos #(.A_SIGNED(B_SIGNED), .A_WIDTH(B_WIDTH), .Y_WIDTH(Z_WIDTH)) B_conv (.A(B), .Y(B_buf));

    wire [Z_WIDTH:0] CARRY;

    adder cc_zero (.a(1'b0), .b(1'b1), .cout(CARRY[0]));

    genvar i;
    generate for (i = 0; i < Z_WIDTH; i = i + 1) begin
        adder cc (.a(A_buf[i]), .b(~B_buf[i]), .cin(CARRY[i]), .cout(CARRY[i+1]));
    end endgenerate

    adder cc_last (.a(1'b0), .b(1'b0), .cin(CARRY[Z_WIDTH]), .sumout(Y));

endmodule

module \$lt (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [Y_WIDTH-1:0] Y;

    wire cmp_o;

    _cmp_ #(.A_SIGNED(A_SIGNED), .B_SIGNED(B_SIGNED), .A_WIDTH(A_WIDTH), .B_WIDTH(B_WIDTH)) i_cmp (.A(A), .B(B), .Y(cmp_o));

    generate if (Y_WIDTH > 1) begin
        assign Y = { {(Y_WIDTH - 1) {1'b0} }, cmp_o };
    end else begin
        assign Y = cmp_o;
    end endgenerate

endmodule

module \$gt (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [Y_WIDTH-1:0] Y;

    wire cmp_o;

    _cmp_ #(.A_SIGNED(B_SIGNED), .B_SIGNED(A_SIGNED), .A_WIDTH(B_WIDTH), .B_WIDTH(A_WIDTH)) i_cmp (.A(B), .B(A), .Y(cmp_o));

    generate if (Y_WIDTH > 1) begin
        assign Y = { {(Y_WIDTH - 1) {1'b0} }, cmp_o };
    end else begin
        assign Y = cmp_o;
    end endgenerate

endmodule

module \$le (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [Y_WIDTH-1:0] Y;

    wire cmp_o;

    _cmp_ #(.A_SIGNED(B_SIGNED), .B_SIGNED(A_SIGNED), .A_WIDTH(B_WIDTH), .B_WIDTH(A_WIDTH)) i_cmp (.A(B), .B(A), .Y(cmp_o));

    generate if (Y_WIDTH > 1) begin
        assign Y = { {(Y_WIDTH - 1) {1'b0} }, ~cmp_o };
    end else begin
        assign Y = ~cmp_o;
    end endgenerate

endmodule

module \$ge (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [Y_WIDTH-1:0] Y;

    wire cmp_o;

    _cmp_ #(.A_SIGNED(A_SIGNED), .B_SIGNED(B_SIGNED), .A_WIDTH(A_WIDTH), .B_WIDTH(B_WIDTH)) i_cmp (.A(A), .B(B), .Y(cmp_o));

    generate if (Y_WIDTH > 1) begin
        assign Y = { {(Y_WIDTH - 1) {1'b0} }, ~cmp_o };
    end else begin
        assign Y = ~cmp_o;
    end endgenerate

endmodule
