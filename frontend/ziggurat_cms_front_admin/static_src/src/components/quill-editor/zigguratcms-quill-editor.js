import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import 'polymer-ui-router/uirouter-sref.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import '../image-picker-dialog.js';
import './zigguratcms-quill-editor-base.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSQuillEditor extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;

            }

        </style>

        <image-picker-dialog id="image-picker-dialog" on-image-picker-selected="imageSelected" api-object-type="zigguratcms-quill-editor-elements-images" api-images-url="[[getAPIUrl(appConfig, '/zigguratcms-quill-editor-elements/', uuid, '/rel/images')]]">
        </image-picker-dialog>

        <zigguratcms-quill-editor-base delta="{{config.delta}}" compiled-html="{{config.compiledHtml}}" on-zigguratcms-quill-editor-select-image="openImageDialog" dirty="{{dirty}}"></zigguratcms-quill-editor-base>

        <iron-ajax id="ajax" handle-as="json" url="[[getAPIUrl(appConfig, '/zigguratcms-quill-editor-elements/', uuid)]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" debounce-duration="100"></iron-ajax>
`;
  }

  static get is() {
      return "zigguratcms-quill-editor";
  }

  static get properties() {
      return {
          status: Number,
          resourceUuid: String,
          uuid: String,
          config: {
              type: Object,
              value() {
                  return {
                      delta: {},
                      compiledHtml: ''
                  }
              },
              notify: true
          },
          isConfigured: {
              type: Boolean,
              value: false
          },
          dirty: {
              type: Boolean,
              value: false
          },
          images: {
              type: Array,
              value() {
                  return []
              }
          }
      }
  }

  static get observers() {
      return [
          'emitChange(config.*)'
      ]
  }

  emitChange() {
      if (!this.isConfigured) {
          return
      }
      this.fire('element-data-changed', {
          config: this.config,
          uuid: this.uuid,
          dirty: this.dirty
      });
  }

  ready() {
      super.ready();
      this.isConfigured = true;
  }

  attached() {
      this.listen(window, 'cms-elements-save-dirty', 'handleSaveDirty');
  }

  detached() {
      this.unlisten(window, 'cms-elements-save-dirty', 'handleSaveDirty');
  }

  handleSaveDirty() {
      console.log('handleSaveDirty', Math.random(), this.uuid);
      if (this.dirty) {
          this.save();
      }
  }

  save() {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      this.$['ajax'].headers['X-XSRF-TOKEN'] = xsrfToken;
      this.$['ajax'].body = {
          config: this.config
      };
      this.$['ajax'].generateRequest();
  }

  handleRequest() {
      this.fire('overlay-ajax-started', {});
  }

  handleResponse() {
      this.fire('overlay-ajax-stopped', {});
      this.dirty = false;
      this.emitChange();
  }

  handleError() {
      this.fire('overlay-ajax-stopped', {});
  }

  openImageDialog(event) {
      event.stopPropagation();
      this.$['image-picker-dialog'].open();
  }

  imageSelected(event) {
      var editorComponent = this.querySelector('zigguratcms-quill-editor-base');
      var range = editorComponent.quill.getSelection();
      var src = this.appConfig.baseUrl + '/uploads/' + event.detail.upload_path + '/' + event.detail.filename;
      editorComponent.quill.insertEmbed(range.index, 'image', src, Quill.sources.USER);
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSQuillEditor.is, ZigguratCMSQuillEditor);
