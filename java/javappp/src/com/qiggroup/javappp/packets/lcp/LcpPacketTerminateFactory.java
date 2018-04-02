// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketTerminateFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import com.qiggroup.javappp.packets.Packet;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketTerminateFactory extends LcpPacketFactory.PacketFactory {

    public static enum Types {
        REQ(0x05), ACK(0x06);
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
     * TODO: (Document constructor)
     */
    public LcpPacketTerminateFactory(LcpPacketFactory parent, Types type) {
        parent.super(type.getCode());
        this.type = type;
    }

    /**
     * @see com.qiggroup.javappp.packets.lcp.LcpPacketFactory.PacketFactory#create(int[], int)
     */
    @Override
    public Packet create(int[] data, int identifier) {

        Packet pkt;
        switch(this.type) {
            case REQ:
                pkt = new LcpPacketTerminateReq(identifier, data);
                break;
            case ACK:
                pkt = new LcpPacketTerminateAck(identifier, data);
                break;
            default:
                pkt = null;
        }
        return pkt;
    }

}
