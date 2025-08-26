#!/bin/bash
set -e

echo "Downloading model files from Google Drive..."

# Movies.pkl
gdown --id 1IbK6BH11YOCi5VYKp7US4-uWJIqrf55i -O backend/movies.pkl

# Similarity.pkl
gdown --id 1pie8Yhz23tRIiWGyNUGiBxCpeRA_LZIQ -O backend/similarity.pkl

echo "Download complete!"
