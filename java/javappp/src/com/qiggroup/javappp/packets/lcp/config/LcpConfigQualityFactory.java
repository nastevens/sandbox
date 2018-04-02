// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigQualityFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigQuality.QualityProtocol;

/**
 * Factory to create <code>LcpConfigOption</code>s for encapsulating the
 * Quality-Protocol LCP configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigQualityFactory extends LcpPacketFactory.ConfigFactory {

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigQualityFactory(LcpPacketFactory parent) {
        parent.super(LcpConfigQuality.TYPE);
    }

    @Override
    public LcpConfigOption create(final int[] data) {

        QualityProtocol qp;
        int qp_int;

        qp_int = data[1];
        qp_int |= (data[0] << 8);

        switch (qp_int) {
        case 0xC025:
            qp = QualityProtocol.LQR;
            break;
        default:
            qp = QualityProtocol.UNKNOWN;
            break;
        }

        int[] data_field = new int[data.length - 2];
        for (int i = 2; i < data.length; ++i) {
            data_field[i - 2] = data[i];
        }

        return new LcpConfigQuality(qp, data_field);

    }
}
