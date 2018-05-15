require('style-loader');
require('css-loader');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
var path = require('path');

const projectName = 'ziggurat_cms_template_podswierkiem';
let destinationDirectory = path.join(process.cwd(), '..', '..','..' ,'static');
let rootDir =  process.cwd(path.join('src', projectName));

// static sources destination
if (process.env.ZIGGURAT_CMS_STATIC_DIR) {
    destinationDirectory = process.env.ZIGGURAT_CMS_STATIC_DIR
}

if (process.env.ZIGGURAT_CMS_ROOT_DIR) {
    rootDir = process.env.ZIGGURAT_CMS_ROOT_DIR
}

if (process.env.ZIGGURAT_CMS_BUILD_ROOT_DIR) {
    rootDirectory = process.env.ZIGGURAT_CMS_BUILD_ROOT_DIR
}

module.exports = {
    // Tell Webpack which file kicks off our app.
    entry: path.resolve(__dirname, 'src/index.js'),
    // Tell Weback to output our bundle to ./dist/bundle.js
    output: {
        filename: 'bundle.js',
        path: path.resolve(destinationDirectory, projectName)
    },
    // Tell Webpack which directories to look in to resolve import statements.
    // Normally Webpack will look in node_modules by default but since we’re overriding
    // the property we’ll need to tell it to look there in addition to the
    // bower_components folder.
    resolve: {
        modules: [
            path.resolve(__dirname, 'node_modules')
        ]
    },
    // These rules tell Webpack how to process different module types.
    // Remember, *everything* is a module in Webpack. That includes
    // CSS, and (thanks to our loader) HTML.
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    { loader: 'css-loader', options: { url: false } }, // translates CSS into CommonJS
                    "sass-loader" // compiles Sass to CSS
                ]
            }
    ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: "css/[name].css"
        }),
        // This plugin will copy files over to ‘./dist’ without transforming them.
        // That's important because the custom-elements-es5-adapter.js MUST
        // remain in ES2015. We’ll talk about this a bit later :)
        new CopyWebpackPlugin([{
            from: path.resolve(rootDir, 'src', 'images'),
            to: 'images'
        }])
    ]
};
