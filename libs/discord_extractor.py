import json
import logging
import subprocess
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Union

from libs import config


def extract_messages(date_start: date) -> Union[Dict[str, List[Dict[str, Any]]], bool]:
    def check_errors(log_line: str) -> str:
        error_type = None
        if "ERROR" in log_line:
            logging.error("Error in Discord chat exporter")
            error_type = "error"
        if "Authentication token is invalid" in line:
            logging.error("Invalid Discord token")
            error_type = "invalid_token"
        return error_type

    extracted_data = {}
    for newsletter in config.NEWSLETTERS_CONFIG:
        channels_params = []
        for channel in newsletter["channels"]:
            channels_params += ["-c", channel]

        command = [
            "docker",
            "run",
            "--rm",
            "-t",
            "-v",
            f"{config.OUTPUT_DIR}:/out",
            "tyrrrz/discordchatexporter:stable",
            "export",
            "--fuck-russia",
            "-t",
            config.DISCORD_TOKEN,
            "--after",
            date_start.strftime("%Y-%m-%d %H:%M"),
            "-f",
            "Json",
            "-o",
            f"%d/{newsletter['name']} - %G - %C.json",
        ] + channels_params

        logging.info(f"Get messages for newsletter \"{newsletter['name']}\"...")
        logging.info(
            f"Command: {' '.join(command).replace(config.DISCORD_TOKEN, '<discord_token>')}"
        )
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Stream stdout and stderr in files
        output_dir = Path(config.OUTPUT_DIR) / date.today().strftime("%Y-%m-%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        for line in process.stdout:
            if check_errors(line) == "invalid_token":
                return False
            with open(output_dir / "stdout.txt", "a") as f:
                f.write(line)
        for line in process.stderr:
            if check_errors(line) == "invalid_token":
                return False
            with open(output_dir / "stderr.txt", "a") as f:
                f.write(line)

        process.wait()  # Wait for the process to complete

        # Read json files
        files = output_dir.glob("*.json")
        extracted_data[newsletter["name"]] = []
        for file in files:
            extracted_data[newsletter["name"]].append(
                {"file": file.as_posix(), "data": json.loads(file.read_text())}
            )

    logging.info("Extract terminated")

    return extracted_data


if __name__ == "__main__":
    r = extract_messages(date.today() - timedelta(days=7))
    with open("/tmp/output.json", "w") as f:
        f.write(json.dumps(r, indent="\t", ensure_ascii=False))
