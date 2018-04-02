/**
 * 
 */
package com.qiggroup.javappp.packets;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import com.qiggroup.javappp.packets.lcp.LcpPacketFactory;

/**
 * @author nstevens
 * 
 */
public class PppParser {

    private PacketMap packetFactories;

    public PppParser() {
        packetFactories = new PacketMap(this);
        new LcpPacketFactory(this);
    }

    public Packet parse(final int[] data) {
        // TODO: Handle Protocol compression (8-bit protocol instead of 16-bit)
        int protocol = (data[0] << 8) | data[1];
        int[] payload = Arrays.copyOfRange(data, 2, data.length);
        PacketFactory factory = this.packetFactories.get(protocol);
        return factory.create(payload);
    }

    public abstract class PacketFactory {

        protected PacketFactory(int protocol) {
            packetFactories.put(Integer.valueOf(protocol), this);
        }

        public abstract Packet create(final int[] data);
    }

    public class PacketMap {

        private Map<Integer, PacketFactory> packetFactories;
        private PppParser parent;

        /**
         * Constructs a new PacketMap
         */
        public PacketMap(PppParser parent) {
            this.parent = parent;
            this.packetFactories = new HashMap<Integer, PacketFactory>();
        }

        /**
         * Gets the <code>PacketFactory</code> used to create packets of the
         * type <code>protocol</code>, or returns a newly configured
         * <code>PppPacketUnknownFactory</code> if the type is not recognized.
         */
        public PacketFactory get(int protocol) {
            PacketFactory tryFactory;
            tryFactory = this.packetFactories.get(Integer.valueOf(protocol));
            if(tryFactory == null) {
                tryFactory = new PppPacketUnknownFactory(this.parent, protocol);
                this.packetFactories.put(Integer.valueOf(protocol), tryFactory);
            }
            return tryFactory;
        }

        /**
         * Sets <code>factory</code> as the handler for <code>code</code>.
         */
        protected PacketFactory put(Integer protocol, PacketFactory factory) {
            return this.packetFactories.put(protocol, factory);
        }
    }

}
