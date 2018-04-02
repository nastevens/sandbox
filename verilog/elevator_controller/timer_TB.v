/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: timer_TB.v
 *****/

module timer_TB;

    reg clk, reset, KT;
    wire T;

    timer DUT ( .clk(clk),
                .reset(reset),
                .KT(KT),
                .T(T)
              );

    initial
    begin
        
        clk = 0;
        KT = 0;
        reset = 1;
        #5 reset = 0;
        #20 KT = 1;
        #5  KT = 0;
        #30 KT = 1;
        #30 KT = 0;
        #30 $finish;

   end

   always #1 clk = ~clk;

endmodule
