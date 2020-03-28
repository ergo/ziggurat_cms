import "js-cookie/src/js.cookie.js"
import "@polymer/polymer/polymer-element.js"
import "@polymer/polymer/lib/mixins/gesture-event-listeners.js"
import "@polymer/app-layout/app-drawer/app-drawer.js"
import "@polymer/app-layout/app-drawer-layout/app-drawer-layout.js"
import "@polymer/app-layout/app-header/app-header.js"
import "@polymer/app-layout/app-header-layout/app-header-layout.js"
import "@polymer/app-layout/app-scroll-effects/app-scroll-effects.js"
import "@polymer/app-layout/app-toolbar/app-toolbar.js"
import "@polymer/app-localize-behavior/app-localize-behavior.js"
import "@polymer/iron-selector/iron-selector.js"
import "@polymer/paper-icon-button/paper-icon-button.js"
import "@polymer/paper-button/paper-button.js"
import "@polymer/paper-toast/paper-toast.js"
import "@polymer/iron-icon/iron-icon.js"
import "@polymer/iron-icons/iron-icons.js"
import "@polymer/iron-icons/social-icons.js"
import "@polymer/iron-icons/editor-icons.js"
import "polymer-ui-router/uirouter-mixin.js"
import "polymer-ui-router/uirouter-router.js"
import "polymer-ui-router/uirouter-sref.js"
import "polymer-ui-router/uirouter-sref-active.js"
import "polymer-ui-router/uirouter-uiview.js"
import "@polymer/iron-flex-layout/iron-flex-layout-classes.js"
import "./behaviors/ziggurat-admin-basic.js"
import "./views/zigguratcms-page404.js"
import "./views/zigguratcms-resources-view.js"
import "./views/zigguratcms-settings-view.js"
import "./views/zigguratcms-users-view.js"
import "./views/zigguratcms-groups-view.js"
import "./views/zigguratcms-index-view.js"
import "./components/user-provider.js"
import "./components/loader-overlay.js"
import "./components/app-debug.js"

import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import '@polymer/app-layout/app-drawer/app-drawer.js';
import '@polymer/app-layout/app-drawer-layout/app-drawer-layout.js';
import '@polymer/app-layout/app-header/app-header.js';
import '@polymer/app-layout/app-header-layout/app-header-layout.js';
import '@polymer/app-layout/app-scroll-effects/app-scroll-effects.js';
import '@polymer/app-layout/app-toolbar/app-toolbar.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
import '@polymer/iron-selector/iron-selector.js';
import '@polymer/paper-icon-button/paper-icon-button.js';
import '@polymer/paper-button/paper-button.js';
import '@polymer/paper-toast/paper-toast.js';
import '@polymer/iron-icon/iron-icon.js';
import '@polymer/iron-icons/iron-icons.js';
import '@polymer/iron-icons/social-icons.js';
import '@polymer/iron-icons/editor-icons.js';
import { UiRouterMixin, uirouter } from 'polymer-ui-router/uirouter-mixin.js';
import 'polymer-ui-router/uirouter-router.js';
import 'polymer-ui-router/uirouter-sref.js';
import 'polymer-ui-router/uirouter-sref-active.js';
import 'polymer-ui-router/uirouter-uiview.js';
import '@polymer/iron-flex-layout/iron-flex-layout-classes.js';
import './behaviors/ziggurat-admin-basic.js';
// import './views/zigguratcms-page404.js';
// import './views/zigguratcms-resources-view.js';
// import './views/zigguratcms-settings-view.js';
// import './views/zigguratcms-users-view.js';
// import './views/zigguratcms-groups-view.js';
// import './views/zigguratcms-index-view.js';
import './components/user-provider.js';
import './components/loader-overlay.js';
import './components/app-debug.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';


class ZigguratCMSAdmin extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior, UiRouterMixin], PolymerElement))) {

