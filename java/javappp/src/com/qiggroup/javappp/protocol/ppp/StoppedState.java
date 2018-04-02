// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      StoppedState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class StoppedState extends PppState {

    private PppActions actions;

    public StoppedState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Stopped");
        this.actions = actions;
    }

    /**
     * @see com.qiggroup.javappp.protocol.ppp.PppState#createTransitions(com.qiggroup.javappp.protocol.ppp.PppStates)
     */
    @Override
    public Transition[] createTransitions(PppStates states) {
        // @formatter:off
        Transition[] retVal = new Transition[] {
        		this.createTransition(
        				states.startingState,
                        actions.new ActionTls(),
                        PppEvents.DOWN),
                this.createTransition(
                		states.stoppedState,
                		null,
                		PppEvents.OPEN),
                this.createTransition(
                        states.closedState,
                        null,
                        PppEvents.CLOSE),
                this.createTransition(
                		states.ackSentState, 
                		actions.new ActionIrcScrSca(), 
                		PppEvents.RCR_PLUS),
        		this.createTransition(
        				states.reqSentState, 
        				actions.new ActionIrcScrSca(), 
        				PppEvents.RCR_MINUS),
        		this.createTransition(states.stoppedState, 
        				actions.new ActionSta(), 
        				PppEvents.RCA, 
        				PppEvents.RCN, 
        				PppEvents.RTR),
				this.createTransition(
						states.stoppedState, 
						null, 
						PppEvents.RTA),
				this.createTransition(
						states.stoppedState, 
						actions.new ActionScj(), 
						PppEvents.RUC),
				this.createTransition(
						states.stoppedState, 
						null, 
						PppEvents.RXJ_PLUS),
				this.createTransition(
						states.stoppedState, 
						actions.new ActionTlf(), 
						PppEvents.RXJ_MINUS),
				this.createTransition(
						states.stoppedState, 
						null, PppEvents.RXR)
        };
        // @formatter:on

        return retVal;
    }
}
