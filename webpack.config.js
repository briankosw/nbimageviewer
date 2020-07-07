const path = require("path");
const components_path = "./nbimageviewer/assets/src/components/";

module.exports = {
    mode: "development",
    entry: {
        carousel: components_path + "Carousel/Carousel.jsx",
        gallery: components_path + "Gallery/Gallery.jsx",
    },
    output: {
        filename: "[name].js",
        path: path.join(__dirname, "nbimageviewer/assets/dist")
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader",
                ]
            }
        ]
    }
}
