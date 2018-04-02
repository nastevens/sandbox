package com.bitcurry.wherever;

import com.bitcurry.wherever.resource.LocationResource;
import org.glassfish.jersey.server.ResourceConfig;

import javax.servlet.ServletContext;
import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Context;

/**
 *
 */

@ApplicationPath("/api/v1")
public class WhereverApiApplication extends ResourceConfig {

    public WhereverApiApplication(final @Context ServletContext servletContext) {

        // Initialize Hibernate JPA provider
        register(JpaProvider.class);

        // Add application resource classes
        register(LocationResource.class);

    }

}
