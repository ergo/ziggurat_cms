import { PolymerElement } from '@polymer/polymer/polymer-element.js';
import '../../shared-styles.js';
import { html } from '@polymer/polymer/lib/utils/html-tag.js';
import { GestureEventListeners } from '@polymer/polymer/lib/mixins/gesture-event-listeners.js';
import { mixinBehaviors } from '@polymer/polymer/lib/legacy/class.js';
import { AppLocalizeBehavior } from '@polymer/app-localize-behavior/app-localize-behavior.js';
window.Quill = require('../../../node_modules/quill/dist/quill.js');

class ZigguratCMSQuillEditorBase extends ZigguratAdminBasicMixin(GestureEventListeners(
    mixinBehaviors([AppLocalizeBehavior],PolymerElement))) {
  static get template() {
    return html`
        <style include="shared-styles">
            :host {
                display: block;
                position: relative;
            }

        </style>

        <div class="toolbar">
            <span class="ql-formats">
            <select class="ql-header">
              <option value="1">Header 1</option>
              <option value="2">Header 2</option>
              <option value="3">Header 3</option>
              <option value="7">Normal</option>
            </select>
          </span>
            <span class="ql-formats">
            <button class="ql-bold" title="Bold"></button>
            <button class="ql-italic" title="Italic"></button>
            <button class="ql-underline" title="Underline"></button>
            <button class="ql-strike" title="strike"></button>
          </span>
            <span class="ql-formats">
            <select class="ql-color" title="Text Color"></select>
            <select class="ql-background" title="Text Background Color"></select>
          </span>
            <span class="ql-formats">
                <button class="ql-script" value="sub"></button>
                <button class="ql-script" value="super"></button>
                </span>
            <span class="ql-formats">
            <button class="ql-blockquote" title="Blockquote"></button>
            <button class="ql-code-block" title="Code Clock"></button>
          </span>
            <span class="ql-formats">
            <button class="ql-list" value="ordered" title="Numbered List"></button>
            <button class="ql-list" value="bullet" title="Bullet List"></button>
            <button class="ql-indent" value="-1" title="Decrease Indent"></button>
            <button class="ql-indent" value="+1" title="Indent"></button>
          </span>
            <span class="ql-formats">
            <select class="ql-align" title="Align">&gt;</select>
          </span>
            <span class="ql-formats">
            <button class="ql-link" title="Link"></button>
            <button class="ql-image" title="Image"></button>
            <button class="ql-video" title="Video"></button>
          </span>
            <span class="ql-formats">
            <button class="ql-clean" title="Clear Formating"></button>
          </span>
        </div>
        <div class="editor"></div>
`;
  }

  static get is() {
      return "zigguratcms-quill-editor-base";
  }
  static get properties() {
      return {
          config: {
              type: Object,
              notify: true
          },
          delta: {
              type: Object,
              notify: true
          },
          compiledHtml: {
              type: Object,
              notify: true
          },
          dirty: {
              type: Boolean,
              value: false,
              notify: true
          }
      }
  }
  static get observers() {
      return [
          'emitChange(config.*)'
      ]
  }

  attached() {
      console.log('ATTACHED QUILL', this.querySelector('.editor'));
      var options = {
          bounds: this,
          modules: {
              toolbar: {
                  container: this.querySelector('.toolbar')
              }
          },
          placeholder: 'Compose an epic...',
          theme: 'snow'
      };
      var quill = new Quill(this.querySelector('.editor'), options);
      this.quill = quill;
      quill.setContents(this.delta);
      quill.on('text-change', function (delta, oldDelta, source) {
          this.dirty = true;
          this.delta = quill.getContents();
          this.compiledHtml = this.quill.root.innerHTML;
      }.bind(this));
      var toolbar = quill.getModule('toolbar');
      toolbar.addHandler('image', function (value) {
          this.openImageDialog();
      }.bind(this));
      this.scopeSubtree(this.querySelector('.editor'), true);
      this.scopeSubtree(this.querySelector('.toolbar'), true);
      this.listen(window, 'tap', 'clickHandler');
  }
  detached() {
      this.unlisten(window, 'tap', 'clickHandler');
  }

  clickHandler(event) {
      var path = event.composedPath();
      for (var i=0; i < path.length; i++ ){
          var target = path[i];
          if (!target.tagName){
              continue
          }
          if (this.contains(target)) {
              this.toggleClass('active', true, this.querySelector('.toolbar'));
              break;
          } else {
              this.toggleClass('active', false, this.querySelector('.toolbar'));
          }
      };
  }
  openImageDialog() {
      this.fire('zigguratcms-quill-editor-select-image');
  }

  _attachDom(dom) {
      this.appendChild(dom);
  }
}

customElements.define(ZigguratCMSQuillEditorBase.is, ZigguratCMSQuillEditorBase);
