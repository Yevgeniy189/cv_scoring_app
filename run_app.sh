#!/bin/bash

# Активируем виртуальное окружение
source /Users/yevgeniy/PycharmProjects/CV_SCORING_RECORDING/.venv/bin/activate

# Запускаем Streamlit в фоне
streamlit run /Users/yevgeniy/PycharmProjects/CV_SCORING_RECORDING/streamlit_app.py

# Ждём и запускаем браузер
sleep 2
open http://localhost:8501