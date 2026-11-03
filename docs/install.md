# 安装与开始使用

[English](install.en.md) · [返回首页](../README.zh-CN.md)

Lynette Thinking 是一组交给 AI 助手使用的指令和参考资料。你需要自己的 Codex 或支持 Skill 的助手；它没有独立模型或项目账户，也不要求项目专属 API key。以下步骤面向 Codex。

## 一步安装

下载并解压仓库，在包含 `README.md` 的仓库根目录执行（Python 3.9+）：

```sh
python3 scripts/install.py
```

脚本仅复制本地文件到 `~/.agents/skills/lynette-thinking`，不联网，不覆盖已有目录。

如果已经装过同名 Skill，先审阅并备份旧版本，再决定替换哪一份；不要在多个自动发现目录保留同名副本。

## 指定项目或手动安装

需要装到一个项目时，从该项目指定目标位置：

```sh
python3 /path/to/extracted-repository/scripts/install.py --target .agents/skills/lynette-thinking
```

把 `/path/to/extracted-repository` 换成实际解压目录。

不使用 Python 时，将仓库里的 `skills/lynette-thinking/` 整个文件夹手动复制到目标位置。个人安装的最终路径应为 `~/.agents/skills/lynette-thinking/SKILL.md`；项目安装则为 `.agents/skills/lynette-thinking/SKILL.md`。

## 第一次对话

安装后，第一次就可以在 Codex 中直接描述具体困境：

> 朋友借场地帮我办读书会，现在开始要求决定主题。我们还没谈过分工，我想保留自己的方向，也不想当场翻脸。

这类需要决定怎么做、怎么开口的职场、家庭或朋友困境属于自动匹配范围，无需点名 Lynette。自动选择取决于宿主与模型；需要明确指定或没有选中时，可以写：

> 请用 $lynette-thinking 帮我想下一步：……

同一问题的后续补充无需重复点名。新安装未显示时，重启 Codex 再检查目录是否放对。

[更多提问与补充方式](../skills/lynette-thinking/README.md) · [使用示例](../skills/lynette-thinking/examples/guided-resolution.zh-CN.md)

安装位置与发现机制依据 [OpenAI 官方说明](https://learn.chatgpt.com/docs/build-skills)。本包提供直接 Skill 安装；其他助手应使用其自身的安装方式，本项目尚未验证所有宿主的兼容性。

## 你的信息与移除方式

Skill 自身没有遥测、后台进程或数据上传代码。对话由所用 AI 产品处理，其数据规则仍适用。描述现实问题时，可以用角色称呼代替姓名，去掉公司、联系方式和无关聊天记录。

需要移除时，只删除你安装的 `lynette-thinking` 文件夹，不删除整个 skills 目录。
