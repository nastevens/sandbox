/**
 */
package com.qiggroup.javafsm.test;

import java.awt.event.ActionListener;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.State;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.StateMachineFactory;
import com.qiggroup.javafsm.api.Transition;

import biz.xsoftware.mock.MockObject;
import biz.xsoftware.mock.MockObjectFactory;
import junit.framework.TestCase;

/**
 */
public class TestMultieventTransition extends TestCase
{
    private MockObject mockOffListener;
    private MockObject mockOnListener;
    private StateMachine sm;
    private Event flipOn;
    private Event alsoFlipOn;
    private Event flipOff;
    private State on;
    private Transition onToOff;

    @Override
    protected void setUp() throws Exception
    {
        super.setUp();

        mockOffListener = MockObjectFactory.createMock(ActionListener.class);
        mockOnListener = MockObjectFactory.createMock(ActionListener.class);

        StateMachineFactory factory = StateMachineFactory.createFactory(null);
        sm = factory.createStateMachine("TestMultieventTransition");

        flipOn = StateMachineFactory.createEvent("flipOn");
        alsoFlipOn = StateMachineFactory.createEvent("alsoFlipOn");
        flipOff = StateMachineFactory.createEvent("flipOff");

        on = sm.createState("on");
        State off = sm.createState("off");

        onToOff = sm.createTransition(on, off, flipOff);
        onToOff.addActionListener((ActionListener)mockOffListener);

        Transition offToOn = sm.createTransition(off, on, flipOn, alsoFlipOn);
        offToOn.addActionListener((ActionListener)mockOnListener);
    }

    @Override
    protected void tearDown() throws Exception
    {
        super.tearDown();
        
        mockOffListener.expect(MockObject.NONE);
        mockOnListener.expect(MockObject.NONE);
    }

    public void testDifferentEvents()
    {
        Memento memento = sm.createMementoFromState("id", on);

        //fire turn off
        sm.fireEvent(memento, flipOff);

        mockOnListener.expect(MockObject.NONE);
        mockOffListener.expect("actionPerformed");

        //fire turn off again...
        sm.fireEvent(memento, flipOff);

        mockOnListener.expect(MockObject.NONE);
        mockOffListener.expect(MockObject.NONE);

        //fire turn on.....
        sm.fireEvent(memento, flipOn);

        mockOnListener.expect("actionPerformed");
        mockOffListener.expect(MockObject.NONE);
        
        //fire turn off again...
        sm.fireEvent(memento, flipOff);

        mockOnListener.expect(MockObject.NONE);
        mockOffListener.expect("actionPerformed");
        
        // and turn back on with the other event
        sm.fireEvent(memento, alsoFlipOn);

        mockOnListener.expect("actionPerformed");
        mockOffListener.expect(MockObject.NONE);
        
        //fire turn off again...
        sm.fireEvent(memento, flipOff);

        mockOnListener.expect(MockObject.NONE);
        mockOffListener.expect("actionPerformed");

        //fire turn on.....
        sm.fireEvent(memento, flipOn);

        mockOnListener.expect("actionPerformed");
        mockOffListener.expect(MockObject.NONE);
    }
}
