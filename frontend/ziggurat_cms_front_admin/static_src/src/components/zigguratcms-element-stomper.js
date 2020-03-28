import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '../shared-styles.js';
import './quill-editor/zigguratcms-quill-editor.js';
import './gallery/zigguratcms-gallery.js';
import './upload-files/zigguratcms-upload-files.js';
import './grid/zigguratcms-grid.js';
import './blog/zigguratcms-blog.js';
import './no-elem.js';
import { dom as dom$0 } from '@polymer/polymer/lib/legacy/polymer.dom.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

class ZigguratCMSElementStomper extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
    static get is() {
        return "zigguratcms-element-stomper";
    }

    static get properties() {
        return {
            resource: Object,
            elementUuid: String,
            rowUuid: String,
            columnUuid: String,
            stompedUuid: String,
            elements: {
                type: Object,
                notify: true
            },
            uiRouterTransition: {
                type: Object,
                value: function () {
                    return {}
                }
            },
            uiRouterParams: {
                type: Object,
                value: function () {
                    return {}
                }
            }
        }
    }

    static get observers() {
        return [
            'setElem(stompedUuid, elements)'
        ]
    }

    getData() {
        for (var x = 0; x < this.elements.length; x++) {
            if (this.elements[x].uuid == this.stompedUuid) {
                return this.elements[x];
            }
        }
    }

    setElem() {
        var data = this.getData();
        var node = document.createElement(data.type);
        var keys = Object.keys(data);
        for (var x = 0; x < keys.length; x++) {
            node[keys[x]] = data[keys[x]];
        }
        node.resourceUuid = this.resource.uuid;
        node.resource = this.resource;
        node.uiRouterTransition = this.uiRouterTransition;
        node.uiRouterParams = this.uiRouterParams;
        node.uiRouterResolvedData = this.uiRouterResolvedData;
        node.elements = this.elements;
        dom$0(this).appendChild(node);
    }

    _attachDom(dom) {
        this.appendChild(dom);
    }
}

customElements.define(ZigguratCMSElementStomper.is, ZigguratCMSElementStomper);
