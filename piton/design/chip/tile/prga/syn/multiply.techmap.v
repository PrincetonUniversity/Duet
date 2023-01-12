module \$mul (A, B, Y);

    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    localparam  MULTIPLIER = A_WIDTH <= 9 && B_WIDTH <= 9 ? 9
                            : A_WIDTH <= 18 && B_WIDTH <= 18 ? 18
                            : A_WIDTH <= 36 && B_WIDTH <= 36 ? 36
                            : 1;

    input [A_WIDTH-1:0] A;
    input [B_WIDTH-1:0] B;
    output [Y_WIDTH-1:0] Y;

    // give up if signed, or width is larger than 36
    wire _TECHMAP_FAIL_ = A_SIGNED || B_SIGNED || A_WIDTH > 36 || B_WIDTH > 36;

    wire [MULTIPLIER-1:0]   u, v;
    wire [2*MULTIPLIER-1:0] w;

    \$pos #(.A_SIGNED(0), .A_WIDTH(A_WIDTH), .Y_WIDTH(MULTIPLIER))      u_conv (.A(A), .Y(u));
    \$pos #(.A_SIGNED(0), .A_WIDTH(B_WIDTH), .Y_WIDTH(MULTIPLIER))      v_conv (.A(B), .Y(v));
    \$pos #(.A_SIGNED(0), .A_WIDTH(2*MULTIPLIER), .Y_WIDTH(Y_WIDTH))    y_conv (.A(w), .Y(Y));

    multiply #(.WIDTH(MULTIPLIER)) m (.a(u),.b(v),.out(w));

endmodule
