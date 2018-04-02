/**
 * 
 */
package com.qiggroup.javappp.packets;

/**
 * @author Nick
 * 
 */
public abstract class Packet {
    
    public abstract int[] generate();

    public abstract void accept(PacketVisitor visitor);

}
