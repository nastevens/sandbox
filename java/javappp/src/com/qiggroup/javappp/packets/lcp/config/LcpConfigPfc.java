// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigPfc.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating the Protocol-Field-Compression
 * (PFC) LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigPfc extends LcpConfigOption {

    public static final int TYPE = 0x07;
    public static final int LENGTH = 2;

    public LcpConfigPfc() {

    }

    @Override
    public int[] generate() {

        int[] data = { TYPE, LENGTH };
        return data;

    }

    @Override
    public String toString() {
        return "<PFC Config>";
    }

}
