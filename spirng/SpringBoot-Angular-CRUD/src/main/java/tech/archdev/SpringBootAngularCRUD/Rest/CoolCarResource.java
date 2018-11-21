package tech.archdev.SpringBootAngularCRUD.Rest;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.archdev.SpringBootAngularCRUD.Domains.Car;
import tech.archdev.SpringBootAngularCRUD.Services.CarService;

import java.util.Collection;
import java.util.stream.Collectors;

@RestController
public class CoolCarResource {
    private CarService service;

    public CoolCarResource(CarService service) {
        this.service = service;
    }

    @GetMapping("/cool-cars")
    public Collection<Car> coolCars() {
        return service.getAllCars().stream()
                .filter(this::isCool)
                .collect(Collectors.toList());
    }

    private boolean isCool(Car car) {
        return !car.getName().equals("AMC Gremlin") &&
                !car.getName().equals("Triumph Stag") &&
                !car.getName().equals("Ford Pinto") &&
                !car.getName().equals("Yugo GV");
    }
}

