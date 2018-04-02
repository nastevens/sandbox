/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: transducers_TB.v
 *****/

module transducers_TB;

    reg clk, reset, GUPB, GLPB, CUPB, CLPB, MU, MD, CUE, CLE, CI, OUE, OLE, OI;
    wire GU, GL, CU, CL, UES, LES, IS, AU, AL;
    wire [1:0] floor;

    transducers DUT (.clk(clk),
                     .reset(reset),
                     .GUPB(GUPB),
                     .GLPB(GLPB),
                     .CUPB(CUPB),
                     .CLPB(CLPB),
                     .MU(MU),
                     .MD(MD),
                     .CUE(CUE),
                     .CLE(CLE),
                     .CI(CI),
                     .OUE(OUE),
                     .OLE(OLE),
                     .OI(OI),
                     .GU(GU),
                     .GL(GL),
                     .CU(CU),
                     .CL(CL),
                     .UES(UES),
                     .LES(LES),
                     .IS(IS),
                     .AU(AU),
                     .AL(AL),
                     .floor(floor));


    initial
    begin
        
        reset = 1;
        clk = 0;
        GUPB = 0; GLPB = 0; CUPB = 0; CLPB = 0;
        MU = 0; MD = 0;
        CUE = 0; CLE = 0; CI = 0;
        OUE = 0; OLE = 0; OI = 0;
        
        #5 reset = 0;

        #5 MU = 1;
        #10 MU = 0;
        #5 MU = 1;
        #5 MU = 0;
        #10 MU = 1;
        #5 MU = 0;

        #5 MD = 1;
        #5 MD = 0;
        #5 MD = 1;
        #5 MD = 0;
        #5 MD = 1;
        #5 MD = 0;

        #5 OUE = 1; OLE = 1; OI  = 1;
        #20 OUE = 0;
        #5 OLE = 0;
        #5 OI = 0;

        #20 CLE = 1; CUE = 1; CI = 1;
        #10 OLE = 1; OUE = 1; OI = 1;
        #20 CLE = 0; CUE = 0; CI = 0;
            OLE = 0; OUE = 0; OI = 0;
        
        #25 $finish;
        

    end

    always #1 clk = ~clk;

endmodule
