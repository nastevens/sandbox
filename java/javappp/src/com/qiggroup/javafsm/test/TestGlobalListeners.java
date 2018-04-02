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
public class TestGlobalListeners extends TestCase
{
    private MockObject beforeCreateStateEntryList;
    private MockObject afterCreateStateEntryList;
    private StateMachine sm;
    private Event flipOn;
    private Event flipOff;
    private State on;
    private MockObject beforeCreateStateExitList;
    private MockObject afterCreateStateExitList;

    /**
     * Creates an instance of TestStateMachine.
     * @param arg0
     */
    public TestGlobalListeners(String arg0)
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
        
        beforeCreateStateEntryList = MockObjectFactory.createMock(ActionListener.class);
        afterCreateStateEntryList = MockObjectFactory.createMock(ActionListener.class);
        beforeCreateStateExitList = MockObjectFactory.createMock(ActionListener.class);
        afterCreateStateExitList = MockObjectFactory.createMock(ActionListener.class);
        
        StateMachineFactory factory = StateMachineFactory.createFactory(null);
        sm = factory.createStateMachine("TestGlobalListeners");
        
        sm.addGlobalStateEntryAction((ActionListener)beforeCreateStateEntryList);
        sm.addGlobalStateExitAction((ActionListener)beforeCreateStateExitList);
        
        flipOn = StateMachineFactory.createEvent("flipOn");
        flipOff = StateMachineFactory.createEvent("flipOff");
        
        on = sm.createState("on");
        State off = sm.createState("off");
        
        sm.addGlobalStateEntryAction((ActionListener)afterCreateStateEntryList);
        sm.addGlobalStateExitAction((ActionListener)afterCreateStateExitList);
        
        sm.createTransition(on, off, flipOff);
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

    public void testBasic() {
        Memento memento = sm.createMementoFromState("id", on);
        
        //fire turn off
        sm.fireEvent(memento, flipOff);

        beforeCreateStateEntryList.expect("actionPerformed");
        beforeCreateStateExitList.expect("actionPerformed");
        afterCreateStateEntryList.expect("actionPerformed");
        afterCreateStateExitList.expect("actionPerformed");

        //fire turn off again results in no events...
        sm.fireEvent(memento, flipOff);
        
        beforeCreateStateEntryList.expect(MockObject.NONE);
        beforeCreateStateExitList.expect(MockObject.NONE);
        afterCreateStateEntryList.expect(MockObject.NONE);
        afterCreateStateExitList.expect(MockObject.NONE);     
        
        //flip on now
        sm.fireEvent(memento, flipOn);
        
        beforeCreateStateEntryList.expect("actionPerformed");
        beforeCreateStateExitList.expect("actionPerformed");
        afterCreateStateEntryList.expect("actionPerformed");
        afterCreateStateExitList.expect("actionPerformed");     
    }
    
}
