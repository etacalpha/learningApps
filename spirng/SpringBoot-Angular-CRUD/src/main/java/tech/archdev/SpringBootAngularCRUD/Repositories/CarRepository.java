package tech.archdev.SpringBootAngularCRUD.Repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import tech.archdev.SpringBootAngularCRUD.Domains.Car;

@RepositoryRestResource
public interface CarRepository extends JpaRepository<Car, Long> {
}
