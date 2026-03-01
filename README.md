# plugin-elevenlabs

A Stavrobot plugin that converts text to speech using [ElevenLabs](https://elevenlabs.io/) voices. It produces an MP3 audio file that Stavrobot delivers back to you.

## Installation

Tell Stavrobot:

> Install the plugin at `https://github.com/stavrobot/plugin-elevenlabs`

After installation, configure your ElevenLabs API key:

> Configure the elevenlabs plugin with my API key: `<your-api-key>`

## Configuration

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `api_key` | Yes | — | Your ElevenLabs API key. Obtain one at [elevenlabs.io](https://elevenlabs.io/). |
| `default_voice_id` | No | `JBFqnCBsd6RMkjVDRZzb` | ElevenLabs voice ID to use when none is specified in the request. |
| `model_id` | No | `eleven_v3` | ElevenLabs model ID. |
| `stability` | No | `0.9` | Voice stability from 0.0 to 1.0. Higher values produce more consistent speech. |

## Usage

Ask Stavrobot to convert text to speech:

> Read this aloud: "Hello, world!"

You can also specify a voice:

> Read this in voice `21m00Tcm4TlvDq8ikWAM`: "Hello, world!"
