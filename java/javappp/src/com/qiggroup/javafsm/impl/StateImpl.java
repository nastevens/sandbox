package com.qiggroup.javafsm.impl;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;

import javax.swing.event.EventListenerList;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.State;

/**
 */
public class StateImpl implements State {
    private String name;
    private Map<Event, TransitionImpl> evtToTransition = new HashMap<Event, TransitionImpl>();
    private EventListenerList entryListeners = new EventListenerList();
    private EventListenerList exitListeners = new EventListenerList();

    /**
     * Creates an instance of StateImpl.
     * 
     * @param name
     */
    public StateImpl(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        // TODO: return all the events and transition to next states???
        return this.name;
    }

    /**
     * @param evt
     * @param transition
     */
    public void addTransition(Event evt, TransitionImpl transition) {
        TransitionImpl t = this.evtToTransition.get(evt);
        if(t != null)
            throw new IllegalArgumentException("A transition our of state="
                    + this + " caused from evt=" + evt
                    + " has already been added.  Cannot add another one.");

        this.evtToTransition.put(evt, transition);
    }

    /**
     * @param smState
     * @param evt
     */
    public void fireEvent(StateMachineState smState, Event evt) {
        TransitionImpl transition = this.evtToTransition.get(evt);
        if(transition == null) {
            transition = this.evtToTransition.get(Event.ANY);
        }
        if(transition == null) {
            smState.getLogger().fine(
                    smState + "No Transition: " + this.getName()
                            + " -> <no transition found>, event=" + evt);
            return;
        }

        StateImpl endState = transition.getEndState();
        String nextState = transition.getEndState().getName();
        smState.getLogger().fine(
                smState + "Transition: " + this.getName() + " -> " + nextState
                        + ", event=" + evt);

        try {
            this.fireExitActions(smState);
            transition.fireTransitionActions(smState);
            endState.fireEntryActions(smState);

            smState.setCurrentStateName(nextState);
        } catch(RuntimeException e) {
            smState.getLogger().warning(
                    smState + "Transition FAILED: " + this.getName() + " -> "
                            + nextState + ", event=" + evt);
            throw e;
        }
    }

    /**
     * @param smState
     */
    private void fireEntryActions(StateMachineState smState) {
        ActionListener[] list = this.entryListeners
                .getListeners(ActionListener.class);
        ActionEvent evt = new ActionEvent(this, 0, null);
        for(int ii = list.length - 1; ii >= 0; ii--) {
            try {
                smState.getLogger().finer(
                        smState + "Entry Action: "
                                + list[ii].getClass().getName() + ", state="
                                + this.getName());
                list[ii].actionPerformed(evt);
            } catch(RuntimeException e) {
                // Do not log stack trace here. It should only be logged at the
                // beginning of a thread
                smState.getLogger()
                        .log(Level.WARNING,
                                smState
                                        + "Exception occurred in client ActionListener="
                                        + list[ii] + ", state="
                                        + this.getName());
                // rethrow and stop executing the rest of the Actions
                throw e;
            }
        }
    }

    /**
     * @param smState
     */
    private void fireExitActions(StateMachineState smState) {
        ActionListener[] list = this.exitListeners
                .getListeners(ActionListener.class);
        ActionEvent evt = new ActionEvent(this, 0, null);
        for(int ii = list.length - 1; ii >= 0; ii--) {
            try {
                smState.getLogger().finer(
                        smState + "Exit Action: "
                                + list[ii].getClass().getName() + ", state="
                                + this.getName());
                list[ii].actionPerformed(evt);
            } catch(RuntimeException e) {
                smState.getLogger()
                        .log(Level.WARNING,
                                smState
                                        + "Exception occurred in client ActionListener="
                                        + list[ii] + ", state="
                                        + this.getName());
                // rethrow and stop executing the rest of the Actions
                throw e;
            }
        }
    }

    /**
     */
    @Override
    public String getName() {
        return this.name;
    }

    /**
     * @see com.qiggroup.javafsm.api.State#addEntryActionListener(java.awt.event.ActionListener)
     */
    @Override
    public State addEntryActionListener(ActionListener listener) {
        if(listener == null)
            throw new IllegalArgumentException("listener cannot be null");
        this.entryListeners.add(ActionListener.class, listener);
        return this;
    }

    /**
     * @see com.qiggroup.javafsm.api.State#addExitActionListener(java.awt.event.ActionListener)
     */
    @Override
    public State addExitActionListener(ActionListener listener) {
        if(listener == null)
            throw new IllegalArgumentException("listener cannot be null");
        this.exitListeners.add(ActionListener.class, listener);
        return this;
    }
}
