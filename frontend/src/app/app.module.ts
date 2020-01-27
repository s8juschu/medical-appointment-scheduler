import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule, NgbTabsetModule } from '@ng-bootstrap/ng-bootstrap';
import { CKEditorModule } from '@ckeditor/ckeditor5-angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { EmployeesComponent } from './components/employees/employees.component';
import { ManageEmployeesComponent } from './components/manage-employees/manage_employees.component';
import { ArchivComponent } from './components/archiv/archiv.component';
import { TopbarComponent } from './components/topbar/topbar.component';
import { AppointmentsComponent } from './components/appointments/appointments.component';
import { Routes, RouterModule } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { AuthGuard } from './guards/auth.guard';
import { TemplatesComponent } from './components/templates/templates.component';
import { ManageTemplatesComponent } from './components/manage-templates/manage-templates.component';

const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  {
    path: 'mitarbeiter',
    component: EmployeesComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'anschreiben',
    component: TemplatesComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'anschreiben_verwalten',
    component: ManageTemplatesComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'archiv',
    component: ArchivComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'termine',
    component: AppointmentsComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'mitarbeiter_verwalten',
    component: ManageEmployeesComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'login',
    component: LoginComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    SidebarComponent,
    EmployeesComponent,
    ManageEmployeesComponent,
    ArchivComponent,
    TopbarComponent,
    AppointmentsComponent,
    LoginComponent,
    HomeComponent,
    TemplatesComponent,
    ManageTemplatesComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFTOKEN'
    }),
    AppRoutingModule,
    NgbModule,
    RouterModule.forRoot(routes),
    MatIconModule,
    FontAwesomeModule,
    MatMenuModule,
    MatButtonModule,
    BrowserAnimationsModule,
    FormsModule,
    NgbTabsetModule,
    ReactiveFormsModule,
    CKEditorModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
