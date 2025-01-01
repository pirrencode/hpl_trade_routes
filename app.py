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
    φ_{ij}^{BL} = exp(
      alpha0
    + alpha1 * ln(Distance)
    + alpha2 * ln(BaselineSpeed_Mean)
    + alpha3 * ln(BaselineTime_Mean + 1)
    + alpha4 * ln(BaselineCO2_Mean + 1)
    + alpha5 * ln(BaselineEnergy_Mean + 1)
    )
    """
    distance   = float(row["Distance"])
    base_speed = float(row["BaselineSpeed_Mean"])
    base_time  = float(row["BaselineTime_Mean"])
    base_co2   = float(row["BaselineCO2_Mean"])
    base_ener  = float(row["BaselineEnergy_Mean"])

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
    φ_{ij}^{HL} = exp(
      alpha0
    + alpha1 * ln(Distance)
    + alpha6 * ln(HLSpeed_Mean)
    + alpha7 * ln(HLTime_Mean + 1)
    + alpha8 * ln(HLCO2_Mean + 1)
    + alpha9 * ln(HLEnergy_Mean + 1)
    )
    """
    distance   = float(row["Distance"])
    hl_speed   = float(row["HLSpeed_Mean"])
    hl_time    = float(row["HLTime_Mean"])
    hl_co2     = float(row["HLCO2_Mean"])
    hl_energy  = float(row["HLEnergy_Mean"])

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
        scenario_id = row["Scenario"]
        
        exports_bl = compute_baseline_exports(row, alpha)
        
        exports_hl = compute_hl_exports(row, alpha)
        
        diff_percent = compute_percent_diff(exports_bl, exports_hl)

        out_dict = {
            "Scenario"   : scenario_id,
            "Distance"   : row["Distance"],
            "BaselineS"  : row["BaselineSpeed_Mean"],
            "BaselineT"  : row["BaselineTime_Mean"],
            "BaselineC"  : row["BaselineCO2_Mean"],
            "BaselineE"  : row["BaselineEnergy_Mean"],
            "HLSpeed_l"  : row["HLSpeed_Mean"],
            "HLTime_M"   : row["HLTime_Mean"],
            "HLCO2_M"    : row["HLCO2_Mean"],
            "HLEnergy_M" : row["HLEnergy_Mean"],
            "BaselineExports": round(exports_bl, 3),
            "HLExports"      : round(exports_hl, 3),
            "DiffPercent"    : round(diff_percent, 2) if diff_percent is not None else None
        }
        rows_output.append(out_dict)

with open(output_file, mode='w', newline='', encoding='utf-8') as f_out:
    fieldnames = [
        "Scenario","Distance",
        "BaselineSpeed_Mean","BaselineTime_Mean","BaselineCO2_Mean","BaselineEnergy_Mean",
        "HLSpeed_Mean","HLTime_Mean","HLCO2_Mean","HLEnergy_Mean",
        "BaselineExports","HLExports","DiffPercent"
    ]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows_output:
        writer.writerow(row)

print(f"Export calculations completed.\nInput:  {input_file}\nOutput: {output_file}")
for r in rows_output:
    print(r)
