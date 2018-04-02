package com.qiggroup.javafsm.impl;

import java.util.Map;

import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.StateMachineFactory;


/**
 */
public class StateMachineFactoryImpl extends StateMachineFactory
{

    /**
     * @see com.qiggroup.javafsm.api.StateMachineFactory#configure(java.util.Map)
     */
    @Override
    protected void configure(Map<String, Object> map)
    {
    }


    /**
     * @see com.qiggroup.javafsm.api.StateMachineFactory#createStateMachine()
     */
    @Override
    public StateMachine createStateMachine()
    {
        return new StateMachineImpl(null);
    }


    /**
     * @see com.qiggroup.javafsm.api.StateMachineFactory#createStateMachine(java.lang.String)
     */
    @Override
    public StateMachine createStateMachine(String id)
    {
        return new StateMachineImpl(id);
    }

}
