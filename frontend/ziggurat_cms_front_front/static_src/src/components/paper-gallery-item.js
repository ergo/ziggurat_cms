import '@polymer/polymer/polymer-legacy.js';
import '@polymer/iron-selector/iron-selector.js';
import '@polymer/iron-image/iron-image.js';
import '@polymer/paper-button/paper-button.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';
class PaperGalleryItem extends GestureEventListeners(PolymerElement) {
  static get template() {
    return html`
        <style>

            :host {
                display: block;
            }

            iron-image {
                width: 100%;
                --iron-image-width: 100%;
                height: 600px;
                --iron-image-height: 100%;
            }

            .caption {
                text-align: center;
            }

        </style>

        <iron-image style="background-color: white;" fade="" preload="" sizing="contain" placeholder="[[placeholder]]" src="[[dynamicSrc(shown)]]"></iron-image>
        <div class="caption">
            <p class="title">[[title]]</p>
            <p class="description">[[description]]</p>
        </div>
`;
  }

  static get is() {
      return "paper-gallery-item";
  }

  static get properties() {
      return {
          title: String,
          description: String,
          src: String,
          ironSelected: {
              type: Boolean,
              observer: 'observeIronSelected'
          },
          shown: {
              type: Boolean,
              value: function () {
                  return false
              }
          }

      }
  }

  observeIronSelected(name, type) {
      this.shown = true;
  }

  dynamicSrc() {
      if (this.shown) {
          return this.src;
      }
  }
}

customElements.define(PaperGalleryItem.is, PaperGalleryItem);