    static get template() {
        return html`
        <uirouter-router id="ui-router" states="[[routerStates]]" auto-start></uirouter-router>

        <loader-overlay opened="[[overlayOpened]]" id="loader-overlay" with-backdrop></loader-overlay>
        <user-provider current-user="{{currentUser}}" user-permissions="{{userPermissions}}"
                       top-level-resource-permissions="{{topLevelResourcePermissions}}"
                       access-to-admin="{{accessToAdmin}}"></user-provider>

        <paper-toast id="default-toast" duration="0" text="[[toastMessage]]" opened="[[toastOpened]]">
            <paper-button on-tap="toastClose" raised>[[localize('Close')]]</paper-button>
        </paper-toast>

        <template is="dom-if" if="[[accessToAdmin]]">

            <app-drawer-layout>
                <app-drawer slot="drawer">
                    <div class="drawer-list">
                        <uirouter-sref-active>
                            <uirouter-sref state="index">
                            <span><iron-icon icon="icons:home"></iron-icon>
                                [[localize('Index page')]]</span>
                            </uirouter-sref>
                        </uirouter-sref-active>

                        <uirouter-sref-active>
                            <uirouter-sref state="resources.list">
                            <span><iron-icon icon="icons:add-circle"></iron-icon>
                                [[localize('Resources')]]</span>
                            </uirouter-sref>
                        </uirouter-sref-active>

                        <uirouter-sref-active>
                            <uirouter-sref state="users.list">
                            <span><iron-icon icon="social:person"></iron-icon>
                                [[localize('Users')]]</span>
                            </uirouter-sref>
                        </uirouter-sref-active>
                        <uirouter-sref-active>
                            <uirouter-sref state="groups">
                            <span><iron-icon icon="social:group"></iron-icon>
                                [[localize('Groups')]]</span>
                            </uirouter-sref>
                        </uirouter-sref-active>
                        <uirouter-sref-active>
                            <uirouter-sref state="settings">
                            <span><iron-icon icon="icons:settings"></iron-icon>
                                [[localize('Settings')]]</span>
                            </uirouter-sref>
                        </uirouter-sref-active>

                        <a name="sign-out" href="/sign_out">
                            <iron-icon icon="icons:exit-to-app"></iron-icon>
                            [[localize('Sign Out')]]</a>
                    </div>
                </app-drawer>
                <app-header-layout>
                    <app-header slot="header">
                        <app-toolbar>
                            <paper-icon-button icon="icons:menu" drawer-toggle></paper-icon-button>
                            <div main-title>{{localize('Administration Panel')}}</div>
                        </app-toolbar>
                    </app-header>

                    <uirouter-uiview id="main-uirouter-view"></uirouter-uiview>

                </app-header-layout>
            </app-drawer-layout>


        </template>
`;
    }

    static get is() {
        return "zigguratcms-admin";
    }

    static get properties() {
        return {
            message: {
                type: String,
                statePath: 'message' // ...and let the magic begin!
            },

            routerStates: {
                type: Object,
                value: function () {
                    return [
                        {name: "index", url: "/index", component: 'zigguratcms-index-view'},
                        {
                            name: "resources",
                            url: "/o/resources",
                            abstract: true,
                            component: 'zigguratcms-resources-view'
                        },
                        {
                            name: "resources.list",
                            url: "/list?:objectId",
                            component: 'zigguratcms-resource-list-view'
                        },
                        {
                            name: "resources.create",
                            url: "/:objectId/create",
                            component: 'zigguratcms-resource-create-node-view'
                        },
                        {
                            name: "resources.edit",
                            url: "/:objectId/edit/type/:type",
                            component: 'zigguratcms-resource-edit-node-view'
                        },
                        {name: "users", url: "/o/users", abstract: true, component: 'zigguratcms-users-view'},
                        {name: "users.list", url: "/list", component: 'user-list'},
                        {name: "users.edit", url: "/:userId/edit", component: 'zigguratcms-users-edit-view'},
                        {name: "groups", url: "/o/groups", component: 'zigguratcms-groups-view'},
                        {name: "settings", url: "/settings", component: 'zigguratcms-settings-view'},
                        {name: "profile", url: "/profile", component: 'zigguratcms-profile-view'}
                    ]
                }
            },
            section: {
                type: String,
                reflectToAttribute: true,
                observer: '_sectionChanged'
            },
            accessToAdmin: {
                type: Boolean,
                value: false,
                notify: true
            },
            currentUser: {
                type: Object,
                value: function () {
                    return {};
                }
            },
            userPermissions: {
                type: Array,
                value: function () {
                    return [];
                }
            },
            topLevelResourcePermissions: {
                type: Array,
                value: function () {
                    return [];
                }
            },
            overlayCounter: {
                type: Number,
                value: 0
            },
            overlayOpened: {
                type: Boolean,
                computed: 'computeOverlayOpened(overlayCounter)'
            },
            toastMessage: String,
            toastOpened: Boolean,
            useKeyIfMissing: {
                value: true,
                type: Boolean
            },
            language: {
                value: function () {
                    return window.TRANSLATION_LANGUAGE || 'en'
                },
                type: String
            },
            resources: {
                type: Object,
                value: function () {
                    return window.TRANSLATIONS || {en: {}}
                }
            }
        }
    }

