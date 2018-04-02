// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      OpenedState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class OpenedState extends PppState {

    private PppActions actions;

    public OpenedState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Opened");
        this.actions = actions;
    }

    /**
     * @see com.qiggroup.javappp.protocol.ppp.PppState#createTransitions(com.qiggroup.javappp.protocol.ppp.PppStates)
     */
    @Override
    public Transition[] createTransitions(PppStates states) {
        // @formatter:off
        Transition[] retVal = new Transition[] {  // - 1 5 6
        		this.createTransition(
        				states.startingState, 
        				actions.new ActionTld(),
        				PppEvents.DOWN),  // 2
        		this.createTransition(
        				states.openedState, 
        				null, 
        				PppEvents.OPEN, 
        				PppEvents.RXJ_PLUS),  // 3 14
        		this.createTransition(
        				states.closingState, 
        				actions.new ActionTldIrcStr(), 
        				PppEvents.CLOSE),  // 4
        		this.createTransition(
        				states.ackSentState, 
        				actions.new ActionTldScrSca(), 
        				PppEvents.RCR_PLUS),  // 7
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionTldScrScn(), 
        				PppEvents.RCR_MINUS),  // 8
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionTldScr(),
        				PppEvents.RCA, 
        				PppEvents.RCN, 
        				PppEvents.RTA),  // 9 10 12
        		this.createTransition(
        				states.stoppingState, 
        				actions.new ActionTldZrcSta(), 
        				PppEvents.RTR),  // 11
        		this.createTransition(
        				states.openedState, 
        				actions.new ActionScj(), 
        				PppEvents.RUC),  // 13
        		this.createTransition(
        				states.stoppingState, 
        				actions.new ActionTldIrcStr(), 
        				PppEvents.RXJ_MINUS),  // 15
        		this.createTransition(
        				states.openedState, 
        				actions.new ActionSer(), 
        				PppEvents.RXR),  // 16
        };
        // @formatter:on

        return retVal;
    }
}
