/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: top_level.v
 *****/

module top_level (clk, GUPB, GLPB, CUPB, CLPB, reset, led_sel, led_out);

    input clk, GUPB, GLPB, CUPB, CLPB, reset;
    output [3:0] led_sel;
    output [7:0] led_out;

    wire sigGU, sigGL, sigCU, sigCL, sigUES, sigLES, sigIS; 
    wire sigAU, sigAL, sigMU, sigMD, sigCUE, sigCLE, sigCI;
    wire sigOUE, sigOLE, sigOI, sigKT, sigLEDClk;
    wire [1:0] sigfloor;

    control main_control (.clk(clk),    .GU(sigGU),   .GL(sigGL),   
                          .CU(sigCU),   .CL(sigCL),   .UES(sigUES),
                          .LES(sigLES), .IS(sigIS),   .AU(sigAU),
                          .AL(sigAL),   .T(sigT),     .MU(sigMU),
                          .MD(sigMD),   .CUE(sigCUE), .CLE(sigCLE),
                          .CI(sigCI),   .OUE(sigOUE), .OLE(sigOLE),
                          .OI(sigOI),   .KT(sigKT),   .reset(reset));
    
    timer main_timer (.clk(clk), .reset(reset), .KT(sigKT), .T(sigT));
    
    transducers main_transducers (.GUPB(GUPB),  .GLPB(GLPB),  .CUPB(CUPB),
                                  .CLPB(CLPB),  .MU(sigMU),   .MD(sigMD),
                                  .CUE(sigCUE), .CLE(sigCLE), .CI(sigCI),
                                  .OUE(sigOUE), .OLE(sigOLE), .OI(sigOI),
                                  .GU(sigGU),   .GL(sigGL),   .CU(sigCU),
                                  .CL(sigCL),   .UES(sigUES), .LES(sigLES),
                                  .IS(sigIS),   .AU(sigAU),   .AL(sigAL),
                                  .floor(sigfloor), .reset(reset), .clk(clk));

     led_divider main_divider (.clk(clk), .reset(reset), .led_clk(sigLEDClk));

     led_decoder main_decoder (.clk(sigLEDClk), .reset(reset), .floor(sigfloor),
                               .UES(sigUES),    .LES(sigLES),  .IS(sigIS),
                               .led_sel(led_sel), .led_out(led_out));

endmodule
