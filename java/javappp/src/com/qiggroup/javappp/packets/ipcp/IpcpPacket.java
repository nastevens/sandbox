// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      IpcpPacket.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.ipcp;

/**
 * TODO: (Document type)
 *
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public interface IpcpPacket {
    public void accept(IpcpPacketVisitor visitor);
}
