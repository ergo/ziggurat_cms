/* webpack.config.js */
require('style-loader');
require('css-loader');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
var path = require('path');

const projectName = 'ziggurat_cms_front_front';
let destinationDirectory = path.join(process.cwd(), '..', '..','..' ,'static')

if (process.env.FRONTEND_ASSSET_ROOT_DIR) {
    destinationDirectory = process.env.FRONTEND_ASSSET_ROOT_DIR
}

module.exports = {
    // Tell Webpack which file kicks off our app.
    entry: {
        main: path.resolve(__dirname, 'src/index.js'),
        sass: path.resolve(__dirname, 'src/sass.js')
    },
    output: {
        filename: 'bundle-[name].js',
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
                // If you see a file that ends in .html, send it to these loaders.
                test: /\.html$/,
                // This is an example of chained loaders in Webpack.
                // Chained loaders run last to first. So it will run
                // polymer-webpack-loader, and hand the output to
                // babel-loader. This let's us transpile JS in our `<script>` elements.
                use: [
                    { loader: 'babel-loader' },
                    { loader: 'polymer-webpack-loader' }
                ]
            },
            {
                // If you see a file that ends in .js, just send it to the babel-loader.
                test: /\.js$/,
                use: 'babel-loader'
                // Optionally exclude node_modules from transpilation except for polymer-webpack-loader:
                // exclude: /node_modules\/(?!polymer-webpack-loader\/).*/
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader", // translates CSS into CommonJS
                    "sass-loader" // compiles Sass to CSS
                ]
            },
            // this is required because of bug:
            // https://github.com/webpack-contrib/polymer-webpack-loader/issues/49
            {
                test: /intl-messageformat.min.js/,
                use: 'imports-loader?this=>window'
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: "css/[name].css"
        }),
        // This plugin will generate an index.html file for us that can be used
        // by the Webpack dev server. We can give it a template file (written in EJS)
        // and it will handle injecting our bundle for us.
        // new HtmlWebpackPlugin({
        //     template: path.resolve(__dirname, 'src/index.ejs')
        // }),
        // This plugin will copy files over to ‘./dist’ without transforming them.
        // That's important because the custom-elements-es5-adapter.js MUST
        // remain in ES2015. We’ll talk about this a bit later :)
        new CopyWebpackPlugin([])
    ]
};
