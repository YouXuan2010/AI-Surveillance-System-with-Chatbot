# AI Surveillance System

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
    git clone https://github.com/your-username/AI-Surveillance-System.git
    ```

2. **Install Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Telegram Bot**:
    - Obtain a Telegram Bot token from the BotFather.
    - Replace the placeholder token in `telegram_bot.py` with your actual token.

4. **Run the System**:
    ```bash
    python main.py
    ```

5. **Access the Telegram Bot**:
    - Search for your Telegram Bot by its username.
    - Interact with the Bot to start the surveillance server and check real-time camera feed.

## Usage

- Upon starting the system, it continuously monitors the camera feed.
- When a person is detected, a 5-second video is recorded, and a security log file is generated.
- Users can access the system and interact with it via the Telegram Bot.

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
