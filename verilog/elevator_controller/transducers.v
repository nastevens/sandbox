/*****
 * Project:  ECE333 Elevator Control Project
 * Author:   Nick Stevens
 * Contact:  nicholas.stevens@ieee.org
 * Filename: transducers.v
 *****/

module transducers (clk,
                    reset,
                    GUPB,
                    GLPB,
                    CUPB,
                    CLPB,
                    MU,
                    MD,
                    CUE,
                    CLE,
                    CI,
                    OUE,
                    OLE,
                    OI,
                    GU,
                    GL,
                    CU,
                    CL,
                    UES,
                    LES,
                    IS,
                    AU,
                    AL,
                    floor);

    /* I/O */
    input clk, reset;
    input GUPB, GLPB, CUPB, CLPB, MU, MD, CUE, CLE, CI, OUE, OLE, OI;
    output GU, GL, CU, CL, UES, LES, IS, AU, AL;
    output [1:0] floor;
    
    /* Registers */
    reg GU, GL, CU, CL, UES, LES, IS;
    reg [1:0] floor;
    reg CUE_state, OUE_state, CLE_state, OLE_state;
    reg CI_state, OI_state, MD_state, MU_state;

    always @ (posedge clk)
    begin

        if (reset)
        begin
            GU  <= 0;
            GL  <= 0;
            CU  <= 0;
            CL  <= 0;
            UES <= 0;
            LES <= 0;
            IS  <= 0;
            floor <= 2'b00;
        end

        /* Use MU and MU_state to only trigger on positive edge of MU */
        else
        begin

            if (MU & ~MU_state)
            begin
                floor <= floor + 1;
                CU <= 0;
                GU <= 0;
                MU_state <= 1;
            end
            
            else
            begin
                if (GUPB) GU <= 1; else if (floor == 2'b11) GU <= 0;
                if (CUPB & ~UES) CU <= 1; else CU <= 0;
                MU_state <= MU;
            end

            if (MD & ~MD_state)
            begin
                floor <= floor - 1;
                CL <= 0;
                GL <= 0;
                MD_state <= 1;
            end
            
            else
            begin
                if (GLPB) GL <= 1; else if (floor == 2'b00) GL <= 0;
                if (CLPB & ~LES) CL <= 1; else CL <= 0;
                MD_state <= MD;
            end
            
            /* Update door statuses, again using _state registers
             * to emulate one-shot */
            if (CUE & ~CUE_state)      begin UES <= 0; CUE_state <= 1; end
            else if (OUE & ~OUE_state) begin UES <= 1; OUE_state <= 1; end
            else begin CUE_state <= CUE; OUE_state <= OUE; end
            
            if (CLE & ~CLE_state)      begin LES <= 0; CLE_state <= 1; end
            else if (OLE & ~OLE_state) begin LES <= 1; OLE_state <= 1; end
            else begin CLE_state <= CLE; OLE_state <= OLE; end
            
            if (CI & ~CI_state)        begin IS  <= 0; CI_state  <= 1; end
            else if ( OI & ~OI_state)  begin IS  <= 1; OI_state  <= 1; end
            else begin CI_state <= CI; OI_state <= OI; end

            
        end

    end

/* Update sensors for arriving at top/bottom floor */
assign AU = floor == 2'b11;
assign AL = floor == 2'b00;

endmodule
