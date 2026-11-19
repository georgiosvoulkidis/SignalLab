# SIGNALLAB: ACOUSTIC SIGNAL PROCESSING WORKBENCH
#### Video Demo: https://youtu.be/k6kvb5tKaFk
#### Description:

## Overview

SignalLab is an interactive web-based audio signal processing application built with Python, Flask, NumPy, SciPy, Matplotlib, and SQLite.

I created this application as my final project for CS50x. Having completed my first year as an Electrical and Computer Engineering (ECE) student, I wanted my final project to bridge the software engineering concepts taught in CS50 (web development, database management, and Python scripting) with fundamental engineering principles from signal processing. Instead of building a generic web utility, I designed SignalLab as an analytical laboratory workbench that accepts uncompressed `.wav` audio files, evaluates their temporal and spectral characteristics, and presents real-time graphical representations alongside quantitative audio metrics.

## Features and Functionality

The application provides a clean dashboard designed for students and educators working with digital audio signals. Main features include:

- File Upload Validation: Accepts user-uploaded audio files while verifying that the input strictly matches the `.wav` audio format.
- Embedded Audio Playback: An HTML5 audio player built into the interface allows users to listen to the uploaded file directly in the browser while reviewing its visual data.
- Time Domain Waveform Analysis: Displays a digital oscilloscope-style line plot showing signal amplitude variation over time.
- Frequency Domain FFT Analysis: Calculates the Fast Fourier Transform (FFT) of the discrete audio samples to map spectral magnitude against frequency in Hertz, identifying the dominant pitch peak.
- Time-Frequency Spectrogram Heatmap: Computes a Short-Time Fourier Transform (STFT) matrix to display how spectral density changes continuously across the recording timeline.
- Quantitative Metrics Overview: Summarizes mathematical characteristics, including sample rate (Hz), playback duration (seconds), dominant peak frequency (Hz), Root Mean Square (RMS) energy, and peak absolute amplitude.
- Database Logging System: Automatically records each analysis run into a local SQLite database (`project.db`) to provide an audit history of processed audio files.

## Detailed File Breakdown

Below is a detailed breakdown of each file created for this project and its functional role within the system architecture:

- `app.py`
This is the core Flask application controller. It manages the server routing, handles file uploads coming from HTTP POST requests, enforces file extension security using `werkzeug.utils.secure_filename`, calls processing functions from the helper module, and manages database operations with SQLite. Upon successful execution of an audio file, it logs the filename, timestamp, sampling rate, duration, and dominant frequency into `project.db` before passing the data to the view engine.

- `helpers.py`
This module acts as the scientific processing engine of the application. It imports `scipy.io.wavfile` to extract uncompressed pulse-code modulation (PCM) integer data and converts it into floating-point arrays using `numpy`. It normalizes variable integer bit depths (16-bit or 32-bit) to a standardized range between -1.0 and 1.0. It calculates key mathematical metrics such as RMS energy using array operations. Furthermore, it computes the Fast Fourier Transform using `numpy.fft.rfft` and generates three distinct dark-themed visualizations (Waveform, FFT Spectrum, and Spectrogram) using `matplotlib`. The generated charts are rendered non-interactively and saved directly to disk as PNG images.

- `templates/layout.html`
Defines the base HTML5 structure for the user interface. It incorporates responsive grid styling from Bootstrap 5 and icon elements from FontAwesome. It establishes a dark visual design intended to mimic professional laboratory equipment and includes navigation elements along with dynamic flash message handling.

- `templates/index.html`
Serves as the main operational view for the application. It contains the audio upload form, the embedded audio player, structured metric summary cards, and the image output display area for the generated Matplotlib graphs.

- `templates/history.html`
Renders a data table that queries and displays past audio analysis logs from `project.db`. It lists historical records including filename, submission date, playback duration, sample rate, and computed peak frequency.

- `project.db`
An SQLite database file containing a table named `history`. It provides persistent storage for tracking metadata from previously uploaded and processed audio files across web sessions.

- `requirements.txt`
Specifies all external Python dependencies required to run the application environment, including Flask, NumPy, SciPy, and Matplotlib.

## Design Choices and Trade-Offs

Throughout the development process, several technical decisions were evaluated:

- Restricting Audio Input to WAV Files
I deliberately limited uploads to uncompressed `.wav` files rather than supporting compressed audio formats such as MP3 or AAC. Formats like MP3 use lossy compression algorithms that intentionally discard higher frequencies to decrease file size. Because this tool is designed to perform exact spectral frequency calculations, retaining raw, uncompressed PCM data was necessary to maintain mathematical precision.

- Server-Side Python Computation vs Client-Side JavaScript
While browser-based WebAudio JavaScript APIs are capable of rendering real-time audio visualizers, performing calculations on the server using Python's scientific libraries (`numpy` and `scipy`) offered higher computational accuracy for Fourier analysis. Server-side rendering also made it straightforward to export static, high-resolution chart images that can be reviewed independently or logged to a database.

- Solving Matplotlib Backend Threading Issues
During initial testing with Flask, Matplotlib generated GUI thread errors because Flask handles requests across multiple threads, and Matplotlib defaults to an interactive desktop window backend. I resolved this issue by adding `matplotlib.use('Agg')` at the beginning of `helpers.py`. This instructs Matplotlib to run in a headless mode, rendering figures directly into static files without opening a desktop GUI window.

- Database Integration for Historical Tracking
I chose SQLite for database storage due to its lightweight, serverless design. Storing analysis history in `project.db` allows users to review previously calculated metrics without needing to re-upload and re-process audio files.

## Instructions to Run the Project

1. Navigate to the project directory:
   ```bash
   cd project
