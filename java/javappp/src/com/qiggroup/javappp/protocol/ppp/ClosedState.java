// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      ClosedState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class ClosedState extends PppState {

    PppActions actions;

    public ClosedState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Closed");
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
                    states.initialState,
                    null,
                    PppEvents.DOWN),
            this.createTransition(
                    states.reqSentState, 
                    actions.new ActionIrcScr(),
                    PppEvents.OPEN),
            this.createTransition(
                    states.closedState,
                    null,
                    PppEvents.CLOSE,
                    PppEvents.RTA,
                    PppEvents.RXJ_PLUS,
                    PppEvents.RXR),
            this.createTransition(
                    states.closedState, 
                    actions.new ActionSta(),
                    PppEvents.RCR_PLUS,
                    PppEvents.RCR_MINUS,
                    PppEvents.RCA,
                    PppEvents.RCN,
                    PppEvents.RTR),
            this.createTransition(
                    states.closedState,
                    actions.new ActionScj(),
                    PppEvents.RUC),
            this.createTransition(
                    states.closedState,
                    actions.new ActionTlf(),
                    PppEvents.RXJ_MINUS)
        };
        // @formatter:on

        return retVal;
    }


}
