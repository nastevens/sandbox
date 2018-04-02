// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppState.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import java.awt.event.ActionListener;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.State;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public abstract class PppState {

    private StateMachine stateMachine;
    private State state;

    public PppState(StateMachine stateMachine, String stateName) {
        this.stateMachine = stateMachine;
        this.state = this.stateMachine.createState(stateName);
    }

    public abstract Transition[] createTransitions(PppStates states);

    /**
     * @return the state
     */
    public State getState() {
        return state;
    }

    protected StateMachine getStateMachine() {
        return this.stateMachine;
    }

    protected Transition createTransition(PppState destination,
            ActionListener listener, Event... events) {
        Transition tran = this.getStateMachine().createTransition(
                this.getState(), destination.getState(), events);
        if(listener != null) {
            tran.addActionListener(listener);
        }
        return tran;
    }

}
