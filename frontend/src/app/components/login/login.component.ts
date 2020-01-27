import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from 'src/app/services';

interface Alert {
  type: string;
  message: string;
}

const ALERTS: Alert[] = [
  {
    type: 'danger',
    message: 'Es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.'
  }
];

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  constructor(private loginService: AuthenticationService) {}

  alerts: Alert[];

  login(username: string, password: string) {
    this.loginService
      .login(username, password)
      .then()
      .catch(() => this.newAlert());
  }

  ngOnInit() {
    this.loginService.autoLogin();
  }

  close(alert: Alert) {
    this.alerts.splice(this.alerts.indexOf(alert), 1);
  }

  newAlert() {
    this.alerts = Array.from(ALERTS);
  }
}
