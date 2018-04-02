// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketConfigureFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import java.util.Arrays;

import com.qiggroup.javappp.packets.lcp.config.LcpConfigOption;

/**
 * Factory to create <code>LcpPacketConfigure</code>s for encapsulating LCP
 * Configuration-type packets.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketConfigureFactory extends LcpPacketFactory.PacketFactory {

    private LcpPacketFactory.LcpConfigMap configFactories;
    
    public static enum Types {
        REQ(0x01), ACK(0x02), NAK(0x03), REJ(0x04);
        private int code;

        private Types(int code) {
            this.code = code;
        }

        public int getCode() {
            return this.code;
        }
    }

    private Types type;

    /**
     * Construct <code>LcpPacketConfigureFactory</code> and register it with the
     * <code>LcpPacketFactory</code>.
     */
    public LcpPacketConfigureFactory(LcpPacketFactory parent,
            LcpPacketFactory.LcpConfigMap configFactories, Types type) {
        parent.super(type.getCode());
        this.configFactories = configFactories;
        this.type = type;
    }

    /**
     * Parses an LCP Configure REQUEST/ACK/NAK/REJECT packet.
     * 
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketConfigure#create()
     */
    @Override
    public LcpPacketConfigure create(final int[] data, final int identifier) {
        
        LcpPacketConfigure pkt;
        switch(this.type) {
            case REQ:
                pkt = new LcpPacketConfigureReq(identifier);
                break;
            case ACK:
                pkt = new LcpPacketConfigureAck(identifier);
                break;
            case NAK:
                pkt = new LcpPacketConfigureNak(identifier);
                break;
            case REJ:
                pkt = new LcpPacketConfigureRej(identifier);
                break;
            default:
                return null;
        }

        LcpConfigOption option;
        LcpPacketFactory.ConfigFactory cfgFactory;
        int optionType, optionLength, i = 0;
        int[] optionPacket;

        while(i < data.length) {
            optionType = data[i];
            optionLength = data[i+1];
            optionPacket = Arrays.copyOfRange(data, i + 2, i + optionLength);
            cfgFactory = this.configFactories.get(optionType);
            option = cfgFactory.create(optionPacket);
            pkt.addConfigOption(option);
            i += optionLength;
        }
        return pkt;
    }

}
