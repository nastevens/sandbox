// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      PppEvents.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.protocol.ppp;

import com.qiggroup.javafsm.api.Event;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public final class PppEvents {
    public static final Event UP = new Event("Up");
    public static final Event DOWN = new Event("Down");
    public static final Event OPEN = new Event("Open");
    public static final Event CLOSE = new Event("Close");
    public static final Event TO_PLUS = new Event("TO+");
    public static final Event TO_MINUS = new Event("TO-");
    public static final Event RCR_PLUS = new Event("RCR+");
    public static final Event RCR_MINUS = new Event("RCR-");
    public static final Event RCA = new Event("RCA");
    public static final Event RCN = new Event("RCN");
    public static final Event RTR = new Event("RTR");
    public static final Event RTA = new Event("RTA");
    public static final Event RUC = new Event("RUC");
    public static final Event RXJ_PLUS = new Event("RXJ+");
    public static final Event RXJ_MINUS = new Event("RXJ-");
    public static final Event RXR = new Event("RXR");
}
