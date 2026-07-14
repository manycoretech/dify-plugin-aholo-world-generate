# Aholo World Generate Dify 插件

在 Dify Workflow、Chatflow 或 Agent 中调用 Aholo World Generate，生成3DGS世界。

## 工具

- `create_world_generation`：通过提示词和可选参考图提交生成任务。
- `get_world_generation`：查询生成任务状态并返回标准化资产 URL。

## 输入

`create_world_generation` 支持：

- `prompt`：可选文本提示词。
- `image_file`：可选本地图片文件，支持 `jpg`、`jpeg`、`png`、`webp`。
- `name`：可选世界名称。
- `region`：`cn` 或 `com`。

`prompt` 与 `image_file` 至少需要提供一个。

## 输出

`create_world_generation` 返回：

- `world_id`
- `status`
- `reference_image_url`

`get_world_generation` 返回：

- `world_id`
- `status`
- `progress`
- `pano_url`
- `spz_url`
- `ply_url`
- `lod_meta_url`
- `up_axis`
- `name`
- `cover`
- `scene`
- `create_time`
- `update_time`

## 凭据

在 provider 凭据中配置 `api_key`。插件只在服务端请求 Aholo API 时使用该密钥，不会在工具输出中返回。

申请 API Key：

- 国内（`cn`）：https://labs.aholo3d.cn/api-keys
- 海外（`com`）：https://labs.aholo3d.com/api-keys

请使用与工具中 `region` 参数一致的区域所申请的 API Key。

## 区域

- `cn`：`https://api.aholo3d.cn`
- `com`：`https://api.aholo3d.com`

## 本地开发

安装依赖：

```bash
pip install -r requirements.txt
```

配置好 `.env` 后，在 Dify 插件 debug 模式中运行：

```bash
python -m main
```

运行单元测试（无需把测试依赖写入运行时 requirements）：

```bash
PYTHONPATH="$PWD" uv run --with-requirements requirements.txt --with pytest python -m pytest tests
```

## 源码仓库

https://github.com/manycoretech/dify-plugin-aholo-world-generate

## 联系方式

请在上述源码仓库提交 GitHub Issue。安全漏洞请查看 [SECURITY.md](../SECURITY.md)。与 Marketplace 发布渠道相关的问题，请遵循 Dify 的[安全披露流程](https://github.com/langgenius/dify-plugins#security-disclosure)。
