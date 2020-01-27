import { Component, OnInit } from '@angular/core';
import { IAppointment, IEmployee } from 'src/app/types';
import { EmployeesService } from 'src/app/services';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AppointmentsService } from '../../services/appointments.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  employees: IEmployee[];

  constructor(
    private employeeService: EmployeesService,
    private modalService: NgbModal,
    private router: Router
  ) {}

  ngOnInit() {
    this.updateEmployeeList();
  }

  // Modal for letter generation
  generateModal(content, employeeId) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.router.navigate(['/anschreiben'], {
          queryParams: { employee: employeeId }
        });
      })
      .catch(_ => {});
  }

  // Converts a DB String to a JS Date
  StringToDate(str: string): Date {
    const buf = str.split('.');
    const year = Number.parseInt(buf[2], 10);
    const month = Number.parseInt(buf[1], 10);
    const day = Number.parseInt(buf[0], 10);
    return new Date(year, month, day);
  }

  // Converts a JS Date to a DB String
  DateToString(date: Date): string {
    const day = date.getDay();
    const month = date.getMonth();
    const year = date.getFullYear();

    return (
      String(day + 100).substr(1, 2) +
      '.' +
      String(month + 100).substr(1, 2) +
      '.' +
      String(year)
    );
  }

  // Modal for hiding employees on the home component
  hideModal(content, employee: IEmployee) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        const date = this.StringToDate(employee.next_reminder);
        date.setMonth(date.getMonth() + employee.reminder_interval);
        this.employeeService
          .update(employee.id, {
            next_reminder: this.DateToString(date)
          })
          .subscribe(() => {
            this.updateEmployeeList();
          });
      })
      .catch(_ => {});
  }

  // Update cached Employees in the needed interval
  updateEmployeeList() {
    const now = new Date();

    const aMonthBefore = new Date(now);
    aMonthBefore.setMonth(aMonthBefore.getMonth() - 1);

    const aMonthAfter = new Date(now);
    aMonthAfter.setMonth(aMonthAfter.getMonth() + 1);

    this.employeeService
      .get({
        active: true,
        wants_reminder: true,
        reminder_after: aMonthBefore.toLocaleDateString(),
        reminder_before: aMonthAfter.toLocaleDateString()
      })
      .subscribe(employees => {
        this.employees = employees;
      });
  }
}
