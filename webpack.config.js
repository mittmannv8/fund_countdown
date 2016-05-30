var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: {
    app: './fundcountdown/scripts/src/main.js',
  },
  output: {
    path: path.join(__dirname, './fundcountdown/scripts/dist/'),
    filename: '[name].js',
  },
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin()
  ],
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loaders: [ 'babel' ],
        exclude: /node_modules/,
        include: __dirname
      }
    ]
  }
}
