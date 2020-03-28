import '@polymer/polymer/polymer-legacy.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class AppDebug extends GestureEventListeners(PolymerElement) {
  static get template() {
    return html`
        <style>
            pre{
                padding: 5px;
                border: 1px solid;
            }
        </style>
        <slot></slot>
        <pre>[[output]]</pre>
`;
  }

  static get is() {
      return "app-debug";
  }
  static get properties() {
      return {
          data: {
              type: Object
          }
      }
  }

  static get observers() {
      return [
          '_dumpOut(data.*)'
      ]
  }

  _dumpOut() {
      try{
          this.output = JSON.stringify(this.data, null, 4);
      }
      catch(e){
          console.log('ERROR', this.data);
          this.output = '<JSON.stringify ERROR>';
      }
  }
}

customElements.define(AppDebug.is, AppDebug);
