#########################################################################
# ----------------------------------------------------------------
# Code is part of Aleksejs Vesjolijs PhD dissertation
# ----------------------------------------------------------------
# Main application logic
#########################################################################

import csv
import math

alpha = {
    "alpha0": 1.0, 
    "alpha1": -0.6,  
    "alpha2":  0.1,  
    "alpha3": -0.05, 
    "alpha4": -0.08, 
    "alpha5": -0.02, 
    "alpha6":  0.15, 
    "alpha7": -0.07, 
    "alpha8": -0.09, 
    "alpha9": -0.03  
}

def compute_baseline_exports(row, alpha):
    """
    φ_{ij}^{bl} = exp(
      alpha0
    + alpha1 * ln(distance)
    + alpha2 * ln(baseline_speed_mean)
    + alpha3 * ln(baseline_time_mean + 1)
    + alpha4 * ln(baseline_co2_mean + 1)
    + alpha5 * ln(baseline_energy_mean + 1)
    )
    """
    distance   = float(row["distance"])
    base_speed = float(row["baseline_speed_mean"])
    base_time  = float(row["baseline_time_mean"])
    base_co2   = float(row["baseline_co2_mean"])
    base_ener  = float(row["baseline_energy_mean"])

    ln_dist   = math.log(distance)
    ln_bspeed = math.log(base_speed)
    ln_btime  = math.log(base_time + 1)
    ln_bco2   = math.log(base_co2 + 1)
    ln_bener  = math.log(base_ener + 1)

    exponent = (
        alpha["alpha0"]
        + alpha["alpha1"] * ln_dist
        + alpha["alpha2"] * ln_bspeed
        + alpha["alpha3"] * ln_btime
        + alpha["alpha4"] * ln_bco2
        + alpha["alpha5"] * ln_bener
    )

    return math.exp(exponent)

def compute_hl_exports(row, alpha):
    """
    φ_{ij}^{hl} = exp(
      alpha0
    + alpha1 * ln(distance)
    + alpha6 * ln(hl_speed_mean)
    + alpha7 * ln(hl_time_mean + 1)
    + alpha8 * ln(hl_co2_mean + 1)
    + alpha9 * ln(hl_energy_mean + 1)
    )
    """
    distance   = float(row["distance"])
    hl_speed   = float(row["hl_speed_mean"])
    hl_time    = float(row["hl_time_mean"])
    hl_co2     = float(row["hl_co2_mean"])
    hl_energy  = float(row["hl_energy_mean"])

    ln_dist    = math.log(distance)
    ln_hspeed  = math.log(hl_speed)
    ln_htime   = math.log(hl_time + 1)
    ln_hco2    = math.log(hl_co2 + 1)
    ln_henergy = math.log(hl_energy + 1)

    exponent = (
        alpha["alpha0"]
        + alpha["alpha1"] * ln_dist
        + alpha["alpha6"] * ln_hspeed
        + alpha["alpha7"] * ln_htime
        + alpha["alpha8"] * ln_hco2
        + alpha["alpha9"] * ln_henergy
    )

    return math.exp(exponent)

def compute_percent_diff(baseline_val, hl_val):
    """
    % diff = ((HL - Baseline) / Baseline) * 100
    """
    if baseline_val == 0:
        return None
    return ((hl_val - baseline_val) / baseline_val) * 100

input_file  = "input_data.csv"
output_file = "output_data.csv"

rows_output = []

with open(input_file, mode='r', encoding='utf-8') as f_in:
    reader = csv.DictReader(f_in)
    
    for row in reader:
        scenario_id = row["scenario"]
        
        exports_bl = compute_baseline_exports(row, alpha)
        
        exports_hl = compute_hl_exports(row, alpha)
        
        diff_percent = compute_percent_diff(exports_bl, exports_hl)

        out_dict = {
            "scenario"   : scenario_id,
            "distance"   : row["distance"],
            "baselinespeed_mean"  : row["baseline_speed_mean"],
            "baselinetime_mean"   : row["baseline_time_mean"],
            "baselineco2_mean"    : row["baseline_co2_mean"],
            "baselineenergy_mean" : row["baseline_energy_mean"],
            "hlspeed_mean"        : row["hl_speed_mean"],
            "hltime_mean"         : row["hl_time_mean"],
            "hlco2_mean"          : row["hl_co2_mean"],
            "hlenergy_mean"       : row["hl_energy_mean"],
            "baselineexports"     : round(exports_bl, 3),
            "hlexports"           : round(exports_hl, 3),
            "diffpercent"         : round(diff_percent, 2) if diff_percent is not None else None
        }
        rows_output.append(out_dict)

with open(output_file, mode='w', newline='', encoding='utf-8') as f_out:
    fieldnames = [
        "scenario","distance",
        "baselinespeed_mean","baselinetime_mean","baselineco2_mean","baselineenergy_mean",
        "hlspeed_mean","hltime_mean","hlco2_mean","hlenergy_mean",
        "baselineexports","hlexports","diffpercent"
    ]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows_output:
        writer.writerow(row)

print(f"Export calculations completed.\nInput:  {input_file}\nOutput: {output_file}")
for r in rows_output:
    print(r)
