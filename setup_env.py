#!/usr/bin/env python3
"""
Setup script to create .env file from example
"""
import os
import shutil


def setup_env():
    # The .env file should be in the root directory (one level above backend)
    env_example = "env.example"
    env_file = ".env"

    if os.path.exists(env_file):
        print(f".env file already exists at {env_file}")
        return

    if not os.path.exists(env_example):
        print(f"env.example not found at {env_example}")
        return

    try:
        shutil.copy2(env_example, env_file)
        print(f"Created .env file from {env_example}")
        print("Please edit .env with your actual database credentials")
    except Exception as e:
        print(f"Error creating .env file: {e}")


if __name__ == "__main__":
    setup_env()
