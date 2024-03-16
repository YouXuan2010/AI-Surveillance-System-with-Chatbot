# AI Surveillance System with Chatbot

The AI Surveillance System is a project designed to provide automated surveillance capabilities using artificial intelligence. 
This system utilizes image-to-text processing to describe images and detect the presence of individuals within camera frames. 
Upon detecting a person, the system initiates a 5-second video recording and generates a security log file containing the date and time of the event. 
The security log file is produced by employing our locally hosted Large Language Model (LLM) from LM Studio, which initializes a local HTTP server emulating the operations of OpenAI's API.
Addtionally, a Telegram Bot has been deployed to facilitate a more user-friendly interface and control over the system.

## Features

- Image-to-text processing for image description
- Person detection within camera frames
- Automated 5-second video recording upon person detection
- Generation of security log files with date and time stamps
- Local HTTP server simulation of OpenAI's API behavior
- Utilization of local Large Language Model (LLM) for security log file generation
- Integration with Telegram Bot for user access and interaction
- Telegram Bot functions include:
  - Starting the surveillance server
  - Checking real-time camera feed

## Getting Started

To get started with the AI Surveillance System, follow these steps:

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/YouXuan2010/AI-Surveillance-System-with-Chatbot.git
    ```

2. **Install Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Telegram Bot**:
    - Obtain a Telegram Bot token from the BotFather.
    - Create .env file under the project directory:
   ```bash
   TELEGRAM_BOT_TOKEN=XXXXXXXXXXX
   ```
4. **Setup Camera and LM Studio server**:
    - Download IP Webcam from Playstore (Only tested using Android phone, Apple user can find others)
    - Start camera server and update *stream_url* in aiss.py
    - Install LM Studio and download any LLM model from HuggingFace Model Hub
    - Start your local LLM server and update the *base_url* in aiss.py 


5. **Run the System**:
    ```bash
    python telebot.py
    ```

6. **Access the Telegram Bot**:
    - Search for your Telegram Bot by its username.
    - Interact with your Bot to start the surveillance server and check real-time camera feed.

## Example Demo
The camera will process the image and detect if there's any people in the image\
For example at some point, the camera captured this:
<img width="700" alt="image" src="https://github.com/YouXuan2010/AI-Surveillance-System-with-Chatbot/assets/100280753/0705c5f0-0be1-4e8e-a651-4de69f4d2155">

The image-to-text model will detect the presence of people and then imform the user via telegram app:
<img width="400" alt="image" src="https://github.com/YouXuan2010/AI-Surveillance-System-with-Chatbot/assets/100280753/7f91182d-9c86-42c7-ae17-6b6b88e83e60">

The security log will be saved in the Security_Logs.txt for future references:
<img width="1000" alt="image" src="https://github.com/YouXuan2010/AI-Surveillance-System-with-Chatbot/assets/100280753/80cc5d7d-8ffa-462b-bf66-91f48b9e7a81">

## Contributing

Contributions are welcome! If you'd like to contribute to the AI Surveillance System, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or feedback regarding the AI Surveillance System, please contact [ME](mailto:youxuan2010@gmail.com).
