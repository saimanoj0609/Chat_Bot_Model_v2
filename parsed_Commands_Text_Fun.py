import json


def process_command_text(text):
    """
    Converts a command block into structured fields.
    """
    field_map = {
        "description": "description",
        "synopsis": "syntax",
        "input": "input",
        "output": "output",
        "example": "example"
    }

    result = {}
    current_field = None
    buffer = []

    lines = text.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        matched = False
        for key in field_map:
            if line.lower().startswith(key):
                if current_field and buffer:
                    result[field_map[current_field]] = '\n'.join(buffer).strip("● ").strip()
                current_field = key
                content = line[len(key):].strip(":\t ")
                buffer = [content] if content else []
                matched = True
                break
        if not matched:
            buffer.append(line)

    if current_field and buffer:
        result[field_map[current_field]] = '\n'.join(buffer).strip("● ").strip()
    return result

def parsing_commands(commands_dict):
    structured_commands = {}
    for command_name, text_block in commands_dict.items():
        structured_commands[command_name] = process_command_text(text_block)

    with open("racadm_structured_commands.json", "w", encoding="utf-8") as f:
        json.dump(structured_commands, f, indent=2)

    print("Structured JSON saved to racadm_structured_commands.json")
