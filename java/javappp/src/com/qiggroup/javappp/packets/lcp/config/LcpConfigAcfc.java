// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAcfc.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Authentication-Protocol LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigAcfc extends LcpConfigOption {

    public static final int TYPE = 0x08;
    public static final int LENGTH = 2;

    public LcpConfigAcfc() {

    }

    @Override
    public int[] generate() {
        int[] data = { TYPE, LENGTH };
        return data;
    }

    @Override
    public String toString() {
        return "<ACFC Config>";
    }
}
