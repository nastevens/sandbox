// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppStates.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.StateMachineFactory;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class PppStates {

    public final PppState initialState;
    public final PppState startingState;
    public final PppState closedState;
    public final PppState stoppedState;
    public final PppState closingState;
    public final PppState stoppingState;
    public final PppState reqSentState;
    public final PppState ackRcvdState;
    public final PppState ackSentState;
    public final PppState openedState;
    private final PppState[] allStates;

    private final StateMachineFactory factory;
    private final StateMachine sm;
    private final PppActions actions;

    public PppStates(PppStateMachine pppState) {

        this.factory = StateMachineFactory.createFactory(null);
        this.sm = factory.createStateMachine("PppStateMachine");
        this.actions = new PppActions(pppState);

        // Create instances of all state handlers
        initialState = new InitialState(this.sm, this.actions);
        startingState = new StartingState(this.sm, this.actions);
        closedState = new ClosedState(this.sm, this.actions);
        stoppedState = new StoppedState(this.sm, this.actions);
        closingState = new ClosingState(this.sm, this.actions);
        stoppingState = new StoppingState(this.sm, this.actions);
        reqSentState = new ReqSentState(this.sm, this.actions);
        ackRcvdState = new AckRcvdState(this.sm, this.actions);
        ackSentState = new AckSentState(this.sm, this.actions);
        openedState = new OpenedState(this.sm, this.actions);
        
        // Allow all state handlers to register their transitions
        this.allStates = new PppState[] {initialState, startingState, closedState,
                stoppedState, closingState, stoppingState, reqSentState,
                ackRcvdState, ackSentState, openedState};
        for(PppState state : this.allStates) {
            state.createTransitions(this);
        }
    }

    public Memento createMemento() {
        return sm.createMementoFromState("PppStateMachine",
                this.initialState.getState());
    }

    /**
     * @return the factory
     */
    public StateMachineFactory getStateMachineFactory() {
        return factory;
    }

    /**
     * @return the sm
     */
    public StateMachine getStateMachine() {
        return sm;
    }

    /**
     * @return the actions
     */
    public PppActions getActions() {
        return actions;
    }

}
