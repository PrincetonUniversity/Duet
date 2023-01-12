module adder (
    input wire      a
    , input wire    b
    , input wire    cin
    , output wire   cout
    , output wire   sumout
    );

    assign {cout, sumout} = a + b + cin;

endmodule
