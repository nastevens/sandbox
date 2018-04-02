// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigQuality.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating the Quality-Protocol LCP
 * configure option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigQuality extends LcpConfigOption {

    public static final int TYPE = 0x04;

    public static enum QualityProtocol {
        LQR, UNKNOWN
    };

    private QualityProtocol qp;
    private int[] data_field;

    public LcpConfigQuality(QualityProtocol qp, int[] data_field) {
        this.qp = qp;
        this.data_field = data_field;
    }

    @Override
    public int[] generate() {

        int[] data = new int[4 + data_field.length];

        data[0] = TYPE;
        data[1] = data.length;

        int qp_int;
        switch (qp) {
        case LQR:
            qp_int = 0xC025;
            break;
        default:
            qp_int = 0;
            break;
        }

        data[2] = (qp_int >> 8) & 0xFF;
        data[3] = qp_int & 0xFF;

        for (int i = 4; i < (4 + data_field.length); ++i) {
            data[i] = data_field[i - 4];
        }

        return data;

    }

    @Override
    public String toString() {

        String qp_string;

        switch (qp) {
        case LQR:
            qp_string = "LQR";
            break;
        default:
            qp_string = "Unknown";
            break;
        }

        return ("<Quality Config: Type " + qp_string + ">");

    }

}
