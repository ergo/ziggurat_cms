let ZigguratAdminBasicMixin = (superClass) => class extends superClass {

    static get properties() {
        return {
            appConfig: {
                type: Object,
                value: function () {
                    return window.APP_CONFIG
                }
            },
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

    getAPIUrl() {
        var args = Array.prototype.slice.call(arguments);
        if (args.indexOf(undefined) !== -1) {
            return undefined
        }
        return this.appConfig.apiUrl + args.slice(1).join('');
    }

    getCSRFToken() {
        return Cookies.get('XSRF-TOKEN');
    }

    dispatchOverlayStarted() {
        this.dispatchEvent(new CustomEvent('overlay-ajax-started', {bubbles: true, composed: true}));
    }

    dispatchOverlayStopped() {
        this.dispatchEvent(new CustomEvent('overlay-ajax-stopped', {bubbles: true, composed: true}));
    }
}

window.ZigguratAdminBasicMixin = ZigguratAdminBasicMixin;
