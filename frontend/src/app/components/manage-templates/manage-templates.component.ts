import { Component, OnInit, ViewChild } from '@angular/core';
import * as jspdf from 'jspdf';
import { CKEditorComponent } from '@ckeditor/ckeditor5-angular';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { ITemplate } from 'src/app/types';
import { TemplateService } from 'src/app/services/template.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-manage-templates',
  templateUrl: './manage-templates.component.html',
  styleUrls: ['./manage-templates.component.css']
})
export class ManageTemplatesComponent implements OnInit {
  @ViewChild('editor', { static: false }) editorComponent: CKEditorComponent;
  Editor = ClassicEditor;

  templateMode = true;

  template: Partial<ITemplate> = { template_body: '' };

  constructor(
    private templateService: TemplateService,
    private route: ActivatedRoute,
    private router: Router,
    private modalService: NgbModal
  ) {}

  ngOnInit() {
    const templateId = Number.parseInt(
      this.route.snapshot.queryParamMap.get('template'),
      10
    );
    const employeeId = Number.parseInt(
      this.route.snapshot.queryParamMap.get('employee'),
      10
    );

    if (templateId) {
      if (employeeId) {
        this.templateMode = false;
        this.templateService
          .getFilledTemplate(employeeId, templateId)
          .subscribe(template => {
            this.template = template;
          });
      } else {
        this.templateService.getById(templateId).subscribe(template => {
          this.template = template;
        });
      }
    } else {
      this.template = { template_body: '' };
    }
  }

  saveModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        if (!this.templateMode) {
          throw new Error('Not in template-mode');
        }
        (this.template.id
          ? this.templateService.update(this.template.id, this.template)
          : this.templateService.create(this.template)
        ).subscribe(() => this.router.navigate(['/anschreiben']));
      })
      .catch(_ => {});
  }

  pdfModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        if (this.templateMode) {
          throw new Error('In template-mode');
        }
        this.createPDF();
      })
      .catch(_ => {});
  }

  deleteModal(content) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(_ => {
        this.templateService
          .delete(this.template.id)
          .subscribe(() => this.router.navigate(['/anschreiben']));
      })
      .catch(_ => {});
  }

  createPDF() {
    const doc = new jspdf('p', 'mm', 'a4');
    doc.fromHTML(this.template.template_body, 15, 15, { width: 180 });
    doc.save(
      this.template.name + '_' + new Date().toLocaleDateString() + '.pdf'
    );
  }

  helpModal(content) {
    this.modalService.open(content, { centered: true, size: 'lg', scrollable: true });
  }

}
