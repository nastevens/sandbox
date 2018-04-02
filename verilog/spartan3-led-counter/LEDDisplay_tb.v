`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   16:11:31 07/30/2012
// Design Name:   LEDDisplay
// Module Name:   C:/LEDDisplay/LEDDisplay_tb.v
// Project Name:  LEDDisplay
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: LEDDisplay
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module LEDDisplay_tb;

	// Inputs
	reg CLKIN;
	reg RESET;

	// Outputs
	wire [7:0] SEG;
	wire [3:0] SEL;
	wire [7:0] COUNT;

	// Instantiate the Unit Under Test (UUT)
	LEDDisplay #(10)
    uut (
		.CLKIN(CLKIN), 
		.RESET(RESET), 
		.SEG(SEG), 
		.SEL(SEL), 
		.COUNT(COUNT)
	);

    always #1 CLKIN = ~CLKIN;

	initial begin
		// Initialize Inputs
		CLKIN = 0;
		RESET = 1;

		// Wait 100 ns for global reset to finish
		#100;
        
		// Add stimulus here
        
        RESET = 0;
        #500;
        $finish;

	end
      
endmodule

