;*********** Header ***********************************************************
; DESC: POVClock
;       A persistance of vision analog clock
; AUTH: Justin Milks
;       Nick Stevens
; DATE: 5/9/2005
; REF:  ECE331
;*********** END Header *******************************************************


;*********** Hardware definitions *********************************************
			#include 	<p16f876.inc>
			__CONFIG	_CP_OFF & _WDT_OFF & _BODEN_OFF & _PWRTE_ON & _XT_OSC & _LVP_OFF & _CPD_OFF
			errorlevel	-302
			errorlevel	-207
;*********** END Hardware definitions *****************************************


;*********** Constant definitions *********************************************
#define		SEC_HAND_HI		B'00000000'
#define		SEC_HAND_LO		B'00001111'
#define		MIN_HAND_HI		B'00000000'
#define		MIN_HAND_LO		B'00111111'
#define		HOUR_HAND_HI	B'00000001'
#define		HOUR_HAND_LO	B'11111111'
#define		ATD_OFF			B'00000110'
#define		DIVISIONS		D'180'
;*********** END Constant definitions *****************************************


;*********** Memory definitions ***********************************************
; uC RAM locations
scratch_ram		equ			0x20
time_block		equ			0x30
				CBLOCK		time_block
					seconds
					minutes
					hours
					day
					date
					month
					year
				ENDC
random_block	equ			0x40
				CBLOCK		random_block
					disp_count_H
					disp_count_L
					burn_bits
					TMR0H
					position
					rtc_data
					rtc_addr
					setting
					cycle_count
				ENDC
div_block		equ			0x50
				CBLOCK		div_block
					count
					temp
					ACCaHI
					ACCaLO
					ACCbHI
					ACCbLO
					ACCcHI
					ACCcLO
					ACCdHI
					ACCdLO
					bcd_byte
					R0
					R1
				ENDC

; Bit settings
#define		SETTING			setting, 0

; RTC Register addresses
#define		RTC_A			0x0A
#define		RTC_B			0x0B
#define		RTC_C			0x0C
#define		RTC_D			0x0D
#define		rtc_sec			0x00
#define		rtc_min			0x02
#define		rtc_hours		0x04
#define		rtc_day			0x06
#define		rtc_date		0x07
#define		rtc_month		0x08
#define		rtc_year		0x09
;*********** END Memory definitions *******************************************


;*********** Port definitions *************************************************
; Input
#define		IR_TRIGGER		PORTB, 0
#define		RTC_IRQ			PORTB, 5
#define		SET_MIN			PORTB, 7
#define		SET_HOUR		PORTB, 6

; Output
#define		SR_DATA			PORTA, 0
#define		SR_CLK			PORTA, 1
#define		SR_RCLK			PORTA, 2
#define		RTC_ALE			PORTB, 3
#define		RTC_WR			PORTB, 2
#define		RTC_RD			PORTB, 1

; Bidirectional
#define		RTC_AD			PORTC
;*********** END Port definitions *********************************************


;*********** Macro definitions ************************************************
BANK0 MACRO
			bcf		STATUS, RP0
			bcf		STATUS, RP1
			ENDM

BANK1 MACRO
			bsf		STATUS, RP0
			bcf		STATUS, RP1
			ENDM

BANK2 MACRO
			bcf		STATUS, RP0
			bsf		STATUS, RP1
			ENDM

BANK3 MACRO
			bsf		STATUS, RP0
			bsf		STATUS, RP1
			ENDM
;*********** END Macro definitions ********************************************


;*********** Program memory start *********************************************
			org		0x00

			goto	start

			; Interrupt vector
			org		0x04
			goto	ISR
			
			; Main program start
			org		0x05

;*********** Main Program *****************************************************
start:
			; Initialize system devices
			call	init_display_timer
			call	init_trigger
			call	init_io
			call	init_sr

			; Run a power-on delay for RTC
			movlw	D'255'
			movwf	scratch_ram
			movwf	scratch_ram+1
			movlw	D'15'
			movwf	scratch_ram+2
pup_delay:
			decfsz	scratch_ram
			goto	pup_delay
			decfsz	scratch_ram+1
			goto	pup_delay
			decfsz	scratch_ram+2
			goto	pup_delay

			; Initialize RTC
			call	init_rtc
			
			; Enable interrupts
			bsf		INTCON, PEIE			; Enable per. interrupts
			bsf		INTCON, GIE				; Enable interrupts globally

