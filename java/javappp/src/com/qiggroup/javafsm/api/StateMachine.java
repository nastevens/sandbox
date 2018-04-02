package com.qiggroup.javafsm.api;

import java.awt.event.ActionListener;


/**
 */
public interface StateMachine
{

    /**
     * Creates the initial state of the state machine.
     * @param stateMachineId is the id of the StateMachine the state will exist in.
     * @param state the initial state.
     * @return A Memento which contains the state that moves around on the state machine.
     */
    public Memento createMementoFromState(String stateMachineId, State state);

    /**
     * @param currentState The current state of the StateMachine(The statemachine is stateless, so you need
     * to tell it the state of the StateMachine)
     * @param event
     */
    public void fireEvent(Memento currentState, Event event);

    /**
     * Creates a State with the given name.
     * @param name the name of the state.
     */
    public State createState(String name);

    /**
     * @param startState is the starting state
     * @param endState is the end state
     * @param events are the Event's that trigger the Transition
     * @return the newly created Transition
     */
    public Transition createTransition(State startState, State endState, Event... events);
    public Transition createTransition(State[] startStates, State endState, Event... events);

    /**
     * @param l is the ActionListener for the action that occurs on entry in any State in this
     *  StateMachine
     */
    public StateMachine addGlobalStateEntryAction(ActionListener l);

    /**
     * @param l is the ActionListener for the action that occurs on exit of any State in this
     *  StateMachine
     */
    public StateMachine addGlobalStateExitAction(ActionListener l);

}
