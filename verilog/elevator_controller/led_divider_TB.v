/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: led_divider_TB.v
 *****/

module  led_divider_TB;
    
    reg clk, reset;
    wire led_clk;

    /* Device under test */
    led_divider DUT (
        .clk(clk),
        .reset(reset),
        .led_clk(led_clk)
    );

    initial begin
        
        clk = 0;
       reset = 1;

        #10 reset = 0;

        #50 $finish;
    end

    always #1 clk = ~clk;

endmodule
