import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/paper-toggle-button/paper-toggle-button.js';
import '../../components/form-validation-decorator.js';
import '../../components/zigguratcms-element-stomper.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSAdminResourceEditCategoryView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <paper-toggle-button checked="{{resource.config.list_children}}">[[localize('List sub-nodes')]]</paper-toggle-button>

        <template is="dom-if" if="[[isAttached]]">

            <zigguratcms-element-stomper stomped-uuid="[[resource.elements.0.uuid]]" elements="{{resource.elements}}" resource="[[resource]]" router-data="[[routerData]]" router-routes="[[routerRoutes]]">
            </zigguratcms-element-stomper>

        </template>
`;
  }

  static get is() {
      return "zigguratcms-resource-edit-category-node-view";
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

customElements.define(ZigguratCMSAdminResourceEditCategoryView.is, ZigguratCMSAdminResourceEditCategoryView);
