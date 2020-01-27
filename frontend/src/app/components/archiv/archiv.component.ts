import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { EmployeesService } from 'src/app/services';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-archiv',
  templateUrl: './archiv.component.html',
  styleUrls: ['./archiv.component.css']
})
export class ArchivComponent implements OnInit {
  // Search Icon
  faSearch = faSearch;
  // Cache fur current Employees, this list is shown in the table
  displayedArchivedEmployees = [];
  // Selected Filter
  selectedFilter = 'lastname';
  // Name of selected Filter
  selectedValue = 'Nachname';

  constructor(
    private employeesService: EmployeesService,
    private router: Router,
    private employeeService: EmployeesService,
    private modalService: NgbModal
  ) {}

  ngOnInit() {
    this.updateDisplayedColumns();
  }

  // Load manage-employee component in archived mode
  loadDetailedView(employeeId: number) {
    this.router.navigate(['/mitarbeiter_verwalten'], {
      queryParams: { id: employeeId }
    });
  }

  // Modal for reactivating an employee
  dearchiveModal(content, employee) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.employeeService
          .update(employee.id, { active: true })
          .subscribe(() => {
            this.router.navigate(['/mitarbeiter']);
          });
      })
      .catch(_ => {});
  }

  // Functionality for the search field
  search(searchterm: string) {
    this.employeeService
      .get({ active: false, [this.selectedFilter]: searchterm })
      .subscribe(employees => {
        this.displayedArchivedEmployees = employees;
      });
  }

  // Updates the chached employees
  private updateDisplayedColumns() {
    this.employeesService.get({ active: false }).subscribe(pagEmpl => {
      this.displayedArchivedEmployees = pagEmpl;
    });
  }

  // Name switching of filter for selection of a filter
  changeDropdownName(value: string) {
    this.selectedValue = value;
  }
}
