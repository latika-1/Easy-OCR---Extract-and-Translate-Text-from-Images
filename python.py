import easyocr as ocr
import gradio as gr
from PIL import Image
import numpy as np
from gradio import components
from googletrans import LANGCODES, Translator


def upload_and_process_image(image_path, target_language, output_file):
    reader = ocr.Reader(['en'], model_storage_directory='.')
    input_image = Image.open(image_path)
    result = reader.readtext(np.array(input_image))
    result_text = [text[1] for text in result]
    
    # Translate the extracted text to target language
    translator = Translator()
    translated_text = translator.translate(" ".join(result_text), dest=target_language).text
    
    # Write the translated text to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)
    
    return translated_text

# Get a list of supported languages from Google Translate API
supported_languages = list(LANGCODES.keys())

image_input = gr.inputs.Image(label="Upload your image here", type="filepath")
language_input = gr.inputs.Dropdown(label="Select target language", choices=supported_languages)
output_file_input = gr.inputs.Textbox(label="Enter output file name")
text_output = gr.outputs.Textbox(label="Extracted and Translated Text")

gr.Interface(fn=upload_and_process_image, inputs=[image_input, language_input, output_file_input], outputs=text_output, title="Easy OCR - Extract and Translate Text from Images").launch()
