;*********** Header ***********************************************************
; DESC: POVClock
;       A persistance of vision analog clock
; AUTH: Justin Milks
;       Nick Stevens
; DATE: 5/9/2005
; REF:  ECE331
;
;*********** END Header *******************************************************

;*********** Hardware definitions *********************************************
			#include 	<p16f876.inc>
			__CONFIG	_CP_OFF & _WDT_OFF & _BODEN_OFF & _PWRTE_ON & _XT_OSC & _LVP_OFF & _CPD_OFF
;*********** END Hardware definitions *****************************************

;*********** Constant definitions *********************************************
#define		FOSC			13500000
#define		FCLK			FOSC / 4
#define		AVG_RPM			30*60
#define		PS_MASK			B'11111000'
#define		DIVIDE_BY_COUNT	6
#define		BURN_MASK		B'00111111'
#define		RTC_A			0x0A
#define		RTC_B			0x0B
#define		RTC_C			0x0C
#define		RTC_D			0x0D
#define		RTC_sec			0x00
;*********** END Constant definitions *****************************************


;*********** Memory definitions ***********************************************
scratch_ram		equ			0x20
burn_bits		equ			0x30
disp_count_H	equ			0x31
disp_count_L	equ			0x32
TMR0H			equ			0x33
tmp_timer		equ			0x34
seconds			equ			0x35
w_bak			equ			0x36
position		equ			0x37
rtc_data		equ			0x38
rtc_addr		equ			0x39
;*********** END Memory definitions *******************************************


;*********** Port definitions *************************************************
; Input
#define		IR_trigger		PORTX, 0
#define		IR_set			PORTX, 0

; Output
#define		LED_sr			PORTX, 0
#define		RTC_ALE			PORTA, 0
#define		RTC_WR			PORTA, 1
#define		RTC_RD			PORTA, 2
#define		RTC_IRQ			PORTB, 7
#define		RTC_AD			PORTC

; Bidirectional
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
start:
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

			call	init_display_timer
			call	init_trigger
			call	init_io
			call	init_rtc
			bsf		INTCON, PEIE			; Enable per. interrupts
			bsf		INTCON, GIE				; Enable interrupts globally
main_loop:
			goto	main_loop

init_display_timer:
			BANK1
			bsf		OPTION_REG, PS0			; |/ 
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

init_trigger:
			BANK1
			bsf		OPTION_REG, INTEDG		; Interrupt on rising edge of portB
			BANK0
			bsf		INTCON, INTE			; Enable RB0 interrupt
			return

init_io:
			BANK1
			movlw	B'11110001'
			movwf	TRISB
			clrf	TRISA
			clrf	TRISC
			movlw	B'00000110'				; Turn off PORTA AtD
			movwf	ADCON1
			BANK0
			movlw	D'6'
			movwf	tmp_timer
			clrf	seconds
			return

init_rtc:
			BANK1
			clrf	RTC_AD					; Set RTC port to outputs
			bcf		RTC_WR					; Write bit output
			bcf		RTC_RD					; Read bit output
			bcf		RTC_ALE					; ALE bit output
			BANK0
			bsf		RTC_WR					; Set write bit high
			bsf		RTC_RD					; Set read bit high
			bcf		RTC_ALE					; Clear ALE bit

			; Turn on oscillator, set bank
			movlw	RTC_A
			movwf	rtc_addr
			movlw	B'00110000'
			movwf	rtc_data
			call	write_rtc

			movlw	0x4B
			movwf	rtc_addr
			movlw	B'00000000'
			movwf	rtc_data
			call	write_rtc

			movlw	RTC_A
			movwf	rtc_addr
			movlw	B'00100011'
			movwf	rtc_data
			call	write_rtc

			; Set up to interrupt every second
			movlw	RTC_B					; RTC register B address
			movwf	rtc_addr				; Put address in register
			movlw	B'10001100'				; Register B init
			movwf	rtc_data				; Put data in register
			call	write_rtc				; Write data to RTC

			; Make sure flags are clear
			movlw	RTC_C
			movwf	rtc_addr
			call	read_rtc

			; Set seconds to same thing
			movlw	RTC_sec
			movwf	rtc_addr
			call	read_rtc

			movlw	RTC_sec
			movwf	rtc_addr
			call	write_rtc	

			; Set seconds to 0
			movlw	0x01
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x02
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x03
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x04
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x05
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x06
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x07
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x08
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc
			; Set seconds to 0
			movlw	0x09
			movwf	rtc_addr
			movlw	0x01
			movwf	rtc_data
			call	write_rtc

			; Set seconds to 0
			movlw	RTC_B
			movwf	rtc_addr
			movlw	B'00001100'
			movwf	rtc_data
			call	write_rtc

			; Enable port change interrupt on PIC
			BANK1
			bcf		OPTION_REG, 7		; Enable PORTB pull-ups
			BANK0
			bcf		INTCON, RBIF			; Clear PORTB int flag
			bsf		INTCON, RBIE			; Enable interrupt on PB change			

			return


write_rtc:
			BANK1
			clrf	RTC_AD
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

