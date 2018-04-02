`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   15:45:18 07/30/2012
// Design Name:   bin2bcd
// Module Name:   C:/LEDDisplay/bin2bcd_tb.v
// Project Name:  LEDDisplay
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: bin2bcd
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module bin2bcd_tb;

	// Inputs
	reg [7:0] A;

	// Outputs
	wire [3:0] ONES;
	wire [3:0] TENS;
	wire [3:0] HUNDREDS;

	// Instantiate the Unit Under Test (UUT)
	bin2bcd uut (
		.A(A), 
		.ONES(ONES), 
		.TENS(TENS), 
		.HUNDREDS(HUNDREDS)
	);

	initial begin
        $display("Beginning simulation");
    
		// Initialize Inputs
		A = 0;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
        A = 8'd0;
        #100;
        A = 8'd20;
        #100;
        A = 8'd40;
        #100;
        A = 8'd128;
        #100;
        A = 8'd255;
        $finish;

	end
      
endmodule

