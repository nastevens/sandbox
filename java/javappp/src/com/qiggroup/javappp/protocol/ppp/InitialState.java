// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      InitialState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class InitialState extends PppState {

    private PppActions actions;

    public InitialState(StateMachine stateMachine, PppActions actions) {
        super(stateMachine, "Initial");
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
                    states.closedState,
                    null,
                    PppEvents.UP),
            this.createTransition(
                    states.startingState,
                    actions.new ActionTls(),
                    PppEvents.OPEN),
            this.createTransition(
                    states.initialState,
                    null,
                    PppEvents.CLOSE)
        };
        // @formatter:on
        
        return retVal;
    }
}
