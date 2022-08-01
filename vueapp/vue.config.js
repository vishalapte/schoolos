const path = require('path');
module.exports = {
    transpileDependencies: true,

    // Should be STATIC_URL + path/to/build
    publicPath: '/static/vue/',

    // Output to a directory in STATICFILES_DIRS
    outputDir: path.resolve(__dirname, '../common/vue/dist/'),

    // Django will hash file names, not webpack
    filenameHashing: false,

    // See: https://vuejs.org/v2/guide/installation.html#Runtime-Compiler-vs-Runtime-only
    runtimeCompiler: true,
    devServer: {
        devMiddleware: {
            // Write files to disk in dev mode, so Django can serve the assets
            writeToDisk: true,
        }
    },
    // configure webpack to look at app directory instead of src as src is gitignored
    // in django for us
    chainWebpack: config => {
        config.entry('app').clear().add("./vuesrc/main.js");
        config.resolve.alias.set('@', path.join(__dirname, "./vuesrc"));
    }
};