read_rtc:
			BANK1
			clrf	RTC_AD
			BANK0
			bsf		RTC_ALE					; Raise ALE
			movfw	rtc_addr				; RTC address
			movwf	RTC_AD					; Put address on bus
			nop
			nop
			bcf		RTC_ALE					; Lower address line
			BANK1
			movlw	0xFF
			movwf	RTC_AD
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
			clrf	RTC_AD
			BANK0
			return

;*********** Interrupt Service Routines ***************************************

ISR:
			btfsc	INTCON, INTF			; Check for trigger interrupt
			call	ISR_trigger
			btfsc	INTCON, T0IF			; Timer 0 overflowed
			call	ISR_timer0
			btfsc	PIR1, TMR1IF			; Timer 1 overflowed
			call	ISR_timer1
			btfsc	INTCON, RBIF			; PORTB change
			call	ISR_portb
			retfie

; Timer 0 - Tracks the time for one revolution
ISR_timer0:
			bcf		INTCON, T0IF			; Clear interrupt flag
			incf	TMR0H, F				; Increase high byte
			return

; TEMP TABLE
temp_table:
			addwf	PCL
			retlw	B'00000001'
			retlw	B'00000010'
			retlw	B'00000100'
			retlw	B'00001000'
			retlw	B'00010000'
			retlw	B'00100000'
			retlw	B'01000000'
			retlw	B'10000000'


; Timer 1 - Times the intervals between displays
ISR_timer1:
			decf	position, F				; Decrement the current position

;			movlw	B'00000111'
;			andwf	position, W
;			call	temp_table
;			movwf	scratch_ram+1
;			andwf	seconds, W
;			xorwf	scratch_ram+1, W
;			btfsc	STATUS, Z
;			goto	light_off
;			bsf		PORTB, 1
;			goto	continue
;light_off:	bcf		PORTB, 1

			movfw	seconds					; Get the current seconds count
			xorwf	position, W				; Compare seconds and position
			btfss	STATUS, Z				; Skip if they were equal
			goto	light_off				; If not equal turn light off
			bsf		PORTB, 1				; If equal turn light on
			goto	continue

light_off:	bcf		PORTB, 1				; Turn light off

continue:			
			movfw	disp_count_L			; |/
			movwf	TMR1L					; | Load 16-bit -counter with
			movfw	disp_count_H			; | delay for display
			movwf	TMR1H					; |\

			bcf		PIR1, TMR1IF			; Clear interrupt flag

			return

ISR_trigger:
			movfw	TMR0H					; Get high byte of timer 0
			movwf	scratch_ram+1			; Store in RAM
			movfw	TMR0					; Get low byte of timer 0
			movwf	scratch_ram+2			; Store in RAM
			
			clrf	TMR0H					; |/ Clear timer 0 registers
			clrf	TMR0					; |\

			; Divide by 64, multiply by 16 = divide by 4 = >> 2
			movlw	D'2'					; Number of divide loops
			movwf	scratch_ram				; Store in RAM
div_loop:
			bcf		STATUS, C				; Clear carry bit
			rrf		scratch_ram+1, F		; Shift high byte right
			rrf		scratch_ram+2, F		; Shift low byte right
			decfsz	scratch_ram, F
			goto	div_loop				; Loop

			; Value obtained above is number of cycles to wait between
			; switching values on the clock.  Subtracting this value from
			; 0xFFFF and storing in the 16-bit timer will trigger display
			; changes
			movfw	scratch_ram+2			; |/
			sublw	0xFF					; |  Subtract low byte from 0xFF
			movwf	disp_count_L			; |\
			movfw	scratch_ram+1			; |/
			sublw	0xFF					; |  Subtract high bytes from 0xFF
			movwf	disp_count_H			; |\

			; Reset display timer with new values
			movfw	disp_count_L
			movwf	TMR1L
			movfw	disp_count_H
			movwf	TMR1H

			; Update temp display
;			decfsz	tmp_timer, F
;			goto	not_next_second
			
;			incf	seconds, F
;			movlw	D'6'
;			movwf	tmp_timer
;			btfsc	seconds, 6
;			clrf	seconds

			; Get seconds from RTC
			movlw	RTC_A
			movwf	rtc_addr
			call	read_rtc
			btfsc	rtc_data, 7
			goto	not_next_second

;			decfsz	scratch_ram+12
;			goto	not_next_second
			movlw	0x00
			movwf	rtc_addr
			call	read_rtc
			movfw	rtc_data
			movwf	seconds	

			movlw	0x01
			movwf	rtc_addr
			call	write_rtc

;			movlw	D'5'
;			movwf	scratch_ram+12

not_next_second:
			movlw	D'60'
			movwf	position
			bcf		INTCON, INTF			; Clear trigger interrupt flag

			return
			

; Interrupts when RTC triggers
ISR_portb:
;			movlw	RTC_C
;			movwf	rtc_addr
;			call	read_rtc
;			incf	seconds, F
;			movlw	D'60'
;			subwf	seconds, W
;			btfsc	STATUS, Z
;			clrf	seconds
			bcf		INTCON, RBIF
			return			

;*********** END Interrupt Service Routines ***********************************

			END
