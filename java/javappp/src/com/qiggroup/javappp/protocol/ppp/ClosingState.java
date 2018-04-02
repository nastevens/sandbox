// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      ClosingState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class ClosingState extends PppState {

    private PppActions actions;

    public ClosingState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Closing");
        this.actions = actions;
    }

    /**
     * @see com.qiggroup.javappp.protocol.ppp.PppState#createTransitions(com.qiggroup.javappp.protocol.ppp.PppStates)
     */
    @Override
    public Transition[] createTransitions(PppStates states) {
        // @formatter:off
        Transition[] retVal = new Transition[] {  // - 1
                this.createTransition(
                		states.initialState, 
                		null, 
                		PppEvents.DOWN),  // 2
                this.createTransition(
                		states.stoppingState, 
                		null, 
                		PppEvents.OPEN),  // 3
                this.createTransition(
                		states.closingState, 
                		null, 
                		PppEvents.CLOSE, 
                		PppEvents.RCR_MINUS, 
                		PppEvents.RCR_PLUS, 
                		PppEvents.RCA, 
                		PppEvents.RCN, 
                		PppEvents.RXJ_PLUS, 
                		PppEvents.RXR),  // 4 7 8 9 10 14 16
                this.createTransition(
                		states.closingState, 
                		actions.new ActionStr(), 
                		PppEvents.TO_PLUS),  // 5
                this.createTransition(
                		states.closedState, 
                		actions.new ActionTlf(), 
                		PppEvents.TO_MINUS, 
                		PppEvents.RTA, 
                		PppEvents.RXJ_MINUS),  // 6 12 15
                this.createTransition(
                		states.closingState, 
                		actions.new ActionSta(), 
                		PppEvents.RTR),  // 11
                this.createTransition(
                		states.closingState, 
                		actions.new ActionScj(), 
                		PppEvents.RUC),  // 13
                
        };
        // @formatter:on

        return retVal;
    }
}
