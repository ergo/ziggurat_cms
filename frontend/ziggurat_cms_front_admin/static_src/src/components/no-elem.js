import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import '@polymer/paper-button/paper-button.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSNoElem extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }
        </style>

        <iron-ajax id="ajax-element" handle-as="json" bubbles="" method="POST" content-type="application/json" on-iron-ajax-response="handleAjaxElementResponse" on-iron-ajax-request="handleAjaxElementRequest" on-iron-ajax-error="AjaxElementError" debounce-duration="100"></iron-ajax>

        <paper-dropdown-menu label="[[localize('Set element type')]]">
            <paper-listbox slot="dropdown-content" selected="{{type}}" attr-for-selected="value">
                <template is="dom-repeat" items="[[possibleTypes]]">
                    <paper-item value="[[item.value]]">[[item.text]]</paper-item>
                </template>
            </paper-listbox>
        </paper-dropdown-menu>

        <paper-button on-tap="changeElementType" raised="">[[localize('Set')]]</paper-button>
`;
  }

  static get is() {
      return "zigguratcms-no-elem";
  }

  static get properties() {
      return {
          appConfig: {
              type: Object,
              value() {
                  return window.APP_CONFIG
              }
          },
          type: String,
          resource: Object,
          possibleTypes: {
              type: Array,
              value() {
                  return [
                      {text: 'Text Editor', value: 'zigguratcms-quill-editor'},
                      {text: 'Gallery', value: 'zigguratcms-gallery'},
                      {text: 'File Uploads', value: 'zigguratcms-upload-files'},
                      {text: 'Blog', value: 'zigguratcms-blog'},
                  ]
              }
          }
      }
  }

  getElementEndpoint(elemType) {
      console.log('getElementEndpoint', this.appConfig.elementMappings[elemType]);
      return this.appConfig.elementMappings[elemType];
  }

  getNodeEndpoint(nodeType) {
      console.log('getNodeEndpoint', this.appConfig.nodeMappings, nodeType, this.appConfig.nodeMappings[nodeType]);
      return this.appConfig.nodeMappings[nodeType];
  }

  changeElementType(event) {
      if (!this.type) {
          return
      }
      var ajaxElem = this.$['ajax-element'];
      var url = this.getAPIUrl(this.appConfig, '/resources/', this.resource.uuid, '/rel/', this.getElementEndpoint(this.type));
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          'element_uuid': this.elementUuid,
          'row_uuid': this.rowUuid,
          'column_uuid': this.columnUuid
      };
      ajaxElem.url = url;
      ajaxElem.generateRequest();
  }

  handleAjaxElementResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.fire('zigguratcms-grid-column-element-created',
          {
              elementUuid: this.elementUuid,
              rowUuid: this.rowUuid,
              columnUuid: this.columnUuid,
              data: event.detail.response
          });
  }

  handleAjaxElementRequest(event) {
      this.fire('overlay-ajax-started', {});
  }

  AjaxElementError(event) {
      this.fire('overlay-ajax-stopped', {});
  }
}

customElements.define(ZigguratCMSNoElem.is, ZigguratCMSNoElem);
