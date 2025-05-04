import json
import torch
from sentence_transformers import SentenceTransformer, util
def chatBot_reponse(user_input):
    # Load structured RACADM commands
    with open("racadm_structured_commands.json", "r", encoding="utf-8") as f:
        commands_dict = json.load(f)
   # Load pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Preprocess command names
    raw_command_names = list(commands_dict.keys())
    command_names = [cmd.strip() for cmd in raw_command_names]
    command_embeddings = model.encode(command_names, convert_to_tensor=True)

    field_keys = ["description", "syntax", "input", "output", "example"]
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    SIMILARITY_THRESHOLD = 0.5
    
    while user_input:
        out_response = ""

        user_input_clean = user_input.lower()
        if user_input == "exit":
            out_response = "Goodbye!"
            break
        # Check for greetings
        if any(greet in user_input_clean for greet in greetings):
            out_response =  "👋 Hello! I’m your RACADM assistant. Ask me about any RACADM command."
            break
        if len(user_input.replace(" ", "")) < 2:
            out_response = "Please enter at least 3 characters to search for a RACADM command."
            continue
        requested_field = None
        for field in field_keys:
            if field in user_input_clean:
                requested_field = field
                break

        direct_matches = [cmd for cmd in command_names if user_input_clean in cmd.lower() or cmd.lower() in user_input_clean]

        if direct_matches:
            matched_command = direct_matches[0]
            original_key = raw_command_names[command_names.index(matched_command)]
            cmd_info = commands_dict[original_key]
            print(f"🔧 Command matched (Direct): {matched_command}")
        else:
            query_embedding = model.encode(user_input, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(query_embedding, command_embeddings)[0]
            best_score = torch.max(scores).item()
            best_idx = torch.argmax(scores).item()

            if best_score < SIMILARITY_THRESHOLD:
                out_response = "Sorry, I couldn't find a matching RACADM command."
                break
            else:
                matched_command = command_names[best_idx]
                original_key = raw_command_names[best_idx]
                cmd_info = commands_dict[original_key]
                print(f"🔧 Command matched (Semantic): {matched_command}  (Score: {best_score:.2f})")

        # Display the response
        if 'cmd_info' in locals():
            if requested_field:
                response = cmd_info.get(requested_field, "No information available for that section.")
                out_response = f"**{requested_field.capitalize()}:**\n{response}"
                break
            else:
                for k, v in cmd_info.items():
                    print(f"{k.capitalize()}:\n{v}\n")
                    if direct_matches and requested_field:
                        out_response = f"{k.capitalize()}:\n{v}\n"
                    else:
                        out_response = cmd_info
                break
    return out_response