// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigPfcFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Protocol-Field-Compression (PFC) LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigPfcFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigPfcFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigPfc.TYPE);
    }

    @Override
    public LcpConfigOption create(final int[] data) {
        return new LcpConfigPfc();
    }

}
