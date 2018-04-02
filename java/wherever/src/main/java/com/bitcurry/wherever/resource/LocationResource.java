package com.bitcurry.wherever.resource;

import com.bitcurry.wherever.JpaProvider;
import com.bitcurry.wherever.dao.LocationDao;
import com.bitcurry.wherever.model.Location;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.servlet.ServletContext;
import javax.ws.rs.BeanParam;
import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import java.util.List;

/**
 *
 */

@Path("/locations")
public class LocationResource {

    private final EntityManagerFactory entityManagerFactory;
    private final LocationDao dao;

    public LocationResource(@Context ServletContext servletContext) {
        entityManagerFactory = JpaProvider.getEntityManagerFactory(servletContext);
        dao = new LocationDao(entityManagerFactory);
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<Location> getAllLocations() {
        EntityManager em = entityManagerFactory.createEntityManager();
        em.getTransaction().begin();
        List<Location> result = em.createQuery("from Location", Location.class).getResultList();
        em.getTransaction().commit();
        em.close();
        return result;
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Location getLocationById(@PathParam("id") Long id) {
        return dao.read(id);
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Long createLocation(@BeanParam Location location) {
        // TODO: Is BeanParam the correct param to use?
        return dao.create(location);
    }

    @POST
    @Path("/{id}")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public void updateLocation(@BeanParam Location location, @PathParam("id") Long id) {
        // TODO: Question - require ID in update JSON, or use URL path parameter?
        dao.update(location);
    }

    @DELETE
    @Path("/{id}")
    public void deleteLocation(@PathParam("id") Long id) {
        dao.delete(dao.read(id));
    }

}
