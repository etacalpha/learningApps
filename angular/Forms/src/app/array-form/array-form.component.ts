import { Component, OnInit } from "@angular/core";
import { FormGroup, FormBuilder, FormArray } from "@angular/forms";

@Component({
  selector: "app-array-form",
  templateUrl: "./array-form.component.html",
  styleUrls: ["./array-form.component.scss"]
})
export class ArrayFormComponent implements OnInit {
  myForm: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    // use method array(FormBuilder.array(initial value)) to create and array of values for a field in a form group
    this.myForm = this.fb.group({
      email: "",
      phone: this.fb.array([])
    });
  }

  // getter method to get phone array from reactive form
  get phoneForms(): FormArray {
    return this.myForm.get("phones") as FormArray;
  }

  // a button to add field to a form

  addPhone(): void {
    //crate from goup to display
    const phone = this.fb.group({
      area: [],
      prefix: [],
      line: []
    });

    //push phone formGroup into myForm formGroup phone array
    this.phoneForms.push(phone);
  }

  // removes phone formGroup from reactive form
  deletePhone(index: number): void {
    this.phoneForms.removeAt(index);
  }
}
