// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigAuth.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating the Authentication-Protocol
 * LCP configure option code.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpConfigAuth extends LcpConfigOption {

    public static final int TYPE = 0x03;

    public static enum AuthType {
        PAP, CHAP, UNKNOWN
    };

    private AuthType auth;
    private int[] data_field;

    /**
     * TODO: (Document constructor)
     */
    public LcpConfigAuth(AuthType auth, int[] data_field) {
        this.auth = auth;
        this.data_field = data_field;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.config.LcpConfigOption#generate()
     */
    @Override
    public int[] generate() {

        int[] data = new int[4 + data_field.length];

        data[0] = TYPE;
        data[1] = data.length;

        int auth_int;
        switch (auth) {
        case PAP:
            auth_int = 0xC023;
            break;
        case CHAP:
            auth_int = 0xC223;
            break;
        default:
            auth_int = 0;
            break;
        }

        data[2] = (auth_int >> 8) & 0xFF;
        data[3] = auth_int & 0xFF;

        for (int i = 4; i < (4 + data_field.length); ++i) {
            data[i] = data_field[i - 4];
        }

        return data;

    }

    @Override
    public String toString() {

        String auth_string;

        switch (auth) {
        case PAP:
            auth_string = "PAP";
            break;
        case CHAP:
            auth_string = "CHAP";
            break;
        default:
            auth_string = "Unknown";
            break;
        }

        return ("Auth config: Auth type " + auth_string);
    }

}
