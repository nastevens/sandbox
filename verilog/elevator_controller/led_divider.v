/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: led_divider.v
 *****/

module led_divider (clk, reset, led_clk);

    input clk, reset;
    output led_clk;
    reg led_clk;
    reg [15:0] div_reg;
    
    /* Divider for LED speed */
    parameter div_count = 16'd25000;
    //parameter div_count = 16'd2;

    always @ (posedge clk)
    begin
        if (reset)
        begin
            div_reg <= 0;
            led_clk <= 0;
        end
        
        else if (div_reg >= div_count)
        begin
            div_reg <= 0;
            led_clk <= ~led_clk;
        end
        
        else
        begin
            div_reg <= div_reg + 1;
        end
    end

endmodule
