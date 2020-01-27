import { Component, OnInit } from '@angular/core';
import { IEmployee } from 'src/app/types';
import { EmployeesService } from 'src/app/services/employees.service';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { Router } from '@angular/router';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  // Search Icon
  faSearch = faSearch;
  // Cache fur current Employees, this list is shown in the table
  displayedEmployees: IEmployee[] = [];
  // Selected Filter
  selectedFilter = 'lastname';
  // Name of selected Filter
  selectedValue = 'Nachname';

  constructor(
    private employeeService: EmployeesService,
    private router: Router
  ) {}

  ngOnInit() {
    this.updateDisplayedColumns();
  }

  // Updates the chached employees
  private updateDisplayedColumns() {
    this.employeeService.get({ active: true }).subscribe(pagEmpl => {
      this.displayedEmployees = pagEmpl;
    });
  }

  // Functionality for the search field
  search(searchterm: string) {
    this.employeeService
      .get({ active: true, [this.selectedFilter]: searchterm })
      .subscribe(employees => {
        this.displayedEmployees = employees;
      });
  }

  // Load manage-employee component in normal mode
  loadDetailedView(employeeId: number) {
    this.router.navigate(['/mitarbeiter_verwalten'], {
      queryParams: { id: employeeId }
    });
  }

  // Name switching of filter for selection of a filter
  changeDropdownName(value: string) {
    this.selectedValue = value;
  }
}
