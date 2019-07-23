import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";

@Component({
  selector: "app-valid-form",
  templateUrl: "./valid-form.component.html",
  styleUrls: ["./valid-form.component.scss"]
})
export class ValidFormComponent implements OnInit {
  myForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.myForm = this.fb.group({
      // when using validators, create an array with default value at index 0, followed by
      // an array of validators
      email: ["", [Validators.required, Validators.email]],

      //.patter take a regular expression to describe the format of accepted text
      password: [
        "",
        [
          Validators.required,
          Validators.pattern("^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-z0-9]+)$")
        ]
      ],
      age: [null, [Validators.required, Validators.min(2), Validators.max(65)]],
      agree: [false, [Validators.requiredTrue]]
    });
  }

  private get email() {
    return this.myForm.get("email");
  }
  private get password() {
    return this.myForm.get("password");
  }
  private get age() {
    return this.myForm.get("age");
  }
  private get agree() {
    return this.myForm.get("agree");
  }
}
