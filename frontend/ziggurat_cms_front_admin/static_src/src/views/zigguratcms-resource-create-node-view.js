import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../components/form-validation-decorator.js';
import '../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminResourceCreateView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <h1 class="section-header">[[localize('Create Node')]]</h1>

        <resource-leaf-provider url="[[getAPIUrl(appConfig, '/resources')]]" on-resource-leaf-provider-response="handleResourceResponse" on-resource-leaf-provider-request="handleResourceRequest" on-resource-leaf-provider-error="handleResourceResponse" resources="{{appResources}}">
        </resource-leaf-provider>
        <iron-form id="resource-form" on-iron-form-error="handleIronFormError" on-iron-form-response="handleIronFormResponse" on-iron-form-submit="handleIronFormSubmit">
            <form method="post" enctype="application/json" action="[[getNewResourceURL(appConfig, resourceType)]]">
                <iron-a11y-keys id="a11y" keys="enter" on-keys-pressed="submitForm"></iron-a11y-keys>

                <form-validation-decorator field-name="parent_uuid_dummy" error-object="[[formErrors]]">
                    <paper-dropdown-menu label="[[localize('Parent Node')]]" name="parent_uuid_dummy" horizontal-align="left">
                        <paper-listbox slot="dropdown-content" selected="{{parentNodeUUID}}" fallback-selection="[[selectedDefaultParent(uiRouterParams, appConfig)]]" attr-for-selected="value">
                            <paper-item value="[[appConfig.applicationUUID]]">------</paper-item>
                            <template is="dom-repeat" items="[[appResources]]">
                                <paper-item value="[[item.uuid]]"><span style="margin-left: [[indentResource(item)]]px">[[item.resource_name]]</span>
                                </paper-item>
                            </template>
                        </paper-listbox>
                    </paper-dropdown-menu>
                </form-validation-decorator>
                <form-validation-decorator field-name="resource_type" error-object="[[formErrors]]">
                    <paper-dropdown-menu label="[[localize('Resource Type')]]" name="resource_type">
                        <paper-listbox slot="dropdown-content" selected="{{resourceType}}" fallback-selection="zigguratcms-page-node" attr-for-selected="value">
                            <paper-item value="zigguratcms-page-node">[[localize('Page Node')]]</paper-item>
                            <paper-item value="zigguratcms-blog-node">[[localize('Blog Node')]]</paper-item>
                            <paper-item value="zigguratcms-category-node">[[localize('Category Node')]]</paper-item>
                            <paper-item value="zigguratcms-link-node">[[localize('Link Node')]]</paper-item>
                        </paper-listbox>
                    </paper-dropdown-menu>
                </form-validation-decorator>
                <input type="hidden" name="resource_type" value="{{resourceType}}">
                <input type="hidden" name="parent_uuid" value="{{parentNodeUUID}}">
                <form-validation-decorator field-name="resource_name" error-object="[[formErrors]]">
                    <paper-input label="{{localize('Resource name')}}" name="resource_name"></paper-input>
                </form-validation-decorator>
                <paper-input label="{{localize('Resource description')}}" name="description"></paper-input>
                <div class="buttons">
                    <paper-button raised="" on-tap="submitForm" disabled="[[formDisabled]]">{{localize('Create')}}
                    </paper-button>
                </div>
            </form>
        </iron-form>
`;
  }

  static get is() {
      return "zigguratcms-resource-create-node-view";
  }

  static get properties() {
      return {
          resourceType: {
              type: String,
              value: 'zigguratcms-page-node',
              notifies: true
          },
          parentNodeUUID: {
              type: String
          }
      }
  }

  submitForm() {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['resource-form'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['resource-form'].submit();
  }

  handleIronFormResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.fire('iron-ajax-response', event.detail);
      var response = event.detail.response;
      this.fire('redirect-url', {
          state: 'resources.edit',
          params: {objectId: response.uuid, type: response.resource_type}
      });
  }

  handleIronFormSubmit(event) {
      this.fire('overlay-ajax-started', {});
  }

  handleIronFormError(event) {
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

  handleResourceRequest() {
      this.fire('overlay-ajax-started', {});
  }

  handleResourceResponse() {
      this.fire('overlay-ajax-stopped', {});
  }

  selectedDefaultParent() {
      if (this.uiRouterParams.objectId) {
          return this.uiRouterParams.objectId;
      }
      else {
          return this.appConfig.applicationUUID;
      }
  }

  indentResource(item) {
      var result = 10 * item.depth;
      return result;
  }

  apiResourceFromType(resourceType) {
      console.log('apiResourceFromType', resourceType);
      return this.appConfig.nodeMappings[resourceType];
  }

  getNewResourceURL(appConfig, resourceType) {
      return this.getAPIUrl(appConfig, '/', this.apiResourceFromType(resourceType))
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminResourceCreateView.is, ZigguratCMSAdminResourceCreateView);
