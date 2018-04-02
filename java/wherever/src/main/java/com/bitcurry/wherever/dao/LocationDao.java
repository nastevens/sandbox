package com.bitcurry.wherever.dao;

import com.bitcurry.wherever.JpaProvider;
import com.bitcurry.wherever.model.Location;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;

/**
 * Created by nickstevens on 4/9/14.
 */
public class LocationDao {

    private final EntityManagerFactory entityManagerFactory;

    public LocationDao(EntityManagerFactory entityManagerFactory) {
        this.entityManagerFactory = entityManagerFactory;
    }

    public Long create(Location location) {
        EntityManager em = entityManagerFactory.createEntityManager();
        em.getTransaction().begin();
        em.persist(location);
        em.getTransaction().commit();
        em.flush();
        Long id = location.getId();
        em.close();
        return id;
    }

    public Location read(Long id) {
        EntityManager em = entityManagerFactory.createEntityManager();
        Location location = em.getReference(Location.class, id);
        em.close();
        return location;
    }

    public void update(Location location) {
        EntityManager em = entityManagerFactory.createEntityManager();
        em.getTransaction().begin();
        em.contains(location);

    }

    public void delete(Location location) {
        EntityManager em = entityManagerFactory.createEntityManager();
        em.getTransaction().begin();
        em.remove(location);
        em.getTransaction().commit();
        em.close();
    }
}
