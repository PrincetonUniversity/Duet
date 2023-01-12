module dual_port_ram #(
    parameter   ADDR_WIDTH = 9
) (
    input wire clk

    , input wire [ADDR_WIDTH-1:0]   addr1
    , input wire [ADDR_WIDTH-1:0]   addr2
    , input wire                    we1
    , input wire                    we2
    , input wire                    data1
    , input wire                    data2
    , output reg                    out1
    , output reg                    out2
    );

    reg _data   [0:(1 << ADDR_WIDTH) - 1];

    always @(posedge clk) begin
        if (we1)
            _data[addr1] <= data1;

        if (we2)
            _data[addr2] <= data2;

        out1 <= _data[addr1];
        out2 <= _data[addr2];
    end

endmodule
