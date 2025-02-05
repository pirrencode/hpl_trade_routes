#########################################################################
# ----------------------------------------------------------------
# Code is part of Aleksejs Vesjolijs PhD dissertation
# ----------------------------------------------------------------
# Monte Carlo Simulations, BETA-PERT method
#########################################################################


import numpy as np
import statistics
import csv

def beta_pert_sample(min_val, mode_val, max_val):
    alpha = 1 + 4 * (mode_val - min_val) / (max_val - min_val)
    beta  = 1 + 4 * (max_val - mode_val) / (max_val - min_val)
    y = np.random.beta(alpha, beta)
    return min_val + (max_val - min_val) * y

def beta_pert_monte_carlo(min_val, mode_val, max_val, n=10000):
    samples = [beta_pert_sample(min_val, mode_val, max_val) for _ in range(n)]
    return statistics.mean(samples), statistics.pstdev(samples), np.percentile(samples, 5), np.percentile(samples, 95)

def main():
    input_csv = "monte_carlo_inputs.csv"
    output_csv = "hyperloop_montecarlo_results.csv"

    def read_scenarios_from_csv(filename):
        scenarios = {}
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [col.strip().lower() for col in reader.fieldnames]
            for row in reader:
                row = {key.strip().lower(): value for key, value in row.items()}
                scenario_id = row["scenario"]
                scenarios[scenario_id] = {
                    "distance": int(row["distance"]),
                    "baseline_speed":  (float(row["baselinespeed_min"]),  float(row["baselinespeed_mode"]),  float(row["baselinespeed_max"])),
                    "baseline_time":   (float(row["baselinetime_min"]),   float(row["baselinetime_mode"]),   float(row["baselinetime_max"])),
                    "baseline_co2":    (float(row["baselineco2_min"]),    float(row["baselineco2_mode"]),    float(row["baselineco2_max"])),
                    "baseline_energy": (float(row["baselineenergy_min"]), float(row["baselineenergy_mode"]), float(row["baselineenergy_max"])),
                    "hl_speed":        (float(row["hlspeed_min"]),        float(row["hlspeed_mode"]),        float(row["hlspeed_max"])),
                    "hl_time":         (float(row["hltime_min"]),         float(row["hltime_mode"]),         float(row["hltime_max"])),
                    "hl_co2":          (float(row["hlco2_min"]),          float(row["hlco2_mode"]),          float(row["hlco2_max"])),
                    "hl_energy":       (float(row["hlenergy_min"]),       float(row["hlenergy_mode"]),       float(row["hlenergy_max"])),
                }
        return scenarios

    scenarios = read_scenarios_from_csv(input_csv)
    N_SAMPLES = 10_000
    results = []

    columns = [
        "scenario", "distance",
        "baseline_speed_mean", "baseline_speed_std", "baseline_speed_p5", "baseline_speed_p95",
        "baseline_time_mean", "baseline_time_std", "baseline_time_p5", "baseline_time_p95",
        "baseline_co2_mean", "baseline_co2_std", "baseline_co2_p5", "baseline_co2_p95",
        "baseline_energy_mean", "baseline_energy_std", "baseline_energy_p5", "baseline_energy_p95",
        "hl_speed_mean", "hl_speed_std", "hl_speed_p5", "hl_speed_p95",
        "hl_time_mean", "hl_time_std", "hl_time_p5", "hl_time_p95",
        "hl_co2_mean", "hl_co2_std", "hl_co2_p5", "hl_co2_p95",
        "hl_energy_mean", "hl_energy_std", "hl_energy_p5", "hl_energy_p95"
    ]

    def run_pert_for_param(param_range):
        return beta_pert_monte_carlo(*param_range, n=N_SAMPLES)

    for scenario_id, scenario_vals in scenarios.items():
        row = {"scenario": scenario_id, "distance": scenario_vals["distance"]}
        for key in ["baseline_speed", "baseline_time", "baseline_co2", "baseline_energy", "hl_speed", "hl_time", "hl_co2", "hl_energy"]:
            mean_val, std_val, p5_val, p95_val = run_pert_for_param(scenario_vals[key])
            row[f"{key}_mean"] = round(mean_val, 2)
            row[f"{key}_std"] = round(std_val, 2)
            row[f"{key}_p5"] = round(p5_val, 2)
            row[f"{key}_p95"] = round(p95_val, 2)
        results.append(row)

    print("Expected Columns:", columns)
    print("Generated Dictionary Keys:", results[0].keys())

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print(f"Monte Carlo results saved to: {output_csv}")
    print("Sample output:")
    for row in results[:3]:
        print(row)

if __name__ == "__main__":
    main()
