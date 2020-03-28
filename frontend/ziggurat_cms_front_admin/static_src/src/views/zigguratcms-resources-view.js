/**
@license
Copyright (c) 2016 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
Code distributed by Google as part of the polymer project is also
subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
*/
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '../shared-styles.js';
import '@polymer/iron-ajax/iron-ajax.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/paper-tooltip/paper-tooltip.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../components/resource-leaf-provider.js';
import './zigguratcms-resource-edit-node-view.js';
import './zigguratcms-resource-create-node-view.js';
import './zigguratcms-resource-list-view.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminResourcesView extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <div class="admin-section-view">

            <uirouter-uiview></uirouter-uiview>

        </div>
`;
  }

  static get is() {
      return "zigguratcms-resources-view";
  }
  static get properties() {
      return {
          appResources: Array,
          resourceUUID: String
      }
  }
  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdminResourcesView.is, ZigguratCMSAdminResourcesView);
