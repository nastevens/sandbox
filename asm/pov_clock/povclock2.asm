;******************************************************************************
; DESC: POVClock
;       A persistance of vision analog clock
; AUTH: Justin Milks
;       Nick Stevens
; DATE: 5/9/2005
; REF:  ECE331
;
; Hardware specifications:
; 
;******************************************************************************
			#include <p16f876.inc>


;*********** Constant definitions *********************************************
#define		FOSC			13500000
#define		FCLK			FOSC / 4
#define		AVG_RPM			30*60
#define		PS_MASK			B'11111000'
#define		DIVIDE_BY_COUNT	6
#define		BURN_MASK		B'00111111'
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
;*********** END Memory definitions *******************************************


;*********** Port definitions *************************************************
; Input
#define		IR_trigger		PORTX, 0
#define		IR_set			PORTX, 0

; Output
#define		LED_sr			PORTX, 0
#define		RTC_ALE			PORTX, 0
#define		RTC_CS			PORTX, 0
#define		RTC_WR			PORTX, 0
#define		RTC_RD			PORTX, 0
#define		RTC_AD			PORTX, 0

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
			call	init_display_timer
			call	init_trigger
			call	init_io
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
			bcf		PIR1, TMR1IF			; Clear timer1 interrupt flag
			clrf	TMR1H					; |/ Clear 16-bit timer1
			clrf	TMR1L					; |\
			return

init_trigger:
			BANK1
			bsf		OPTION_REG, INTEDG		; Interrupt on rising edge of RB0
			BANK0
			bsf		INTCON, INTE			; Enable RB0 interrupt
			return

init_io
			BANK1
			movlw	B'00000001'
			movwf	TRISB
			BANK0
			movlw	D'6'
			movwf	tmp_timer
			clrf	seconds
			return

;*********** Interrupt Service Routines ***************************************

ISR:
			btfsc	INTCON, INTF			; Check for trigger interrupt
			call	ISR_trigger
			btfsc	INTCON, T0IF			; Timer 0 overflowed
			call	ISR_timer0
			btfsc	PIR1, TMR1IF			; Timer 1 overflowed
			call	ISR_timer1
			retfie

ISR_timer0:
			bcf		INTCON, T0IF			; Clear interrupt flag
			incf	TMR0H, F				; Increase high byte
			return

ISR_timer1:
			incf	position, F			
			movfw	seconds
			subwf	position, W
			movwf	scratch_ram+6
			btfss	scratch_ram+6, 7
			goto	light_off
			bsf		PORTB, 1
			goto	continue

light_off:	bcf		PORTB, 1

continue:			
			movfw	disp_count_L			; |/
			movwf	TMR1L					; | Load 16-bit counter with
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

			; Get the number of bits we must "burn" when displaying
			;movlw	BURN_MASK
			;andwf	scratch_ram+2, W		; Number of bits to "burn"
			;movwf	burn_bits				; Move to RAM

			; Update temp display
			decfsz	tmp_timer, F
			goto	not_next_second
			
			incf	seconds, F
			movlw	D'6'
			movwf	tmp_timer
			btfsc	seconds, 6
			clrf	seconds

not_next_second:
			clrf	position
			bcf		INTCON, INTF			; Clear trigger interrupt flag

			return
			
;*********** END Interrupt Service Routines ***********************************

			END
