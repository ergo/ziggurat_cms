import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '../components/form-validation-decorator.js';
import '../components/zigguratcms-element-stomper.js';
import '../shared-styles.js';
import './resource-edit/resource-edit-page-node.js';
import './resource-edit/resource-edit-link-node.js';
import './resource-edit/resource-edit-category-node.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../behaviors/ziggurat-admin-basic.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { dom as dom$0 } from '@polymer/polymer/lib/legacy/polymer.dom.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSAdminResourceEditNodeView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <iron-ajax id="ajax-resource" auto="" url="[[getAPIUrl(appConfig, '/', endpointType, '/', uiRouterParams.objectId)]]" handle-as="json" bubbles="" content-type="application/json" last-response="{{resource}}" debounce-duration="100"></iron-ajax>

        <resource-leaf-provider url="[[getAPIUrl(appConfig, '/resources')]]" on-resource-leaf-provider-response="handleResourceResponse" on-resource-leaf-provider-request="handleResourceRequest" on-resource-leaf-provider-error="handleResourceError" resources="{{appResources}}">
        </resource-leaf-provider>

        <resource-leaf-provider url="[[getAPIUrl(appConfig, '/resources/', resource.parent_uuid, '/rel/children')]]" on-resource-leaf-provider-response="handleResourceResponse" on-resource-leaf-provider-request="handleResourceRequest" on-resource-leaf-provider-error="handleResourceError" resources="{{directChildren}}">
        </resource-leaf-provider>

        <h1 class="section-header">[[localize('Edit Node')]]</h1>

        <object-cloned-data data="[[resource]]" shadow-data="{{shadowedResource}}" only-once=""></object-cloned-data>

        <iron-form id="resource-form" on-iron-form-error="handleTopElementFormError" on-iron-form-response="handleTopElementFormResponse" on-iron-form-presubmit="handleTopElementFormPresubmit">
            <form is="iron-form" method="post" enctype="application/json" action="[[getAPIUrl(appConfig, '/', endpointType, '/',uiRouterParams.objectId)]]">
                <iron-a11y-keys id="a11y" keys="enter" on-keys-pressed="submitForm"></iron-a11y-keys>

                <form-validation-decorator field-name="parent_uuid" error-object="[[formErrors]]">
                    <paper-dropdown-menu label="Parent Node" name="parent_uuid" horizontal-align="left">
                        <paper-listbox slot="dropdown-content" selected="{{resource.parent_uuid}}" fallback-selection="[[defaultSelection(appConfig.applicationUUID, resource.parent_uuid)]]" attr-for-selected="value">
                            <paper-item value="[[appConfig.applicationUUID]]">------</paper-item>
                            <template is="dom-repeat" items="[[appResources]]">
                                <paper-item value="[[item.uuid]]"><span style="margin-left: [[indentResource(item)]]px">[[item.resource_name]]</span>
                                </paper-item>
                            </template>
                        </paper-listbox>
                    </paper-dropdown-menu>
                </form-validation-decorator>


                <template is="dom-if" if="[[directChildren]]">

                    <form-validation-decorator field-name="position" error-object="[[formErrors]]">
                        <paper-dropdown-menu label="Node Position" name="position">
                            <paper-listbox slot="dropdown-content" selected="{{resource.ordering}}" fallback-selection="[[shadowedResource.ordering]]" attr-for-selected="value">
                                <template is="dom-repeat" items="[[computePositions(directChildren)]]">
                                    <paper-item value="[[item.ordering]]">[[item.ordering]]: [[item.resource_name]]
                                    </paper-item>
                                </template>
                            </paper-listbox>
                        </paper-dropdown-menu>
                    </form-validation-decorator>
                </template>

                <form-validation-decorator field-name="resource_name" error-object="[[formErrors]]">
                    <paper-input label="{{localize('Resource name')}}" value="{{resource.resource_name}}" name="resource_name"></paper-input>
                </form-validation-decorator>
                <paper-input label="{{localize('Resource description')}}" value="{{resource.description}}" name="description"></paper-input>
                <div class="buttons">
                    <paper-button raised="" on-tap="submitForm" disabled="[[formDisabled]]">
                        [[localize('Update')]]
                        <template is="dom-if" if="[[dirty]]">
                            <span class="flashing">(<iron-icon icon="icons:save"></iron-icon> [[localize('unsaved changes')]])</span>
                        </template>
                    </paper-button>
                </div>
            </form>
        </iron-form>
