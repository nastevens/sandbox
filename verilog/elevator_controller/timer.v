/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: timer.v
 *****/

module timer (clk, reset, KT, T);

    input clk, reset, KT;
    output T;
    reg T, running;
    reg [27:0] timer_reg;

    parameter timer_count = 28'd50000000;
    //parameter timer_count = 28'd8;

    always @ (posedge clk)
    begin
        
        if (reset)
        begin
            running <= 0;
            timer_reg <= 0;
            T <= 0;
        end

        /* If timer has reached the high count value, reset */
        else if (timer_reg >= timer_count)
        begin
            running <= 0;
            timer_reg <= KT ? timer_reg : 0;
            T <= 1;
        end        

        /* If Kick Timer is active, start counting 
         * Uses trinary to ignore KT if it stays high,
         * since we are only going to trigger on the positive edge */
        else if (KT)
        begin
            running <= 1;
            timer_reg <= running ? timer_reg + 1 : timer_reg;
            T <= 0;
        end
        
        /* If running, increment */
        else timer_reg <= running ? timer_reg + 1 : timer_reg;
            
    end

endmodule
