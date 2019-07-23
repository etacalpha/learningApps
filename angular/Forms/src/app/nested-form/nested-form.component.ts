import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder } from "@angular/forms";

@Component({
  selector: "app-nested-form",
  templateUrl: "./nested-form.component.html",
  styleUrls: ["./nested-form.component.scss"]
})
export class NestedFormComponent implements OnInit {
  myForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    //create a seperate group that can be reused in the form
    const phone = this.fb.group({
      area: [],
      prefix: [],
      line: []
    });

    this.myForm = this.fb.group({
      email: "",
      homePhone: phone,
      cellPhone: phone
    });
  }
}
