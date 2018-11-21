package tech.archDev.springBootVueCRUD.Rest;

import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
import org.springframework.stereotype.Component;
import tech.archDev.springBootVueCRUD.Domains.Todo;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.core.Ordered;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import tech.archDev.springBootVueCRUD.Repositories.TodoRepository;

import java.util.Collections;
import java.util.stream.Stream;

/**
 * IDs are not returned by RestRepository by default. I like them exposed so that the client can easily find
 * the ID of created and listed resources.
 * */
@Component
public class RestRepositoryConfigurator implements RepositoryRestConfigurer {

    @Override
    public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config) {
        config.exposeIdsFor(Todo.class);
    }

    // Bootstrap some test data into the in-memory database
    @Bean
    ApplicationRunner init(TodoRepository repository) {
        return args -> {
            Stream.of("Buy milk", "Eat pizza", "Write tutorial", "Study Vue.js", "Go kayaking").forEach(name -> {
                Todo todo = new Todo();
                todo.setTitle(name);
                repository.save(todo);
            });
            repository.findAll().forEach(System.out::println);
        };
    }

    // Fix the CORS errors
    @Bean
    public FilterRegistrationBean simpleCorsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        // *** URL below needs to match the Vue client URL and port ***
        config.setAllowedOrigins(Collections.singletonList("http://localhost:8080"));
        config.setAllowedMethods(Collections.singletonList("*"));
        config.setAllowedHeaders(Collections.singletonList("*"));
        source.registerCorsConfiguration("/**", config);
        FilterRegistrationBean bean = new FilterRegistrationBean<>(new CorsFilter(source));
        bean.setOrder(Ordered.HIGHEST_PRECEDENCE);
        return bean;
    }
}
