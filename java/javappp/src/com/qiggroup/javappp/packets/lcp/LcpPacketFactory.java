// Project:   JavaPPP - a pure Java implementation of the PPP protocol
// File:      LcpPacketFactory.java
// Copyright: 2012 QiG Group

package com.qiggroup.javappp.packets.lcp;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import com.qiggroup.javappp.packets.Packet;
import com.qiggroup.javappp.packets.PppParser;
import com.qiggroup.javappp.packets.lcp.LcpPacketConfigureFactory.Types;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigAccmFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigAcfcFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigAuthFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigMagicNumFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigMruFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigOption;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigPfcFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigQualityFactory;
import com.qiggroup.javappp.packets.lcp.config.LcpConfigUnknownFactory;

/**
 * Factory to create <code>LcpPacket</code>s for encapsulating LCP packets.
 * 
 * @author Nick Stevens <nstevens@qiggroup.com>
 */
public class LcpPacketFactory extends PppParser.PacketFactory {

    private LcpPacketMap packetFactories;
    private LcpConfigMap configFactories;

    /**
     * Construct <code>LcpPacketFactory</code> and register it with the
     * <code>PppParser</code>.
     */
    public LcpPacketFactory(PppParser parent) {
        parent.super(0xc021);
        packetFactories = new LcpPacketMap(this);
        configFactories = new LcpConfigMap(this);

        // Register LCP configuration option factories
        new LcpConfigMruFactory(this);
        new LcpConfigAccmFactory(this);
        new LcpConfigAuthFactory(this);
        new LcpConfigQualityFactory(this);
        new LcpConfigMagicNumFactory(this);
        new LcpConfigPfcFactory(this);
        new LcpConfigAcfcFactory(this);

        // Register LCP packet parser factories
        new LcpPacketConfigureFactory(this, configFactories, Types.REQ);
        new LcpPacketConfigureFactory(this, configFactories, Types.ACK);
        new LcpPacketConfigureFactory(this, configFactories, Types.NAK);
        new LcpPacketConfigureFactory(this, configFactories, Types.REJ);
        new LcpPacketTerminateFactory(this, LcpPacketTerminateFactory.Types.REQ);
        new LcpPacketTerminateFactory(this, LcpPacketTerminateFactory.Types.ACK);
        
    }

    @Override
    public Packet create(final int data[]) {
        int code = data[0];
        int identifier = data[1];
        // Skip "length" field in bytes 2 and 3
        int[] payload = Arrays.copyOfRange(data, 4, data.length);
        PacketFactory pktFactory;
        pktFactory = this.packetFactories.get(code);
        return pktFactory.create(payload, identifier);
    }
    
    

    public abstract class PacketFactory {

        /**
         * Construct <code>PacketFactory</code> and register it as the Factory
         * to process packet codes given by <code>code</code>
         * 
         * @param code config code this Factory handles
         */
        protected PacketFactory(int code) {
            packetFactories.put(Integer.valueOf(code), this);
        }

        /**
         * Abstract method that will receive the payload of each LCP packet as
         * it is parsed by the PppParser.
         * 
         * @param data payload of LCP packet (no code, length, or id fields)
         * @param identifier id received in packet
         */
        public abstract Packet create(final int[] data,
                final int identifier);
    }
    
    
    
    public class LcpPacketMap {
        
        private Map<Integer, PacketFactory> packetFactories;
        private LcpPacketFactory parent;
        
        /**
         * Constructs a new LcpPacketMap
         */
        public LcpPacketMap(LcpPacketFactory parent) {
            this.parent = parent;
            this.packetFactories = new HashMap<Integer, PacketFactory>();
        }
        
        /**
         * Gets the <code>PacketFactory</code> used to create
         * <code>LcpPacket</code>s of the type <code>type</code>, or returns a
         * newly configured <code>LcpPacketUnknownFactory</code> if the type is
         * not recognized.
         */
        public PacketFactory get(int code) {
            PacketFactory tryFactory;
            tryFactory = this.packetFactories.get(Integer.valueOf(code));
            if(tryFactory == null) {
                tryFactory = new LcpPacketUnknownFactory(this.parent, code);
                this.packetFactories.put(Integer.valueOf(code), tryFactory);
            }
            return tryFactory;
        }
        
        /**
         * Sets <code>factory</code> as the handler for <code>code</code>.
         */
        protected PacketFactory put(Integer code, PacketFactory factory) {
            return this.packetFactories.put(code, factory);
        }
    }

    
    
    public abstract class ConfigFactory {

        /**
         * Construct <code>ConfigFactory</code> and register it as the Factory
         * to process config types given by <code>type</code>
         * 
         * @param type config code this Factory handles
         */
        protected ConfigFactory(int type) {
            configFactories.put(Integer.valueOf(type), this);
        }

        /**
         * Abstract method that will receive the payload of each configuration
         * item as it is received by the LCP packet parser
         * 
         * @param data payload of config option (no type or length fields)
         */
        public abstract LcpConfigOption create(final int[] data);
    }
    
    
    
    public class LcpConfigMap {
        
        private Map<Integer, ConfigFactory> configFactories;
        private LcpPacketFactory parent;
        
        /**
         * Constructs a new LcpConfigMap
         */
        public LcpConfigMap(LcpPacketFactory parent) {
            this.parent = parent;
            this.configFactories = new HashMap<Integer, ConfigFactory>();
        }
        
        /**
         * Gets the <code>ConfigFactory</code> used to create
         * <code>LcpConfigOption</code>s of the type <code>type</code>, or
         * returns a newly configured <code>LcpConfigUnknownFactory</code> set
         * up to match the unrecognized code.
         */
        public ConfigFactory get(int type) {
            ConfigFactory tryFactory;
            tryFactory = this.configFactories.get(Integer.valueOf(type));
            if(tryFactory == null) {
                tryFactory = new LcpConfigUnknownFactory(this.parent, type);
                this.configFactories.put(Integer.valueOf(type), tryFactory);
            }
            return tryFactory;
        }
        
        /**
         * Sets <code>factory</code> as the handler for type <code>type</code>.
         */
        protected ConfigFactory put(Integer type, ConfigFactory factory) {
            return this.configFactories.put(type, factory);
        }
    }
}
