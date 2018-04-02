`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:46:39 07/30/2012 
// Design Name: 
// Module Name:    LEDDisplay 
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
module LEDDisplay(
    input CLKIN,
    input RESET,
    output reg [7:0] SEG,
    output reg [3:0] SEL,
    output reg [7:0] COUNT
);

parameter period = 50000000;

localparam blank = 8'b1111_1111;

reg [25:0] ticks;
reg [1:0] led_sel;
reg [8:0] led_ticks;
reg en;

wire [3:0] ones_bcd;
wire [3:0] tens_bcd;
wire [3:0] hundreds_bcd;

wire [7:0] ones_led;
wire [7:0] tens_led;
wire [7:0] hundreds_led;

assign blank_hundreds = (hundreds_bcd == 0);
assign blank_tens = blank_hundreds & (tens_bcd == 0);



// LED select counter
always @ (posedge CLKIN)
    if (RESET)
        led_sel = 2'b0;
    else if (led_ticks == 0)
        led_sel = led_sel + 1;
    else
        led_sel = led_sel;



// Downsample clock to approx 100kHz for LEDs        
always @ (posedge CLKIN)
    if (RESET)
        led_ticks <= 9'b0;
    else
        led_ticks <= led_ticks + 1;



// Decode output based on LED select
always @ (posedge CLKIN)
    if (RESET)
        begin
        SEG <= 8'b1111_1111;
        SEL <= 4'b1111;
        end
    else
        case (led_sel)
            2'b00:  begin
                    SEG <= ones_led;
                    SEL <= 4'b1110;
                    end
            2'b01:  begin
                    SEG <= blank_tens ? blank : tens_led;
                    SEL <= 4'b1101;
                    end
            2'b10:  begin
                    SEG <= blank_hundreds ? blank : hundreds_led;
                    SEL <= 4'b1011;
                    end
            2'b11:  begin
                    SEG <= 8'b1111_1111;
                    SEL <= 4'b0111;
                    end
        endcase



// 0-255 counter
always @ (posedge CLKIN)
    if (RESET)
        COUNT <= 8'b0;
    else if (en)
        COUNT <= COUNT + 1;
    else
        COUNT <= COUNT;    



// Period counter
always @ (posedge CLKIN)
    if (RESET)
        begin
        ticks   <= 26'b0;
        en      <= 1'b0;
        end
    else if (ticks >= period)
        begin
        ticks   <= 26'b0;
        en      <= 1'b1;
        end
    else
        begin
        ticks   <= ticks + 1;
        en      <= 1'b0;
        end


bin2bcd converter (
    .A(COUNT), 
    .ONES(ones_bcd), 
    .TENS(tens_bcd), 
    .HUNDREDS(hundreds_bcd)
);

bcd2led ones_converter (
    .BCD(ones_bcd),
    .LED(ones_led)
);

bcd2led tens_converter (
    .BCD(tens_bcd),
    .LED(tens_led)
);

bcd2led hundreds_converter (
    .BCD(hundreds_bcd),
    .LED(hundreds_led)
);

endmodule


