import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '../../components/form-validation-decorator.js';
import '../../components/zigguratcms-element-stomper.js';
import '../../shared-styles.js';
import '../../behaviors/ziggurat-admin-basic.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSAdminResourceEditPageView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <template is="dom-if" if="[[isAttached]]">
            <zigguratcms-element-stomper stomped-uuid="[[resource.elements.0.uuid]]" elements="{{resource.elements}}" resource="[[resource]]" ui-router-transition="[[uiRouterTransition]]" ui-router-params="[[uiRouterParams]]" ui-router-resolved-data="[[uiRouterResolvedData]]">
            </zigguratcms-element-stomper>
        </template>
`;
  }

  static get is() {
      return "zigguratcms-resource-edit-page-node-view";
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

customElements.define(ZigguratCMSAdminResourceEditPageView.is, ZigguratCMSAdminResourceEditPageView);
