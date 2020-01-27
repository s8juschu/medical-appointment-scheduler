import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  loggedIn = false;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  public get currentLoggendIn(): boolean {
    return this.loggedIn;
  }

  async login(username: string, password: string) {
    const res = await this.http
      .post(
        '/rest-auth/login/',
        {
          email: username,
          password
        },
        { observe: 'response' }
      )
      .toPromise();

    if (res.status === 200) {
      this.loggedIn = true;
      this.redirect();
    } else {
      this.loggedIn = false;
      throw new Error();
    }
  }

  autoLogin() {
    this.http.get('/employees/', { observe: 'response' }).subscribe(res => {
      this.loggedIn = res.status === 200;
      if (this.loggedIn) {
        this.redirect();
      }
    });
  }

  logout() {
    this.loggedIn = false;
    this.http
      .post(
        '/api-auth/logout/',
        {},
        { observe: 'response', responseType: 'text' }
      )
      .subscribe(res => {
        if (res.status === 200) {
          this.loggedIn = false;
          this.router.navigate(['/login']);
        }
      });
  }

  private redirect() {
    const redirekt = this.route.snapshot.queryParamMap.get('returnUrl') || '/';
    const params = this.route.snapshot.queryParamMap.get('params') || '{}';
    this.router.navigate([redirekt], { queryParams: JSON.parse(params) });
  }
}
