# 简介
微信公众号头像合成回复demo

# 注意点
- 由于依赖包超过250MB限制，不能部署到deta.sh, 故只能本地调试
- ngrok内网穿透的话，`ngrok.io`域名貌似已被微信屏蔽，需要自建ngrok服务器启用未被屏蔽域名或其它穿透工具
- `wechatpy`中的WeChatClient需要一个存储服务，项目里使用的是dict简单服务，有条件的同学可以换redis。
