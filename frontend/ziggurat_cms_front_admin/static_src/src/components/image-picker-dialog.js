import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '@vaadin/vaadin-upload';
import '@polymer/iron-list/iron-list.js';
import '@polymer/iron-icons/iron-icons.js';
import '@polymer/iron-icons/image-icons.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/paper-toggle-button/paper-toggle-button.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSImagePickerDialog extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }

            .dialog-contents{
                width: 500px;
            }

            #image-list-header{
                width: 100%;
            }

            #scroller{
                max-height: 350px;
                overflow-y: auto;
            }

            #image-list-body {
                width: 100%;
            }

            .col-image {

            }

            .col-image img {
                width: 50px;
            }

            .col-actions {
                width: 110px;
            }

        </style>

        <iron-ajax id="ajax-images" url="[[apiImagesUrl]]" handle-as="json" bubbles="" on-iron-ajax-response="handleImagesResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" content-type="application/json" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-image-delete" handle-as="json" url="[[getAPIUrl(appConfig, '/', apiObjectType, '/', selectedItem.uuid)]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleResponse" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

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

        <paper-dialog id="actions-upload">
            <div class="dialog-contents">
            <h3>[[localize('Upload')]]</h3>

            <div>

                <vaadin-upload accept="image/*" id="image-upload" on-upload-before="handleUploadRequest" on-upload-success="handleUploadSuccess" target="[[apiImagesUrl]]">
                </vaadin-upload>

            </div>

            <div class="table responsive default" id="image-list-header">
                <div class="row responsive header">
                    <div class="cell responsive col-image">[[localize('Image')]]</div>
                    <div class="cell responsive col-info">[[localize('Info')]]</div>
                    <div class="cell responsive col-actions">[[localize('Actions')]]</div>
                </div>
            </div>
                <div id="scroller">
            <div class="table responsive default" id="image-list-body">
                <template is="dom-repeat" items="[[images]]" id="image-repeater">
                    <div class="row responsive">
                        <div class="cell responsive col-image">
                            <img src="[[appConfig.baseUrl]]/uploads/[[item.upload_path]]/[[item.miniature_filename]]">
                        </div>
                        <div class="cell responsive col-info">
                            <p><strong>[[item.name]]</strong></p>
                        </div>
                        <div class="cell responsive col-actions">
                            <paper-icon-button icon="image:add-to-photos" title="Insert image" data-uuid\$="[[item.uuid]]" on-tap="imageInsert">
                            </paper-icon-button>
                            <paper-icon-button icon="icons:delete" title="Remove image" data-uuid\$="[[item.uuid]]" on-tap="imageDeleteDialogOpen">
                            </paper-icon-button>

                        </div>
                    </div>
                </template>
            </div>
                </div>

            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Close')]]</paper-button>
            </div>
            </div>
        </paper-dialog>
`;
  }

  static get is() {
      return "image-picker-dialog";
  }
  static get properties() {
      return {
          confirmedDelete: Boolean,
          selectedItem: Object,
          apiObjectType: String,
          patchObjectName: String,
          imageObjectTypes: String,
          images: {
              type: Array,
              value () {
                  return []
              }
          }
      }
  }

  handleUploadRequest (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['image-upload'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['image-upload'].headers['Accept'] = 'application/json';
  }
  handleUploadSuccess (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('images', 0, 0, JSON.parse(event.detail.xhr.responseText));
  }
  open () {
      this.$['actions-upload'].open();
      this.$['ajax-images'].generateRequest();
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
  imageInsert (event) {
      this.selectedItem = this.$$('#image-repeater').itemForElement(event.target);
      this.fire('image-picker-selected', this.selectedItem);
      this.$['actions-upload'].close();
  }
  imageDeleteDialogOpen (event) {
      this.selectedItem = this.$$('#image-repeater').itemForElement(event.target);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  imageDelete(){
      this.$['actions-upload'].close();
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-image-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  handleImagesResponse(event){
      this.fire('overlay-ajax-stopped', {});
      this.images = event.detail.response.reverse();
  }

  //            _attachDom(dom) {
  //                this.appendChild(dom);
  //            }
}

customElements.define(ZigguratCMSImagePickerDialog.is, ZigguratCMSImagePickerDialog);
