# 🎉 Welcome to the Morpheus AI Project!

This repository is dedicated to the creation of a **Morpheus Mistral AI Chatbot and Voice Bot**, powered by the amazing Cartesia technology! This has been a super fun project, and I’m excited to share it with you!

## 🚀 Project Overview

Morpheus AI combines the power of Mistral AI's fine-tuning capabilities with Cartesia's voice synthesis to create an interactive chatbot that can respond in a natural and engaging manner. Whether you're looking to chat or just want to hear Morpheus' voice, this project has got you covered!

## 📦 Contents

- `morpheus_fine_tuning_script.py`: The Python script for fine-tuning the Mistral AI model.
- `morpheus_fine_tuning_data.jsonl`: The training data in JSONL format, ready for fine-tuning.
- `morpheus_voice_samples/`: Directory containing original MP3 files of Morpheus' voice.
- `cartesia_cloned_voice/`: Directory containing the cloned voice files from Cartesia.

## 🛠️ Setup and Fine-Tuning Process

### Step 1: Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/morpheus-ai-fine-tuning.git
cd morpheus-ai-fine-tuning
```

### Step 2: Google Colab Setup

1. Go to [Google Colab](https://colab.research.google.com/).
2. Create a new notebook.
3. In the first cell, mount your Google Drive to access the files:

```python
from google.colab import drive
drive.mount('/content/drive')
```

4. Navigate to the directory where you want to save the project files:

```python
%cd /content/drive/MyDrive/path/to/project/folder
```

5. Clone the GitHub repository in Colab:

```python
!git clone https://github.com/your-username/morpheus-ai-fine-tuning.git
%cd morpheus-ai-fine-tuning
```

### Step 3: Install Required Libraries

Run the following command to install the necessary libraries:

```python
!pip install requests tqdm tenacity mistralai
```

### Step 4: Run the Fine-Tuning Script

1. Copy the contents of `morpheus_fine_tuning_script.py` into a new cell in your Colab notebook.
2. Run the cell to execute the script.
3. When prompted, enter your Mistral AI API key.
4. Upload the `morpheus_fine_tuning_data.jsonl` file when requested.

### Step 5: Monitor the Fine-Tuning Process

The script will provide real-time updates on the fine-tuning process. Keep an eye on the output for any errors or completion messages.

## 📄 JSONL File Format

The `morpheus_fine_tuning_data.jsonl` file follows the Mistral AI fine-tuning format. Each line should be a valid JSON object with the following structure:

```json
{
  "messages": [
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Assistant response"}
  ]
}
```

Feel free to add more data to this file, ensuring each new entry follows the same structure!

## 🎤 Voice Cloning

The original Morpheus voice samples are located in the `morpheus_voice_samples/` directory. The cloned voice files from Cartesia can be found in the `cartesia_cloned_voice/` directory.

## 🛠️ Troubleshooting

If you encounter any issues during the fine-tuning process, please check the following:

1. Ensure your Mistral AI API key is valid and has sufficient credits.
2. Verify that the JSONL file is correctly formatted and follows Mistral AI's guidelines.
3. Check your internet connection, as the process requires a stable connection to communicate with the Mistral AI API.

For any persistent issues, please open an issue in this GitHub repository, and I'll be happy to help!

## 🤝 Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your proposed changes. Your contributions are welcome!

## 📜 License
