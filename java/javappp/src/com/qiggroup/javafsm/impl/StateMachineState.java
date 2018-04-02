package com.qiggroup.javafsm.impl;

import java.util.logging.Logger;

import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.State;


/**
 */
public class StateMachineState implements Memento
{
    private static final long serialVersionUID = 1L;

    private Logger log;
    private String id;
    private String stateName;
    private transient boolean inProcess = false;
    private StateMachineImpl stateMachine;

    public StateMachineState(String rawMapId, String stateMachineId, State state, StateMachineImpl sm)
    {
        this.id = rawMapId+","+stateMachineId;
        this.stateName = state.getName();
        this.stateMachine = sm;
        log = Logger.getLogger("com.qiggroup.javafsm.impl."+rawMapId+"."+stateMachineId);
    }

    @Override
    public String toString() {
        return "["+id+"] ";
    }

    public String getCurrentStateName()
    {
        return stateName;
    }

    public void setCurrentStateName(String name)
    {
        if(name == null)
            throw new IllegalArgumentException("name cannot be null");
        this.stateName = name;
    }

    public boolean isInProcess()
    {
        return inProcess;
    }

    public void setInProcess(boolean inProcess)
    {
        this.inProcess = inProcess;
    }

    public StateMachineImpl getStateMachine()
    {
        return stateMachine;
    }

    public Logger getLogger()
    {
        return log;
    }
}
