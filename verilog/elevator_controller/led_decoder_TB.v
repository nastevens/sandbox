/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: led_decoder_TB.v
 *****/

module  led_decoder_TB;
    
    reg clk, reset, UES, LES, IS;
    reg [1:0] floor;
    wire [3:0] led_sel;
    wire [7:0] led_out;

    /* Device under test */
    led_decoder DUT (
        .clk(clk),
        .reset(reset),
        .floor(floor),
        .UES(UES),
        .LES(LES),
        .IS(IS),
        .led_sel(led_sel),
        .led_out(led_out)
    );

    initial begin
        
        clk = 0;
        reset = 1;
        floor = 0;
        UES = 0;
        LES = 0;
        IS = 0;
        
        #10 reset = 0;

        #10 LES=1; UES=1; IS=1;
        #10 LES=0; UES=0; IS=0;
        #10 floor=1;
        #10 floor=2;
        #10 floor=3;
        #20 $finish;
    end

    always #1 clk = ~clk;

endmodule
