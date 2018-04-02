package com.qiggroup.javafsm.test;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.logging.Logger;

import com.qiggroup.javafsm.api.Event;
import com.qiggroup.javafsm.api.Memento;
import com.qiggroup.javafsm.api.State;
import com.qiggroup.javafsm.api.StateMachine;
import com.qiggroup.javafsm.api.StateMachineFactory;
import com.qiggroup.javafsm.api.Transition;

import junit.framework.TestCase;
import biz.xsoftware.mock.MockObject;
import biz.xsoftware.mock.MockObjectFactory;

/**
 */
public class TestStateMachine extends TestCase
{
	private static final Logger log = Logger.getLogger(TestStateMachine.class.getName());
    private MockObject mockOffListener;
    private MockObject mockOnListener;
    private StateMachine sm;
    private Event flipOn;
    private Event flipOff;
    private State on;
    private Transition onToOff;

    /**
     * Creates an instance of TestStateMachine.
     * @param arg0
     */
    public TestStateMachine(String arg0)
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

        mockOffListener = MockObjectFactory.createMock(ActionListener.class);
        mockOnListener = MockObjectFactory.createMock(ActionListener.class);

        StateMachineFactory factory = StateMachineFactory.createFactory(null);
        sm = factory.createStateMachine("TestStateMachine");

        flipOn = StateMachineFactory.createEvent("flipOn");
        flipOff = StateMachineFactory.createEvent("flipOff");

        on = sm.createState("on");
        State off = sm.createState("off");

        onToOff = sm.createTransition(on, off, flipOff);
        onToOff.addActionListener((ActionListener)mockOffListener);

        Transition offToOn = sm.createTransition(off, on, flipOn);
        offToOn.addActionListener((ActionListener)mockOnListener);
    }

    /**
     * @see junit.framework.TestCase#tearDown()
     */
    @Override
    protected void tearDown() throws Exception
    {
        super.tearDown();
        
        mockOffListener.expect(MockObject.NONE);
        mockOnListener.expect(MockObject.NONE);
    }

    public void testBasic() {
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
    }

    /**
     * This makes sure an Exception causes the statemachine to not get corrupted.  This covers a
     * bug we had where an exception would not allow future firing into statemachine.
     *
     */
    public void testExceptionHandled() {
        Memento memento = sm.createMementoFromState("id", on);

        mockOffListener.addThrowException("actionPerformed", new IllegalMonitorStateException());

        try {
            //fire turn off
            sm.fireEvent(memento, flipOff);
            fail("Should have thrown exception");
        } catch(IllegalMonitorStateException e) {
        	log.info("This exception is expected");
        }

        mockOffListener.expect("actionPerformed");

        //should now be able to fire in to statemachine still!!!!!
        sm.fireEvent(memento, flipOff);

        mockOnListener.expect(MockObject.NONE);
        mockOffListener.expect("actionPerformed");
    }

    public void testOrder()
    {
        Memento memento = sm.createMementoFromState("id", on);

        MockObject mockFake = MockObjectFactory.createMock(FakeInterface.class);
        onToOff.addActionListener(new FakeListener1((FakeInterface)mockFake));
        onToOff.addActionListener(new FakeListener2((FakeInterface)mockFake));

        //fire turn off
        sm.fireEvent(memento, flipOff);
        
        mockOffListener.expect("actionPerformed");
        mockFake.expect("first", "second");
    }

    private interface FakeInterface
    {
        public void first();
        public void second();
    }

    private class FakeListener1 implements ActionListener
    {
        private FakeInterface fake;

        public FakeListener1(FakeInterface fake)
        {
            this.fake = fake;
        }

        public void actionPerformed(ActionEvent e)
        {
            fake.first();
        }
    }

    private class FakeListener2 implements ActionListener
    {
        private FakeInterface fake;

        public FakeListener2(FakeInterface fake)
        {
            this.fake = fake;
        }

        public void actionPerformed(ActionEvent e)
        {
            fake.second();
        }
    }
}