main_loop:
			goto	main_loop

;*********** END Main Program *************************************************

;*********** Initialization Routines ******************************************

;**************************************
;* Initialize LED shift register
;**************************************
init_sr:
			movlw	D'16'					; Loop through 16 bits
			movwf	scratch_ram				
			bsf		SR_DATA
init_sr_loop:
			bcf		SR_CLK
			bsf		SR_CLK
			decfsz	scratch_ram
			bcf		SR_CLK
			bsf		SR_RCLK
			bcf		SR_RCLK
			return

;**************************************
;* Initialize display timer
;**************************************
init_display_timer:
			BANK1
			bcf		OPTION_REG, PS0			; |/ 
			bsf		OPTION_REG, PS1			; |  Set prescalar
			bcf		OPTION_REG, PS2			; |\
			bcf		OPTION_REG, PSA			; Use prescalar for timer0
			bcf		OPTION_REG, T0CS		; Use oscillator clock
			bsf		PIE1, TMR1IE			; Enable timer1 interrupt
			BANK0
			bcf		INTCON, T0IF			; Clear timer0 interrupt flag
			bsf		INTCON, T0IE			; Enable timer0 interrupt
			bsf		T1CON, TMR1ON			; Turn timer1 on
			bcf		T1CON, TMR1CS			; Use internal timer for timer1
			bcf		T1CON, T1OSCEN			; Turn off timer 1 oscillator
			bcf		PIR1, TMR1IF			; Clear timer1 interrupt flag
			clrf	TMR1H					; |/ Clear 16-bit timer1
			clrf	TMR1L					; |\
			return

;**************************************
;* Initialize synchro trigger
;**************************************
init_trigger:
			BANK1
			bsf		OPTION_REG, INTEDG		; Interrupt on rising edge of portB
			BANK0
			bsf		INTCON, INTE			; Enable RB0 interrupt
			return

;**************************************
;* Initialize I/O pins
;**************************************
init_io:
			BANK1
			clrf	TRISA
			movlw	B'11110001'
			movwf	TRISB
			bcf		OPTION_REG, 7			; Enable PORTB pull-ups
			clrf	TRISC
			movlw	ATD_OFF					;|/ Turn off PORTA AtD
			movwf	ADCON1					;|\
			BANK0
			return

;**************************************
;* Initialize RTC
;**************************************
init_rtc:
			bsf		RTC_WR					; Set write bit high
			bsf		RTC_RD					; Set read bit high
			bcf		RTC_ALE					; Clear ALE bit
			clrf	seconds					; Clear seconds counter

			; Turn on oscillator
			movlw	RTC_A					; RTC register A
			movwf	rtc_addr				; Put address in register
			movlw	B'00110000'				; Turn on oscillator
			movwf	rtc_data				; Put data in register
			call	write_rtc				; Write to RTC

			movlw	0x4B
			movwf	rtc_addr
			movlw	B'01100000'
			movwf	rtc_data
			call	write_rtc

			movlw	RTC_A
			movwf	rtc_addr
			movlw	B'00100000'
			movwf	rtc_data
			call	write_rtc

			; Set up to interrupt every second
			movlw	RTC_B					; RTC register B address
			movwf	rtc_addr				; Put address in register
			movlw	B'00000100'				; Register B init
			movwf	rtc_data				; Put data in register
			call	write_rtc				; Write data to RTC

			; Make sure flags are clear
			movlw	RTC_C
			movwf	rtc_addr
			call	read_rtc				; Reading from RTC flags clears



			; Set seconds to 0
;			movlw	RTC_B
;			movwf	rtc_addr
;			movlw	B'00001100'				; Set to binary value mode
;			movwf	rtc_data
;			call	write_rtc

			; Set seconds to 15
			movlw	rtc_sec
			movwf	rtc_addr
			movlw	D'15'
			movwf	rtc_data
			movwf	seconds
			call	write_rtc

			; Set minutes to 45
			movlw	rtc_min
			movwf	rtc_addr
			movlw	D'30'
			movwf	rtc_data
			movwf	minutes
			call	write_rtc

			; Set hours to 2
			movlw	rtc_hours
			movwf	rtc_addr
			movlw	D'9'
			movwf	rtc_data
			movwf	hours
			call	write_rtc

			; Enable port change interrupt on PIC
			bcf		INTCON, RBIF			; Clear PORTB int flag
;			bsf		INTCON, RBIE			; Enable interrupt on PB change			

			return

