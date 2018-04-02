/**
 * 
 */
package com.qiggroup.javappp.frame;

import java.io.OutputStream;

/**
 * @author Nick
 * 
 */
public class FrameWriterThread extends Thread {

    private OutputStream os;

    /*
     * The FCS field is calculated over all bits of the Address, Control,
     * Protocol, Information and Padding fields, not including any start and
     * stop bits (asynchronous) nor any bits (synchronous) or octets
     * (asynchronous or synchronous) inserted for transparency. This also does
     * not include the Flag Sequences nor the FCS field itself.
     * 
     * Octects flagged in ACCM are discarded before calculating the FCS
     */
    public FrameWriterThread(OutputStream os) {
        this.os = os;
    }

    @Override
    public void run() {
        // TODO Auto-generated method stub
        super.run();
    }

}
