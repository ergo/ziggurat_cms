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
import '../behaviors/ziggurat-admin-basic.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
class ZigguratCMSAdmin404View extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
    Oops you hit a 404. 
`;
  }

  static get is() {
      return "cms-page404";
  }
  static get properties() {
      return {}
  }
  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSAdmin404View.is, ZigguratCMSAdmin404View);
