# Ensure the llama3 model is pulled before starting Ollama

echo "Pulling llama3 model"
ollama pull llama3

echo "Starting Ollama Server"
ollama serve
