import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '@polymer/iron-overlay-behavior/iron-overlay-behavior.js';
import '@polymer/paper-spinner/paper-spinner.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSAdminResourceLeafProvider extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <iron-ajax id="ajax-navigator" auto="" url="[[url]]" handle-as="json" bubbles="" content-type="application/json" last-response="{{resources}}" on-iron-ajax-response="handleResourceResponse" on-iron-ajax-request="handleResourceRequest" on-iron-ajax-error="handleResourceError" debounce-duration="100"></iron-ajax>
`;
  }

  static get is() {
      return "resource-leaf-provider";
  }
  static get properties() {
      return {
          url: String,
          resources: {
              type: Object,
              notify: true
          }
      }
  }
  handleResourceResponse (event) {
      event.stopPropagation();
      this.fire('resource-leaf-provider-response', event.detail);
  }
  handleResourceRequest (event) {
      event.stopPropagation();
      this.fire('resource-leaf-provider-request', {});
  }
  handleResourceError (event) {
      this.fire('resource-leaf-provider-error', {});
  }
}

customElements.define(ZigguratCMSAdminResourceLeafProvider.is, ZigguratCMSAdminResourceLeafProvider);
