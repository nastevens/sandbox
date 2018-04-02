// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppActions.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import com.sun.istack.internal.logging.Logger;

/**
 * TODO: (Document type)
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
// TODO: Probably turn pppState into a strategy (to handle IPCP)
public class PppActions {

    private static Logger logger = Logger.getLogger(PppActions.class);
    private PppStateMachine pppState;

    public PppActions(PppStateMachine pppState) {
        this.pppState = pppState;
    }

    /**
     * IRC = Initialize Restart Count
     */
    public class ActionIrc implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrc");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * IRC = Initialize Restart Count SCR = Send Configure Request
     */
    public class ActionIrcScr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrcScr");
            pppState.sendConfigureReq();

            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * IRC = Initialize Restart Count SCR = Send Configure Request SCA = Send
     * Configure Ack
     */
    public class ActionIrcScrSca implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrcScrSca");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * IRC = Initialize Restart Count SCR = Send Configure Request SCN = Send
     * Configure Nak
     */
    public class ActionIrcScrScn implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrcScrScn");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * IRC = Initialize Restart Count STR = Send Terminate Request
     */
    public class ActionIrcStr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrcStr");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * IRC = Initialize Restart Count TLU = This Layer Up
     */
    public class ActionIrcTlu implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionIrcTlu");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SCA = Send Configure Ack
     */
    public class ActionSca implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionSca");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SCA = Send Configure Ack TLU = This Layer Up
     */
    public class ActionScaTlu implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionScaTlu");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SCJ = Send Code Reject
     */
    public class ActionScj implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionScj");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SCN = Send Configure Nak
     */
    public class ActionScn implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionScn");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SCR = Send Configure Request
     */
    public class ActionScr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionScr");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * SER = Send Echo Reply
     */
    public class ActionSer implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionSer");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * STA = Send Terminate Ack
     */
    public class ActionSta implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionSta");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * STR = Send Terminate Request
     */
    public class ActionStr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionStr");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down
     */
    public class ActionTld implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTld");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down IRC = Initialize Restart Count STR = Send Terminate
     * Request
     */
    public class ActionTldIrcStr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTldIrcStr");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down
     */
    public class ActionTldScr implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTldScr");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down SCR = Send Configure Request SCA = Send Configure
     * Ack
     */
    public class ActionTldScrSca implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTldScrSca");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down SCR = Send Configure Request SCN = Send Configure
     * Nak
     */
    public class ActionTldScrScn implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTldScrScn");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLD = This Layer Down ZRC = Zero Restart Count STA = Send Terminate Ack
     */
    public class ActionTldZrcSta implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTldZrcSta");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLF = This Layer Finished
     */
    public class ActionTlf implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTlf");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }

    /**
     * TLS = This Layer Started
     */
    public class ActionTls implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            logger.info("Action triggered: ActionTls");
            // throw new UnsupportedOperationException("Not yet implemented");
        }
    }
}
