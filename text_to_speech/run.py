#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///

import json
import pathlib
import sys
from typing import TypedDict

import requests


KNOWN_PARAMETERS: set[str] = {"text", "voice_id"}
OUTPUT_DIR = pathlib.Path("/tmp/elevenlabs")
OUTPUT_FILE = OUTPUT_DIR / "output.mp3"
# The tool runs inside a Docker container where the working directory is text_to_speech/,
# so the plugin config lives one level up.
CONFIG_PATH = pathlib.Path("../config.json")


class Config(TypedDict):
    api_key: str
    default_voice_id: str
    model_id: str
    stability: float


def read_params() -> dict[str, str]:
    raw = json.load(sys.stdin)
    unknown = set(raw.keys()) - KNOWN_PARAMETERS
    if unknown:
        print(f"Unknown parameters: {sorted(unknown)}", file=sys.stderr)
        sys.exit(1)
    if "text" not in raw:
        print("Missing required parameter: text", file=sys.stderr)
        sys.exit(1)
    return raw


def read_config() -> Config:
    return json.loads(CONFIG_PATH.read_text())


def call_elevenlabs_api(
    text: str,
    voice_id: str,
    api_key: str,
    model_id: str,
    stability: float,
) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    response = requests.post(
        url,
        headers={"xi-api-key": api_key},
        json={
            "text": text,
            "model_id": model_id,
            "output_format": "mp3_44100_128",
            "voice_settings": {
                "stability": stability,
                # similarity_boost is required by the API alongside stability.
                "similarity_boost": 0.5,
            },
        },
    )
    if not response.ok:
        print(response.text, file=sys.stderr)
        sys.exit(1)
    return response.content


def write_output(audio_bytes: bytes) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_bytes(audio_bytes)


def main() -> None:
    params = read_params()
    config = read_config()

    text: str = params["text"]
    # Prefer an explicit voice_id from the caller; fall back to the configured default
    # so the plugin works out of the box without requiring callers to know voice IDs.
    voice_id: str = params.get("voice_id", config["default_voice_id"])

    audio_bytes = call_elevenlabs_api(
        text=text,
        voice_id=voice_id,
        api_key=config["api_key"],
        model_id=config["model_id"],
        stability=config["stability"],
    )
    write_output(audio_bytes)
    print(json.dumps({"file": "output.mp3"}))


if __name__ == "__main__":
    main()
