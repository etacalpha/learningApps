package tech.archDev.springBootVueCRUD.Repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import tech.archDev.springBootVueCRUD.Domains.Todo;

@RepositoryRestResource
public interface TodoRepository extends JpaRepository<Todo, Long> {}


