"""
domains/reaper/mcp_server/audio_fx.py
Post-processing audio effects for headless REAPER rendering.

Applies analog warmth, saturation, vinyl texture, and lo-fi character
to the clinical GM SoundFont output from fluidsynth.

All processing uses scipy + numpy — no external audio plugins needed.
"""
from __future__ import annotations

import numpy as np


def soft_clip(signal: np.ndarray, drive: float = 2.0) -> np.ndarray:
    """Warm tube-style soft clipping (tanh saturation)."""
    return np.tanh(signal * drive) / np.tanh(drive)


def tape_saturation(signal: np.ndarray, amount: float = 0.3) -> np.ndarray:
    """Tape-style saturation: asymmetric soft clip + slight compression."""
    # Asymmetric: positive peaks clip softer than negative
    driven = signal * (1.0 + amount * 2)
    pos = np.tanh(driven * 0.8)
    neg = np.tanh(driven * 1.2)
    out = np.where(signal >= 0, pos, neg)
    # Blend with dry signal
    return signal * (1 - amount) + out * amount


def vinyl_noise(length: int, sr: int = 44100, level: float = 0.008) -> np.ndarray:
    """Generate vinyl crackle / hiss texture."""
    rng = np.random.default_rng(42)
    # Base hiss (pink noise approximation)
    white = rng.normal(0, 1, length)
    # Simple pink noise: cumulative filter
    b = [0.049922035, -0.095993537, 0.050612699, -0.004709510]
    a = [1.0, -2.494956002, 2.017265875, -0.522189400]
    from scipy.signal import lfilter
    pink = lfilter(b, a, white)
    pink = pink / (np.abs(pink).max() + 1e-10) * level

    # Crackle: sparse random pops
    crackle = np.zeros(length)
    n_pops = int(length / sr * 8)  # ~8 pops per second
    pop_positions = rng.integers(0, length, n_pops)
    pop_amplitudes = rng.uniform(0.01, 0.04, n_pops)
    for pos, amp in zip(pop_positions, pop_amplitudes):
        # Short click (2-5 samples)
        pop_len = rng.integers(2, 6)
        end = min(pos + pop_len, length)
        crackle[pos:end] = amp * rng.choice([-1, 1])

    return pink + crackle


def lofi_filter(signal: np.ndarray, sr: int = 44100, cutoff: float = 8000) -> np.ndarray:
    """Lo-fi character: gentle low-pass + slight bit reduction."""
    from scipy.signal import butter, sosfilt
    # Low-pass filter
    nyq = sr / 2
    freq = min(cutoff, nyq * 0.95)
    sos = butter(4, freq, btype='low', fs=sr, output='sos')
    filtered = sosfilt(sos, signal, axis=0)
    return filtered


def stereo_widen(signal: np.ndarray, amount: float = 0.3) -> np.ndarray:
    """Widen stereo image via mid-side processing."""
    if signal.ndim == 1:
        return signal
    mid = (signal[:, 0] + signal[:, 1]) / 2
    side = (signal[:, 0] - signal[:, 1]) / 2
    # Boost sides
    side = side * (1 + amount)
    out = np.column_stack([mid + side, mid - side])
    return out


def bass_boost(signal: np.ndarray, sr: int = 44100, gain_db: float = 4.0, freq: float = 80) -> np.ndarray:
    """Boost sub-bass frequencies for 808 warmth."""
    from scipy.signal import butter, sosfilt
    sos = butter(2, freq, btype='low', fs=sr, output='sos')
    bass = sosfilt(sos, signal, axis=0)
    gain = 10 ** (gain_db / 20)
    return signal + bass * (gain - 1)


def apply_kanye_chain(
    audio: np.ndarray,
    sr: int = 44100,
    style: str = "kanye_soul",
) -> np.ndarray:
    """Apply a genre-appropriate mastering chain.

    Styles:
        kanye_soul: Warm tape saturation + vinyl + bass boost + lo-fi filter
        lofi_hiphop: Heavy vinyl + low-pass + bit crush feel
        synthwave: Stereo widen + tape + bright
        clean: Light saturation only
    """
    out = audio.copy().astype(np.float64)

    if style == "kanye_soul":
        out = tape_saturation(out, amount=0.35)
        out = bass_boost(out, sr=sr, gain_db=5.0, freq=90)
        out = lofi_filter(out, sr=sr, cutoff=12000)
        noise = vinyl_noise(len(out), sr=sr, level=0.006)
        if out.ndim == 2:
            noise = np.column_stack([noise, noise])
        out = out + noise
        out = stereo_widen(out, amount=0.2)
        out = soft_clip(out, drive=1.5)

    elif style == "lofi_hiphop":
        out = tape_saturation(out, amount=0.25)
        out = lofi_filter(out, sr=sr, cutoff=8000)
        out = bass_boost(out, sr=sr, gain_db=3.0, freq=70)
        noise = vinyl_noise(len(out), sr=sr, level=0.012)
        if out.ndim == 2:
            noise = np.column_stack([noise, noise])
        out = out + noise
        out = soft_clip(out, drive=1.3)

    elif style == "synthwave":
        out = tape_saturation(out, amount=0.2)
        out = stereo_widen(out, amount=0.4)
        out = bass_boost(out, sr=sr, gain_db=3.0, freq=100)
        out = soft_clip(out, drive=1.8)

    elif style == "clean":
        out = tape_saturation(out, amount=0.1)
        out = soft_clip(out, drive=1.2)

    else:
        out = tape_saturation(out, amount=0.2)
        out = soft_clip(out, drive=1.4)

    # Final normalize to -1 dB headroom
    peak = np.abs(out).max()
    if peak > 0:
        target = 10 ** (-1.0 / 20)  # -1 dB
        out = out * (target / peak)

    return out.astype(np.float32)
