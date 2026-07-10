# Aholo World Generate Dify Plugin

Generate Aholo 3DGS indoor worlds from Dify workflows, chatflows, or agents.

## Tools

- `create_world_generation`: submits a world generation task from a prompt and optionally one reference image.
- `get_world_generation`: queries a generation task and returns normalized asset URLs.

## Inputs

`create_world_generation` supports:

- `prompt`: optional text prompt.
- `image_file`: optional local image file (`jpg`, `jpeg`, `png`, `webp`).
- `name`: optional world name.
- `cover`: optional HTTPS cover URL.
- `region`: `cn` or `com`.

At least one of `prompt` or `image_file` is required.

## Outputs

`create_world_generation` returns:

- `world_id`
- `status`
- `reference_image_url`

`get_world_generation` returns:

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

## Credentials

Configure the provider credential `api_key` with your Aholo API key. The key is sent only to Aholo API services and is never returned in tool outputs.

Get an API key:

- China (`cn`): https://labs.aholo3d.cn/api-keys
- Global (`com`): https://labs.aholo3d.com/api-keys

Use an API key from the same region you select in the tool (`cn` or `com`).

## Region

- `cn`: `https://api.aholo3d.cn`
- `com`: `https://api.aholo3d.com`

## Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run in Dify plugin debug mode after configuring your `.env`:

```bash
python -m main
```

Run unit tests without adding test dependencies to the runtime requirements:

```bash
PYTHONPATH="$PWD" uv run --with-requirements requirements.txt --with pytest python -m pytest tests
```

## Source repository

https://github.com/manycoretech/dify-plugin-aholo-world-generate

## Contact

Open GitHub issues on the source repository above. For security vulnerabilities, see [SECURITY.md](./SECURITY.md). For Marketplace-related disclosure, follow Dify's [security disclosure process](https://github.com/langgenius/dify-plugins#security-disclosure).
