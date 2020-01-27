import { Component, OnInit } from '@angular/core';
import { TemplateService } from 'src/app/services/template.service';
import { ITemplate } from 'src/app/types';
import { Router, ActivatedRoute } from '@angular/router';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-templates',
  templateUrl: './templates.component.html',
  styleUrls: ['./templates.component.css']
})
export class TemplatesComponent implements OnInit {
  faSearch = faSearch;
  templates: ITemplate[];

  constructor(
    private templateService: TemplateService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.templateService.get().subscribe(templates => {
      this.templates = templates;
    });
  }

  loadDetailedView(templateId: number) {
    const employeeId = this.route.snapshot.queryParamMap.get('employee');
    this.router.navigate(['/anschreiben_verwalten'], {
      queryParams: { template: templateId, employee: employeeId }
    });
  }
}
