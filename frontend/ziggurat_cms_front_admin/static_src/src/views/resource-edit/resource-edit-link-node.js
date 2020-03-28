import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/paper-input/paper-input.js';
import '../../components/form-validation-decorator.js';
import '../../components/zigguratcms-element-stomper.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSAdminResourceEditLinkView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <paper-input name="url" value="{{resource.config.link}}" label="URL to redirect to" placeholder="[[localize('Your URL')]]"></paper-input>
`;
  }

  static get is() {
      return "zigguratcms-resource-edit-link-node-view";
  }

  static get properties() {
      return {
          isAttached: {
              type: Boolean
          },
          resource: {
              type: Object
          }
      }
  }

  connectedCallback() {
      super.connectedCallback();
      this.isAttached = true;
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminResourceEditLinkView.is, ZigguratCMSAdminResourceEditLinkView);
