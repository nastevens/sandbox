`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:21:54 07/30/2012 
// Design Name: 
// Module Name:    bcd2led 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module bcd2led(
    input [3:0] BCD,
    output reg [7:0] LED
    );

    always @ (BCD)
    begin
        case(BCD)
            4'd0: LED = 8'b00000011;
            4'd1: LED = 8'b10011111;
            4'd2: LED = 8'b00100101;
            4'd3: LED = 8'b00001101;
            4'd4: LED = 8'b10011001;
            4'd5: LED = 8'b01001001;
            4'd6: LED = 8'b01000001;
            4'd7: LED = 8'b00011111;
            4'd8: LED = 8'b00000001;
            4'd9: LED = 8'b00001001;
            default: LED = 8'b11101111;
        endcase
    end

endmodule