;**************************************
;* Initialize display so that it shows
;* current set value while being set
;**************************************
init_set_delay:
			

;*********** END Initialization Routines **************************************

;*********** RTC Routines *****************************************************

;**************************************
;* Write RTC
;* Writes a byte in rtc_data to register
;* in rtc_addr on the RTC
;**************************************
write_rtc:
			BANK1
			clrf	RTC_AD					; Make sure port is outputs
			BANK0
			bsf		RTC_ALE					; Raise ALE
			movfw	rtc_addr				; RTC address
			movwf	RTC_AD					; Put address on bus
			nop
			nop
			bcf		RTC_ALE					; Lower address line
			bcf		RTC_WR					; Lower write line
			movfw	rtc_data				; RTC Data
			movwf	RTC_AD					; Move data to bus
			nop
			nop
			bsf		RTC_WR					; Load data into register
			return

;**************************************
;* Read RTC
;* Reads byte at rtc_addr and stores it
;* into rtc_data
;**************************************
read_rtc:
			BANK1
			clrf	RTC_AD					; Check output mode
			BANK0

			bsf		RTC_ALE					; Raise ALE
			movfw	rtc_addr				; RTC address
			movwf	RTC_AD					; Put address on bus
			nop
			nop
			bcf		RTC_ALE					; Lower address line

			BANK1
			clrf	RTC_AD					; Set to all inputs
			comf	RTC_AD
			BANK0

			bcf		RTC_RD					; Lower read line
			clrf	rtc_data				; TEMP
			nop
			nop
			movfw	RTC_AD					; Get data from line
			movwf	rtc_data				; Store data
			nop
			nop
			bsf		RTC_RD					; Raise read line

			BANK1
			clrf	RTC_AD					; Set back to outputs
			BANK0

			return

;*********** END RTC Routines *************************************************

;*********** Interrupt Service Routines ***************************************
ISR:
			btfsc	SETTING
			goto	exit_isr
			btfsc	INTCON, T0IF			; Timer 0 overflowed
			call	ISR_timer0
			btfsc	PIR1, TMR1IF			; Timer 1 overflowed
			call	ISR_timer1
exit_isr:
			btfsc	INTCON, RBIF			; PORTB change
			call	ISR_portb
			btfsc	INTCON, INTF			; Check for trigger interrupt
			call	ISR_trigger
			retfie

;**************************************
;* ISR Timer 0
;* Keeps track of time for 1 rev
;**************************************
ISR_timer0:
			bcf		INTCON, T0IF			; Clear interrupt flag
			incf	TMR0H, F				; Increase high byte
			return

;**************************************
;* ISR Timer 1
;* Times interval between displays
;**************************************
ISR_timer1:

			movfw	disp_count_L			; |/
			movwf	TMR1L					; | Load 16-bit -counter with
			movfw	disp_count_H			; | delay for display
			movwf	TMR1H					; |\

			bcf		PIR1, TMR1IF			; Clear interrupt flag

			; ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			; Display time around clock
			; ========================================
			decf	position, F				; Decrement the current position
			clrf	scratch_ram
			clrf	scratch_ram+1
			comf	scratch_ram+1, F
			clrf	scratch_ram+2
			comf	scratch_ram+2, F

			movlw	0
			xorwf	position, W
			btfsc	STATUS, Z
			bcf		scratch_ram+2, 1

			movlw	DIVISIONS/4
			xorwf	position, W
			btfsc	STATUS, Z
			bcf		scratch_ram+2, 1

			movlw	2*DIVISIONS/4
			xorwf	position, W
			btfsc	STATUS, Z
			bcf		scratch_ram+2, 1

			movlw	3*DIVISIONS/4
			xorwf	position, W
			btfsc	STATUS, Z
			bcf		scratch_ram+2, 1

disp_seconds:
			movfw	seconds					; Get the current seconds count
			addwf	seconds, W
			addwf	seconds, W
			xorwf	position, W				; Compare seconds and position
			btfss	STATUS, Z				; Skip if they weren't equal
			goto	disp_minutes			; ... and go to minutes
			movlw	SEC_HAND_HI				; |/
			andwf	scratch_ram+1, F		; | Mask output with seconds
			movlw	SEC_HAND_LO				; | hand
			andwf	scratch_ram+2, F		; |\

