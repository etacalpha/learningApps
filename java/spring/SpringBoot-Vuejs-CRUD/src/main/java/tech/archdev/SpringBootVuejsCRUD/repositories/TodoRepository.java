package tech.archdev.SpringBootVuejsCRUD.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import tech.archdev.SpringBootVuejsCRUD.domains.Todo;

@RepositoryRestResource
public interface TodoRepository extends JpaRepository<Todo, Long> {}

