/**
`zigguratcms-grid`
Grid that stamps other elements

@demo demo/index.html
*/
/*
  FIXME(polymer-modulizer): the above comments were extracted
  from HTML and may be out of place here. Review them and
  then delete this comment!
*/
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';

import '@polymer/polymer/polymer-legacy.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/paper-button/paper-button.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@polymer/paper-item/paper-item.js';
import '@polymer/paper-toggle-button/paper-toggle-button.js';
import './zigguratcms-grid-column-holder.js';
import '../app-debug.js';
import '../object-cloned-data.js';
import '../../behaviors/ziggurat-admin-basic.js';
import '../../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { addListener, removeListener } from '@polymer/polymer/lib/utils/gestures.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { PolymerElement } from '@polymer/polymer/polymer-element.js';

class ZigguratCMSGrid extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
            }

        </style>

        <paper-dialog id="actions-delete">
            <h3>[[localize('Confirm')]]</h3>
            <p>[[localize('Are you sure you want to delete this row?')]]</p>
            <p>[[localize('There is no undo - all elements and their data will be permanently removed.')]]</p>
            <paper-toggle-button checked="{{confirmedDelete}}">Confirm</paper-toggle-button>
            <div class="buttons">
                <paper-button dialog-dismiss="">Decline</paper-button>
                <template is="dom-if" if="[[confirmedDelete]]">
                    <paper-button dialog-confirm="" autofocus="" on-tap="rowDelete">Accept</paper-button>
                </template>
            </div>
        </paper-dialog>

        <object-cloned-data data="{{selectedRow}}" keys="['position']" shadow-data="{{shadowedRowData}}"></object-cloned-data>

        <paper-dialog id="actions-row-patch">
            <h3>[[localize('Row Config')]]</h3>

            <p>
                <paper-dropdown-menu label="Row Position">
                    <paper-listbox slot="dropdown-content" attr-for-selected="value" selected="{{shadowedRowData.rowIndex}}">
                        <template is="dom-repeat" items="[[shadowedRowData.totalRows]]">
                            <paper-item value="[[index]]">[[incrIndex(index, 1)]]</paper-item>
                        </template>
                    </paper-listbox>
                </paper-dropdown-menu>
            </p>

            <div class="buttons">
                <paper-button dialog-dismiss="">[[localize('Decline')]]</paper-button>
                <paper-button dialog-confirm="" autofocus="" on-tap="rowPatch">[[localize('Accept')]]</paper-button>
            </div>
        </paper-dialog>

        <iron-ajax id="ajax-rows-post" handle-as="json" url="[[newRowsUrl]]" bubbles="" method="POST" content-type="application/json" last-response="{{row}}" on-iron-ajax-response="handleRowPostResponse" on-iron-ajax-request="handleRequest" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-row-patch" handle-as="json" url="[[patchRowUrl]]" bubbles="" method="PATCH" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleRowPatchResponse" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-row-delete" handle-as="json" url="[[patchRowUrl]]" bubbles="" method="DELETE" content-type="application/json" on-iron-ajax-request="handleRequest" on-iron-ajax-response="handleRowDeleteResponse" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-column-post" handle-as="json" url="[[newColumnUrl]]" bubbles="" method="POST" content-type="application/json" last-response="{{newColumn}}" on-iron-ajax-response="handleColumnPostResponse" on-iron-ajax-request="handleRequest" debounce-duration="100"></iron-ajax>

        <div>
            <paper-button raised="" on-tap="rowPostEvent">
                <iron-icon icon="icons:add-circle"></iron-icon>
                [[localize('Add Section')]]
            </paper-button>
        </div>

        <template is="dom-repeat" items="[[config.rows]]" id="row-repeater">
            <div class="row-holder">
                <div class="controls">
                    <a on-tap="rowConfigDialogOpen">
                        <iron-icon icon="icons:settings" title="Configure"></iron-icon>
                    </a>
                    <a on-tap="columnPost">
                        <iron-icon icon="icons:add-circle" title="Add Column"></iron-icon>
                    </a>
                    <a on-tap="rowDeleteDialogOpen">
                        <iron-icon icon="icons:delete" title="Delete Row"></iron-icon>
                    </a>
                </div>

                <zigguratcms-column-holder elements="[[elements]]" ui-router-transition="[[uiRouterTransition]]" ui-router-params="[[uiRouterParams]]" ui-router-resolved-data="[[uiRouterResolvedData]]" resource="[[resource]]" element-uuid="[[uuid]]" columns="[[item.columns]]" class\$="[[item.className]]" row-index="[[index]]" row-uuid="[[item.uuid]]">
                </zigguratcms-column-holder>
            </div>
        </template>
