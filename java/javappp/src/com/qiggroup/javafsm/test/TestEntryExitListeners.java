package com.qiggroup.javafsm.test;

import java.awt.event.ActionListener;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.State;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.StateMachineFactory;

import junit.framework.TestCase;
import biz.xsoftware.mock.MockObject;
import biz.xsoftware.mock.MockObjectFactory;

/**
 */
public class TestEntryExitListeners extends TestCase
{
    private MockObject entryList;
    private MockObject exitList;
    private StateMachine sm;
    private Event flipOn;
    private Event flipOff;
    private State on;
    private State off;

    /**
     * Creates an instance of TestStateMachine.
     * @param arg0
     */
    public TestEntryExitListeners(String arg0)
    {
        super(arg0);
    }

    /**
     * @see junit.framework.TestCase#setUp()
     */
    @Override
    protected void setUp() throws Exception
    {
        super.setUp();
        
        exitList = MockObjectFactory.createMock(ActionListener.class);
        entryList = MockObjectFactory.createMock(ActionListener.class);
        
        StateMachineFactory factory = StateMachineFactory.createFactory(null);
        sm = factory.createStateMachine("TestEntryExitListeners");
        
        flipOn = StateMachineFactory.createEvent("flipOn");
        flipOff = StateMachineFactory.createEvent("flipOff");
        
        on = sm.createState("on");
        off = sm.createState("off");
        
        sm.createTransition(on, off, flipOff);
        
        on.addEntryActionListener((ActionListener)entryList);
        on.addExitActionListener((ActionListener)exitList);

        sm.createTransition(off, on, flipOn);
    }

    /**
     * @see junit.framework.TestCase#tearDown()
     */
    @Override
    protected void tearDown() throws Exception
    {
        super.tearDown();
    }

    public void testEntryListener()
    {
        Memento memento = sm.createMementoFromState("id", off);
        
        //fire flipOn and enter state on
        sm.fireEvent(memento, flipOn);

        exitList.expect(MockObject.NONE);
        entryList.expect("actionPerformed");
        entryList.expect(MockObject.NONE);
    }
    
    public void testExitListener()
    {
        Memento memento = sm.createMementoFromState("id", on);
        
        //fire flipOff and exit state on
        sm.fireEvent(memento, flipOff);

        exitList.expect("actionPerformed");
        entryList.expect(MockObject.NONE);
        exitList.expect(MockObject.NONE);
    }
}
