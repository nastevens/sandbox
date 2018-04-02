/**
 * 
 */
package com.qiggroup.javappp.frame;

import java.io.IOException;
import java.io.InputStream;

import com.qiggroup.javappp.util.EventListenerList;

/**
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class FrameReaderThread extends Thread {

    private final byte FLAG = (byte) 0x7E;

    private InputStream in;
    private EventListenerList frameEventListeners;

    /*
     * On reception, the Address and Control fields are decompressed by
     * examining the first two octets. If they contain the values 0xff and 0x03,
     * they are assumed to be the Address and Control fields. If not, it is
     * assumed that the fields were compressed and were not transmitted.
     */
    public FrameReaderThread(InputStream in) {
        this.in = in;
        this.frameEventListeners = new EventListenerList();
    }

    /**
     * Continuously monitor the InputStream and pass decoded incoming data to
     * the higher level protocols.
     */
    @Override
    public void run() {

        Frame newFrame = new Frame();
        int available;
        int readByte;

        while(true) {
            try {
                available = this.in.available();
            } catch(IOException e) {
                break;
            }
            if(available > 0) {
                try {
                    readByte = this.in.read();
                } catch(IOException e) {
                    break;
                }

                if(readByte < 0) {
                    break;
                }

                if(readByte == FLAG) {
                    if(newFrame.isValid()) {
                        this.doFrameEvent(newFrame);
                        // System.out.println("Received valid frame <" +
                        // newFrame.getDataPayload().length + "> " +
                        // "bytes long");
                    } else {
                        System.out.println("Discarded invalid frame");
                    }
                    newFrame = new Frame();
                } else {
                    newFrame.addPayload(readByte);
                }
            } else if(available < 0) {
                break;
            } else {
                try {
                    Thread.sleep(100);
                } catch(InterruptedException e) {
                    break;
                }
            }
        }

        System.out.println("FrameReaderThread finishing up...");
    }

    private void doFrameEvent(Frame f) {
        FrameEventListener[] listeners;
        listeners = frameEventListeners.getListeners(FrameEventListener.class);
        for(FrameEventListener listener : listeners) {
            listener.frameReceived(f);
        }
    }

    public void addFrameEventListener(FrameEventListener listener) {
        this.frameEventListeners.add(FrameEventListener.class, listener);
    }

    public void removeFrameEventListener(FrameEventListener listener) {
        this.frameEventListeners.remove(FrameEventListener.class, listener);
    }
}
