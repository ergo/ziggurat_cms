import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import { IronOverlayBehavior } from '@polymer/iron-overlay-behavior/iron-overlay-behavior.js';
import '@polymer/paper-spinner/paper-spinner.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
const $_documentContainer = document.createElement('template');

$_documentContainer.innerHTML = `<dom-module id="loader-overlay">
    <style>
        paper-spinner{
            width: 100px;
            height: 100px;
            --paper-spinner-stroke-width: 10px;
        }

    </style>
    <template>
        <paper-spinner active="" class="page-loader thick"></paper-spinner>
    </template>

</dom-module>`;

document.head.appendChild($_documentContainer.content);

class ZigguratCMSLoaderOverlay extends GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior, IronOverlayBehavior],PolymerElement)) {
    static get is() {
        return "loader-overlay";
    }
    static get properties() {
        return {
            noCancelOnOutsideClick: {
                type: Boolean,
                value: true
            },
            noCancelOnEscKey: {
                type: Boolean,
                value: true
            }
        }
    }
//        _attachDom(dom) {
//            this.appendChild(dom);
//        }
}

customElements.define(ZigguratCMSLoaderOverlay.is, ZigguratCMSLoaderOverlay);
