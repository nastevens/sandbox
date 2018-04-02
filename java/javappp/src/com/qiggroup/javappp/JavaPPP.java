/**
 * 
 */
package com.qiggroup.javappp;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.logging.ConsoleHandler;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.qiggroup.javappp.frame.FrameReaderThread;
import com.qiggroup.javappp.packets.PppParser;
import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;
import com.qiggroup.javappp.protocol.ppp.PppStateMachine;

/**
 * @author Nick
 * 
 */
public class JavaPPP {

    private static Logger rootLogger = Logger.getLogger("");

    public static void main(String[] args) {
        // ConsoleHandler hand = new ConsoleHandler();
        // hand.setLevel(Level.FINEST);
        // logger.addHandler(hand);
        rootLogger.setLevel(Level.FINE);
        for(Handler handler : rootLogger.getHandlers()) {
            rootLogger.removeHandler(handler);
        }
        ConsoleHandler handler = new ConsoleHandler();
        handler.setLevel(Level.FINEST);
        rootLogger.addHandler(handler);
        JavaPPP app = new JavaPPP();
        app.go();
    }

    public void go() {
        FileInputStream fs = null;
        PppParser parser = new PppParser();

        new LcpPacketFactory(parser);
        try {
            fs = new FileInputStream("C:\\ppp_init_frame.bin");
        } catch(FileNotFoundException e) {
            System.err.println("File not found");
        }

        FrameReaderThread readerThread;
        PppStateMachine stateMachine;

        if(fs != null) {
            readerThread = new FrameReaderThread(fs);
            stateMachine = new PppStateMachine();
            readerThread.addFrameEventListener(stateMachine);
            stateMachine.lowerUp();
            stateMachine.open();
            readerThread.start();
            try {
                Thread.sleep(2000);
            } catch(InterruptedException e) {
            }
            ;
            readerThread.interrupt();
        }
    }
}
