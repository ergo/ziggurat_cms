import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/iron-image/iron-image.js';
import '@vaadin/vaadin-upload';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-input/paper-textarea.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSAdminGallery extends ZigguratAdminBasicMixin(GestureEventListeners(
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

            #image-list-table {
                width: 100%
            }

            #image-list-table .image {
                width: 150px
            }

            #image-list-table .actions {
                width: 125px
            }

        </style>

        <iron-ajax id="ajax-resource" auto="" url="[[apiImagesUrl]]" handle-as="json" bubbles="" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" content-type="application/json" last-response="{{images}}" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-image-patch" handle-as="json" url="[[patchImageUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleImageEditResponse" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-image-delete" handle-as="json" url="[[patchImageUrl]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleDeleteResponse" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this image?')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">[[localize('Confirm')]]</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="imageDelete">[[localize('Accept')]]</paper-button>
                </template>
            </div>
        </paper-dialog>

        <object-cloned-data data="{{selectedItem}}" shadow-data="{{shadowedItemData}}"></object-cloned-data>

        <h2>[[localize('Gallery Management')]]</h2>

        <vaadin-upload accept="image/*" id="image-upload" on-upload-before="handleUploadRequest" on-upload-success="handleUploadSuccess" target="[[apiImagesUrl]]"></vaadin-upload>

        <div class="table responsive default" id="image-list-table">
            <div class="row responsive header">
                <div class="cell responsive">[[localize('Image')]]</div>
                <div class="cell responsive">[[localize('Info')]]</div>
                <div class="cell responsive">[[localize('Actions')]]</div>
            </div>
            <template is="dom-repeat" items="[[images]]" id="image-repeater">
                <div class="row responsive">
                    <div class="cell responsive image">
                        <iron-image src="[[appConfig.baseUrl]]/uploads/[[item.upload_path]]/[[item.miniature_filename]]"></iron-image>
                    </div>
                    <div class="cell responsive info">
                        <template is="dom-if" if="[[isEdited(item, selectedItem, editing)]]">
                            <p class="name">
                                <paper-input label="Name" value="{{shadowedItemData.name}}" maxlength="128"></paper-input>
                            </p>
                            <p class="description">
                                <paper-textarea label="Description" value="{{shadowedItemData.description}}" maxlength="1000"></paper-textarea>
                            </p>
                            <p class="buttons">
                                <paper-button raised="" on-tap="cancelEdit">[[localize('Cancel')]]</paper-button>
                                <paper-button raised="" on-tap="updateImage">[[localize('Update')]]</paper-button>
                            </p>
                        </template>
                        <template is="dom-if" if="[[!isEdited(item, selectedItem, editing)]]">
                            <p class="name"><strong>[[item.name]]</strong></p>
                            <p class="description">[[item.description]]</p>
                        </template>
                    </div>
                    <div class="cell responsive actions">
                        <paper-icon-button icon="editor:mode-edit" title="Edit" on-tap="imageEditItem">
                        </paper-icon-button>

                        <paper-icon-button icon="icons:delete" title="Delete" on-tap="imageDeleteDialogOpen">
                        </paper-icon-button>
                    </div>
                </div>
            </template>
        </div>
`;
  }

  static get is() {
      return "zigguratcms-gallery";
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
          images: {
              type: Array,
              value () {
                  return []
              }
          },
          dirty: {
              type: Boolean,
              value: false
          },
          apiImagesUrl: {
              type: String,
              computed: 'computedApiImagesUrl(appConfig, uuid)'
          },
          patchImageUrl: {
              type: String,
              computed: 'computedPatchImageUrl(appConfig, selectedItem.uuid)'
          }
      }
  }

  computedApiImagesUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-gallery-elements/', uuid, '/rel/images')
  }
  computedPatchImageUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-gallery-elements-images/', uuid)
  }
  handleUploadRequest (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['image-upload'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['image-upload'].headers['Accept'] = 'application/json';
  }
  handleUploadSuccess (event) {
      console.log('handleUploadSuccess', event.detail.xhr.response);
      this.push('images', JSON.parse(event.detail.xhr.responseText));
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
  imageDeleteDialogOpen (event) {
      this.selectedItem = this.$$('#image-repeater').itemForElement(event.target);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  imageDelete () {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-image-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  handleDeleteResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('images', this.images.indexOf(this.selectedItem), 1);
  }
  imageEditItem (event) {
      this.selectedItem = this.$$('#image-repeater').itemForElement(event.target);
      this.editing = true;
  }
  isEdited (item, editing) {
      return (item === this.selectedItem) && this.editing;
  }
  cancelEdit (event) {
      console.log('cancelEdit');
      this.editing = false;
  }
  updateImage (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-image-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          name: this.shadowedItemData.name,
          description: this.shadowedItemData.description,
      };
      ajaxElem.generateRequest();
  }
  handleImageEditResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.editing = false;
      this.splice('images', this.images.indexOf(this.selectedItem), 1, event.detail.response);
  }

  //            _attachDom(dom) {
  //                this.appendChild(dom);
  //            }
}

customElements.define(ZigguratCMSAdminGallery.is, ZigguratCMSAdminGallery);
