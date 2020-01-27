import { Component, enableProdMode, OnInit } from '@angular/core';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { faTimes } from '@fortawesome/free-solid-svg-icons';
import {
  NgbModal,
  NgbDateAdapter,
  NgbDateParserFormatter
} from '@ng-bootstrap/ng-bootstrap';
import { IEmployee, IAppointment } from 'src/app/types';
import { EmployeesService } from 'src/app/services';
import { Router, ActivatedRoute } from '@angular/router';
import { AppointmentsService } from 'src/app/services/appointments.service';
import { IDepartment } from '../../types/department.interface';
import { DepartmentsService } from '../../services/departments.service';
import {
  CustomAdapter,
  CustomDateParserFormatter
} from 'src/app/adapters/datepicker.adapters';

@Component({
  selector: 'app-manage-employees',
  templateUrl: './manage_employees.component.html',
  styleUrls: ['./manage_employees.component.css'],
  providers: [
    { provide: NgbDateAdapter, useClass: CustomAdapter },
    { provide: NgbDateParserFormatter, useClass: CustomDateParserFormatter }
  ]
})
export class ManageEmployeesComponent implements OnInit {
  faCalendar = faCalendar;
  faPlus = faPlus;
  faTimes = faTimes;

  selectedOption: number;

  startDate = new Date(1990, 0, 1);

  datePlaceholder = 'tt.mm.jjjj';

  employee: Partial<IEmployee> = {};
  appointments: IAppointment[];
  departments: IDepartment[];

  filter = {};

  constructor(
    private departmentsService: DepartmentsService,
    private employeeService: EmployeesService,
    private appointmentService: AppointmentsService,
    private modalService: NgbModal,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.queryParams.id;
    if (id) {
      this.employeeService.getById(id).subscribe(employee => {
        this.employee = employee;
      });
      this.appointmentService.get({ employee: id }).subscribe(appointments => {
        this.appointments = appointments;
      });
    } else {
      this.employee = {};
      this.appointments = [];
    }
    this.departmentsService.get().subscribe(departments => {
      this.departments = departments;
    });
  }

  setDepartment(id: number) {
    this.employee.department = id;
  }

  isCreationMode(): boolean {
    return this.employee && !this.employee.id;
  }

  isUpdateMode(): boolean {
    return this.employee && this.employee.id && this.employee.active;
  }

  isArchiveMode(): boolean {
    return this.employee && this.employee.id && !this.employee.active;
  }

  saveModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.employee.id
          ? this.employeeService
              .update(this.employee.id, this.employee)
              .subscribe()
          : this.employeeService.create(this.employee).subscribe();
        this.employee = {};
        this.router.navigate(['/mitarbeiter']);
      })
      .catch(_ => {});
  }

  deleteModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(() => {
        this.employeeService.delete(this.employee.id).subscribe();
        this.employee = {};
        this.router.navigate(['/mitarbeiter']);
      })
      .catch(_ => {});
  }

  archiveModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.employeeService
          .update(this.employee.id, { active: false })
          .subscribe(() => {
            this.router.navigate(['/archiv']);
          });
      })
      .catch(_ => {});
  }

  dearchiveModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.employeeService
          .update(this.employee.id, { active: true })
          .subscribe(() => {
            this.router.navigate(['/mitarbeiter']);
          });
      })
      .catch(_ => {});
  }

  newAppointmentModal(content) {
    this.modalService
      .open(content)
      .result.then(date => {
        this.appointmentService
          .create({ employee: this.employee.id, date })
          .subscribe(appointment => {
            this.employeeService
              .getById(this.employee.id)
              .subscribe(employee => {
                this.employee = employee;
                this.appointments.push(appointment);
              });
          });
      })
      .catch(_ => {});
  }

  deleteAppointment(content, id) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(() => {
        this.appointmentService.delete(id).subscribe(_ => {
          this.appointmentService
            .get({ employee: this.employee.id })
            .subscribe(appointments => {
              this.appointments = appointments;
            });
        });
      })
      .catch(_ => {});
  }

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

  newAbteilungModal(content) {
    this.modalService
      .open(content)
      .result.then(name => {
        this.departmentsService.create({ name }).subscribe(res => {
          this.departments.push(res);
          this.employee.department = res.id;
        });
      })
      .catch(_ => {});
  }

  deleteAbteilungModal(content) {
    this.modalService
      .open(content)
      .result.then(() => {
        this.departmentsService.delete(this.selectedOption).subscribe(() => {
          this.departmentsService.get().subscribe(departments => {
            this.departments = departments;
          });
        });
      })
      .catch(_ => {});
  }
}
