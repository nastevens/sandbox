// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      AckSentState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class AckSentState extends PppState {

    private PppActions actions;

    public AckSentState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Ack-Sent");
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
        				states.ackSentState, 
        				null, 
        				PppEvents.OPEN, 
        				PppEvents.RTA, 
        				PppEvents.RXJ_PLUS, 
        				PppEvents.RXR),  // 3 12 14 16
        		this.createTransition(
        				states.closingState, 
        				actions.new ActionIrcStr(), 
        				PppEvents.CLOSE),  // 4
        		this.createTransition(
        				states.ackSentState, 
        				actions.new ActionScr(), 
        				PppEvents.TO_PLUS),  // 5
        		this.createTransition(
        				states.stoppedState, 
        				actions.new ActionTlf(), 
        				PppEvents.TO_MINUS, 
        				PppEvents.RXJ_MINUS),  // 6 15
        		this.createTransition(
        				states.ackSentState, 
        				actions.new ActionSca(), 
        				PppEvents.RCR_PLUS),  // 7
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionScn(), 
        				PppEvents.RCR_MINUS),  // 8
        		this.createTransition(
        				states.openedState, 
        				actions.new ActionIrcTlu(), 
        				PppEvents.RCA),  // 9
        		this.createTransition(
        				states.ackSentState, 
        				actions.new ActionIrcScr(), 
        				PppEvents.RCN),  // 10
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionSta(), 
        				PppEvents.RTR),  // 11
        		this.createTransition(
        				states.ackSentState, 
        				actions.new ActionScj(), 
        				PppEvents.RUC),  // 13
        };
        // @formatter:on

        return retVal;
    }
}
