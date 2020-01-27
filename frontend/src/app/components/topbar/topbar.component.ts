import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { faCogs } from '@fortawesome/free-solid-svg-icons';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { AuthenticationService } from 'src/app/services';

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.css']
})
export class TopbarComponent implements OnInit {
  faSearch = faSearch;
  faCogs = faCogs;
  faSignOutAlt = faSignOutAlt;
  faBars = faBars;
  constructor(private authService: AuthenticationService) {}

  logout() {
    this.authService.logout();
  }

  ngOnInit() {}
}
