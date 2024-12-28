# TTS for Home Assistant

这是一个 Home Assistant 的文字转语音(TTS)自定义组件，提供高质量的语音合成服务，让您的智能家居系统能够说话。

## ✨ 功能特点

- 🎯 高质量语音：采用先进的语音合成技术，声音自然流畅
- 🌍 多语言支持：支持中文、英文等多种语言
- ⚡ 实时合成：低延迟的语音生成
- 📱 场景丰富：适配各类智能家居语音播报场景
- 🔒 安全可靠：数据传输加密，保护隐私

## 📦 安装方法

### HACS 安装（推荐）

1. 确保已经安装了 [HACS](https://hacs.xyz/)
2. HACS > 集成 > 右上角菜单 > Custom repositories
3. 添加仓库：`https://github.com/aiakit/tts`
4. 类别选择：Integration
5. 在 HACS 集成页面搜索 "HomingAI TTS"
6. 点击下载
7. 重启 Home Assistant

### 手动安装

1. 下载此仓库的最新版本
2. 将 `custom_components/homingai_tts` 文件夹复制到您的 `custom_components` 目录
3. 重启 Home Assistant

## ⚙️ 配置说明

[![Open your Home Assistant instance and show an integration.](https://my.home-assistant.io/badges/integration.svg)](https://my.home-assistant.io/redirect/integration/?domain=homingai_tts)

1. 在 Home Assistant 的配置页面中添加集成
2. 搜索 "HomingAI TTS"
3. 完成HomingAI的授权
4. 点击"提交"完成配置


# 🎯 支持格式

- 输出格式：MP3, WAV
- 采样率：16kHz, 24kHz
- 声音类型：多种男声女声可选
- 语言支持：中文(zh-CN)、英文(en-US)等

## ⚠️ 注意事项

- 确保网络连接稳定
- 检查音频设备是否正常工作
- 正确配置授权信息
- 注意API调用限制

## 🔧 故障排除

如果遇到问题，请检查：

1. 授权信息是否正确
2. 网络连接是否正常
3. 音频设备是否正常工作
4. Home Assistant 日志中的错误信息
5. 查看[技术文档](https://homingai.com)获取更多帮助

## 📝 问题反馈

如果您遇到任何问题或有改进建议，欢迎通过以下方式反馈：

- [提交 Issue](https://github.com/aiakit/tts/issues)
- [技术支持](https://homingai.com)

## 📄 许可证

本项目采用 Apache License 2.0 许可证，详见 [LICENSE](LICENSE) 文件。

## 🔄 更新日志

### v1.0.0 (2024-03-19)
- ✨ 初始版本发布
- 🎯 支持多种语音合成选项
- 🌍 支持多语言
- ⚡ 优化合成性能
- 📱 完善配置界面

## 🤝 贡献指南

欢迎提交 Pull Request 或者建立 Issue。

---

Made with ❤️ by HomingAI Team