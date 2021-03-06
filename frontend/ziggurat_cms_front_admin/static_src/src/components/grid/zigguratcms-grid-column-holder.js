import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/paper-toggle-button/paper-toggle-button.js';
import '../../shared-styles.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../zigguratcms-element-stomper.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { dom as dom$0 } from '@polymer/polymer/lib/legacy/polymer.dom.js';
import { addListener, removeListener } from '@polymer/polymer/lib/utils/gestures.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSGridColumnHolder extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <iron-ajax id="ajax-column-patch" handle-as="json" url="[[patchColumnUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleColumnPatchResponse" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-column-delete" handle-as="json" url="[[patchColumnUrl]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleColumnDeleteResponse" debounce-duration="100"></iron-ajax>

        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this column?')]]</p>
            <p>[[localize('There is no undo - all elements and their data will be permanently removed.')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">Confirm</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="columnDelete">[[localize('Accept')]]</paper-button>
                </template>
            </div>
        </paper-dialog>

        <object-cloned-data data="{{selectedColumn}}" keys="['position', 'config']" shadow-data="{{shadowedColumnData}}"></object-cloned-data>

        <paper-dialog id="actions-column-patch">
            <h3>Column Config</h3>

            <p>
                <paper-dropdown-menu label="Column Position">
                    <paper-listbox slot="dropdown-content" attr-for-selected="value" selected="{{shadowedColumnData.columnIndex}}">
                        <template is="dom-repeat" items="[[shadowedColumnData.totalColumns]]">
                            <paper-item value="[[index]]">[[incrIndex(index, 1)]]</paper-item>
                        </template>
                    </paper-listbox>
                </paper-dropdown-menu>
            </p>
            <p>
                <paper-dropdown-menu label="Column Size">
                    <paper-listbox slot="dropdown-content" attr-for-selected="value" selected="{{shadowedColumnData.config.span}}">
                        <template is="dom-repeat" items="[[shadowedColumnData.columnSizes]]">
                            <paper-item value="[[incrIndex(index, 1)]]">[[incrIndex(index, 1)]]</paper-item>
                        </template>
                    </paper-listbox>
                </paper-dropdown-menu>
            </p>
            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <paper-button dialog-confirm="" autofocus="" on-tap="columnPatch">[[localize('Accept')]]</paper-button>
            </div>
        </paper-dialog>
        <div class="container">


            <div class="row">

                <template is="dom-if" if="[[!columns.length]]">
                    <div class="col-md-12">
                        <div class="column-contents">
                            [[localize('No columns set')]]
                        </div>
                    </div>
                </template>
                <template is="dom-repeat" items="[[columns]]" as="column" id="column-repeater">
                    <div class\$="col-md-[[column.config.span]] column">
                        <div class="column-contents">
                            <div class="controls">
                                <a on-tap="columnConfigDialogOpen">
                                    <iron-icon icon="icons:settings" title="Configure"></iron-icon>
                                </a>
                                <a on-tap="columnDeleteDialogOpen">
                                    <iron-icon icon="icons:delete" title="Delete Column"></iron-icon>
                                </a>
                            </div>

                            <template is="dom-repeat" items="[[column.element_uuids]]" as="elemUuid">
                                <zigguratcms-element-stomper stomped-uuid="[[elemUuid]]" elements="[[elements]]" ui-router-transition="[[uiRouterTransition]]" ui-router-params="[[uiRouterParams]]" ui-router-resolved-data="[[uiRouterResolvedData]]" resource="[[resource]]" element-uuid="[[elementUuid]]" row-uuid="[[rowUuid]]" column-uuid="[[column.uuid]]">
                                </zigguratcms-element-stomper>
                            </template>

                            <template is="dom-if" if="[[!column.element_uuids.length]]">
                                <zigguratcms-no-elem ui-router-transition="[[uiRouterTransition]]" ui-router-params="[[uiRouterParams]]" ui-router-resolved-data="[[uiRouterResolvedData]]" resource="[[resource]]" element-uuid="[[elementUuid]]" row-uuid="[[rowUuid]]" column-uuid="[[column.uuid]]">
                                </zigguratcms-no-elem>
                            </template>
                        </div>
                    </div>
                </template>
            </div>
        </div>
`;
  }

  static get is() {
      return "zigguratcms-column-holder";
  }

  static get properties() {
      return {
          noElemData: {
              type: Object,
              value() {
                  return [{
                      type: 'no-elem',
                      config: {},
                      uuid: '0'
                  }]
              }
          },
          rowIndex: Number,
          elementUuid: String,
          rowUuid: String,
          resource: Object,
          selectedColumn: Object,
          columns: {
              type: Array,
              value() {
                  return []
              },
              notify: true
          },
          isConfigured: Boolean,
          patchColumnUrl: {
              type: String,
              computed: 'computedPatchColumnUrl(appConfig, selectedColumn.uuid, elementUuid)'
          }
      }
  }

  static get observers() {
      return [
          'emitChange(columns.*)'
      ]
  }

  computedPatchColumnUrl(appConfig, uuid, elementUuid) {
      return this.getAPIUrl(appConfig, '/zigguratcms-grid-elements-columns/', uuid, '?element=', elementUuid)
  }

  emitChange() {
      if (!this.isConfigured) {
          return
      }
      this.fire('row-columns-changed', {
          columns: this.columns,
          uuid: this.rowUuid,
          dirty: false
      });
  }

  showConfigRowEvent(event) {
      this.fire('zigguratcms-grid-row-config-dialog', {
          uuid: this.rowUuid,
          index: Number(this.rowIndex)
      });
  }

  handleColumnDeleteResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('columns', this.columns.indexOf(this.selectedColumn), 1);
  }

  handleRequest(event) {
      this.fire('overlay-ajax-started', {});
  }

  rowPositionPlus(event) {
      var payload = {index: Number(this.rowIndex)};
      console.log('rowPositionPlus', payload);
      this.fire('zigguratcms-grid-row-position-plus', payload);
  }

  rowPositionMinus(event) {
      var payload = {index: Number(this.rowIndex)}
      console.log('rowPositionMinus', payload);
      this.fire('zigguratcms-grid-row-position-minus', payload);
  }

  rowDeleteEvent(event) {
      var payload = {uuid: this.rowUuid, index: Number(this.rowIndex)};
      console.log('rowDeleteEvent', payload);
      this.fire('zigguratcms-grid-row-delete-dialog', payload);
  }

  showOptions() {
      this.querySelector('paper-dialog').open();
  }

  columnDeleteDialogOpen(event) {
      event.preventDefault();
      event.stopPropagation();
      console.log('columnDeleteDialogOpen', event.detail);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }

  columnDelete() {
      console.log('columnDelete');
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-column-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }

  columnPatch() {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-column-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          position: this.shadowedColumnData.columnIndex + 1,
          config: {span: this.shadowedColumnData.config.span}
      };
      ajaxElem.generateRequest();
  }

  columnConfigDialogOpen(event) {
      event.preventDefault();
      event.stopPropagation();
      this.set(['shadowedColumnData', 'totalColumns'], new Array(this.columns.length));
      this.set(['shadowedColumnData', 'columnIndex'], this.columns.indexOf(this.selectedColumn));
      this.set(['shadowedColumnData', 'columnSizes'], new Array(12));
      this.$['actions-column-patch'].open();
  }

  handleColumnPatchResponse(event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('columns', this.columns.indexOf(this.selectedColumn), 1);
      this.async(function () {
          this.splice('columns', event.detail.response.position - 1, 0, event.detail.response);
      });
  }

  incrIndex(index, amount) {
      return Number(index) + Number(amount);
  }

  clickHandler(event) {
      var nodes = dom$0(this).querySelectorAll('.column');
      for (var x = 0; x < nodes.length; x++) {
          this.toggleClass('active', false, nodes[x]);
      }
      var path = event.composedPath();
      for (var i = 0; i < path.length; i++) {
          var target = path[i];
          if (!target.tagName) {
              continue
          }
          var data = this.$['column-repeater'].itemForElement(target);
          if (data && data !== undefined) {
              this.selectedColumn = data;
              var ix = this.$['column-repeater'].indexForElement(target);
              this.toggleClass('active', true, nodes[ix]);
              break;
          }
      }
  }

  columnNewElementCreated(event) {
      for (var x = 0; x < this.columns.length; x++) {
          var column = this.columns[x];
          if (column.uuid == event.detail.columnUuid) {
              this.push(['columns', x, 'element_uuids'], event.detail.data.uuid);
              this.push(['elements'], event.detail.data);
          }
      }
  }

  connectedCallback() {
      super.connectedCallback();
      this.addEventListener('zigguratcms-grid-column-element-created', this.columnNewElementCreated.bind(this));
      addListener(window, 'tap', this.clickHandler.bind(this));
  }

  disconnectedCallback() {
      super.disconnectedCallback();
      this.removeEventListener('zigguratcms-grid-column-element-created', this.columnNewElementCreated.bind(this));
      removeListener(window, 'tap', this.clickHandler.bind(this));
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSGridColumnHolder.is, ZigguratCMSGridColumnHolder);
