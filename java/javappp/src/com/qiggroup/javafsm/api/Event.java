package com.qiggroup.javafsm.api;

/**
 */
public class Event
{
    /**
     * Causes a Transition to occur on any event.
     */
    public static final Event ANY = new Event("Any");
    
    private String name;

    /**
     * Creates an instance of Event.
     * @param name
     */
    public Event(String name)
    {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }
}
