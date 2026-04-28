import numpy as np
import streamlit as st
from scipy import stats

st.title("Does p = 0.01 mean your result will replicate 99% of the time?")

st.write("""
In any one study, the effect is either real or it isn't.

But a very small p-value can happen in BOTH situations.

Let's see what that means for replication.
""")

# -------------------------
# Controls
# -------------------------
st.sidebar.header("Set the world")

truth = st.sidebar.radio(
    "Is there actually a real effect?",
    ["No (nothing is happening)", "Yes (there is a real effect)"]
)

real = True if "Yes" in truth else False

effect_size = st.sidebar.slider(
    "Effect size (if real)",
    0.0, 2.0, 0.5
)

n = st.sidebar.slider(
    "Sample size per group",
    5, 100, 20
)

# -------------------------
# Experiment function
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
if st.button("Run a study."):

    attempts = 0

    # Keep going until we get p < 0.01
    while True:
        p = run_experiment(real)
        attempts += 1
        if p < 0.01:
            break

    st.subheader("Your study")

    st.write(f"You got p = {p:.3f}")


    # 🔥 Make the key distinction explicit
    if real:
        st.markdown("""
### 🎯 Reality: there IS a real effect

You found a strong result because something is actually there.
""")
    else:
        st.markdown("""
### 🎲 Reality: there is NO real effect

👉 You got a very convincing result purely by chance.

If you run enough studies, this will eventually happen.
""")

    # -------------------------
    # Replication
    # -------------------------
    replications = 200
    successes = 0

    for _ in range(replications):
        p_rep = run_experiment(real)
        if p_rep < 0.05:
            successes += 1

    replication_rate = successes / replications

    st.markdown("---")
    st.subheader("Now repeat the same study many times")

    st.write(f"Out of {replications} new studies:")
    st.write(f"Significant results: {successes}")

    st.markdown(f"## 👉 Replication rate: {replication_rate:.2%}")

    # 🔥 Drive the lesson home
    if real:
        st.markdown("""
---

Even though the effect is real, not every study detects it.

👉 A small p-value does NOT mean the result will replicate 99% of the time.
""")
    else:
        st.markdown("""
---

You started with a *very convincing* result (p < 0.01).

But nothing is actually there.

👉 Replication fails because the original result was just luck.

This is what a false positive looks like.
""")

    st.markdown("""
---

**Bottom line:**

A small p-value tells you how unusual THIS dataset is.

It does NOT tell you:
- whether the result is real
- or how often it will replicate
""")
