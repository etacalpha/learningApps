package tech.archdev.SpringBootAngularCRUD;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import tech.archdev.SpringBootAngularCRUD.Services.CarService;

import java.util.stream.Stream;

@SpringBootApplication
public class SpringBootAngularCrudApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootAngularCrudApplication.class, args);
	}

	@Bean
	ApplicationRunner init(CarService service) {
		return args -> {
			Stream.of("Ferrari", "Jaguar", "Porsche", "Lamborghini", "Bugatti",
					"AMC Gremlin", "Triumph Stag", "Ford Pinto", "Yugo GV").forEach(name -> {
				service.createCar(name);
			});
			service.getAllCars().forEach(System.out::println);
		};
	}
}

