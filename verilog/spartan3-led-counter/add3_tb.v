`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   15:55:17 07/30/2012
// Design Name:   add3
// Module Name:   C:/LEDDisplay/add3_tb.v
// Project Name:  LEDDisplay
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: add3
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module add3_tb;

	// Inputs
	reg [3:0] IN;

	// Outputs
	wire [3:0] OUT;

	// Instantiate the Unit Under Test (UUT)
	add3 uut (
		.IN(IN), 
		.OUT(OUT)
	);

	initial begin
		// Initialize Inputs
		IN = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
        IN = 4;
        
        #100;
        
        IN = 8;
        
        
        
		// Add stimulus here

	end
      
endmodule

