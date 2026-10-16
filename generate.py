#!/usr/bin/env python3

import os
import subprocess
import shutil


def generate_stubs():
    packages = [
        "pulumi-aws",
        "pulumi-gcp",
        "pulumi-azure-native",
    ]
    for package in packages:
        package_name = package.replace("-", "_")
        # PEP 561 stub-only package: `<module>-stubs/` holding only `.pyi`
        # files, so it never shares a directory with the runtime package.
        stubs_dir = f"packages/{package}-stubs/src/{package_name}-stubs"
        shutil.rmtree(stubs_dir, ignore_errors=True)
        os.makedirs(os.path.dirname(stubs_dir), exist_ok=True)
        _ = subprocess.run(
            [
                "pyright",
                "--createstub",
                f"{package_name}",
            ],
            check=True,
        )
        _ = subprocess.run(
            [
                "mv",
                f"typings/{package_name}",
                stubs_dir,
            ],
            check=True,
        )
    _ = subprocess.run(
        [
            "ruff",
            "check",
            "packages",
            "--fix",
            "--unsafe-fixes",
        ],
        check=False,
    )
    _ = subprocess.run(
        [
            "ruff",
            "format",
            f"packages",
        ],
        check=False,
    )
    os.rmdir("typings")


if __name__ == "__main__":
    generate_stubs()
