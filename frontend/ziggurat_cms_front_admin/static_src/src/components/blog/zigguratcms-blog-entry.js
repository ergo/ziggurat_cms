import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@vaadin/vaadin-upload';
import 'polymer-ui-router/uirouter-sref.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-input/paper-textarea.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import '../image-picker-dialog.js';
import '../quill-editor/zigguratcms-quill-editor-base.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminBlogEntry extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }
        </style>

        <image-picker-dialog id="image-picker-dialog" router-routes="[[routerRoutes]]" on-image-picker-selected="imageSelected" api-object-type="zigguratcms-blog-elements-images" api-images-url="[[apiImagesUrl]]">
        </image-picker-dialog>

        <iron-ajax id="ajax-entries-patch" handle-as="json" url="[[elementPatchUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>

        <form-validation-decorator field-name="name" error-object="[[formErrors]]">
        <paper-input name="name" placeholder="Entry Title" maxlength="256" label="Entry Title" value="{{entry.name}}"></paper-input>
        </form-validation-decorator>

        <paper-button raised="" on-tap="save">[[localize('Save Entry')]]</paper-button>
        <paper-button raised="" on-tap="fireDismiss">[[localize('Dismiss')]]</paper-button>

        <hr>

        <zigguratcms-quill-editor-base delta="{{entry.config.delta}}" compiled-html="{{entry.config.compiledHtml}}" on-zigguratcms-quill-editor-select-image="openImageDialog" dirty="{{dirty}}"></zigguratcms-quill-editor-base>
`;
  }

  static get is() {
      return "zigguratcms-blog-entry";
  }
  static get properties() {
      return {
          entry: Object,
          dirty: {
              type: Boolean,
              value: false
          },
          apiImagesUrl: {
              type: String,
              computed: 'computedApiImagesUrl(appConfig, entry.uuid)'
          },
          elementPatchUrl: {
              type: String,
              computed: 'computedElementPatchUrl(appConfig, entry.uuid)'
          }
      }
  }

  computedApiImagesUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-blog-elements-entries/', uuid, '/rel/images')
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
  handleError (event) {
      event.stopPropagation();
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
  save (event) {
      this.editing = true;
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-entries-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          name: this.entry.name,
          config: this.entry.config
      };
      ajaxElem.generateRequest();
  }
  fireDismiss (event) {
      this.fire('zigguratcms-blog-entry-dismiss');
  }
  openImageDialog (event) {
      event.stopPropagation();
      this.$['image-picker-dialog'].open();
  }
  imageSelected (event) {
      var editorComponent = this.querySelector('zigguratcms-quill-editor-base');
      var range = editorComponent.quill.getSelection();
      var src = this.appConfig.baseUrl + '/uploads/' + event.detail.upload_path + '/' + event.detail.filename;
      editorComponent.quill.insertEmbed(range.index, 'image', src, Quill.sources.USER);
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminBlogEntry.is, ZigguratCMSAdminBlogEntry);