disp_minutes:
			movfw	minutes					; Get the current minutes count
			addwf	minutes, W
			addwf	minutes, W
			xorwf	position, W				; Compare minutes and position
			btfss	STATUS, Z				; Skip if they weren't equal
			goto	disp_hours				; ... and go to hours
			movlw	MIN_HAND_HI				; |/
			andwf	scratch_ram+1, F		; | Mask output with minutes
			movlw	MIN_HAND_LO				; | hand
			andwf	scratch_ram+2, F		; |\

disp_hours:
			movfw	hours					; Get the current hour count
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			addwf	hours, W
			xorwf	position, W				; Compare hour and position
			btfss	STATUS, Z				; Skip if they weren't equal
			goto	no_hours				; ... and go to no_hours
			movlw	HOUR_HAND_HI			; |/
			andwf	scratch_ram+1, F		; | Mask output with hour
			movlw	HOUR_HAND_LO			; | hand
			andwf	scratch_ram+2, F		; |\

no_hours:
			movlw	D'16'
			movwf	scratch_ram+3
sr_loop:
			bcf		SR_DATA
			btfsc	scratch_ram+2, 0
			bsf		SR_DATA
			bsf		SR_CLK
			bcf		SR_CLK
			rrf		scratch_ram+1, F
			rrf		scratch_ram+2, F
			decfsz	scratch_ram+3
			goto	sr_loop
			bsf		SR_RCLK
			bcf		SR_RCLK


			return

;**************************************
;* ISR Trigger
;* Takes action when revolution trigger
;* is tripped
;**************************************
ISR_trigger:

			movfw	TMR0H					; Get high byte of timer 0
			movwf	scratch_ram+1			; Store in RAM
			movfw	TMR0					; Get low byte of timer 0
			movwf	scratch_ram+2			; Store in RAM
			bcf		INTCON, INTF			; Clear trigger interrupt flag
			bcf		SETTING

;			movlw	D'10'
;			movwf	scratch_ram+3
;			movwf	scratch_ram+4
;debounce_delay:
;			decfsz	scratch_ram+3
;			goto	debounce_delay
;			decfsz	scratch_ram+4
;			goto	debounce_delay
			
			clrf	TMR0H					; |/ Clear timer 0 registers
			clrf	TMR0					; |\

			; Divide by number of DIVISIONS
			movlw	DIVISIONS
			movwf	ACCaLO
			clrf	ACCaHI
			movfw	scratch_ram+2
			movwf	ACCbLO
			movfw	scratch_ram+1
			movwf	ACCbHI
			call	divide

			; Multiply by prescalar value
			movlw	D'3'					; Number of multiply loops
			movwf	scratch_ram				; Store in RAM
mult_loop:
			bcf		STATUS, C				; Clear carry bit
			rlf		ACCbLO, F				; Shift low byte left
			rlf		ACCbHI, F				; Shift high byte left
			decfsz	scratch_ram, F
			goto	mult_loop				; Loop			

			; Value obtained above is number of cycles to wait between
			; switching values on the clock.  Subtracting this value from
			; 0xFFFF and storing in the 16-bit timer will trigger display
			; changes
			movfw	ACCbLO					; |/
			sublw	0xFF					; |  Subtract low byte from 0xFF
			movwf	disp_count_L			; |\
			movfw	ACCbHI					; |/
			sublw	0xFF					; |  Subtract high bytes from 0xFF
			movwf	disp_count_H			; |\


noupdate:
			; Reset display timer with new values
			movfw	disp_count_L
			movwf	TMR1L
			movfw	disp_count_H
			movwf	TMR1H

			; Since there will likely be a remainder of division,
			; we need to "burn" the remainder from the division
			movfw	ACCcLO
			movwf	burn_bits  
			
			incf	cycle_count
			movlw	D'10'
			xorwf	cycle_count, W
			btfss	STATUS, Z
			goto	not_next_second
			clrf	cycle_count	
			incf	seconds
			movlw	D'60'
			xorwf	seconds, W
			btfss	STATUS, Z
			goto	not_next_second
			clrf	seconds
			incf	minutes

			; ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			; TEMP - Get time from RTC on every cycle
			; ========================================
;			movlw	D'15'
;			movwf	hours
;			movlw	D'30'
;			movwf	minutes
;			movlw	D'45'
;			movwf	seconds

;			movlw	RTC_A
;			movwf	rtc_addr
;			call	read_rtc
;			btfsc	rtc_data, 7
;			goto	not_next_second
;
;			movlw	rtc_sec
;			movwf	rtc_addr
;			call	read_rtc
;			movfw	rtc_data
;			movwf	seconds

