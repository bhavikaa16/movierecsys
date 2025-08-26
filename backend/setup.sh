#!/bin/bash
set -e

echo "Downloading model files from Google Drive..."

# Movies.pkl
gdown --id 1IbK6BH11YOCi5VYKp7US4-uWJIqrf55i -O movies.pkl

# Similarity.pkl
gdown --id 1pie8Yhz23tRIiWGyNUGiBxCpeRA_LZIQ -O similarity.pkl

echo "Download complete!"
