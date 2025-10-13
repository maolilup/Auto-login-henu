###
基于python开发的自动校园网登录脚本
模拟网页 JavaScript 中的 auth() 和 check() 函数，进行初步的身份验证。
通过 requests 库直接模拟了 JS 发起的关键网络请求（API 认证和最终的 quickauth GET 请求），并正确构造了请求所需的参数，直接与后端认证服务进行交互，完成了自动登录。
