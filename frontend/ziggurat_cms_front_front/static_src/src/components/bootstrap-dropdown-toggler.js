import '@polymer/polymer/polymer-legacy.js';
import { FlattenedNodesObserver } from '@polymer/polymer/lib/utils/flattened-nodes-observer.js';
import { Debouncer } from '@polymer/polymer/lib/utils/debounce.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { addListener, removeListener } from '@polymer/polymer/lib/utils/gestures.js';
import { timeOut } from '@polymer/polymer/lib/utils/async.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class BootstrapDropdownToggler extends GestureEventListeners(PolymerElement) {
  static get template() {
    return html`
        <slot></slot>
`;
  }

  static get is() {
      return "bootstrap-dropdown-toggler";
  }

  static get properties() {
      return {
          toggled: {
              type: Boolean,
              value: false,
              reflectToAttribute: true
          },
          clsName: {
              type: String,
              value: 'show'
          },
          targetSelector: String,
      }
  }

  constructor() {
      super();
      this._boundHoverListener = this.hoverHandler.bind(this);
  }

  connectedCallback() {
      super.connectedCallback();
      window.addEventListener('mousemove', this._boundHoverListener);
      addListener(this, 'tap', this.toggleCls.bind(this));
  }

  disconnectedCallback() {
      super.disconnectedCallback();
      window.addEventListener('mousemove', this._boundHoverListener);
      removeListener(this, 'tap', this.toggleCls.bind(this));
  }

  hoverHandler(event) {
      this._debouncer = Debouncer.debounce(this._debouncer,
          timeOut.after(50),
          () => {
              var path = event.path || event.composedPath();
              for (var i = 0; i < path.length; i++) {
                  var target = path[i];
                  if (!target.tagName) {
                      continue
                  }
                  if (this.contains(target)) {
                      this.toggled = true;
                      break;
                  } else {
                      this.toggled = false;
                  }
              }
              this.setCls();

          });

  }

  toggleCls() {
      this.toggled = !this.toggled;
      this.setCls();
  }

  setCls(event) {
      let effectiveChildren =
          FlattenedNodesObserver.getFlattenedNodes(this).filter(n => n.nodeType === Node.ELEMENT_NODE);
      if (effectiveChildren.length > 0) {
          let node = effectiveChildren[0].querySelector(this.targetSelector);
          if (node) {
              node.classList.toggle(this.clsName, this.toggled);
          }
      }
  }
}

customElements.define(BootstrapDropdownToggler.is, BootstrapDropdownToggler);
