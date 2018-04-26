// import Quill from '../../node_modules/quill/core';
//
// import { AlignClass, AlignStyle } from '../../node_modules/quill/formats/align';
// import { DirectionAttribute, DirectionClass, DirectionStyle } from '../../node_modules/quill/formats/direction';
// import { IndentClass as Indent } from '../../node_modules/quill/formats/indent';
//
// import Blockquote from '../../node_modules/quill/formats/blockquote';
// import Header from '../../node_modules/quill/formats/header';
// import List, { ListItem } from '../../node_modules/quill/formats/list';
//
// import { BackgroundClass, BackgroundStyle } from '../../node_modules/quill/formats/background';
// import { ColorClass, ColorStyle } from '../../node_modules/quill/formats/color';
// import { FontClass, FontStyle } from '../../node_modules/quill/formats/font';
// import { SizeClass, SizeStyle } from '../../node_modules/quill/formats/size';
//
// import Bold from '../../node_modules/quill/formats/bold';
// import Italic from '../../node_modules/quill/formats/italic';
// import Link from '../../node_modules/quill/formats/link';
// import Script from '../../node_modules/quill/formats/script';
// import Strike from '../../node_modules/quill/formats/strike';
// import Underline from '../../node_modules/quill/formats/underline';
//
// import Image from '../../node_modules/quill/formats/image';
// import Video from '../../node_modules/quill/formats/video';
//
// import CodeBlock, { Code as InlineCode } from '../../node_modules/quill/formats/code';
//
// import Formula from '../../node_modules/quill/modules/formula';
// import Syntax from '../../node_modules/quill/modules/syntax';
// import Toolbar from '../../node_modules/quill/modules/toolbar';
//
// import Icons from '../../node_modules/quill/ui/icons';
// import Picker from '../../node_modules/quill/ui/picker';
// import ColorPicker from '../../node_modules/quill/ui/color-picker';
// import IconPicker from '../../node_modules/quill/ui/icon-picker';
// import Tooltip from '../../node_modules/quill/ui/tooltip';
//
// import BubbleTheme from '../../node_modules/quill/themes/bubble';
// import SnowTheme from '../../node_modules/quill/themes/snow';
//
//
// Quill.register({
//     'attributors/attribute/direction': DirectionAttribute,
//
//     'attributors/class/align': AlignClass,
//     'attributors/class/background': BackgroundClass,
//     'attributors/class/color': ColorClass,
//     'attributors/class/direction': DirectionClass,
//     'attributors/class/font': FontClass,
//     'attributors/class/size': SizeClass,
//
//     'attributors/style/align': AlignStyle,
//     'attributors/style/background': BackgroundStyle,
//     'attributors/style/color': ColorStyle,
//     'attributors/style/direction': DirectionStyle,
//     'attributors/style/font': FontStyle,
//     'attributors/style/size': SizeStyle
// }, true);
//
// Quill.register({
//     'formats/align': AlignClass,
//     'formats/direction': DirectionClass,
//     'formats/indent': Indent,
//
//     'formats/background': BackgroundStyle,
//     'formats/color': ColorStyle,
//     'formats/font': FontClass,
//     'formats/size': SizeClass,
//
//     'formats/blockquote': Blockquote,
//     'formats/code-block': CodeBlock,
//     'formats/header': Header,
//     'formats/list': List,
//
//     'formats/bold': Bold,
//     'formats/code': InlineCode,
//     'formats/italic': Italic,
//     'formats/link': Link,
//     'formats/script': Script,
//     'formats/strike': Strike,
//     'formats/underline': Underline,
//
//     'formats/image': Image,
//     'formats/video': Video,
//
//     'formats/list/item': ListItem,
//
//     'modules/formula': Formula,
//     'modules/syntax': Syntax,
//     'modules/toolbar': Toolbar,
//
//     'themes/bubble': BubbleTheme,
//     'themes/snow': SnowTheme,
//
//     'ui/icons': Icons,
//     'ui/picker': Picker,
//     'ui/icon-picker': IconPicker,
//     'ui/color-picker': ColorPicker,
//     'ui/tooltip': Tooltip
// }, true);
//
// let BlockEmbed = Quill.import('blots/block/embed');
//
// class VideoBlot extends BlockEmbed {
//     static create(url) {
//         let node = super.create();
//
//         // Set non-format related attributes with static values
//         node.setAttribute('frameborder', '0');
//         node.setAttribute('allowfullscreen', true);
//         node.setAttribute('src', url);
//         return node;
//     }
//
//     static formats(node) {
//         // We still need to report unregistered embed formats
//         let format = {};
//         if (node.hasAttribute('height')) {
//             format.height = node.getAttribute('height');
//         }
//         if (node.hasAttribute('width')) {
//             format.width = node.getAttribute('width');
//         }
//         return format;
//     }
//
//     static value(node) {
//         return node.getAttribute('src');
//     }
//
//     format(name, value) {
//         // Handle unregistered embed formats
//         if (name === 'height' || name === 'width') {
//             if (value) {
//                 this.domNode.setAttribute(name, value);
//             } else {
//                 this.domNode.removeAttribute(name, value);
//             }
//         } else {
//             super.format(name, value);
//         }
//     }
// }
// VideoBlot.blotName = 'video';
// VideoBlot.tagName = 'iframe';
//
// Quill.register(VideoBlot);
//
//
// module.exports = Quill;
//
