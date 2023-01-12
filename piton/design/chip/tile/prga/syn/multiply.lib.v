module multiply #(
    parameter   WIDTH   = 9
) (
    input wire [WIDTH-1:0]      a
    , input wire [WIDTH-1:0]    b
    , output wire [2*WIDTH-1:0]   out
    );

    assign out = a * b;

endmodule
