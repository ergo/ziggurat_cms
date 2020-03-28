import '@polymer/polymer/polymer-legacy.js';
import '@polymer/polymer/lib/utils/flattened-nodes-observer.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { addListener, removeListener } from '@polymer/polymer/lib/utils/gestures.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';
class BootstrapNavToggler extends GestureEventListeners(PolymerElement) {
  static get template() {
    return html`
        <slot></slot>
`;
  }

  static get is() {
      return "bootstrap-nav-toggler";
  }

  static get properties() {
      return {
          toggled: {
              type: Boolean,
              value: false,
              reflectToAttribute: true
          },
          /**
           * Looks in document for element to apply "show" class
           */
          targetSelector: String,
          clsName: {
              type: String,
              value: 'show'
          }
      }
  }

  toggleCls(event) {
      this.toggled = !this.toggled;
      this.dispatchEvent(new CustomEvent('bootstrap-nav-toggler-toggle', {detail: {toggled: this.toggled}}));
      var node = window.document.querySelector(this.targetSelector);
      node.classList.toggle(this.clsName, this.toggled);
  }

  connectedCallback() {
      super.connectedCallback();
      addListener(this, 'tap', this.toggleCls.bind(this));
  }

  disconnectedCallback() {
      super.connectedCallback();
      removeListener(this, 'tap', this.toggleCls.bind(this));
  }
}

customElements.define(BootstrapNavToggler.is, BootstrapNavToggler);
