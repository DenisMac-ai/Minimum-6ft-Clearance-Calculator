import streamlit as st

# Define line types and corresponding constants
LINE_TYPES = {
    "Tube Lines": {"base_clearance": 1588, "arl": 1289},
    "Sub-surface/Open Lines": {"base_clearance": 1842, "arl": 2099}
}

def calculate_clearance(line_type, or_versine, or_cant, ir_versine, ir_cant):
    try:
        # Ensure valid input values
        if or_versine <= 0 or ir_versine <= 0 or or_cant < 0 or ir_cant < 0:
            return "All Versine values must be positive, and Cant values must be non-negative."
        
        # Retrieve constants
        line_data = LINE_TYPES[line_type]
        base_clearance = line_data["base_clearance"]
        arl = line_data["arl"]
        
        # Calculate Radius for Outer Road (OR) and Inner Road (IR)
        r_or = 12500 / or_versine
        r_ir = 12500 / ir_versine
        
        # Calculate Centre Throw (CT) and End Throw (ET)
        ct = (14653 / r_or) if r_or >= 136 else (25110 / r_or - 77)
        et = (18011 / r_ir) if r_ir >= 136 else (21713 / r_ir)
        
        # Calculate Cant Effect (CE)
        cant_diff = abs(or_cant - ir_cant)
        ce = (cant_diff * arl) / 1505
        
        # Determine final clearance
        is_positive_ce = or_cant >= ir_cant
        final_clearance = base_clearance + round(ct) + round(et) + (round(ce) if is_positive_ce else -round(ce))
        
        return f"Minimum 6ft Clearance: {final_clearance} mm"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI Setup
st.title("Minimum 6ft Clearance Calculator")
st.markdown("Enter values to calculate the required clearance.")

# User Inputs
line_type = st.selectbox("Select Line Type", list(LINE_TYPES.keys()))
or_versine = st.number_input("Outer Road Versine (mm)", min_value=0.01, step=0.1)
or_cant = st.number_input("Outer Road Cant (mm)", min_value=0.0, step=0.1)
ir_versine = st.number_input("Inner Road Versine (mm)", min_value=0.01, step=0.1)
ir_cant = st.number_input("Inner Road Cant (mm)", min_value=0.0, step=0.1)

# Calculate & Display Result
if st.button("Calculate Clearance"):
    result = calculate_clearance(line_type, or_versine, or_cant, ir_versine, ir_cant)
    if "Error" in result:
        st.error(result)
    else:
        st.success(result)
