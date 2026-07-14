# app/ml/attack_generator.py
import random

def bot_typing(seed=None):
    """Very fast, near-perfectly uniform timing -> automated script."""
    rnd = random.Random(seed)
    return {
        "wpm": rnd.uniform(85, 110),
        "avg_dwell": rnd.uniform(0.02, 0.035),
        "avg_flight": rnd.uniform(0.008, 0.015),
        "std_dwell": rnd.uniform(0.0005, 0.002),
        "std_flight": rnd.uniform(0.0005, 0.002),
        "backspace_rate": 0.0,
        "longest_pause": rnd.uniform(0.01, 0.02),
    }

def high_speed_typing(seed=None):
    """Extremely fast bursts -- e.g. credential stuffing or paste-like input."""
    rnd = random.Random(seed)
    return {
        "wpm": rnd.uniform(120, 160),
        "avg_dwell": rnd.uniform(0.01, 0.02),
        "avg_flight": rnd.uniform(0.003, 0.008),
        "std_dwell": rnd.uniform(0.0003, 0.001),
        "std_flight": rnd.uniform(0.0003, 0.001),
        "backspace_rate": 0.0,
        "longest_pause": rnd.uniform(0.005, 0.01),
    }

def noisy_impersonator(seed=None):
    """Slow, hesitant, highly inconsistent -> unfamiliar user imitating the real one."""
    rnd = random.Random(seed)
    return {
        "wpm": rnd.uniform(8, 16),
        "avg_dwell": rnd.uniform(0.18, 0.30),
        "avg_flight": rnd.uniform(0.20, 0.35),
        "std_dwell": rnd.uniform(0.06, 0.12),
        "std_flight": rnd.uniform(0.08, 0.15),
        "backspace_rate": rnd.uniform(0.1, 0.3),
        "longest_pause": rnd.uniform(0.8, 2.0),
    }

def random_noise_injection(seed=None):
    """Random values across the whole plausible range -- broad stress test."""
    rnd = random.Random(seed)
    return {
        "wpm": rnd.uniform(5, 160),
        "avg_dwell": rnd.uniform(0.01, 0.35),
        "avg_flight": rnd.uniform(0.005, 0.4),
        "std_dwell": rnd.uniform(0.0005, 0.15),
        "std_flight": rnd.uniform(0.0005, 0.15),
        "backspace_rate": rnd.uniform(0, 0.4),
        "longest_pause": rnd.uniform(0.01, 2.0),
    }

ATTACK_GENERATORS = {
    "bot_typing": bot_typing,
    "high_speed_typing": high_speed_typing,
    "noisy_impersonator": noisy_impersonator,
    "random_noise_injection": random_noise_injection,
}

def generate_attack_batch(n_per_type=10, seed=42):
    rnd = random.Random(seed)
    batch = []
    for name, fn in ATTACK_GENERATORS.items():
        for _ in range(n_per_type):
            profile = fn(seed=rnd.randint(0, 999999))
            profile["dwell_flight_ratio"] = round(profile["avg_dwell"] / profile["avg_flight"], 4) if profile["avg_flight"] > 0 else 0
            profile["attack_type"] = name
            batch.append(profile)
    return batch