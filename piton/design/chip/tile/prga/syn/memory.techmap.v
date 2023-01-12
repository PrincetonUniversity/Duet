module _mmap__dpram_a10d32 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 10;
    localparam      DATA_WIDTH = 32;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule

module _mmap__dpram_a11d16 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 11;
    localparam      DATA_WIDTH = 16;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule

module _mmap__dpram_a12d8 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 12;
    localparam      DATA_WIDTH = 8;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule

module _mmap__dpram_a13d4 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 13;
    localparam      DATA_WIDTH = 4;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule

module _mmap__dpram_a14d2 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 14;
    localparam      DATA_WIDTH = 2;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule

module _mmap__dpram_a15d1 (CLK1, A1ADDR, A1DATA, A1EN, B1ADDR, B1DATA);

    localparam      ADDR_WIDTH = 15;
    localparam      DATA_WIDTH = 1;

    input                   CLK1;
    input [ADDR_WIDTH-1:0]  A1ADDR;
    input [DATA_WIDTH-1:0]  A1DATA;
    input                   A1EN;
    input [ADDR_WIDTH-1:0]  B1ADDR;
    output [DATA_WIDTH-1:0] B1DATA;

    parameter       INIT    = 1'bx;
    parameter       CLKPOL1 = 1;
    parameter       CLKPOL2 = 1;

    genvar i;
    generate for (i = 0; i < DATA_WIDTH; i = i + 1) begin
        dual_port_ram #(
            .ADDR_WIDTH     (ADDR_WIDTH)
        ) _TECHMAP_REPLACE (
            .clk        (CLK1)

            ,.addr1     (A1ADDR)
            ,.we1       (A1EN)
            ,.data1     (A1DATA[i])

            ,.addr2     (B1ADDR)
            ,.we2       (1'b0)
            ,.out2      (B1DATA[i])
            );
    end endgenerate

endmodule
