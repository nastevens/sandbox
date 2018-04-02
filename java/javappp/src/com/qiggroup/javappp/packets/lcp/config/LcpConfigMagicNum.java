// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpConfigMagicNum.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp.config;

/**
 * <code>LcpConfigOption</code> for encapsulating the Magic-Number LCP configure
 * option code.
 * 
 * @author Tyler Schloesser <tschloesser@qiggroup.com>
 */
public class LcpConfigMagicNum extends LcpConfigOption {

    public static final int TYPE = 0x05;
    public static final int LENGTH = 6;

    private int magic_number;

    public LcpConfigMagicNum(int magic_number) {
        this.magic_number = magic_number;
    }

    @Override
    public int[] generate() {

        int[] data = new int[LENGTH];
        data[0] = TYPE;
        data[1] = LENGTH;

        data[2] = (magic_number >> 24) & 0xFF;
        data[3] = (magic_number >> 16) & 0xFF;
        data[4] = (magic_number >> 8) & 0xFF;
        data[5] = magic_number & 0xFF;

        return data;

    }

    @Override
    public String toString() {
        return ("<Magic Number Config Value 0x"
                + Integer.toHexString(magic_number) + ">");
    }

}
