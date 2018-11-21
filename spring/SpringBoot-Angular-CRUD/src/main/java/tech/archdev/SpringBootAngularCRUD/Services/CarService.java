package tech.archdev.SpringBootAngularCRUD.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import tech.archdev.SpringBootAngularCRUD.Domains.Car;
import tech.archdev.SpringBootAngularCRUD.Repositories.CarRepository;

import java.util.ArrayList;
import java.util.List;

@Service
public class CarService {

    @Autowired
    private CarRepository carRepository;

    // Create
    public void createCar(String name){
        Car newCar = new Car();
        newCar.setName(name);
        carRepository.save(newCar);
    }

    //save
    public void saveCar(Car car){
        carRepository.save(car);
    }

    // Read
    public List<Car> getAllCars(){
        ArrayList<Car> allCars = new ArrayList<>();
        allCars.addAll(carRepository.findAll());
        return allCars;
    }

    // Update
    public void updateCar(String name, Long id){
        Car chosenCar = getById(id);
        chosenCar.setName(name);
        carRepository.save(chosenCar);
    }

    //Delete
    public void deleteCar(Long id){
        Car chosenCar = getById(id);
        carRepository.delete(chosenCar);
    }

    //getById
    public Car getById(long id){
        Car chosenCar = carRepository.getOne(id);
        return chosenCar;
    }

}

