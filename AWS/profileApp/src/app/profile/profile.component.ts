import { Component, OnInit } from "@angular/core";
import { APIService } from "../API.service";
import { User } from "../../user";
import { Auth } from "aws-amplify";

@Component({
  selector: "app-profile",
  templateUrl: "./profile.component.html",
  styleUrls: ["./profile.component.scss"]
})
export class ProfileComponent implements OnInit {
  userId: string;
  userName: string;
  user = new User("", "", "", "", "", "");

  constructor(private api: APIService) {}

  ngOnInit() {
    Auth.currentAuthenticatedUser({
      bypassCache: false
    })
      .then(async user => {
        this.userId = user.attributes.sub;
        this.userName = user.username;
      })
      .catch(err => console.log(err));
  }

  async updateProfile() {
    const user = {
      id: this.userId,
      username: this.user.firstName + "_" + this.user.lastName,
      firstName: this.user.firstName,
      lastName: this.user.lastName,
      bio: this.user.aboutMe
    };
    await this.api.CreateUser(user);
  }
}
