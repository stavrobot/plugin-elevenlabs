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


KNOWN_PARAMETERS: set[str] = {"audio"}
# The tool runs inside a Docker container where the working directory is speech_to_text/,
# so the plugin config lives one level up.
CONFIG_PATH = pathlib.Path("../config.json")


class Config(TypedDict):
    api_key: str
    stt_model_id: str


def read_params() -> dict[str, str]:
    raw = json.load(sys.stdin)
    unknown = set(raw.keys()) - KNOWN_PARAMETERS
    if unknown:
        print(f"Unknown parameters: {sorted(unknown)}", file=sys.stderr)
        sys.exit(1)
    if "audio" not in raw:
        print("Missing required parameter: audio", file=sys.stderr)
        sys.exit(1)
    return raw


def read_config() -> Config:
    return json.loads(CONFIG_PATH.read_text())


def call_elevenlabs_api(audio_path: str, api_key: str, model_id: str) -> str:
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    with open(audio_path, "rb") as audio_file:
        response = requests.post(
            url,
            headers={"xi-api-key": api_key},
            files={"file": audio_file},
            data={"model_id": model_id},
        )
    if not response.ok:
        print(response.text, file=sys.stderr)
        sys.exit(1)
    return response.json()["text"]


def main() -> None:
    params = read_params()
    config = read_config()

    transcription = call_elevenlabs_api(
        audio_path=params["audio"],
        api_key=config["api_key"],
        model_id=config["stt_model_id"],
    )
    print(json.dumps({"text": transcription}))


if __name__ == "__main__":
    main()