`;
  }

  static get is() {
      return "zigguratcms-grid";
  }
  static get properties() {
      return {
          status: Number,
          resource: Object,
          uuid: String,
          parentElementPKey: String,
          selectedRow: Object,
          shadowedRowData: Object,
          dirty: {
              type: Boolean,
              value: false
          },
          config: {
              type: Object,
              value () {
                  return {}
              },
              notify: true
          },
          isConfigured: Boolean,
          newRowsUrl: {
              type: String,
              computed: 'computedNewRowsUrl(appConfig, uuid)'
          },
          patchRowUrl: {
              type: String,
              computed: 'computedPatchRowUrl(appConfig, selectedRow.uuid, uuid)'
          },
          newColumnUrl: {
              type: String,
              computed: 'computedNewColumnUrl(appConfig, selectedRow.uuid, uuid)'
          }
      }
  }

  static get observers() {
      return [
          'emitChange(config.*)'
      ]
  }

  computedNewRowsUrl(appConfig, uuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-grid-elements/', uuid, '/rel/rows')
  }
  computedPatchRowUrl(appConfig, selectedRowUuid,  elementUuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-grid-elements-rows/', selectedRowUuid, '?element=', elementUuid)
  }
  computedNewColumnUrl(appConfig, selectedRowUuid, elementUuid){
      return this.getAPIUrl(appConfig, '/zigguratcms-grid-elements-rows/', selectedRowUuid, '/rel/columns', '?element=', elementUuid)
  }

  incrIndex (index, amount) {
      return Number(index) + Number(amount);
  }

  handleRowPostResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.push('config.rows', this.row);
  }

  handleRowDeleteResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('config.rows', this.config.rows.indexOf(this.selectedRow), 1);
  }
  handleRequest (event) {
      this.fire('overlay-ajax-started', {});
  }
  rowPostEvent (event) {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-rows-post'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {};
      ajaxElem.generateRequest();
  }
  handleRowPatchResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      this.splice('config.rows', this.config.rows.indexOf(this.selectedRow), 1);
      this.async(function () {
          this.splice('config.rows', event.detail.response.position - 1, 0, event.detail.response);
      });
  }
  columnPost (event) {
      event.preventDefault();
      event.stopPropagation();
      this.selectedRow = this.querySelector('#row-repeater').itemForElement(event.target);
      console.log('columnAdd');
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-column-post'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  rowPatch () {
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-row-patch'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.body = {
          position: this.shadowedRowData.rowIndex + 1
      };
      ajaxElem.generateRequest();
  }
  rowConfigDialogOpen (event) {
      event.preventDefault();
      event.stopPropagation();
      this.selectedRow = this.querySelector('#row-repeater').itemForElement(event.target);
      this.set(['shadowedRowData', 'totalRows'], new Array(this.config.rows.length));
      this.set(['shadowedRowData', 'rowIndex'], event.detail.index);
      this.$['actions-row-patch'].open();
  }
  rowDeleteDialogOpen (event) {
      event.preventDefault();
      event.stopPropagation();
      this.selectedRow = this.querySelector('#row-repeater').itemForElement(event.target);
      console.log('selectedRow', this.selectedRow);
      this.confirmedDelete = false;
      this.$['actions-delete'].open();
  }
  rowDelete (event) {
      console.log('rowDelete');
      var xsrfToken = Cookies.get('XSRF-TOKEN');
      var ajaxElem = this.$['ajax-row-delete'];
      ajaxElem.headers['X-XSRF-TOKEN'] = xsrfToken;
      ajaxElem.generateRequest();
  }
  emitChange () {
      if (!this.isConfigured) {
          return
      }
      this.fire('element-data-changed', {
          config: this.config,
          uuid: this.uuid,
          dirty: false
      });
  }
  handleColumnPostResponse (event) {
      this.fire('overlay-ajax-stopped', {});
      if (event.detail.response) {
          var ix = this.config.rows.indexOf(this.selectedRow);
          this.push(['config', 'rows', ix, 'columns'], event.detail.response);
      }
  }
  handleColumnsChanged (event) {
      for (var x = 0; x < this.config.rows.length; x++) {
          if (this.config.rows[x].uuid === event.detail.uuid) {
              this.set(['config', 'rows', x, 'columns'], event.detail.columns.slice());
          }
      }
  }
  ready () {
      super.ready();
      this.isConfigured = true;
  }
  clickHandler (event) {
      var nodes = this.querySelectorAll('.row-holder');
      for (var x = 0; x < nodes.length; x++) {
          this.toggleClass('active', false, nodes[x]);
      }
      var path = event.composedPath();
      for (var i=0; i < path.length; i++ ){
          var target = path[i];
          if (!target.tagName){
              continue
          }
          var data = this.$['row-repeater'].itemForElement(target);
          if (data && data !== undefined) {
              this.selectedRow = data;
              var ix = this.$['row-repeater'].indexForElement(target);
              this.toggleClass('active', true, nodes[ix]);
              break;
          }
      }
  }

  connectedCallback() {
      super.connectedCallback();

      this.listen(window, 'tap', 'clickHandler');
      this.addEventListener('row-columns-changed', this.handleColumnsChanged.bind(this));
      addListener(window, 'tap', this.clickHandler.bind(this));
  }
  disconnectedCallback() {
      super.disconnectedCallback();
      this.removeEventListener('row-columns-changed', this.handleColumnsChanged.bind(this));
      removeListener(window, 'tap', this.clickHandler.bind(this));
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSGrid.is, ZigguratCMSGrid);
