package com.qiggroup.javafsm.api;

import java.awt.event.ActionListener;

/**
 */
public interface Transition
{

    /**
     * @param listener
     */
    Transition addActionListener(ActionListener listener);

}