;			movlw	rtc_min
;			movwf	rtc_addr
;			call	read_rtc
;			movfw	rtc_data
;			movwf	minutes
;
;			movlw	rtc_hours
;			movwf	rtc_addr
;			call	read_rtc
;			movfw	rtc_data
;			movwf	hours
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F
;			addwf	hours, F

;			movlw	0x01
;			movwf	rtc_addr
;			call	write_rtc	

not_next_second:
			movlw	DIVISIONS-1
			movwf	position
			call	ISR_timer1

			return
			
;**************************************
;* ISR PORTB
;* Takes action when a change occurs
;* on PORTB[4:7]
;**************************************
ISR_portb:
			; TEMP TEMP TEMP TEMP TEMP
;			bcf		INTCON, INTE
;			BANK1
;			bcf		PIE1, TMR1IE
;			BANK0

			movlw	D'255'
			movwf	scratch_ram
			movwf	scratch_ram+1
debounce:
			decfsz	scratch_ram
			goto	debounce
			decfsz	scratch_ram+1
			goto	debounce

			; Enter/reset set mode, where the current
			; time will remain displayed on the output
			; for 2 seconds
			; TODO

			btfss	SET_MIN
			call	set_minutes
			btfss	SET_HOUR
			call	set_hours
			movfw	PORTB
			bcf		INTCON, RBIF
			return			


;**************************************
;* ISR set
;* Sets the clock when one of the set
;* buttons is pressed
;**************************************
set_minutes:
			bsf		SETTING

			incf	minutes, F
			movlw	D'60'
			xorwf	minutes, W
			btfsc	STATUS, Z
			clrf	minutes
			movlw	rtc_min
			movwf	rtc_addr
			movfw	minutes
			movwf	rtc_data
			call	write_rtc

			; Convert the numbers to BCD and show on LEDs
			movfw	minutes
			movwf	bcd_byte
			call	bin2bcd
			
			; Convert BCD to "linecode"
			movlw	0xF0
			andwf	R1, W
			movwf	scratch_ram
			swapf	scratch_ram, F
			movlw	0x0F
			andwf	R1, W
			movwf	scratch_ram+1

			movlw	D'5'
			movwf	count
lc_loop8:			
			bsf		STATUS, C
			movf	scratch_ram, F
			btfsc	STATUS, Z
			goto	at_zero
			decf	scratch_ram, F
			bcf		STATUS, C
at_zero:
			rlf		scratch_ram+3
			rlf		scratch_ram+2
			decfsz	count
			goto	lc_loop8

			movlw	D'9'
			movwf	count
lc_loop82:			
			bsf		STATUS, C
			movf	scratch_ram+1, F
			btfsc	STATUS, Z
			goto	at_zero2
			decf	scratch_ram+1, F
			bcf		STATUS, C
at_zero2:
			rlf		scratch_ram+3
			rlf		scratch_ram+2
			decfsz	count
			goto	lc_loop82

			movlw	D'2'
			movwf	count
loop_twice:
			bsf		STATUS, C
			rlf		scratch_ram+3
			rlf		scratch_ram+2
			decfsz	count
			goto	loop_twice
		

			movlw	D'16'
			movwf	count
sr_lc_loop:
			bcf		SR_DATA
			btfsc	scratch_ram+3, 0
			bsf		SR_DATA
			bsf		SR_CLK
			bcf		SR_CLK
			rrf		scratch_ram+2, F
			rrf		scratch_ram+3, F
			decfsz	count
			goto	sr_lc_loop
			bsf		SR_RCLK
			bcf		SR_RCLK
			
			return
			
set_hours:

			bsf		SETTING

			incf	hours, F
			movlw	D'13'
			xorwf	hours, W
			movlw	D'1'
			btfsc	STATUS, Z
			movwf	hours
			movlw	rtc_hours
			movwf	rtc_addr
			movfw	hours
			movwf	rtc_data
			call	write_rtc
		
			; Convert number to "linecode"
			movfw	hours
			movwf	scratch_ram

			movlw	D'12'
			movwf	count
lc_loop12:			
			bsf		STATUS, C
			movf	scratch_ram, F
			btfsc	STATUS, Z
			goto	at_zero3
			decf	scratch_ram, F
			bcf		STATUS, C
