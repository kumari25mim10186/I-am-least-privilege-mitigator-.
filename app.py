import streamlit as st
import json
import os

from agent.iam_agent import IAMAgent
from simulator.cloud_environment import CloudSimulator


st.set_page_config(
    page_title="IAMGuard AI",
    page_icon="🛡️",
    layout="wide"
)


st.title("🛡️ IAMGuard AI")

st.subheader(
    "Autonomous Cloud IAM Least-Privilege Mitigator"
)

st.write(
    "An Agentic AI system that analyzes IAM permissions, "
    "detects excessive access, simulates policy changes, "
    "and verifies service functionality."
)


st.divider()


# Dashboard
col1, col2, col3, col4 = st.columns(4)

col1.metric("IAM Roles", "2")
col2.metric("Permissions", "12")
col3.metric("Access Logs", "8")
col4.metric("Environment", "SIMULATED")


st.divider()


if st.button(
    "🤖 Run Autonomous IAM Agent",
    type="primary"
):

    with st.spinner("Agent analyzing IAM environment..."):

        agent = IAMAgent()

        candidates = agent.analyze()

        proposed_policy = agent.generate_policy()

        simulator = CloudSimulator(
            agent.dependencies
        )

        simulation_results = simulator.simulate(
            proposed_policy
        )

    st.success("Agent execution completed!")

    # Candidate permissions
    st.header("🔍 Suspicious / Unused Permissions")

    if candidates:

        for candidate in candidates:

            dependency = agent.check_dependency(
                candidate["permission"]
            )

            if dependency:

                st.warning(
                    f"⚠️ {candidate['permission']} "
                    f"appears unused but is required by "
                    f"{dependency}"
                )

            else:

                st.error(
                    f"🔴 {candidate['permission']} "
                    f"→ Candidate for removal"
                )

    # Simulation
    st.header("🧪 Policy Simulation")

    for result in simulation_results:

        if result["status"] == "PASSED":

            st.success(
                f"✓ {result['service']} — PASSED"
            )

        else:

            st.error(
                f"✗ {result['service']} — FAILED"
            )

            st.write(
                "Missing permissions:",
                result["missing_permissions"]
            )

    # Final policy
    st.header("🔐 Proposed Least-Privilege Policy")

    st.json(proposed_policy)

    # Evidence
    st.header("📋 Evidence")

    st.json(agent.evidence)

    # Save files
    agent.save_policy(
        proposed_policy,
        "proposed_policy.json"
    )

    with open(
        "output/evidence.json",
        "w"
    ) as file:

        json.dump(
            agent.evidence,
            file,
            indent=4
        )

    st.success(
        "Policy and evidence saved to output/"
    )