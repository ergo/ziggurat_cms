import '@polymer/polymer/polymer-legacy.js';
const $_documentContainer = document.createElement('template');

$_documentContainer.innerHTML = `<dom-module id="shared-styles">
    <template>
        <style type="text/css">

            :host {
                box-sizing: border-box;
            }

            a, a:link, a:visited {
                text-decoration: none;
                color: #1976d2;
            }

            a:hover {
                text-decoration: none;
                color: #0d47a1;
            }

            uirouter-sref ::slotted(a), uirouter-sref a {
                text-decoration: none;
                color: #1976d2;
            }

            uirouter-sref ::slotted(a):hover, uirouter-sref a:hover {
                text-decoration: none;
                color: #0d47a1;
            }

            .table {
                display: table;
            }

            .table .row {
                display: table-row;
            }

            .table .cell {
                display: table-cell;
            }

            @media screen and (max-width: 768px) {
                .table.responsive {
                    display: block;
                }

                .row.responsive {
                    display: block;
                    border-bottom: 1px solid #cccccc;
                    margin-bottom: 20px;
                }

                .cell.responsive {
                    display: block;
                }
            }

            .table.default .header .cell {
                border-bottom: 2px solid #2e6da4;
            }

            .table.default .header .cell {
                padding: 10px;
            }

            .table.default .cell {
                padding: 10px;
                vertical-align: top;
            }

        </style>
    </template>
</dom-module>`;

document.head.appendChild($_documentContainer.content);

/**
@license
Copyright (c) 2016 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
Code distributed by Google as part of the polymer project is also
subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
*/
/* shared styles for all views */
/*
  FIXME(polymer-modulizer): the above comments were extracted
  from HTML and may be out of place here. Review them and
  then delete this comment!
*/
;
