import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";

@Component({
  selector: "app-basic-form",
  templateUrl: "./basic-form.component.html",
  styleUrls: ["./basic-form.component.scss"]
})
export class BasicFormComponent implements OnInit {
  //declare variable for form class(FormGroup)
  myForm: FormGroup;

  //create service to to make and control FormGroup
  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    // create form object of type FomGroup with FormBuilder
    this.myForm = this.fb.group({
      email: "",
      message: "",
      career: ""
    });
    // update form object with everychange by calling method valueChanges on form Object
    this.myForm.valueChanges.subscribe(console.log);
  }
}
