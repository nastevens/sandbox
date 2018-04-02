/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: control.v
 *****/

module control (clk,    /* Synchro clock */
                reset,  /* Reset signal */
                GU,     /* Go Upper */
                GL,     /* Go Lower */
                CU,     /* Call Upper */
                CL,     /* Call Lower */
                UES,    /* Upper Ext. Status */
                LES,    /* Lower Ext. Status */
                IS,     /* Internal Status */
                AU,     /* Arrived Upper */
                AL,     /* Arrived Lower */
                T,      /* Timer */
                MU,     /* Move Up */
                MD,     /* Move Down */
                CUE,    /* Close Upper External */
                CLE,    /* Close Lower External */
                CI,     /* Close Internal */
                OUE,    /* Open Upper External */
                OLE,    /* Open Lower External */
                OI,     /* Open Internal */
                KT);    /* Kick Timer */


    input  clk, reset, GU, GL, CU, CL, UES, LES, IS, AU, AL, T;
    output MU, MD, CUE, CLE, CI, OUE, OLE, OI, KT;
    reg MU, MD, CUE, CLE, CI, OUE, OLE, OI, KT;

    reg [3:0] state;

    /* State definition parameters */
    parameter   EMU=4'b0000,    /* Elevator Moving Up */
                EMD=4'b0001,    /* Elevator Moving Down */
                WLC=4'b0010,    /* Waiting at Lower, Doors Closed */
                WLO=4'b0011,    /* Waiting at Lower, Doors Open */
                WUC=4'b0100,    /* Waiting at Upper, Doors Closed */
                WUO=4'b0101,    /* Waiting at Upper, Doors Open */
                CDU=4'b0110,    /* Closing Upper Doors */
                ODU=4'b0111,    /* Opening Upper Doors */
                CDL=4'b1000,    /* Closing Lower Doors */
                ODL=4'b1001,    /* Opening Lower Doors */
                SET=4'b1010,    /* Waiting for elevator to settle */
                STA=4'b1011;    /* Waiting for elevator to start */


    always @ (posedge clk)
    begin

        if (reset)
        begin
            state <= WLC;
            MU <= 0; MD <= 0; CUE <= 0; CI <= 0; CLE <= 0;
            OUE <= 0; OLE <= 0; OI <= 0; KT <= 0;
        end

        else begin
        case (state)

        SET: begin

                if (T) begin
                    if (AU) begin
                        state <= ODU;
                        KT <= 0;
                        OUE <= 1;
                        OI <= 1;
                    end

                    else if (AL) begin
                        state <= ODL;
                        KT <= 0;
                        OLE <= 1;
                        OI <= 1;
                    end
                end

                else begin
                    KT <= 0;
                    state <= SET;
                end

             end
        
        STA: begin

                if (T & ~KT) begin
                    if (AU) begin
                        state <= EMD;
                        MD <= 1;
                        KT <= 1;
                    end

                    else if (AL) begin
                        state <= EMU;
                        MU <= 1;
                        KT <= 1;
                    end
                end

                else begin
                    KT <= 0;
                    state <= STA;
                end

             end
        
        EMU: begin

                /* If arrived at upper level kick timer to wait until
                 * elevators settles, then open doors */
                if (AU) begin
                    state <= SET;
                    KT <= 1;
                    MU <= 0;
                end

                /* If timer expires kick it and move up a level */
                else if (T) begin
                    state <= EMU;
                    MU <= 1;
                    KT <= 1;
                end
               
                else begin
                    state <= EMU;
                    KT <= 0;
                    MU <= 0;
                end

              end
             
        EMD: begin

                /* If arrived at lower level, open doors */
                if (AL) begin
                    state <= SET;
                    KT <= 1;
                    MD <= 0;
                end

                /* If timer expires kick it and move down a level */
                else if (T) begin
                    state <= EMD;
                    MD <= 1;
                    KT <= 1;
                end
               
                else begin
                    state <= EMD;
                    KT <= 0;
                    MD <= 0;
                end
                
             end
             
        WLC: begin
               
                /* If doors are still open, close them! */
                if (LES | IS) begin 
                    state <= CDL;
                    CLE <= 1;
                    CI <= 1;
                end
                
                /* Service lower calls before upper */
                else if (GL | CL) begin
                    state <= ODL;
                    OLE <= 1;
                    OI <= 1;
                end
                
                else if (GU | CU) begin
                    state <= STA;
                    KT <= 1;
                end
                
                else state <= WLC;
             
             end
             
        WLO: begin
                 
                /* If doors are closed, open them! */
                if (~LES | ~IS) begin
                    state <= ODL;
                    OLE <= 1;
                    OI <= 1;
                end

                /* Service lower call/goto buttons */
                else if (CL) begin
                    state <= WLO;
                    KT <= 1;
                end

                else if (GL) begin
                    state <= WLO;
                    KT <= 1;
                end
                
                /* If timer expires close doors */
                else if (T & ~KT) begin
                    state <= CDL;
                    CLE <= 1;
                    CI <= 1;
                end

                else begin
                    KT <= 0;
                    state <= WLO;
                end
             end
        
        CDL: begin
                    
                /* Lower level calls cancel close */
                if (GL | CL) begin
                    state <= ODL;
                    OLE <= 1;
                    OI <= 1;
                end

                /* If both doors are closed move to next state */
                else if (~LES & ~IS) begin
                    state <= WLC;
                end

                else state <= CDL;

                /* Kill signals */
                CLE <= 0;
                CI <= 0;
             end
             
        ODL: begin
            
                /* If both doors are open, move to next state */
                if (LES & IS) begin
                    state <= WLO;
                    KT <= 1;
                end

                else state <= ODL;

                /* Kill signals */
                OLE <= 0;
                OI <= 0;
             
             end
              
        WUC: begin
                
                /* If doors are still open, close them! */
                if (UES | IS) begin 
                    state <= CDU;
                    CUE <= 1;
                    CI <= 1;
                end
                
                /* Service upper calls before lower */
                else if (GU | CU) begin
                    state <= ODU;
                    OUE <= 1;
                    OI <= 1;
                end
                
                else if (GL | CL) begin
                    state <= STA;
                    KT <= 1;
                end
                
                else state <= WUC;
             
             end
             
        WUO: begin
                
                /* If doors are closed, open them! */
                if (~UES | ~IS) begin
                    state <= ODU;
                    OUE <= 1;
                    OI <= 1;
                end

                /* Service upper call/goto buttons */
                else if (CU) begin
                    state <= WUO;
                    KT <= 1;
                end

                else if (GU) begin
                    state <= WUO;
                end
                
                /* If timer expires close doors */
                else if (T & ~KT) begin
                    state <= CDU;
                    CUE <= 1;
                    CI <= 1;
                end
 
                else begin
                    KT <= 0;
                    state <= WUO;
                end

             end
             
        CDU: begin
                
                /* Upper level calls cancel close */
                if (GU | CU) begin
                    state <= ODU;
                    OUE <= 1;
                    OI <= 1;
                end

                /* If both doors are closed move to next state */
                else if (~UES & ~IS) begin
                    state <= WUC;
                end

                else state <= CDU;

                /* Kill signals */
                CUE <= 0;
                CI <= 0;
                
             end
             
        ODU: begin

                /* If both doors are open, move to next state */
                if (UES & IS) begin
                    state <= WUO;
                    KT <= 1;
                end

                else state <= ODU;

                /* Kill signals */
                OUE <= 0;
                OI <= 0;
                
             end
             
       
        endcase
        end

    end
    

endmodule
                
