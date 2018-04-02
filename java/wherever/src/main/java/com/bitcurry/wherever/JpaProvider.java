package com.bitcurry.wherever;

import org.glassfish.jersey.server.spi.AbstractContainerLifecycleListener;
import org.glassfish.jersey.server.spi.Container;

import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.servlet.ServletContext;
import javax.ws.rs.core.Context;
import javax.ws.rs.ext.Provider;

/**
 *
 */

@Provider
public class JpaProvider extends AbstractContainerLifecycleListener {

    private static final String ENTITY_MANAGER_FACTORY = "entityManagerFactory";
    private static final String PERSISTENCE_UNIT_NAME = "com.bitcurry.wherever";

    @Context
    private ServletContext servletContext;

    private EntityManagerFactory entityManagerFactory;

    public JpaProvider() {
        System.out.println("JpaProvider created");
    }

    @Override
    public void onStartup(Container container) {
        // Initialize EntityManagerFactory for JPA
        System.out.println("Setting up JPA");
        entityManagerFactory = Persistence.createEntityManagerFactory(PERSISTENCE_UNIT_NAME);
        servletContext.setAttribute(ENTITY_MANAGER_FACTORY, entityManagerFactory);
    }

    @Override
    public void onShutdown(Container container) {
        // Remove EntityManagerFactory for JPA
        System.out.println("Shutting down JPA");
        servletContext.removeAttribute(ENTITY_MANAGER_FACTORY);
        entityManagerFactory.close();
        entityManagerFactory = null;

    }

    public static EntityManagerFactory getEntityManagerFactory(ServletContext servletContext) {
        return (EntityManagerFactory)servletContext.getAttribute(ENTITY_MANAGER_FACTORY);
    }
}
