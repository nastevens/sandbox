/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: led_decoder.v
 *****/

module led_decoder (clk, reset, floor, UES, LES, IS, led_sel, led_out);

    input clk, reset, UES, LES, IS;
    input [1:0] floor;
    output [3:0] led_sel;
    output [7:0] led_out;

    reg [3:0] led_sel;
    reg [7:0] led_out;
    reg [1:0] state;

    wire floor_0 = ~(floor == 2'b00);
    wire floor_1 = ~(floor == 2'b01);
    wire floor_2 = ~(floor == 2'b10);
    wire floor_3 = ~(floor == 2'b11);
    
    wire [7:0] led_0 = {floor_0, floor_0, 1'b1, LES,  1'b1, floor_0, IS | floor_0, 1'b1};
    wire [7:0] led_1 = {floor_1, floor_1, 1'b1, 1'b0, 1'b1, floor_1, IS | floor_1, 1'b1}; 
    wire [7:0] led_2 = {floor_2, floor_2, 1'b1, 1'b0, 1'b1, floor_2, IS | floor_2, 1'b1}; 
    wire [7:0] led_3 = {floor_3, floor_3, 1'b1, UES,  1'b1, floor_3, IS | floor_3, 1'b1}; 
    
    /* Outputs the display unless reset is pushed */
    wire [7:0] reset_on = reset ? 8'b11111111 : 8'b00000000;
    always @ (posedge clk)
    begin
        state <= state + 1;
        case (state)
            0: begin led_sel <= 4'b0111; led_out <= led_0 | reset_on; end
            1: begin led_sel <= 4'b1011; led_out <= led_1 | reset_on; end
            2: begin led_sel <= 4'b1101; led_out <= led_2 | reset_on; end
            3: begin led_sel <= 4'b1110; led_out <= led_3 | reset_on; end
        endcase
    end

    /* Initial block for simulation */
    initial
    begin
        led_sel = 0;
        led_out = 0;
        state = 0;
    end

endmodule
