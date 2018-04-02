/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: top_level_TB.v
 *****/

module  top_level_TB;
    reg clk, GUPB, GLPB, CUPB, CLPB, reset;
    wire [3:0] led_sel;
    wire [7:0] led_out;

    /* Device under test */
    top_level DUT (
        .clk(clk),
        .GUPB(GUPB),
        .GLPB(GLPB),
        .CUPB(CUPB),
        .CLPB(CLPB),
        .reset(reset),
        .led_sel(led_sel),
        .led_out(led_out)
    );

    initial begin
        
        clk = 0;
        GUPB = 0;
        GLPB = 0;
        CUPB = 0;
        CLPB = 0;
        reset = 1;

        #10 reset = 0;

        #5  CUPB = 1;
        #5  CUPB = 0;
        #200 GLPB = 1;
        #5  GLPB = 0;
        #20 $finish;
    end

    always #1 clk = ~clk;

endmodule
