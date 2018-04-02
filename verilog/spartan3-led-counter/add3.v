`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    15:44:28 07/30/2012 
// Design Name: 
// Module Name:    add3 
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
module add3(
    input [3:0] IN,
    output reg [3:0] OUT
);

always @ (IN)
    case (IN)
        4'b0000: OUT = 4'b0000;
        4'b0001: OUT = 4'b0001;
        4'b0010: OUT = 4'b0010;
        4'b0011: OUT = 4'b0011;
        4'b0100: OUT = 4'b0100;
        4'b0101: OUT = 4'b1000;
        4'b0110: OUT = 4'b1001;
        4'b0111: OUT = 4'b1010;
        4'b1000: OUT = 4'b1011;
        4'b1001: OUT = 4'b1100;
        default: OUT = 4'b0000;
    endcase
    
endmodule
