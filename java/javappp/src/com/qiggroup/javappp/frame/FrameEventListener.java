/**
 * 
 */
package com.qiggroup.javappp.frame;

import java.util.EventListener;

/**
 * @author Nick
 * 
 */
public interface FrameEventListener extends EventListener {

    void frameReceived(Frame f);

}