`;
  }

  static get is() {
      return "zigguratcms-resource-edit-node-view";
  }

  static get properties() {
      return {
          resourceType: {
              type: String,
              notifies: true
          },
          uiRouterParams:{
              type: Object
          },
          uiRouterResolvedData:{
              type: Object
          },
          uiRouterTransition:{
              type: Object
          },
          resource: {
              type: Object
          },
          endpointType: {
              type: String,
              computed: 'computeEndpointType(appConfig, uiRouterParams.*)'
          },
          dirty: {
              type: Boolean,
              computed: 'computeDirty(resource.elements.*)'
          }
      }
  }

  static get observers() {
      return ['stompElement(resource)']
  }
  handleSaveDirty() {
      console.log('handleSaveDirty enode', Math.random());
  }
  computeDirty() {
      if (!this.resource  || !this.resource.elements) {
          return false;
      }
      for (var x = 0; x < this.resource.elements.length; x++) {
          if (this.resource.elements[x].dirty) {
              return true;
          }
      }
      return false;
  }

  defaultSelection(uuid, parentUuid) {
      if (!uuid || !parentUuid){
          return this.appConfig.applicationUUID;
      }
      return this.resource.parent_uuid || this.appConfig.applicationUUID;
  }

  connectedCallback() {
      super.connectedCallback();
      this.addEventListener('element-data-changed', this.handleElementDataChange);
//                this.addEventListener('resource-data-changed', this.handleResourceDataChange);
  }
  disconnectedCallback() {
      super.disconnectedCallback();
      this.removeEventListener('element-data-changed', this.handleElementDataChange);
//                this.removeEventListener('resource-data-changed', this.handleResourceDataChange);
  }

  stompElement() {
      if(!this.resource){
          return false;
      }
      console.log('stomping', this.resource.resource_type);
      var rType = this.resource.resource_type;
      var elemType = null;
      if (['zigguratcms-blog-node', 'zigguratcms-page-node'].indexOf(rType) !== -1) {
          elemType = 'zigguratcms-resource-edit-page-node-view';
      }
      if (rType === 'zigguratcms-link-node') {
          elemType = 'zigguratcms-resource-edit-link-node-view';
      }
      if (rType === 'zigguratcms-category-node') {
          elemType = 'zigguratcms-resource-edit-category-node-view';
      }
      if (!elemType) {
          return
      }
      var node = document.createElement(elemType);
      node.resource = this.resource;
      node.uiRouterTransition = this.uiRouterTransition;
      node.uiRouterParams = this.uiRouterParams;
      node.uiRouterResolvedData = this.uiRouterResolvedData;
      dom$0(this).appendChild(node);

  }

  handleElementDataChange(event) {
      console.log('handleElementDataChange', event.detail);
      for (var x = 0; x < this.resource.elements.length; x++) {
          if (this.resource.elements[x].uuid === event.detail.uuid) {
              this.set(['resource', 'elements', x, 'config'], Object.assign({}, event.detail.config));
              this.set(['resource', 'elements', x, 'dirty'], event.detail.dirty);

          }
      }
  }
  submitForm() {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['resource-form'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['resource-form'].submit();
      this.fire('overlay-ajax-started', {});
      this.fire('cms-elements-save-dirty');
  }
  handleTopElementFormResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.fire('iron-ajax-response', event.detail);
  }
  handleTopElementFormError(event) {
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
  handleTopElementFormPresubmit(event) {
      // forms dont support PATCH so we have to alter this here
      this.$['resource-form'].request.method = 'PATCH';
      this.$['resource-form'].request.body = this.resource;
  }
  computeEndpointType() {
      return this.appConfig.nodeMappings[this.uiRouterParams.type];
  }
  handleResourceRequest() {
      this.fire('overlay-ajax-started', {});
  }
  handleResourceResponse() {
      this.fire('overlay-ajax-stopped', {});
  }
  indentResource(item) {
      var result = 10 * item.depth;
      return result;
  }
  computePositions() {
      var positions = this.directChildren.slice();
      if (this.resource.parent_uuid !== this.shadowedResource.parent_uuid) {
          var newPosition = this.directChildren.length + 1;
          positions.push({
              ordering: newPosition,
              resource_name: '*Last in new parent*'
          });
          this.async(function(){
              this.set('resource.ordering', newPosition);
          }, 10);

      }
      else{
          this.async(function(){
              this.set('resource.ordering', this.shadowedResource.ordering);
          }, 10);
      }
      console.log('computePositions', positions);
      return positions;
  }
  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminResourceEditNodeView.is, ZigguratCMSAdminResourceEditNodeView);
