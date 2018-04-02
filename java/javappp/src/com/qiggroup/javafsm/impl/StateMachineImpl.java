package com.qiggroup.javafsm.impl;

import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;

import javax.swing.event.EventListenerList;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.IllegalFireEventException;
import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.State;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.Transition;


/**
 */
public class StateMachineImpl implements StateMachine
{
    private final Map<String, StateImpl> nameToState = new HashMap<String, StateImpl>();
    private final EventListenerList globalEntryListeners = new EventListenerList();
    private final EventListenerList globalExitListeners = new EventListenerList();
    private final String rawMapId;

    /**
     * Creates an instance of StateMachineImpl.
     * @param id
     */
    public StateMachineImpl(String id)
    {
        if(id == null)
            rawMapId = "unnamed";
        else
            rawMapId = id;
    }

    public Memento createMementoFromState(String stateMachineId, State state) {
        State name = nameToState.get(state.getName());
        if(name == null)
            throw new IllegalArgumentException(this + "This state does not exist in this statemachine.  name="+name);
        return new StateMachineState(rawMapId, stateMachineId, state, this);
    }

    /**
     * @see com.qiggroup.javafsm.api.StateMachine#createState(java.lang.String)
     */
    public synchronized State createState(String name)
    {
    	StateImpl state = nameToState.get(name);
    	if(state != null)
    		throw new IllegalArgumentException("This state already exists. You can't create the same state twice");
        state = new StateImpl(name);
        nameToState.put(name, state);
        for(ActionListener l : globalEntryListeners.getListeners(ActionListener.class)) {
            state.addEntryActionListener(l);
        }

        for(ActionListener l : globalExitListeners.getListeners(ActionListener.class)) {
            state.addExitActionListener(l);
        }
        return state;
    }

    public Transition createTransition(State[] startStates, State endState, Event... events)
    {
        if(events.length < 1)
        {
            throw new IllegalArgumentException(this + "You must specify at least one event");
        }
        else if(!(endState instanceof StateImpl))
        {
            throw new IllegalArgumentException(rawMapId + "endState are not created using this StateMachine");
        }   if(startStates.length < 1)
        {
            throw new IllegalArgumentException(rawMapId + "You must specify at least one event");
        }


        TransitionImpl transition = new TransitionImpl((StateImpl)endState);
        for(State startState : startStates)
        {
            StateImpl startImpl = (StateImpl)startState;
            for(Event event : events)
            {
                startImpl.addTransition(event, transition);
            }
        }
        return transition;
    }
    /**
     * @see com.qiggroup.javafsm.api.StateMachine#createTransition(com.qiggroup.javafsm.api.State, com.qiggroup.javafsm.api.State, com.qiggroup.javafsm.api.Event[])
     */
    public Transition createTransition(State startState, State endState, Event... events)
    {
        State[] startStates = {startState};
        return createTransition(startStates, endState, events);

    }

    @Override
    public void fireEvent(Memento memento, Event evt)
    {
        if(memento == null)
            throw new IllegalArgumentException(this + "memento cannot be null");
        else if(evt == null)
            throw new IllegalArgumentException(this + "evt cannot be null");
        else if(!(memento instanceof StateMachineState))
            throw new IllegalArgumentException(this + "memento was not created using StateMachine.createMementoFromIntialState and must be");
        else if( ((StateMachineState)memento).getStateMachine() != this)
            throw new IllegalArgumentException(this + "memento was not created with this specific statemachine.  " +
                    "you got your statemachines mixed up with the mementos");

        StateMachineState smState = (StateMachineState)memento;
        synchronized(memento) {
            if(smState.isInProcess())
                throw new IllegalFireEventException(smState+"The StateMachine is currently " +
                        "transitioning and running a client ActionListener which calls back into the StateMachine.  This is illegal");
            smState.setInProcess(true);
        }

        try {
            //get the current state
            StateImpl state = nameToState.get(smState.getCurrentStateName());

            state.fireEvent(smState, evt);
        } catch(RuntimeException e) {
            //NOTE: Stack trace is not logged here.  That is the responsibility of the javasm client
            //so exceptions don't get logged multiple times.
            smState.getLogger().log(Level.WARNING, this+"Exception occurred going out of state="+smState.getCurrentStateName()+", event="+evt);
            throw e;
        } finally {
            smState.setInProcess(false);
        }
    }

    /**
     * @see com.qiggroup.javafsm.api.StateMachine#addGlobalStateEntryAction(java.awt.event.ActionListener)
     */
    public synchronized StateMachine addGlobalStateEntryAction(ActionListener l)
    {
        //first add it to all created states
        for(State state : nameToState.values()) {
            state.addEntryActionListener(l);
        }
        globalEntryListeners.add(ActionListener.class, l);
        return this;
    }

    /**
     * @see com.qiggroup.javafsm.api.StateMachine#addGlobalStateExitAction(java.awt.event.ActionListener)
     */
    public synchronized StateMachine addGlobalStateExitAction(ActionListener l)
    {
        //first add it to all created states
        for(State state : nameToState.values()) {
            state.addExitActionListener(l);
        }
        globalExitListeners.add(ActionListener.class, l);
        return this;
    }

    @Override
    public String toString() {
        return "[" + rawMapId + "] ";
    }
}
