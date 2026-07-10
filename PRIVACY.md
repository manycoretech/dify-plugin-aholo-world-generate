# Privacy Policy

This plugin sends user-provided inputs to Aholo API services in order to create and query world generation tasks.

## Data Sent to Aholo

- Aholo API key, sent as a provider credential for authentication.
- Text prompts submitted to `create_world_generation`.
- Optional uploaded image files, uploaded to Aholo asset services before generation.
- Optional cover URLs and world names.
- World IDs submitted to `get_world_generation`.

## Data Returned

The plugin returns task status, progress, metadata, and asset URLs from Aholo API responses.

## Storage

This plugin does not store prompts, uploaded files, API keys, or Aholo API responses in plugin storage.

Aholo API services may process and retain submitted data according to Aholo's own terms and privacy policy.

## Secrets

The Aholo API key is used only for server-side API calls. It is not included in text, JSON, or workflow variable outputs.
