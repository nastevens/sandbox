// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAcfcFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Address-and-Control-Field-Compression (ACFC) LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigAcfcFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigAcfcFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigAcfc.TYPE);
    }

    @Override
    public LcpConfigOption create(final int[] data) {
        return new LcpConfigAcfc();
    }

}
