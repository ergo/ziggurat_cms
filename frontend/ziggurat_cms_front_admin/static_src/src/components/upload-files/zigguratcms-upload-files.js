import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@vaadin/vaadin-upload';
import 'polymer-ui-router/uirouter-sref.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-input/paper-textarea.js';
import '../../shared-styles.js';
import '../../behaviors/ziggurat-admin-basic.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSAdminUploadFiles extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }

            .filename {
                color: #777777
            }

            #file-list-table {
                width: 100%
            }

            #file-list-table .file {
                width: 150px
            }

            #file-list-table .actions {
                width: 125px
            }

            .description.wrapped{
                white-space: pre-wrap;
            }

        </style>


        <iron-ajax id="ajax-resource" auto="" url="[[apiFilesUrl]]" handle-as="json" bubbles="" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" content-type="application/json" last-response="{{files}}" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-file-patch" handle-as="json" url="[[patchFileUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleFileEditResponse" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-file-delete" handle-as="json" url="[[patchFileUrl]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleDeleteResponse" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this file?')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">[[localize('Confirm')]]</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="fileDelete">[[localize('Accept')]]</paper-button>
                </template>
            </div>
        </paper-dialog>

        <object-cloned-data data="{{selectedItem}}" shadow-data="{{shadowedItemData}}"></object-cloned-data>

        <h2>[[localize('File Uploads Management')]]</h2>

        <vaadin-upload id="file-upload" on-upload-before="handleUploadRequest" on-upload-success="handleUploadSuccess" target="[[apiFilesUrl]]"></vaadin-upload>

        <div class="table responsive default" id="file-list-table">
            <div class="row responsive header">
                <div class="cell responsive">[[localize('Ext.')]]</div>
                <div class="cell responsive">[[localize('Info')]]</div>
                <div class="cell responsive">[[localize('Actions')]]</div>
            </div>
            <template is="dom-repeat" items="[[files]]" id="file-repeater">
                <div class="row responsive">
                    <div class="cell responsive file">
                        <strong>[[item.extension]]</strong>
                    </div>
                    <div class="cell responsive info">
                        <template is="dom-if" if="[[isEdited(item, selectedItem, editing)]]">
                            <p class="name">
                                <paper-input label="Name" value="{{shadowedItemData.name}}"></paper-input>
                            </p>
                            <p class="description">
                                <paper-textarea label="Description" value="{{shadowedItemData.description}}"></paper-textarea>
                            </p>
                            <p class="buttons">
                                <paper-button raised="" on-tap="cancelEdit">Cancel</paper-button>
                                <paper-button raised="" on-tap="updateFile">Update</paper-button>
                            </p>
                        </template>
                        <template is="dom-if" if="[[!isEdited(item, selectedItem, editing)]]">
                            <p class="filename">[[item.original_filename]]</p>
                            <p class="name"><strong>[[item.name]]</strong></p>
                            <p class="description wrapped">[[item.description]]</p>
                        </template>
                    </div>
                    <div class="cell responsive actions">
                        <paper-icon-button icon="editor:mode-edit" title="Edit" on-tap="fileEditItem">
                        </paper-icon-button>

                        <paper-icon-button icon="icons:delete" title="Delete" on-tap="fileDeleteDialogOpen">
                        </paper-icon-button>
                    </div>
                </div>
            </template>
        </div>
`;
  }

  static get is() {
      return "zigguratcms-upload-files";
  }
  static get properties() {
      return {
          status: Number,
          resourceUuid: String,
          uuid: String,
          parentElementPKey: String,
          resource: Object,
          element: Object,
          selectedItem: {
              type: Object,
              value: null
          },
          editing: {
              type: Boolean,
              value: false
          },
          files: {
              type: Array,
              value () {
                  return []
              }
          },
          dirty: {
              type: Boolean,
              value: false
          },
          apiFilesUrl: {
              type: String,
              computed: 'computeApiFilesUrl(appConfig, uuid)'
          },
          patchFileUrl: {
              type: String,
              computed: 'computePatchFileUrl(appConfig, selectedItem.uuid)'
          }
      }
  }

  computeApiFilesUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-upload-files-elements/', uuid, '/rel/files');
  }
  computePatchFileUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-upload-files-elements-files/', uuid);
  }

  handleUploadRequest (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['file-upload'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['file-upload'].headers['Accept'] = 'application/json';

  }
  handleUploadSuccess (event) {
      console.log('handleUploadSuccess', event.detail.xhr.response);
      this.push('files', JSON.parse(event.detail.xhr.responseText));
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
  fileDeleteDialogOpen (event) {
      this.selectedItem = this.$$('#file-repeater').itemForElement(event.target);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  fileDelete () {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-file-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  handleDeleteResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('files', this.files.indexOf(this.selectedItem), 1);
  }
  fileEditItem (event) {
      this.selectedItem = this.$$('#file-repeater').itemForElement(event.target);
      this.editing = true;
  }
  isEdited (item, editing) {
      return (item === this.selectedItem) && this.editing;
  }
  cancelEdit (event) {
      console.log('cancelEdit');
      this.editing = false;
  }
  updateFile (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-file-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          name: this.shadowedItemData.name,
          description: this.shadowedItemData.description,
      };
      ajaxElem.generateRequest();
  }
  handleFileEditResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.editing = false;
      this.splice('files', this.files.indexOf(this.selectedItem), 1, event.detail.response);
  }

  //            _attachDom(dom) {
  //                this.appendChild(dom);
  //            }
}

customElements.define(ZigguratCMSAdminUploadFiles.is, ZigguratCMSAdminUploadFiles);
