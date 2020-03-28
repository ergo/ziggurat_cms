import '@polymer/polymer/polymer-legacy.js';
import '@polymer/iron-selector/iron-selector.js';
import '@polymer/iron-image/iron-image.js';
import '@polymer/paper-button/paper-button.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import './paper-gallery-item.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { beforeNextRender } from '@polymer/polymer/lib/utils/render-status.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';
class PaperGallery extends GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement)) {
  static get template() {
    return html`
        <style>

            :host {
                display: block;
            }

            .image-selector ::slotted(.iron-selected)  {
                display: block !important;
            }

            .image-selector ::slotted(*) {
                display: none;
            }

            .image-selector ::slotted(iron-image) {
                width: 100%;
                --iron-image-width: 100%;
                height: 600px;
                --iron-image-height: 100%;
            }

            .controls {
                text-align: center;
                margin: 10px 0;
            }

            paper-item {
                cursor: pointer;
            }


        </style>

        <div class="controls">
            <paper-button raised="" on-tap="selectPrevious">[[localize('Previous')]]</paper-button>

            <span>[[computedSelected]]/[[items.length]]</span>

            <paper-button raised="" on-tap="selectNext">[[localize('Next')]]</paper-button>
        </div>

        <iron-selector selected="[[selected]]" selectable="paper-gallery-item" selected-attribute="iron-selected" class="image-selector">
            <slot name="entries"></slot>
        </iron-selector>

        <div class="controls">
            <paper-button raised="" on-tap="selectPrevious">[[localize('Previous')]]</paper-button>

            <span>[[computedSelected]]/[[items.length]]</span>

            <paper-button raised="" on-tap="selectNext">[[localize('Next')]]</paper-button>
        </div>

        <template is="dom-if" if="[[showList]]">
            <paper-listbox selected="{{selected}}">
                <template is="dom-repeat" items="[[computedItemData(items)]]">
                    <paper-item class="paper-item-link">[[item.title]]</paper-item>
                </template>
            </paper-listbox>
        </template>
`;
  }

  static get is() {
      return "paper-gallery";
  }

  static get properties() {
      return {
          selected: {
              type: Number,
              value() {
                  return 0
              }
          },
          items: {
              type: Array,
              value() {
                  return []
              }
          },
          computedSelected: {
              computed: 'computeSelected(selected)'
          },
          showList: {
              type: Boolean,
              value: false
          },
          // Localization
          useKeyIfMissing: {
              value: true,
              type: Boolean
          },
          language: {
              value() {
                  return window.TRANSLATION_LANGUAGE || 'en';
              },
              type: String
          },
          resources: {
              type: Object,
              value() {
                  return window.TRANSLATIONS || {en:{}, pl:{}}
              }
          }
      }
  }

  computedItemData() {
      var metadata = [];
      for (var x = 0; x < this.items.length; x++) {
          var item = this.items[x];
          metadata.push({
              title: item.title,
              description: item.description
          });
      }
      return metadata;
  }

  connectedCallback() {
      super.connectedCallback();
      beforeNextRender(this, function() {
          var children = this.getEffectiveChildren('entries');
          this.items = children;
      });
  }

  computeSelected() {
      return this.selected + 1;
  }

  selectPrevious() {
      this.selected = this.selected - 1;
      if (this.selected < 0) {
          this.selected = this.items.length - 1;
      }
  }
  selectNext() {
      if (this.selected + 1 < this.items.length) {
          this.selected = this.selected + 1;
      }
      else {
          this.selected = 0
      }

  }
}

customElements.define(PaperGallery.is, PaperGallery);
