const path = require("path");

module.exports = {
    devtool: "source-map",
    entry: "./frontend/index.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "src", "porfavor", "static")
    },
    module: {
        rules: [
            {
                test: /\.js?/,
                include: path.resolve(__dirname, "frontend"),
                loader: "babel-loader"
            },
            {
                test: /\.(jpe?g|png|gif)$/i, // to support eg. background-image property
                loader: "file-loader",
                options: {
                    name: "[name].[ext]",
                    outputPath: "img/",
                    publicPath: "static/img/"
                    // the images will be emmited to public/assets/images/ folder
                    // the images will be put in the DOM <style> tag as eg. background: url(assets/images/image.png);
                }
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, // to support @font-face rule
                loader: "url-loader",
                options: {
                    limit: "10000",
                    name: "[name].[ext]",
                    outputPath: "fonts/",
                    publicPath: "static/fonts/"
                    // the fonts will be emmited to public/assets/fonts/ folder
                    // the fonts will be put in the DOM <style> tag as eg. @font-face{ src:url(assets/fonts/font.ttf); }
                }
            },
            {
                test: /\.css$/,
                loaders: ["style-loader", "css-loader"]
            }
        ]
    }
};
