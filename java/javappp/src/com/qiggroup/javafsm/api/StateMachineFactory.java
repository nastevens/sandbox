package com.qiggroup.javafsm.api;

import java.util.Map;


/**
 */
public abstract class StateMachineFactory
{

    public static final String KEY_IMPLEMENTATION_CLASS = "stateMachine.Implementation";
    public static final String VAL_DEFAULT_SM           = "com.qiggroup.javafsm.impl.StateMachineFactoryImpl";  
    
    public static StateMachineFactory createFactory(Map<String, Object> map) {
        String className = VAL_DEFAULT_SM;
        if(map != null) {
            Object tmp = map.get(KEY_IMPLEMENTATION_CLASS);
            if(!(tmp instanceof String))
                throw new IllegalArgumentException("key=StateMachineFactory.KEY_IMPLEMENTATION_CLASS must be of type String and wasn't");
            className = (String)tmp;
        }

        StateMachineFactory retVal = null;
        try {
            Class<? extends StateMachineFactory> theClass = Class.forName(className).asSubclass(StateMachineFactory.class);
            retVal = theClass.newInstance();
            retVal.configure(map);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Class not found.  See the exception causing this one for more info.", e);
        } catch (InstantiationException e) {
            throw new RuntimeException("bug", e);
        } catch (IllegalAccessException e) {
            throw new RuntimeException("bug", e);
        }
        
        return retVal; 
    }

    protected abstract void configure(Map<String, Object> map);

    /**
     */
    public abstract StateMachine createStateMachine();

    /**
     */
    public abstract StateMachine createStateMachine(String id);
    
}
