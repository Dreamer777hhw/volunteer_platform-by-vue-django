const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
const path = require('path');

module.exports = {
  // 其他配置项
  publicPath: process.env.NODE_ENV === 'production' ? '/media/' : '/',
  outputDir: path.resolve(__dirname, 'dist'), // 打包输出目录
  // devServer: {
  //   contentBase: path.resolve(__dirname, '../volunteer_management'), // 设置开发服务器的根目录
  // },
};