# OpenAI chatbot accelerator

Requires `OPENAI_API_KEY` environment variable set.

To run, pass a location to store document database as an argument:

`python app.py <path to store document database>`  

# Setup system service

```bash
sudo cp openaichatbotaccelerator.service /lib/systemd/system/
sudo systemctl enable openaichatbotaccelerator.service
sudo systemctl start openaichatbotaccelerator.service
```
