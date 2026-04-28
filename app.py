import numpy as np
import streamlit as st
from scipy import stats

st.title("Does p = 0.01 mean your result will replicate 99% of the time?")

st.write("""
You often hear: "If p = 0.01, this result is very reliable."

But does that mean it will replicate 99% of the time?

Let's test that.
""")

# -------------------------
# Controls
# -------------------------
st.sidebar.header("Set the world")

effect_size = st.sidebar.slider(
    "Effect size (if real)",
    0.0, 2.0, 0.5
)

n = st.sidebar.slider(
    "Sample size per group",
    5, 100, 20
)

real = st.sidebar.radio(
    "Is there actually a real effect?",
    ["Yes", "No"]
)

real = True if real == "Yes" else False

# -------------------------
# Function
# -------------------------
def run_experiment(real):
    if real:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(effect_size, 1, n)
    else:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(0, 1, n)

    _, p = stats.ttest_ind(group1, group2)
    return p

# -------------------------
# Run demo
# -------------------------
if st.button("Find a strong result (p < 0.01)"):

    # Step 1: force a strong result
    attempts = 0
    while True:
        p = run_experiment(real)
        attempts += 1
        if p < 0.01:
            break

    st.subheader("Your study")

    st.write(f"You got p = {p:.3f}")

    if real:
        st.write("🎭 Hidden truth: There IS a real effect.")
    else:
        st.write("🎭 Hidden truth: There is NO real effect.")

    # Step 2: replicate
    replications = 200
    successes = 0

    for _ in range(replications):
        p_rep = run_experiment(real)
        if p_rep < 0.05:
            successes += 1

    st.markdown("---")
    st.subheader("Now repeat the same study many times")

    st.write(f"Out of {replications} new studies:")
    st.write(f"Significant results: {successes}")

    replication_rate = successes / replications

    st.markdown(f"## 👉 Replication rate: {replication_rate:.2%}")

    st.markdown("""
---

You got a very small p-value.

But that does NOT mean the result will replicate 99% of the time.

The p-value describes how unusual THIS dataset is—not how often future studies succeed.
""")
