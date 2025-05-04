from flask import Flask, render_template, request, jsonify
from parsed_Commands_Text_Fun import parsing_commands
from pdf_Data_Extraction import pdf_data_extractor
from chatBot_Func import chatBot_reponse
app = Flask(__name__)
pdf_path = r"C:\Users\Saimanoj_Pulluri\OneDrive - Dell Technologies\Desktop\PDF_work\chat_bot_trail\iDRAC9_7.10.30.00_RACADM_CLI_Guide 6.pdf"
input_file_path = r"C:\Users\Saimanoj_Pulluri\OneDrive - Dell Technologies\Desktop\PDF_work\chat_bot_trail\extracted_tables.txt"
output_file_path = r"C:\Users\Saimanoj_Pulluri\OneDrive - Dell Technologies\Desktop\PDF_work\chat_bot_trail\parsed_commands.txt"

commands_data = pdf_data_extractor(pdf_path,input_file_path, output_file_path)
parsing_commands(commands_data)

@app.route('/')
def home():
    return render_template('chatBot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    if not user_msg:
        return jsonify({'reply': 'I didn’t get that. Please try again.'})
    
    bot_response = chatBot_reponse(user_msg)
    print(bot_response)

    return jsonify({'reply': bot_response})

if __name__ == '__main__':
    app.run(debug=False)
