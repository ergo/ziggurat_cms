import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@vaadin/vaadin-upload';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-input/paper-textarea.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../../shared-styles.js';
import '../../behaviors/ziggurat-admin-basic.js';
import './zigguratcms-blog-entry.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

var STATUS = {
    ACTIVE: 1,
    DISABLED: 0,
    DELETED: -1,
    DRAFT: 2
};

class ZigguratCMSAdminBlog extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }


        </style>

        <iron-ajax id="ajax-entries-list" auto="" url="[[apiEntriesUrl]]" handle-as="json" bubbles="" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" content-type="application/json" last-response="{{entries}}" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-entries-post" handle-as="json" url="[[apiEntriesUrl]]" bubbles="" method="POST" content-type="application/json" on-iron-ajax-response="handleEntryPostResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-entries-get" handle-as="json" url="[[elementPatchUrl]]" bubbles="" method="GET" content-type="application/json" last-response="{{editedEntry}}" on-iron-ajax-response="handleResponseGet" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>


        <iron-ajax id="ajax-entries-patch" handle-as="json" url="[[elementPatchUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-response="handleResponsePatch" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-entries-delete" handle-as="json" url="[[elementPatchUrl]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-response="handleResponseDelete" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this entry?')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">Confirm</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="blogDelete">[[localize('Accept')]]</paper-button>
                </template>
            </div>
        </paper-dialog>

        <template is="dom-if" if="[[editing]]" restamp="">

            <zigguratcms-blog-entry blog-uuid="[[uuid]]" entry="{{editedEntry}}" on-zigguratcms-blog-entry-dismiss="dismissEntry">
            </zigguratcms-blog-entry>

        </template>
        <template is="dom-if" if="[[!editing]]">
            <h2>[[localize('Blog Management')]]</h2>


            <paper-button raised="" on-tap="addEntry">[[localize('Add Entry')]]</paper-button>

            <div class="table responsive default" id="blog-list-table">
                <div class="row responsive header">
                    <div class="cell responsive">[[localize('Status')]]</div>
                    <div class="cell responsive">[[localize('Title')]]</div>
                    <div class="cell responsive">[[localize('Actions')]]</div>
                </div>
                <template is="dom-repeat" items="[[entries]]" id="entry-repeater">
                    <div class="row responsive">
                        <div class="cell responsive status">
                            <paper-toggle-button checked="[[isEntryActive(item)]]" on-change="statusChange"></paper-toggle-button>
                        </div>
                        <div class="cell responsive info">
                            <p class="name"><strong>[[computedName(item.name)]]</strong></p>
                        </div>
                        <div class="cell responsive actions">
                            <paper-icon-button icon="editor:mode-edit" title="Edit" on-tap="blogEditItem">
                            </paper-icon-button>

                            <paper-icon-button icon="icons:delete" title="Delete" on-tap="blogDeleteDialogOpen">
                            </paper-icon-button>
                        </div>
                    </div>
                </template>
            </div>

        </template>
`;
  }

  static get is() {
      return "zigguratcms-blog";
  }
  static get properties() {
      return {
          status: Number,
          resourceUuid: String,
          uuid: String,
          resource: Object,
          element: Object,
          selectedItem: {
              type: Object
          },
          editing: {
              type: Boolean,
              value: false
          },
          editedEntry: Object,
          entries: {
              type: Array,
              value () {
                  return []
              }
          },
          dirty: {
              type: Boolean,
              value: false
          },
          apiEntriesUrl: {
              type: String,
              computed: 'computedApiEntriesUrl(appConfig, uuid)'
          },
          elementPatchUrl: {
              type: String,
              computed: 'computedElementPatchUrl(appConfig, selectedItem.uuid)'
          }
      }
  }

  computedApiEntriesUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-blog-elements/', uuid, '/rel/entries')
  }
  computedElementPatchUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-blog-elements-entries/', uuid)
  }
  handleRequest (event) {
      this.fire('overlay-ajax-started', {});
  }
  handleResponse () {
      this.fire('overlay-ajax-stopped', {});
  }
  handleError () {
      this.fire('overlay-ajax-stopped', {});
  }
  handleEntryPostResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('entries', 0, null, event.detail.response);
  }
  addEntry (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-entries-post'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {};
      ajaxElem.generateRequest();
  }
  dismissEntry (event) {
      this.editing = false;
      var ajaxElem = this.$['ajax-entries-list'];
      ajaxElem.generateRequest();
  }
  isEntryActive (item) {
      return item.status == STATUS.ACTIVE;
  }
  _findSelectedItem(node){
      return this.querySelector('#entry-repeater').itemForElement(node);
  }
  statusChange (event) {
      this.selectedItem = this._findSelectedItem(event.target);
      var status = this.selectedItem.status == STATUS.ACTIVE ? STATUS.DRAFT : STATUS.ACTIVE;
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-entries-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {status: status};
      ajaxElem.generateRequest();
  }
  handleResponsePatch (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('entries', this.entries.indexOf(this.selectedItem), 1, event.detail.response);
  }
  computedName (name) {
      if (name) {
          return name
      }
      return 'Draft blog post';
  }
  blogDeleteDialogOpen (event) {
      this.selectedItem = this._findSelectedItem(event.target);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  blogDelete (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-entries-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  handleResponseDelete (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('entries', this.entries.indexOf(this.selectedItem), 1);
  }
  blogEditItem (event) {
      console.log('blogEditItem');
      this.selectedItem = this._findSelectedItem(event.target);
      var ajaxElem = this.$['ajax-entries-get'];
      ajaxElem.generateRequest();
  }
  handleResponseGet(){
      this.fire('overlay-ajax-stopped', {});
      this.editing = true;
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminBlog.is, ZigguratCMSAdminBlog);
