import '@polymer/polymer/polymer-legacy.js';
import { IronValidatorBehavior } from '@polymer/iron-validator-behavior/iron-validator-behavior.js';
import { Polymer } from '@polymer/polymer/lib/legacy/polymer-fn.js';

Polymer({

    is: 'custom-validator',

    behaviors: [
        IronValidatorBehavior
    ],

    validate: function(values) {
        console.log('test validate',values);
        return false;
    }

});
