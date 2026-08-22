"""Pipe-flow / pressure-loss laboratory task model."""

LAB_NAME = "Pipe Flow / Pressure-Loss Laboratory"

LAB_TASKS = [
    {
        "id": "inspection",
        "task": "Equipment inspection",
        "skill": "Identify components, check setup, confirm readiness",
        "safety": "low",
        "prerequisites": [],
        "minutes": 8,
    },
    {
        "id": "operation",
        "task": "Pump and valve operation",
        "skill": "Operate the system safely and reach target conditions",
        "safety": "medium",
        "prerequisites": ["inspection"],
        "minutes": 12,
    },
    {
        "id": "flow_measurement",
        "task": "Flow-rate measurement",
        "skill": "Acquire and record flow conditions",
        "safety": "low",
        "prerequisites": ["operation"],
        "minutes": 12,
    },
    {
        "id": "pressure_measurement",
        "task": "Pressure measurement",
        "skill": "Zero instruments and obtain repeated measurements",
        "safety": "low",
        "prerequisites": ["operation"],
        "minutes": 12,
    },
    {
        "id": "reynolds",
        "task": "Reynolds-number calculation",
        "skill": "Connect measurements to flow-regime interpretation",
        "safety": "low",
        "prerequisites": ["flow_measurement"],
        "minutes": 10,
    },
    {
        "id": "uncertainty",
        "task": "Uncertainty analysis",
        "skill": "Identify variability and systematic sources",
        "safety": "low",
        "prerequisites": ["flow_measurement", "pressure_measurement"],
        "minutes": 15,
    },
    {
        "id": "troubleshooting",
        "task": "Troubleshooting",
        "skill": "Diagnose an unexpected reading or unstable condition",
        "safety": "medium",
        "prerequisites": ["inspection", "operation"],
        "minutes": 12,
    },
    {
        "id": "interpretation",
        "task": "Results interpretation",
        "skill": "Connect data to theory and model assumptions",
        "safety": "low",
        "prerequisites": ["reynolds", "uncertainty"],
        "minutes": 15,
    },
]
