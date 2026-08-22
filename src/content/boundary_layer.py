"""Instructor-defined concept map and five-question boundary-layer diagnostic."""

COURSE = {
    "name": "Advanced Fluid Mechanics",
    "module": "Boundary-Layer Theory",
    "objectives": [
        "Explain the physical meaning of the no-slip condition.",
        "Use thin-boundary-layer scaling to identify dominant terms.",
        "Interpret pressure-gradient effects on near-wall momentum.",
        "Distinguish a separation criterion from a sufficient observation.",
        "Connect governing equations, assumptions, and physical behavior.",
    ],
}

CONCEPTS = {
    "no_slip": {
        "label": "No-slip condition",
        "prerequisites": ["continuum assumption"],
    },
    "thin_layer_scaling": {
        "label": "Thin-boundary-layer scaling",
        "prerequisites": ["order-of-magnitude analysis", "Navier-Stokes terms"],
    },
    "pressure_gradient": {
        "label": "Pressure-gradient interpretation",
        "prerequisites": ["momentum balance"],
    },
    "separation": {
        "label": "Boundary-layer separation",
        "prerequisites": ["wall shear stress", "pressure gradient"],
    },
    "physical_interpretation": {
        "label": "Equation-to-physics interpretation",
        "prerequisites": ["dimensional reasoning"],
    },
}

QUESTIONS = [
    {
        "id": "q1",
        "kind": "mcq",
        "concept": "no_slip",
        "prompt": "At a stationary solid wall, the classical no-slip condition implies:",
        "options": [
            "Only the wall-normal fluid velocity is zero",
            "The fluid velocity at the wall equals the wall velocity",
            "The wall shear stress must be zero",
            "The pressure gradient must vanish at the wall",
        ],
        "answer": "The fluid velocity at the wall equals the wall velocity",
        "explanation": "No-slip constrains fluid velocity relative to the wall; it does not by itself set wall shear or pressure gradient to zero.",
    },
    {
        "id": "q2",
        "kind": "mcq",
        "concept": "thin_layer_scaling",
        "prompt": "For a thin boundary layer with streamwise scale L and thickness δ ≪ L, which velocity gradient is typically larger?",
        "options": [
            "∂u/∂x",
            "∂u/∂y",
            "They are necessarily equal",
            "Neither can be estimated by scaling",
        ],
        "answer": "∂u/∂y",
        "explanation": "The same velocity change occurs over the much shorter wall-normal length scale δ, making the wall-normal gradient larger in order of magnitude.",
    },
    {
        "id": "q3",
        "kind": "mcq",
        "concept": "separation",
        "prompt": "Does observing zero wall shear stress at one location, by itself, prove a separated flow region exists downstream?",
        "options": ["Yes", "No"],
        "answer": "No",
        "explanation": "Zero wall shear is associated with incipient separation, but interpreting separation requires the local flow context and behavior around that point.",
    },
    {
        "id": "q4",
        "kind": "text",
        "concept": "thin_layer_scaling",
        "prompt": "In 2–4 sentences, explain why the wall-normal viscous term becomes dominant in the classical thin-boundary-layer approximation.",
        "rubric": [
            "Recognizes δ ≪ L",
            "Compares wall-normal and streamwise derivatives by order of magnitude",
            "Connects the scaling result to the dominant viscous term",
        ],
    },
    {
        "id": "q5",
        "kind": "text",
        "concept": "pressure_gradient",
        "prompt": "In 2–4 sentences, explain how an adverse pressure gradient can contribute to boundary-layer separation.",
        "rubric": [
            "Pressure increases in the streamwise direction",
            "Near-wall fluid has relatively low momentum",
            "Adverse gradient decelerates near-wall flow / can drive reversal",
        ],
    },
]

GAP_TAXONOMY = {
    "missing_prerequisite": "Missing prerequisite",
    "conceptual_misunderstanding": "Conceptual misunderstanding",
    "mathematical_error": "Mathematical error",
    "physical_interpretation_gap": "Physical interpretation gap",
    "assumption_recognition_gap": "Assumption-recognition gap",
    "boundary_condition_error": "Boundary-condition error",
    "computational_error": "Computational error",
    "uncertain": "Uncertain / ambiguous",
}
