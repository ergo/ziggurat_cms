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
import '../shared-styles.js';
import '../behaviors/ziggurat-admin-basic.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-input/paper-textarea.js';
import '../components/form-validation-decorator.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSAdminSettingsView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <resource-leaf-provider url="[[getAPIUrl(appConfig, '/resources')]]" on-resource-leaf-provider-response="handleResourceResponse" on-resource-leaf-provider-request="handleResourceRequest" on-resource-leaf-provider-error="handleResourceError" resources="{{appResources}}">
        </resource-leaf-provider>

        <iron-ajax id="ajax-resource" auto="" url="[[getAPIUrl(appConfig, '/resources/', appConfig.applicationUUID)]]" handle-as="json" bubbles="" content-type="application/json" last-response="{{resource}}" debounce-duration="100"></iron-ajax>

        <div class="admin-section-view">
            <h1 class="section-header">[[localize('Settings')]]</h1>
            <iron-form id="resource-form" on-iron-form-error="handleIronFormError" on-iron-form-response="handleIronFormResponse" on-iron-form-presubmit="handleIronFormPresubmit">
                <form method="post" enctype="application/json" action="[[getAPIUrl(appConfig, '/applications/', appConfig.applicationUUID)]]">

                    <form-validation-decorator field-name="parent_uuid_dummy" error-object="[[formErrors]]">
                        <paper-dropdown-menu label="[[localize('Index page Node')]]" name="parent_uuid_dummy">
                            <paper-listbox slot="dropdown-content" selected="{{resource.config.index_node_uuid}}" attr-for-selected="value">
                                <template is="dom-repeat" items="[[appResources]]">
                                    <paper-item value="[[item.uuid]]">
                                        <span style="margin-left: [[indentResource(item)]]px">[[item.resource_name]]</span>
                                    </paper-item>
                                </template>
                            </paper-listbox>
                        </paper-dropdown-menu>
                    </form-validation-decorator>
                    <paper-input label="[[localize('HTTP title')]]" value="{{resource.config.http_title}}"></paper-input>
                    <paper-textarea label="[[localize('Brand html')]]" value="{{resource.config.brand_html}}" always-float-label=""></paper-textarea>
                    <div class="buttons">
                        <paper-button raised="" on-tap="formSubmit" disabled="[[formDisabled]]">{{localize('Update')}}
                        </paper-button>
                    </div>
                </form>
            </iron-form>
        </div>
`;
  }

  static get is() {
      return "zigguratcms-settings-view";
  }

  static get properties() {
      return {}
  }

  indentResource(item) {
      let result = 10 * item.depth;
      return result;
  }

  handleResourceRequest() {
      this.dispatchOverlayStarted();
  }

  handleResourceResponse() {
      this.dispatchOverlayStopped();
  }

  formSubmit() {
      this.$['resource-form'].headers['X-XSRF-TOKEN'] = this.getCSRFToken();
      this.$['resource-form'].submit();
      this.dispatchOverlayStarted();
  }

  handleIronFormResponse(event) {
      this.dispatchOverlayStopped();
      this.dispatchEvent(new CustomEvent('iron-ajax-response', {
          detail: event.detail,
          bubbles: true,
          composed: true
      }));
  }

  handleIronFormError(event) {
      this.dispatchOverlayStopped();
      if (event.detail.request.xhr.status === 422) {
          this.fire('toast-message', {
              message: this.localize('Form contains invalid data')
          });
          this.formErrors = event.detail.request.xhr.response;
      }
      else {
          this.fire('iron-ajax-error', event.detail);
          this.dispatchEvent(new CustomEvent('iron-ajax-error', {
              detail: event.detail,
              bubbles: true,
              composed: true
          }));
      }
  }

  handleIronFormPresubmit(event) {
      // forms dont support PATCH so we have to alter this here
      this.$['resource-form'].request.method = 'PATCH';
      this.$['resource-form'].request.body = this.resource;
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminSettingsView.is, ZigguratCMSAdminSettingsView);