    computeOverlayOpened() {
        console.log('overlay counter', this.overlayCounter)
        if (this.overlayCounter > 0) {
            return true;
        }
        return false;
    }

    handleOverlayAjaxCounter(event) {
        if (event.type == 'overlay-ajax-started') {
            this.overlayCounter += 1
        } else if (this.overlayCounter > 0) {
            this.overlayCounter -= 1;
        }
    }

    toastClose() {
        this.$['default-toast'].close();
    }

    handleToastMessage(event) {
        console.log('handleToastMessage', event);
        this.toastMessage = event.detail.message;
        this.$['default-toast'].open();
    }

    handleFlashMessage(event) {
        console.log('handleFlashMessage', event.detail);
        if (event.detail.messages.length > 0) {
            var message = event.detail.messages[event.detail.messages.length - 1].msg;
            this.dispatchEvent(new CustomEvent('toast-message', {detail: {message: message}}));
        }
    }

    handleIronAjaxError(event) {
        console.log('handleIronAjaxError', event);
        if (event.detail.request.xhr) {
            let flashMessages = event.detail.request.xhr.getResponseHeader('x-flash-messages');
            if (flashMessages) {
                let messages = JSON.parse(flashMessages);
                // no flash may mean we got a 500 response
                if (messages.length == 0) {
                    messages = [
                        {msg: this.localize('HTTP response error'), level: 'danger'}
                    ];
                }
                this.dispatchEvent(new CustomEvent('flash-message', {detail: {messages: messages}}));
            }
        }
    }

    handleIronAjaxResponse(event) {
        console.log('handleIronAjaxResponse', event.detail.response);
        if (event.detail.xhr) {
            let flashMessages = event.detail.xhr.getResponseHeader('x-flash-messages');
            if (flashMessages) {
                flashMessages = JSON.parse(flashMessages);
                this.dispatchEvent(new CustomEvent('flash-message', {detail: {messages: flashMessages}}));
            }
        }
    }

    handleRedirectUrl(event) {
        console.log('event.detail', event.detail);
        uirouter.stateService.go(event.detail.state, event.detail.params || {}, event.detail.options || {});
    }

    constructor() {
        super();
    }

    connectedCallback() {
        super.connectedCallback();
        this.addEventListener('overlay-ajax-started', this.handleOverlayAjaxCounter);
        this.addEventListener('overlay-ajax-stopped', this.handleOverlayAjaxCounter);
        this.addEventListener('toast-message', this.handleToastMessage);
        this.addEventListener('flash-message', this.handleFlashMessage);
        this.addEventListener('iron-ajax-error', this.handleIronAjaxError);
        this.addEventListener('iron-ajax-response', this.handleIronAjaxResponse);
        this.addEventListener('redirect-url', this.handleRedirectUrl);
    }

    disconnectedCallback() {
        super.disconnectedCallback();
        this.removeEventListener('overlay-ajax-started', this.handleOverlayAjaxCounter);
        this.removeEventListener('overlay-ajax-stopped', this.handleOverlayAjaxCounter);
        this.removeEventListener('toast-message', this.handleToastMessage);
        this.removeEventListener('flash-message', this.handleFlashMessage);
        this.removeEventListener('iron-ajax-error', this.handleIronAjaxError);
        this.removeEventListener('iron-ajax-response', this.handleIronAjaxResponse);
        this.removeEventListener('redirect-url', this.handleRedirectUrl);
    }

    _attachDom(dom) {
        this.appendChild(dom);
    }
}

customElements.define(ZigguratCMSAdmin.is, ZigguratCMSAdmin);
