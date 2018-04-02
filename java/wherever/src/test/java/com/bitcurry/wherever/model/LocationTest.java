package com.bitcurry.wherever.model;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import java.net.MalformedURLException;
import java.net.URI;

/**
 *
 */
public class LocationTest {
    public static void main(String[] args) {
        EntityManagerFactory entityManagerFactory = Persistence.createEntityManagerFactory("com.bitcurry.wherever");
        EntityManager entityManager = entityManagerFactory.createEntityManager();
        try {
            entityManager.getTransaction().begin();
            entityManager.persist(new Location(
                    "Uncle Franky's",
                    URI.create("http://unclefrankys.com").toURL(),
                    URI.create("http://yelp.com/some-page").toURL()));
            entityManager.persist(new Location(
                    "Chipotle",
                    URI.create("http://chipotle.com").toURL(),
                    URI.create("http://yelp.com/other-page").toURL()));
            entityManager.getTransaction().commit();
        } catch (MalformedURLException e) {
            System.out.println(e.getMessage());
        }
        entityManager.close();
        entityManagerFactory.close();
    }
}
