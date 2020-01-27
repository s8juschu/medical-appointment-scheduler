import { Component, OnInit } from '@angular/core';
import { AppointmentsService } from '../../services/appointments.service';
import { IAppointment, IEmployee } from '../../types';
import { faAngleLeft } from '@fortawesome/free-solid-svg-icons';
import { faAngleRight } from '@fortawesome/free-solid-svg-icons';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { EmployeesService } from 'src/app/services';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.css']
})
export class AppointmentsComponent implements OnInit {
  constructor(
    private appointmentsService: AppointmentsService,
    private employeeService: EmployeesService,
    private modalService: NgbModal,
    private router: Router
  ) {}

  anio: number = new Date().getFullYear();

  faAngleLeft = faAngleLeft;
  faAngleRight = faAngleRight;
  faTimes = faTimes;
  faEdit = faEdit;

  displayedAppointmentsPerMonth: Array<Array<IAppointment>> = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
  ];

  employees: IEmployee[];

  inc() {
    this.anio += 1;
    this.updateDisplayedColumns();
  }
  dec() {
    this.anio -= 1;
    this.updateDisplayedColumns();
  }

  private updateDisplayedColumns() {
    this.appointmentsService
      .get({
        min_date: String(this.anio) + '-01-01',
        max_date: String(this.anio) + '-12-31'
      })
      .subscribe(pagEmpl => {
        this.employeeService.get().subscribe(employees => {
          this.employees = employees;

          this.displayedAppointmentsPerMonth = [];
          for (let i = 0; i < 12; i++) {
            this.displayedAppointmentsPerMonth.push([]);
          }
          for (const e of pagEmpl) {
            const month = Number.parseInt(e.date.split('.')[1], 10);
            this.displayedAppointmentsPerMonth[month - 1].push(e);
          }
        });
      });
  }

  getEmployeeNameById(id: number): string {
    const employee = this.employees.find(e => e.id === id);
    if (!employee) {
      this.employeeService.get().subscribe(employees => {
        this.employees = employees;
      });
    }
    return '| ' + employee.last_name + ', ' + employee.first_name;
  }

  ngOnInit() {
    this.updateDisplayedColumns();
  }

  deleteAppointment(content, id) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(() => {
        this.appointmentsService.delete(id).subscribe(() => {
          this.updateDisplayedColumns();
        });
      })
      .catch(_ => {});
  }

  loadDetailedView(employeeId: number) {
    this.router.navigate(['/mitarbeiter_verwalten'], {
      queryParams: { id: employeeId }
    });
  }
}
