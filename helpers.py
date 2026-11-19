import os
import matplotlib
matplotlib.use('Agg')  # Flask thread-safe mode
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

def process_audio(file_path, filename):
    sample_rate, data = wavfile.read(file_path)

    # Αν είναι stereo, παίρνουμε το 1ο κανάλι
    if len(data.shape) > 1:
        data = data[:, 0]

    # Normalized Data (-1.0 to 1.0)
    if data.dtype == np.int16:
        norm_data = data / 32768.0
    elif data.dtype == np.int32:
        norm_data = data / 2147483648.0
    else:
        norm_data = data.astype(float)

    length_in_sec = len(data) / sample_rate
    time = np.linspace(0., length_in_sec, len(data))

    # Advanced Metrics
    rms_energy = float(np.sqrt(np.mean(norm_data**2)))
    peak_amplitude = float(np.max(np.abs(norm_data)))

    # Dark Style Configuration for Charts
    plt.style.use('dark_background')

    # --- Plot 1: Waveform (Time Domain) ---
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(time, norm_data, color='#00f2fe', linewidth=0.7, alpha=0.85)
    ax.set_title('TIME DOMAIN WAVEFORM (Amplitude vs Time)', fontsize=10, pad=10, color='#00f2fe', fontweight='bold')
    ax.set_xlabel('Time (s)', fontsize=8)
    ax.set_ylabel('Amplitude', fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.2, color='#ffffff')
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#020617')
    plt.tight_layout()

    waveform_path = os.path.join('static', 'uploads', f"wave_{filename}.png")
    plt.savefig(waveform_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close()

    # --- Plot 2: FFT Frequency Spectrum ---
    fft_spectrum = np.fft.rfft(norm_data)
    freq = np.fft.rfftfreq(len(norm_data), d=1/sample_rate)
    fft_magnitude = np.abs(fft_spectrum)

    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(freq, fft_magnitude, color='#ff007f', linewidth=0.8, alpha=0.9)
    ax.set_title('FREQUENCY SPECTRUM (FFT Magnitude vs Frequency)', fontsize=10, pad=10, color='#ff007f', fontweight='bold')
    ax.set_xlabel('Frequency (Hz)', fontsize=8)
    ax.set_ylabel('Magnitude', fontsize=8)
    ax.grid(True, linestyle=':', alpha=0.2, color='#ffffff')
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#020617')
    plt.tight_layout()

    fft_path = os.path.join('static', 'uploads', f"fft_{filename}.png")
    plt.savefig(fft_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close()

    # --- Plot 3: Spectrogram (Frequency vs Time Heatmap) ---
    fig, ax = plt.subplots(figsize=(10, 3.2))
    Pxx, freqs, bins, im = ax.specgram(norm_data, Fs=sample_rate, NFFT=1024, cmap='magma')
    ax.set_title('SPECTROGRAM (Time-Frequency Heatmap)', fontsize=10, pad=10, color='#38bdf8', fontweight='bold')
    ax.set_xlabel('Time (s)', fontsize=8)
    ax.set_ylabel('Frequency (Hz)', fontsize=8)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#020617')
    plt.tight_layout()

    spectrogram_path = os.path.join('static', 'uploads', f"spec_{filename}.png")
    plt.savefig(spectrogram_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close()

    dominant_freq = round(float(freq[np.argmax(fft_magnitude)]), 2)

    return {
        "duration": round(length_in_sec, 2),
        "sample_rate": sample_rate,
        "dominant_freq": dominant_freq,
        "rms_energy": round(rms_energy, 4),
        "peak_amplitude": round(peak_amplitude, 4),
        "waveform_img": f"uploads/wave_{filename}.png",
        "fft_img": f"uploads/fft_{filename}.png",
        "spectrogram_img": f"uploads/spec_{filename}.png"
    }
