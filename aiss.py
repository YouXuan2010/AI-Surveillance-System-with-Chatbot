from openai import OpenAI
import openai
import os
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import cv2
import time
import datetime


client = OpenAI(base_url='http://localhost:1234/v1', api_key='not-needed')

def mistral7b(user_input):
    try:
        streamed_completion = client.chat.completions.create(model="local-model", 
                                                            messages=[{"role": "system", "content": "You expert at writing security logs. Write the log using the given description."}, 
                                                                      {"role": "user", "content": user_input}],
                                                            stream=True)  
        full_response = ""
        line_buffer = ""

        for chunk in streamed_completion:
            delta_content = chunk.choices[0].delta.content
            if delta_content is not None:
                line_buffer += delta_content

                if '\n' in line_buffer:
                    lines = line_buffer.split('\n')
                    for line in lines[:-1]:
                        full_response += line + '\n'
                    line_buffer = lines[-1]

        if line_buffer:
            # # Add timestamp and date to the remaining buffer
            # timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            # date = datetime.datetime.now().strftime("%Y-%m-%d")
            # line_with_timestamp = f"[{date} {timestamp}] {line_buffer}"
            # print(line_with_timestamp)  # Print line with timestamp for debugging
            full_response += line_buffer

        return full_response, True
    
    except openai.APIConnectionError as e:
        print("Error connecting to OpenAI API:", e , "Please check LM Studio is running and accessible at the specified URL")
        return str(e), False
	
def process_image(images_dir):
    # Find all images in the directory
    images = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png')]

    if not images:
        print('No images found in the directory')
        return None, None
    
    # Sort the images by modification time
    latest_images = max(images, key=os.path.getmtime)

    for image in images:
        if image != latest_images:
            os.remove(image)
            print(f"Removed {image}")

    # Process the latest image
    model_id = "vikhyatk/moondream2"
    revision = "2024-03-06"
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    image = Image.open(latest_images)
    enc_image = model.encode_image(image)

    return model, enc_image, tokenizer

def start_video_capture(stream_url, output_dir, capture_duration=5):
    """
    Captures video from the stream for the given duration and saves it as .mp4 using H.264 codec.
    Returns the path to the captured video.

    :param stream_url: URL of the video stream
    :param output_dir: Directory to save the captured video
    :param capture_duration: Duration of the video to capture
    """
    ensure_dir_exists(output_dir)

    cap = cv2.VideoCapture(stream_url)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1270)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open video stream")
        return None

    # Get actual frame size
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))    

    # Define the codec and create VideoWriter object
    # Attempt to use H.264 codec ('X264' or 'avc1') for better compression
    # Note: Might need to change the codec based on the system
    fourcc = cv2.VideoWriter_fourcc(*'X264')

    output_path = os.path.join(output_dir, f'captured_video_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    start_time = time.time()
    print("Started capturing video...")

    while int(time.time() - start_time) < capture_duration:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        out.write(frame)
        # cv2.imshow('Capturing Video', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f'Video captured and saved at {output_path}')

    return output_path

def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def capture_frame(stream_url, images_dir='images'):
    # Capture a single frame from the video stream and save it into a directory
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("Error: Could not open video stream")
        return 0
    
    ensure_dir_exists(images_dir)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
    else:
        filename = os.path.join(images_dir, f'frame_{int(time.time())}.jpg')
        cv2.imwrite(filename, frame)
        print(f'Frame captured and saved at {filename}')
    
    cap.release()
    return 1

def save_file(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write(text + '\n')
    except Exception as e:
        print(f"Error occurred while saving file: {e}")
    
def main():

    stream_url = 'http://192.168.0.103:8080/video'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, "images")
    video_dir = os.path.join(current_dir, "video")

    person_detected = False

    while True:
        if capture_frame(stream_url, images_dir=images_dir):
            print("Frame captured. Processing the image...")
            text_model, image_embeds, tokenizer = process_image(images_dir)
            prompt = "Is there a PERSON in the image? (ONLY ANSWER WITH YES OR NO)"
            # prompt = "Is there a zombie in the image? (ONLY ANSWER WITH YES OR NO)"
            print(">", prompt)

            # Ensure text_model and image_embeds are not valid
            if text_model is not None and image_embeds is not None:
                answer = text_model.answer_question(image_embeds, prompt, tokenizer).strip().upper()
            else:
                print("Could not process the image")
                continue
                
            print("Response:", answer)

            if answer == "YES":
                person_detected = True
                print("Person detected! Starting video capture...")
                video_path = start_video_capture(stream_url, output_dir=video_dir, capture_duration=5)

                # text_model, image_embeds, tokenizer2 = process_image(images_dir)
                prompt2 = "Describe the image in details, try to identify Gender, Objects, Clothing color, Shoes, Environment, Weather etc:"
                # prompt2 = "Describe the gameplay image in details, try to identify what is happening in the scene"
                answer2 = text_model.answer_question(image_embeds, prompt2, tokenizer)
                print("Image Description:", answer2)
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                log = f"[{date} {timestamp}] Image Description: {answer2}"
                # log = "Image Description: " + answer2
                log2, success = mistral7b(log)
                if success:
                    print(log2)
                    save_file('Security_Logs.txt', log2)
                else:
                    print(log2)
                    return False

                print("Notifying user via Telegram...")
                return True

            elif answer == "NO":
                person_detected = False
            else:
                print("Invalid response. Please answer with YES or NO")
                continue

            print("Person detected:", person_detected)
        else:
            print("Failed to capture frame. Please check the video stream.")
            break
    return False
            

# Run the main coroutine
if __name__ == "__main__":
    main()