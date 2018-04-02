// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      StartingState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class StartingState extends PppState {

    private PppActions actions;

    public StartingState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Starting");
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
                    states.reqSentState,
                    actions.new ActionIrcScr(),
                    PppEvents.UP),
            this.createTransition(
                    states.startingState,
                    null,
                    PppEvents.OPEN),
            this.createTransition(
                    states.initialState,
                    actions.new ActionTlf(),
                    PppEvents.CLOSE)
        };
        // @formatter:on

        return retVal;
    }
}
