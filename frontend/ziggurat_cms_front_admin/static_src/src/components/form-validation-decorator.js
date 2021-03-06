import { Polymer } from '@polymer/polymer/lib/legacy/polymer-fn.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { dom } from '@polymer/polymer/lib/legacy/polymer.dom.js';
Polymer({
  _template: html`
        <slot></slot>
`,

  is: 'form-validation-decorator',

  properties: {
      fieldName: String,
      errorKeyName: String,
      errorObject: Object
  },

  observers: [
      'checkErrors(errorObject.*)'
  ],

  checkErrors: function () {
      var field = this.fieldName;
      var errorKeyName = this.errorKeyName || this.fieldName;
      var invalidFields = Object.keys(this.errorObject);

      var nodes = dom(this).querySelectorAll('*[name=' + field + ']');
      if (nodes.length > 0) {
          if (invalidFields.indexOf(errorKeyName) !== -1) {
              nodes[0].invalid = true;
              nodes[0].errorMessage = this.errorObject[errorKeyName][0];
          }
          else {
              nodes[0].invalid = false;
          }
      }
  }
});
