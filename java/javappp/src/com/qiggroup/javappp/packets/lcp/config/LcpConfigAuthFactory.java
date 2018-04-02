// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAuthFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigAuth.AuthType;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Authentication-Protocol LCP configure option code.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigAuthFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     * 
     * @author Nick Stevens <nstevens@qiggroup.com>
     */
    public LcpConfigAuthFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigAuth.TYPE);
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.PacketFactory#create(int[])
     */
    @Override
    public LcpConfigOption create(final int[] data) {

        AuthType auth;
        int auth_int;

        auth_int = data[1];
        auth_int |= (data[0] << 8);

        switch (auth_int) {
        case 0xC023:
            auth = AuthType.PAP;
            break;
        case 0xC223:
            auth = AuthType.CHAP;
            break;
        default:
            auth = AuthType.UNKNOWN;
            break;
        }

        int[] data_field = new int[data.length - 2];
        for (int i = 2; i < data.length; ++i) {
            data_field[i - 2] = data[i];
        }

        return new LcpConfigAuth(auth, data_field);

    }
}