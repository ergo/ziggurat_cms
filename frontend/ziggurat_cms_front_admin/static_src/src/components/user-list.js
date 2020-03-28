import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '../behaviors/ziggurat-admin-basic.js';
import '../shared-styles.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-button/paper-button.js';
import 'polymer-ui-router/uirouter-sref.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSAdminUserList extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior], PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles"></style>

        <iron-ajax id="ajax-users" url="[[getAPIUrl(appConfig, '/users')]]" auto="" handle-as="json" bubbles="" on-iron-ajax-response="handleResponse" on-iron-ajax-request="handleRequest" on-iron-ajax-error="handleError" last-response="{{users}}" content-type="application/json" debounce-duration="100"></iron-ajax>

        <div class="table default" id="resource-list-table">
            <div class="row header">
                <div class="cell">[[localize('User Name')]]</div>
                <div class="cell">[[localize('Email')]]</div>
                <div class="cell">[[localize('Actions')]]</div>
            </div>
            <template is="dom-repeat" items="[[users]]" as="user">
                <div class="row">
                    <div class="cell">[[user.public_user_name]]</div>
                    <div class="cell">[[user.public_email]]</div>
                    <div class="cell actions">
                        <uirouter-sref state="users.edit" param-user-id\$="[[user.uuid]]">
                            <paper-icon-button icon="editor:mode-edit" title="Edit User">
                            </paper-icon-button>
                        </uirouter-sref>
                    </div>
                    <div class="cell type">[[node.resource_type]]</div>
                </div>
            </template>
        </div>
`;
  }

  static get is() {
      return "user-list";
  }

  static get properties() {
      return {}
  }

  handleRequest(event) {
      this.fire('overlay-ajax-started', {});
  }

  handleResponse() {
      this.fire('overlay-ajax-stopped', {});
  }

  handleError(event) {
      event.stopPropagation();
      this.fire('overlay-ajax-stopped', {});
  }
}

customElements.define(ZigguratCMSAdminUserList.is, ZigguratCMSAdminUserList);
