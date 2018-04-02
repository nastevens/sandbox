// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      AckRcvdState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class AckRcvdState extends PppState {

    private PppActions actions;

    public AckRcvdState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Ack-Rcvd");
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
        				states.startingState, 
        				null, 
        				PppEvents.DOWN),  // 2
        		this.createTransition(
        				states.ackRcvdState, 
        				null, 
        				PppEvents.OPEN, 
        				PppEvents.RXR),  // 3 16
        		this.createTransition(
        				states.closingState, 
        				actions.new ActionIrcStr(), 
        				PppEvents.CLOSE),  // 4
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionScr(), 
        				PppEvents.TO_PLUS, 
        				PppEvents.RCA, 
        				PppEvents.RCN),  // 5 9 10
        		this.createTransition(
        				states.stoppedState, 
        				actions.new ActionTlf(), 
        				PppEvents.TO_MINUS, 
        				PppEvents.RXJ_MINUS),  // 6 15
        		this.createTransition(
        				states.openedState, 
        				actions.new ActionScaTlu(), 
        				PppEvents.RCR_PLUS),  // 7
        		this.createTransition(
        				states.ackRcvdState, 
        				actions.new ActionScn(), 
        				PppEvents.RCR_MINUS),  // 8
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionSta(), 
        				PppEvents.RTR),  // 11
        		this.createTransition(
        				states.reqSentState, 
        				null, 
        				PppEvents.RTA,  
        				PppEvents.RXJ_PLUS),  // 12 14
        		this.createTransition(
        				states.ackRcvdState, 
        				actions.new ActionScj(), 
        				PppEvents.RUC)  // 13
        };
        // @formatter:on

        return retVal;
    }
}
