/**
@license
Copyright (c) 2016 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
Code distributed by Google as part of the polymer project is also
subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
*/
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '../behaviors/ziggurat-admin-basic.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '../shared-styles.js';
import '../components/user-list.js';
import '../components/validators/custom-validator.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminUsersEditView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <h1 class="section-header">[[localize('Edit user')]]</h1>

        <custom-validator id="compare-fields" validator-name="compare-fields"></custom-validator>

        <iron-form id="user-form" on-iron-form-error="handleFormError" on-iron-form-response="handleFormResponse" on-iron-form-submit="handleRequest" on-iron-form-presubmit="handleFormPresubmit">
            <form method="post" enctype="application/json" action="[[getAPIUrl(appConfig, '/users/', uiRouterParams.userId)]]">
                <iron-a11y-keys id="a11y" keys="enter" on-keys-pressed="submitForm"></iron-a11y-keys>

                <form-validation-decorator field-name="password" error-object="[[formErrors]]">
                    <paper-input label="{{localize('Password')}}" value="{{user.password}}" name="password" type="password" validator="compare-fields"></paper-input>
                </form-validation-decorator>

                <paper-input label="{{localize('Password Confirm')}}" class="password_confirm" on-change="checkPassword" value="{{user.password_confirm}}" name="password_confirm" type="password" validator="compare-fields"></paper-input>

                <div class="buttons">
                    <paper-button raised="" on-tap="submitForm" disabled="[[formDisabled]]">
                        [[localize('Update')]]
                        <template is="dom-if" if="[[dirty]]">
                            <span class="flashing">(<iron-icon icon="icons:save"></iron-icon> unsaved changes)</span>
                        </template>
                    </paper-button>
                </div>
            </form>
        </iron-form>

        <iron-ajax id="ajax-resource" auto="" url="[[getAPIUrl(appConfig, '/users/', uiRouterParams.userId)]]" handle-as="json" bubbles="" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" content-type="application/json" last-response="{{user}}" debounce-duration="100"></iron-ajax>
`;
  }

  static get is() {
      return "zigguratcms-users-edit-view";
  }
  static get properties() {
      return {}
  }
  handleRequest(event) {
      this.fire('overlay-ajax-started', {});
  }
  handleResponse() {
      this.fire('overlay-ajax-stopped', {});
  }
  handleError(event) {
      event.stopPropagation();
      this.fire('overlay-ajax-stopped', {});
  }
  submitForm() {
      this.$['user-form'].submit();
  }
  handleFormResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.fire('iron-ajax-response', event.detail);
  }
  handleFormError(event) {
      this.fire('overlay-ajax-stopped', {});
      if (event.detail.request.xhr.status === 422) {
          this.fire('toast-message', {
              message: this.localize('Form contains invalid data')
          });
          this.formErrors = event.detail.request.xhr.response;
      }
      else {
          this.fire('iron-ajax-error', event.detail);
      }
  }

  attached() {
      this.$['compare-fields'].validate = this.checkPassword.bind(this);
  }

  checkPassword() {
      var passwordField = this.$$('paper-input[name="password"]');
      var confirmField = this.$$('paper-input[name="password_confirm"]');
      if (passwordField.value === confirmField.value) {
          return true;
      }
      var msg = this.localize('Password fields need to match');
      passwordField.errorMessage = msg;
      confirmField.errorMessage = msg;
      return false
  }
  handleFormPresubmit(event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['user-form'].headers['X-XSRF-TOKEN'] = xsrfToken;
      // forms dont support PATCH so we have to alter this here
      this.$['user-form'].request.method = 'PATCH';
      this.$['user-form'].request.body = this.user;
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminUsersEditView.is, ZigguratCMSAdminUsersEditView);
