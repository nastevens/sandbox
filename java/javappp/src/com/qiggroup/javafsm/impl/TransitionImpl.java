package com.qiggroup.javafsm.impl;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.qiggroup.javafsm.api.Transition;
import com.qiggroup.javappp.util.EventListenerList;

/**
 */
public class TransitionImpl implements Transition {
    private static final Logger log = Logger.getLogger(TransitionImpl.class
            .getName());
    private EventListenerList listeners = new EventListenerList();
    private StateImpl endState;

    /**
     * Creates an instance of TransitionImpl.
     * 
     * @param endState
     */
    public TransitionImpl(StateImpl endState) {
        this.endState = endState;
    }

    /**
     * @see com.qiggroup.javafsm.api.Transition#addActionListener(java.awt.event.ActionListener)
     */
    @Override
    public Transition addActionListener(ActionListener listener) {
        if(listener == null)
            throw new IllegalArgumentException("listener cannot be null");
        this.listeners.add(ActionListener.class, listener);
        return this;
    }

    /**
     * @return Returns the endState.
     */
    public StateImpl getEndState() {
        return this.endState;
    }

    /**
     * 
     */
    public void fireTransitionActions(StateMachineState smState) {
        ActionListener[] list = this.listeners
                .getListeners(ActionListener.class);
        ActionEvent event = new ActionEvent(this, 0, null);
        for(int ii = list.length - 1; ii >= 0; ii--) {
            try {
                if(log.isLoggable(Level.FINER)) {
                    smState.getLogger().finer(
                            smState + "Action: "
                                    + list[ii].getClass().getName()
                                    + ", state="
                                    + smState.getCurrentStateName());
                }
                list[ii].actionPerformed(event);
            } catch(RuntimeException e) {
                smState.getLogger()
                        .log(Level.WARNING,
                                smState
                                        + "Exception occurred in client ActionListener="
                                        + list[ii]);
                // rethrow and stop executing the rest of the Actions
                throw e;
            }
        }
    }

}
