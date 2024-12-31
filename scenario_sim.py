# ----------------------------------------------------------------
# Code is part from Aleksejs Vesjolijs PhD dissertation
# ----------------------------------------------------------------

import numpy as np
import statistics
import csv

def beta_pert_sample(min_val, mode_val, max_val):
    """
    Draw one random sample from a Beta-PERT distribution given min, mode, and max.
    """
    alpha = 1 + 4 * (mode_val - min_val) / (max_val - min_val)
    beta  = 1 + 4 * (max_val - mode_val) / (max_val - min_val)

    y = np.random.beta(alpha, beta)

    x = min_val + (max_val - min_val) * y
    return x

def beta_pert_monte_carlo(min_val, mode_val, max_val, n=10000):
    """
    Monte Carlo simulation for Beta-PERT distribution.
    Returns (mean, std, p5, p95).
    """
    samples = []
    for _ in range(n):
        val = beta_pert_sample(min_val, mode_val, max_val)
        samples.append(val)
    mean_val = statistics.mean(samples)
    std_val  = statistics.pstdev(samples)
    p5       = np.percentile(samples, 5)
    p95      = np.percentile(samples, 95)
    return mean_val, std_val, p5, p95

def main():
    # ----------------------------------------------------------------
    # 1. DEFINE SCENARIOS & RANGES
    # ----------------------------------------------------------------
    #
    # For each scenario, we specify 'distance' as a single fixed value (no MC),
    # and every other parameter has (min, mode, max).
    # These ranges are illustrative: adapt them for your actual data/assumptions.
    #
    # Keys in each scenario:
    #   - distance (fixed, integer)
    #   - baseline_speed      (min, mode, max)
    #   - baseline_time       (min, mode, max)
    #   - baseline_co2        (min, mode, max)
    #   - baseline_energy     (min, mode, max)
    #   - hl_speed            (min, mode, max)
    #   - hl_time             (min, mode, max)
    #   - hl_co2              (min, mode, max)
    #   - hl_energy           (min, mode, max)

    scenarios = {
        "S1": {
            "distance": 800,
            "baseline_speed":  (80,   90,  120),
            "baseline_time":   (9,    10,   11),
            "baseline_co2":    (20,   22,   25),
            "baseline_energy": (80,  100,  120),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (0.8,  1.0,  1.2),
            "hl_co2":          (1,    2,    3),
            "hl_energy":       (50,  55,   60)
        },
        "S2": {
            "distance": 1500,
            "baseline_speed":  (80,   90,  120),
            "baseline_time":   (15,   16,   17),
            "baseline_co2":    (35,   40,   45),
            "baseline_energy": (150, 180,  200),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (1.5,  1.6,  1.7),
            "hl_co2":          (2,    3,    4),
            "hl_energy":       (90,  100, 110)
        },
        "S3": {
            "distance": 900,
            "baseline_speed":  (110,  115, 120),
            "baseline_time":   (8,    8.5,   9),
            "baseline_co2":    (18,   20,   22),
            "baseline_energy": (90,  100,  110),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (1.0, 1.1,  1.2),
            "hl_co2":          (2,   2.5,   3),
            "hl_energy":       (50,  60,    70)
        },
        "S4": {
            "distance": 500,
            "baseline_speed":  (80,  90,   100),
            "baseline_time":   (5,   5.5,   6),
            "baseline_co2":    (12,  14,   15),
            "baseline_energy": (50,  60,   70),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (0.4, 0.5,  0.6),
            "hl_co2":          (1,   1.5,   2),
            "hl_energy":       (30,  35,   40)
        },
        "S5": {
            "distance": 600,
            "baseline_speed":  (100, 110, 120),
            "baseline_time":   (5,   5.5,   6),
            "baseline_co2":    (14,  16,   18),
            "baseline_energy": (60,  70,   80),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (0.5, 0.6,  0.7),
            "hl_co2":          (1,   1.5,   2),
            "hl_energy":       (35,  40,   45)
        },
        "S6": {
            "distance": 400,
            "baseline_speed":  (100, 110, 120),
            "baseline_time":   (4,   4.5,   5),
            "baseline_co2":    (10,  12,   14),
            "baseline_energy": (40,  50,   60),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (0.4, 0.45, 0.5),
            "hl_co2":          (1,   1.2,   1.5),
            "hl_energy":       (25,  28,   30)
        },
        "S7": {
            "distance": 1200,
            "baseline_speed":  (100, 105, 110),
            "baseline_time":   (11,  11.5,  12),
            "baseline_co2":    (28,  31,   35),
            "baseline_energy": (120, 140,  160),
            "hl_speed":        (900, 950, 1000),
            "hl_time":         (1.2, 1.25, 1.3),
            "hl_co2":          (2,   2.5,   3),
            "hl_energy":       (70,  80,   90)
        },
        "S8": {
            "distance": 1100,
            "baseline_speed":  (110, 115, 120),
            "baseline_time":   (9,   9.5,  10),
            "baseline_co2":    (25,  28,   30),
            "baseline_energy": (100, 120, 140),
            "hl_speed":        (900, 950, 1000),
            "hl_time":         (1.1, 1.15, 1.2),
            "hl_co2":          (2,   2.8,   3),
            "hl_energy":       (60,  70,   80)
        },
        "S9": {
            "distance": 750,
            "baseline_speed":  (80,  90,   110),
            "baseline_time":   (8,   8.5,   9),
            "baseline_co2":    (18,  20,   22),
            "baseline_energy": (70,  80,   90),
            "hl_speed":        (800, 900, 1000),
            "hl_time":         (0.8, 0.85, 0.9),
            "hl_co2":          (1,   2,     3),
            "hl_energy":       (40,  45,   50)
        },
        "S10": {
            "distance": 1000,
            "baseline_speed":  (70,  85,  100),
            "baseline_time":   (10,  11.5, 13),
            "baseline_co2":    (25,  28,   32),
            "baseline_energy": (100, 120, 140),
            "hl_speed":        (900, 950, 1000),
            "hl_time":         (1.0, 1.1,  1.2),
            "hl_co2":          (2,   2.5,   3),
            "hl_energy":       (60,  70,   80)
        },
        "S11": {
            "distance": 6000,
            "baseline_speed":  (60,   80,  120),
            "baseline_time":   (70,   75,   80),
            "baseline_co2":    (120, 130, 150),
            "baseline_energy": (400, 500, 600),
            "hl_speed":        (900, 950, 1000),
            "hl_time":         (6,    6.5,   7),
            "hl_co2":          (30,   35,   40),
            "hl_energy":       (250,  300, 350)
        },
        "S12": {
            "distance": 1200,
            "baseline_speed":  (80,   90,   110),
            "baseline_time":   (12,   12.5,  13),
            "baseline_co2":    (30,   34,    38),
            "baseline_energy": (120,  140,  160),
            "hl_speed":        (800,  900, 1000),
            "hl_time":         (1.2,  1.35, 1.5),
            "hl_co2":          (3,    3.5,   4),
            "hl_energy":       (70,   80,    90)
        }
    }

    N_SAMPLES = 10_000

    # ----------------------------------------------------------------
    # 2. MONTE CARLO CALCULATIONS
    # ----------------------------------------------------------------

    results = []

    columns = [
        "Scenario",
        "Distance",

        "BaselineSpeed_Mean",  "BaselineSpeed_Std",  "BaselineSpeed_P5",  "BaselineSpeed_P95",
        "BaselineTime_Mean",   "BaselineTime_Std",   "BaselineTime_P5",   "BaselineTime_P95",
        "BaselineCO2_Mean",    "BaselineCO2_Std",    "BaselineCO2_P5",    "BaselineCO2_P95",
        "BaselineEnergy_Mean", "BaselineEnergy_Std", "BaselineEnergy_P5", "BaselineEnergy_P95",

        "HLSpeed_Mean",   "HLSpeed_Std",   "HLSpeed_P5",   "HLSpeed_P95",
        "HLTime_Mean",    "HLTime_Std",    "HLTime_P5",    "HLTime_P95",
        "HLCO2_Mean",     "HLCO2_Std",     "HLCO2_P5",     "HLCO2_P95",
        "HLEnergy_Mean",  "HLEnergy_Std",  "HLEnergy_P5",  "HLEnergy_P95"
    ]

    def run_pert_for_param(param_range):
        min_val, mode_val, max_val = param_range
        mean_val, std_val, p5_val, p95_val = beta_pert_monte_carlo(min_val, mode_val, max_val, n=N_SAMPLES)
        return mean_val, std_val, p5_val, p95_val

    for scenario_id, scenario_vals in scenarios.items():
        row = {"Scenario": scenario_id}
        
        dist = scenario_vals["distance"]
        row["Distance"] = dist

        bl_speed_mean, bl_speed_std, bl_speed_p5, bl_speed_p95 = run_pert_for_param(scenario_vals["baseline_speed"])
        row["BaselineSpeed_Mean"] = round(bl_speed_mean,2)
        row["BaselineSpeed_Std"]  = round(bl_speed_std,2)
        row["BaselineSpeed_P5"]   = round(bl_speed_p5,2)
        row["BaselineSpeed_P95"]  = round(bl_speed_p95,2)

        bl_time_mean, bl_time_std, bl_time_p5, bl_time_p95 = run_pert_for_param(scenario_vals["baseline_time"])
        row["BaselineTime_Mean"] = round(bl_time_mean,2)
        row["BaselineTime_Std"]  = round(bl_time_std,2)
        row["BaselineTime_P5"]   = round(bl_time_p5,2)
        row["BaselineTime_P95"]  = round(bl_time_p95,2)

        bl_co2_mean, bl_co2_std, bl_co2_p5, bl_co2_p95 = run_pert_for_param(scenario_vals["baseline_co2"])
        row["BaselineCO2_Mean"] = round(bl_co2_mean,2)
        row["BaselineCO2_Std"]  = round(bl_co2_std,2)
        row["BaselineCO2_P5"]   = round(bl_co2_p5,2)
        row["BaselineCO2_P95"]  = round(bl_co2_p95,2)

        bl_energy_mean, bl_energy_std, bl_energy_p5, bl_energy_p95 = run_pert_for_param(scenario_vals["baseline_energy"])
        row["BaselineEnergy_Mean"] = round(bl_energy_mean,2)
        row["BaselineEnergy_Std"]  = round(bl_energy_std,2)
        row["BaselineEnergy_P5"]   = round(bl_energy_p5,2)
        row["BaselineEnergy_P95"]  = round(bl_energy_p95,2)

        hl_speed_mean, hl_speed_std, hl_speed_p5, hl_speed_p95 = run_pert_for_param(scenario_vals["hl_speed"])
        row["HLSpeed_Mean"] = round(hl_speed_mean,2)
        row["HLSpeed_Std"]  = round(hl_speed_std,2)
        row["HLSpeed_P5"]   = round(hl_speed_p5,2)
        row["HLSpeed_P95"]  = round(hl_speed_p95,2)

        hl_time_mean, hl_time_std, hl_time_p5, hl_time_p95 = run_pert_for_param(scenario_vals["hl_time"])
        row["HLTime_Mean"] = round(hl_time_mean,2)
        row["HLTime_Std"]  = round(hl_time_std,2)
        row["HLTime_P5"]   = round(hl_time_p5,2)
        row["HLTime_P95"]  = round(hl_time_p95,2)

        hl_co2_mean, hl_co2_std, hl_co2_p5, hl_co2_p95 = run_pert_for_param(scenario_vals["hl_co2"])
        row["HLCO2_Mean"] = round(hl_co2_mean,2)
        row["HLCO2_Std"]  = round(hl_co2_std,2)
        row["HLCO2_P5"]   = round(hl_co2_p5,2)
        row["HLCO2_P95"]  = round(hl_co2_p95,2)

        hl_energy_mean, hl_energy_std, hl_energy_p5, hl_energy_p95 = run_pert_for_param(scenario_vals["hl_energy"])
        row["HLEnergy_Mean"] = round(hl_energy_mean,2)
        row["HLEnergy_Std"]  = round(hl_energy_std,2)
        row["HLEnergy_P5"]   = round(hl_energy_p5,2)
        row["HLEnergy_P95"]  = round(hl_energy_p95,2)

        results.append(row)

    out_csv = "hyperloop_montecarlo_results.csv"
    with open(out_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Monte Carlo results saved to: {out_csv}")
    print("Sample output:")
    for row in results[:3]:
        print(row)

if __name__ == "__main__":
    main()
