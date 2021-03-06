import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ObjectClonedData extends PolymerElement {
    static get is() {
        return "object-cloned-data";
    }

    static get properties() {
        return {
            data: {
                type: Object,
                notify: true
            },
            keys: Array,
            shadowData: {
                type: Object,
                notify: true
            },
            onlyOnce: {
                type: Boolean,
                value: false
            }
        }
    }

    static get observers() {
        return [
            'clone(data.*)'
        ]
    }

    getKeys() {
        var keys = [];
        if (this.keys) {
            keys = this.keys
        }
        else if (this.data) {
            keys = Object.keys(this.data);
        }
        return keys;
    }

    clone() {
        if (typeof this.shadowData === 'object' && this.onlyOnce) {
            return false
        }
        var keys = this.getKeys();
        this.shadowData = {};
        for (var x = 0; x < keys.length; x++) {
            this.set(['shadowData', keys[x]], JSON.parse(JSON.stringify(this.data[keys[x]])));
        }
    }

    reflect() {
        var keys = this.getKeys();
        for (var x = 0; x < keys.length; x++) {
            this.set(['data', keys[x]], this.shadowData[keys[x]]);
        }
    }
}

customElements.define(ObjectClonedData.is, ObjectClonedData);