at_zero3:
			rlf		scratch_ram+3
			rlf		scratch_ram+2
			decfsz	count
			goto	lc_loop12


			movlw	D'4'
			movwf	count
loop_four:
			bsf		STATUS, C
			rlf		scratch_ram+3
			rlf		scratch_ram+2
			decfsz	count
			goto	loop_four
		

			movlw	D'16'
			movwf	count
sr_lc_loop2:
			bcf		SR_DATA
			btfsc	scratch_ram+3, 0
			bsf		SR_DATA
			bsf		SR_CLK
			bcf		SR_CLK
			rrf		scratch_ram+2, F
			rrf		scratch_ram+3, F
			decfsz	count
			goto	sr_lc_loop2
			bsf		SR_RCLK
			bcf		SR_RCLK
			
			return


exit_set:
			return



;*********** END Interrupt Service Routines ***********************************

;******************************************************************************
;                Double Precision Division from Microchip App Notes
;******************************************************************************
;   Division : ACCb(16 bits) / ACCa(16 bits) -> ACCb(16 bits) with
;                                               Remainder in ACCc (16 bits)
;      (a) Load the Denominator in location ACCaHI & ACCaLO ( 16 bits )
;      (b) Load the Numerator in location ACCbHI & ACCbLO ( 16 bits )
;      (c) CALL D_div
;      (d) The 16 bit result is in location ACCbHI & ACCbLO
;      (e) The 16 bit Remainder is in locations ACCcHI & ACCcLO
;
;   Performance :
;               Program Memory  :       037
;               Clock Cycles    :       310
;
;        NOTE :
;               The performance specs are for Unsigned arithmetic ( i.e,
;               with "SIGNED equ  FALSE ").
;
;
;       Program:          DBL_DIVS.ASM 
;       Revision Date:   
;                         1-13-97      Compatibility with MPASMWIN 1.40
;
;*******************************************************************;
divide:
			call	setup
			clrf	ACCcHI
			clrf	ACCcLO
dloop:
			bcf		STATUS,C
			rlf		ACCdLO, F
			rlf		ACCdHI, F
			rlf		ACCcLO, F
			rlf		ACCcHI, F
			movf	ACCaHI,W
			subwf	ACCcHI,W          ;check if a>c
			btfss	STATUS,Z
			goto	nochk
			movf	ACCaLO,W
			subwf	ACCcLO,W        ;if msb equal then check lsb
nochk:
			btfss	STATUS,C    ;carry set if c>a
			goto	nogo
			movf	ACCaLO,W        ;c-a into c
			subwf	ACCcLO, F
			btfss	STATUS,C
			decf	ACCcHI, F
			movf	ACCaHI,W
			subwf	ACCcHI, F
			bsf		STATUS,C    ;shift a 1 into b (result)
nogo:
		    rlf		ACCbLO, F
			rlf		ACCbHI, F
			decfsz	temp, F         ;loop untill all bits checked
			goto	dloop

			return

;*******************************************************************
;
setup:
			movlw	.16             ; for 16 shifts
			movwf	temp
			movf	ACCbHI,W          ;move ACCb to ACCd
			movwf	ACCdHI
			movf	ACCbLO,W
			movwf	ACCdLO
			clrf	ACCbHI
			clrf	ACCbLO
			return

;********************************************************************
;                  Binary To BCD Conversion Routine
; The 8 bit binary number is input in location bcd_byte
; The 3 digit BCD number is returned in R0 and R1 with R0
; containing the MSD in its right most nibble.
;
;       Program:          B16TOBCD.ASM 
;       Revision Date:   
;                         1-13-97      Compatibility with MPASMWIN 1.40
;
;*******************************************************************;
bin2bcd:
			bcf		STATUS,0                ; clear the carry bit
			movlw	.8
			movwf	count
			clrf	R0
			clrf	R1

loop8:
			rlf		bcd_byte, F
			rlf		R1, F
			rlf		R0, F

			decfsz	count, F
			goto	adjDEC
			return

adjDEC:
			movlw	R1
			movwf	FSR
			call	adjBCD

			movlw	R0
			movwf	FSR
			call	adjBCD

			goto    loop8

adjBCD:
			movlw	0x03
			addwf	INDF, W
			movwf	temp
			btfsc	temp, 3          ; test if result > 7
			movwf	INDF
			movlw   0x30
			addwf	INDF, W
			movwf	temp
			btfsc   temp, 7          ; test if result > 7
			movwf	INDF               ; save as MSD
			return

			END
