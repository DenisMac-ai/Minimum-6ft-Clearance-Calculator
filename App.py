import streamlit as st
import math

# Function to calculate radius
def calculate_radius(versine):
    return 12500 / versine

# Function to calculate CT and ET based on radius and line type
def calculate_ct_et(radius, is_ct=True, line_type="Tube Lines"):
    if line_type == "Tube Lines":
        if is_ct:
            return 12651 / radius  # CT for Tube Lines
        else:
            return 16382 / radius  # ET for Tube Lines
    else:  # Sub-surface/Open Lines
        if radius >= 136:
            return 14653 / radius if is_ct else 18011 / radius  # CT and ET for R >= 136
        else:
            return (25110 / radius - 77) if is_ct else 21713 / radius  # CT and ET for R < 136

def calculate_clearance(line_type, or_versine, or_cant, ir_versine, ir_cant):
    try:
        # Validate inputs
        if or_versine <= 0 or ir_versine <= 0 or or_cant < 0 or ir_cant < 0:
            raise ValueError("All Versine values must be positive, and Cant values must be non-negative.")

        # Set constants based on line type
        if line_type == "Tube Lines":
            base_clearance = 1588
            arl = 1289
        else:  # Sub-surface/Open Lines
            base_clearance = 1842
            arl = 2099

        # Calculate radii
        r_or = calculate_radius(or_versine)
        r_ir = calculate_radius(ir_versine)

        # Round radii to nearest integer (down if < 0.5, up if >= 0.5)
        r_or_rounded = int(r_or + 0.5) if (r_or % 1) >= 0.5 else int(r_or)
        r_ir_rounded = int(r_ir + 0.5) if (r_ir % 1) >= 0.5 else int(r_ir)

        # Calculate CT and ET
        ct = calculate_ct_et(r_or_rounded, is_ct=True, line_type=line_type)
        et = calculate_ct_et(r_ir_rounded, is_ct=False, line_type=line_type)

        # Round CT and ET to nearest integer
        ct_rounded = int(ct + 0.5) if (ct % 1) >= 0.5 else int(ct)
        et_rounded = int(et + 0.5) if (et % 1) >= 0.5 else int(et)

        # Calculate Cant Effect (CE)
        cant_diff = abs(or_cant - ir_cant)
        ce = (cant_diff * arl) / 1505

        # Round CE to nearest integer
        ce_rounded = int(ce + 0.5) if (ce % 1) >= 0.5 else int(ce)

        # Determine if CE is added or subtracted based on cant difference
        is_positive_ce = or_cant >= ir_cant
        final_clearance = base_clearance + ct_rounded + et_rounded + (ce_rounded if is_positive_ce else -ce_rounded)

        # Return results including radii
        return final_clearance, r_or_rounded, r_ir_rounded

    except ValueError as e:
        st.error(str(e) if str(e) else "Please enter valid numerical values.")
        return None, None, None

# Streamlit app
st.title("Minimum 6ft Clearance Calculator")

# Line type selection
line_type = st.selectbox("Select Line Type", ["Tube Lines", "Sub-surface/Open Lines"])

# Input fields
col1, col2 = st.columns(2)

with col1:
    or_versine = st.number_input("Outer Road Versine (mm)", min_value=0.1, value=37.0)
    or_cant = st.number_input("Outer Road Cant (mm)", min_value=0.0, value=41.0)

with col2:
    ir_versine = st.number_input("Inner Road Versine (mm)", min_value=0.1, value=40.0)
    ir_cant = st.number_input("Inner Road Cant (mm)", min_value=0.0, value=38.0)

# Calculate button
if st.button("Calculate Clearance"):
    result, r_or, r_ir = calculate_clearance(line_type, or_versine, or_cant, ir_versine, ir_cant)
    if result is not None:
        st.success(f"Minimum 6ft Clearance: {result} mm")
        st.write(f"Outer Road Radius: {r_or} meters")
        st.write(f"Inner Road Radius: {r_ir} meters")

# Add some space and instructions
st.markdown("---")
st.write("Enter the Versine (mm) and Cant (mm) measurements for both Outer and Inner Roads, then select the line type and click 'Calculate Clearance' to get the result.")