import yaml
import json
from pathlib import Path

def yaml_to_notebook(yaml_file, output_dir="outputs/jupyterlite"):
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load_all(f)
        front, *body = data  # Hugo-style front matter split not needed, safe_load_all still works

    title = front.get("title", "Untitled Challenge")
    instructions = body[0] if body else ""

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n\n", instructions]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [front["stage1_code"]]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [front["tests"]]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 🔍 Extension ideas\n",
                    *[f"- {ext}\n" for ext in front.get("extensions", [])]
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    output_path = Path(output_dir) / f"{front['slug']}.ipynb"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)

    print(f"✅ Wrote {output_path}")

if __name__ == "__main__":
    # Example: build one exercise
    yaml_to_notebook("exercises/calculations/pizza-party.yaml")
