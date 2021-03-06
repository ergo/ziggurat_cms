import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '../behaviors/ziggurat-admin-basic.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import {UiRouterMixin} from 'polymer-ui-router/uirouter-mixin.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/iron-form/iron-form.js';
import '@polymer/iron-ajax/iron-ajax.js';
import '@polymer/paper-dialog/paper-dialog.js';
import '@polymer/paper-input/paper-input.js';
import '@polymer/paper-button/paper-button.js';
import '../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';

class ZigguratCMSUserProvider extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <iron-ajax id="ajax-user" url="[[getAPIUrl(appConfig, '/users/self')]]" handle-as="json" bubbles="" on-iron-ajax-response="handleUserResponse" on-iron-ajax-error="handleUserRequestError" on-iron-ajax-request="handleUserRequest" content-type="application/json" debounce-duration="100"></iron-ajax>

        <iron-ajax id="ajax-user-permissions" url="[[getAPIUrl(appConfig, '/resources/', applicationUuid, '/rel/permissions')]]" handle-as="json" bubbles="" on-iron-ajax-request="handlePermissionsRequest" on-iron-ajax-response="handlePermissionsResponse" content-type="application/json" debounce-duration="100"></iron-ajax>

        <paper-dialog id="login-dialog" no-cancel-on-outside-click="" no-cancel-on-esc-key="">
            <h2>{{localize('Login Form')}}</h2>
            <iron-form id="login-form" on-iron-form-presubmit="handleIronFormPresubmit" on-iron-form-error="handleLoginResponseError" on-iron-form-response="handleLoginResponse">
                <form method="post" enctype="application/x-www-form-urlencoded" action="[[appConfig.baseUrl]]/sign_in">
                    <iron-a11y-keys id="a11y" keys="enter" on-keys-pressed="submitForm"></iron-a11y-keys>
                    <paper-input label="{{localize('User Name')}}" name="login" disabled="[[formDisabled]]"></paper-input>
                    <paper-input label="{{localize('Password')}}" type="password" name="password" disabled="[[formDisabled]]"></paper-input>
                    <div class="buttons">
                        <paper-button raised="" on-tap="submitForm" disabled="[[formDisabled]]">{{localize('Sign In')}}
                        </paper-button>
                    </div>
                </form>
            </iron-form>
        </paper-dialog>
`;
  }

  static get is() {
      return "user-provider";
  }

  static get properties() {
      return {
          formDisabled: Boolean,
          userUuid: String,
          applicationUuid: String,
          currentUser: {
              type: Object,
              value() {
                  return {};
              },
              notify: true
          },
          accessToAdmin: {
              type: Boolean,
              value: false,
              notify: true
          },
          userPermissions: {
              type: Array,
              value() {
                  return [];
              },
              notify: true
          },
          topLevelResourcePermissions: {
              type: Array,
              value() {
                  return [];
              },
              notify: true
          }
      }
  }
  constructor() {
      super();
  }
  connectedCallback() {
      super.connectedCallback();
      console.log('debug', this.appConfig);
      this.userUuid = window.USER_UUID;
      this.applicationUuid = this.appConfig.applicationUUID;
      if (!this.userUuid) {
          this.$['login-dialog'].open();
      }
      else {
          this.fetchUser();
      }

  }

  fetchUser() {
      if (this.userUuid) {
          this.$['ajax-user'].generateRequest();
      }
  }

  hasAccessToAdmin() {
      var access = false;
      for (var x = 0; x < this.topLevelResourcePermissions.length; x++) {
          var elem = this.topLevelResourcePermissions[x];
          if (['admin_panel', 'administration', 'root_administraion'].indexOf(elem.perm_name) !== -1) {
              access = true;
          }
      }
      if (!access) {
          this.fire('toast-message', {message: this.localize('You have insufficient permissions.')});
      }
      console.log('hasAccessToAdmin', access);
      return access;
  }

  submitForm() {
      this.$['login-form'].headers['X-XSRF-TOKEN'] = this.getCSRFToken();
//                this.$['login-form'].headers['Content-type'] = "application/json";
      this.$['login-form'].submit();
  }

  handleIronFormPresubmit(event) {
      console.log('handleIronFormPresubmit', event);
      this.formDisabled = true;
  }

  handleUserResponse(event) {
      console.log('handleUserResponse', event);
      this.currentUser = event.detail.response;
      this.fire('user-login-success', this.currentUser);
      this.$['ajax-user-permissions'].generateRequest();
      this.dispatchOverlayStopped();

  }

  handleUserRequest(event) {
      console.log('handleUserRequest', event.detail);
      this.fire('user-login-request', {});
      this.dispatchOverlayStarted();
  }

  handleUserRequestError(event) {
      // we don't want to show http error on first load
      event.stopPropagation();
      console.log('handleUserRequestError', event.detail);
      this.fire('user-login-error', {});
      this.dispatchOverlayStopped();
      this.$['login-dialog'].open();
      this.formDisabled = false;
  }

  handleLoginResponseError(event) {
      console.log('handleLoginResponseError', event);
      this.formDisabled = false;
      this.fire('iron-ajax-error', event.detail);
  }

  handleLoginResponse(event) {
      console.log('handleLoginResponse', event);
      this.formDisabled = false;
      this.fire('user-login-success', {});
      this.fire('iron-ajax-response', event.detail);
      this.userUuid = event.detail.response.uuid;
      this.$['ajax-user-permissions'].generateRequest();
  }

  handlePermissionsRequest(event) {
      this.dispatchOverlayStarted();
  }

  handlePermissionsResponse(event) {
      this.dispatchOverlayStopped();
      this.topLevelResourcePermissions = event.detail.response;
      this.accessToAdmin = this.hasAccessToAdmin(
          this.topLevelResourcePermissions);
      if (!this.accessToAdmin) {
          this.$['login-dialog'].open();
      }
      else {
          this.$['login-dialog'].close();
      }
  }
}

customElements.define(ZigguratCMSUserProvider.is, ZigguratCMSUserProvider);
