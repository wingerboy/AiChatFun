// vue.config.js 配置说明
// 这里只列一部分，具体配置惨考文档啊

const proxy = require('http-proxy-middleware');

module.exports = {
  lintOnSave: true,
  runtimeCompiler: true,
  devServer: {
    port: 7000, // 端口号
    host: "localhost",
    https: false, // https:{type:Boolean}
    open: true, //配置自动启动浏览器
    // proxy: 'http://43.153.81.198:8000', // 配置跨域处理,只有一个代理
    proxy:{
      '/api':{
          target: 'http://43.153.81.198:8000',//代理地址，这里设置的地址会代替axios中设置的baseURL
          changeOrigin: true,// 如果接口跨域，需要进行这个参数配置
          secure: false,
          //ws: true, // proxy websockets
          //pathRewrite方法重写url
          pathRewrite: {
              '^/api': '/' 
              //pathRewrite: {'^/api': '/'} 重写之后url为 http://192.168.1.16:8085/xxxx
              //pathRewrite: {'^/api': '/api'} 重写之后url为 http://192.168.1.16:8085/api/xxxx
         }
    }},
    // proxy: {}, // 配置多个代理
    overlay: {
      warnings: false,
      errors: true,
    },
  },
};
