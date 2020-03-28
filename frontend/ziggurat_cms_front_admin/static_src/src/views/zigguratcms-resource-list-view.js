import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import '@polymer/paper-button/paper-button.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../components/form-validation-decorator.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminResourceListView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <iron-ajax id="ajax-node-delete" handle-as="json" url="[[getAPIUrl(appConfig, '/zigguratcms-page-nodes/', nodeToDeleteUuid)]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleNodeDeleteResponse" debounce-duration="100"></iron-ajax>


        <h1 class="section-header">[[localize('Resources')]]</h1>
        <p>[[localize('Manage your resources.')]]</p>

        <template is="dom-if" if="[[resourceUUID]]">
        <uirouter-sref state="resources.create" param-object-id\$="[[resourceUUID]]" generated-u-r-l="{{generatedUrl2}}">
            <paper-button raised="">[[localize('Create page')]]</paper-button>
        </uirouter-sref>
        </template>

        <resource-leaf-provider url="[[getAPIUrl(appConfig, '/resources/', resourceUUID, '/rel/children')]]" on-resource-leaf-provider-response="handleResourceResponse" on-resource-leaf-provider-request="handleResourceRequest" on-resource-leaf-provider-error="handleResourceError" resources="{{appResources}}">
        </resource-leaf-provider>


        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this node?')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">[[localize('Confirm')]]</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="nodeDelete">[[localize('Accept')]]</paper-button>
                </template>
            </div>
        </paper-dialog>

        <div class="table default" id="resource-list-table">
            <div class="row header">
                <div class="cell">[[localize('Resource Name')]]</div>
                <div class="cell">[[localize('Actions')]]</div>
                <div class="cell">[[localize('Type')]]</div>
            </div>
            <template is="dom-repeat" items="[[appResources]]" as="node">
                <div class="row">
                    <div class="cell resource">[[node.resource_name]]</div>
                    <div class="cell actions">

                        <uirouter-sref state="resources.edit" param-object-id\$="[[node.uuid]]" param-type\$="[[node.resource_type]]">
                            <paper-icon-button icon="editor:mode-edit" title="Edit Node">
                            </paper-icon-button>
                        </uirouter-sref>

                        <uirouter-sref state="resources.list" param-object-id\$="[[node.uuid]]">
                            <paper-icon-button icon="icons:folder" title="Child resources">
                            </paper-icon-button>
                        </uirouter-sref>

                        <a on-tap="nodeDeleteDialogOpen" href="#" data-uuid\$="[[node.uuid]]">
                            <paper-icon-button icon="icons:delete" title="Delete"></paper-icon-button>
                        </a>

                    </div>
                    <div class="cell type">[[node.resource_type]]</div>
                </div>
            </template>
        </div>
`;
  }

  static get is() {
      return "zigguratcms-resource-list-view";
  }
  static get properties() {
      return {
          appResources: Array,
          resourceType: {
              type: String,
              notifies: true
          },
          /**
           * Viewed resource UUID
           */
          resourceUUID: {
              type: String
          },
          resource: {
              type: Object
          },
          endpointType: {
              type: String,
              computed: 'computeEndpointType(routeData.resourceType)'
          }
      }
  }
  handleResourceResponse(event) {
      this.currentUser = event.detail.response;
      this.fire('overlay-ajax-stopped', {});

  }
  handleResourceRequest(event) {
      this.fire('overlay-ajax-started', {});
  }
  handleResourceError(event) {
      this.fire('overlay-ajax-stopped', {});
  }
  computeEndpointType(nodeType) {
      var types = {
          'zigguratcms-page-node': 'zigguratcms-page-nodes'
      };
      return types[nodeType];
  }
  nodeDeleteDialogOpen(event) {
      event.preventDefault();
      event.stopPropagation();
      console.log('nodeDeleteDialogOpen', event, event.currentTarget.getAttribute('data-uuid'));
      this.nodeToDeleteUuid = event.currentTarget.getAttribute('data-uuid');
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  nodeDelete() {
      console.log('nodeDelete');
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-node-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  handleRequest(event) {
      this.fire('overlay-ajax-started', {});
  }
  handleNodeDeleteResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      for (var x = 0; x < this.appResources.length; x++) {
          console.log('xxxx', this.appResources[x].uuid, this.nodeToDeleteUuid)
          if (this.appResources[x].uuid === this.nodeToDeleteUuid) {
              this.splice('appResources', x, 1);
              break
          }
      }
  }
  connectedCallback(){
      super.connectedCallback();
      if (this.uiRouterParams.objectId){
          this.resourceUUID = this.uiRouterParams.objectId;
      }
      else{
          this.resourceUUID = this.appConfig.applicationUUID;
      }

  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminResourceListView.is, ZigguratCMSAdminResourceListView);
