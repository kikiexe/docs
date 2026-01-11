import os
import json

base_dir = "d:/documents/docs"

structure = {
    "introduction": {
        "position": 1,
        "label": "Introduction",
        "items": {
            "context-positioning.md": "Context & Positioning",
            "overview.md": "Overview",
            "why-veilfi-exists": {
                "label": "Why Veilfi Exists",
                "items": {
                    "problem-space.md": "Problem Space",
                    "solution-overview.md": "Solution Overview"
                }
            },
            "who-is-this-for": {
                "label": "Who is this for?",
                "items": {
                    "borrowers.md": "Borrowers",
                    "liquidity-providers.md": "Liquidity Providers",
                    "integrators.md": "Integrators"
                }
            }
        }
    },
    "core-concepts": {
        "position": 2,
        "label": "Core Concepts",
        "items": {
            "key-concepts-definitions": {
                "label": "Key Concepts & Definitions",
                "items": {
                    "credit-position.md": "Credit Position",
                    "collateral-efficiency.md": "Collateral Efficiency",
                    "leverage-abstraction.md": "Leverage Abstraction",
                    "risk-tranching.md": "Risk Tranching"
                }
            },
            "core-principles": {
                "label": "Core Principles",
                "items": {
                    "capital-efficiency-first.md": "Capital Efficiency First",
                    "risk-isolation.md": "Risk Isolation",
                    "permissionless-credit.md": "Permissionless Credit",
                    "modular-growth.md": "Modular Growth"
                }
            },
            "credit-model-overview": {
                "label": "Credit Model Overview",
                "items": {
                    "how-borrowing-works.md": "How Borrowing Works in Veilfi",
                    "how-risk-is-priced.md": "How Risk is Priced",
                    "how-liquidation-differs.md": "How Liquidation Differs"
                }
            }
        }
    },
    "protocol-design": {
        "position": 3,
        "label": "Protocol Design",
        "items": {
            "architecture-overview": {
                "label": "Architecture Overview",
                "items": {
                    "core-protocol-layer.md": "Core Protocol Layer",
                    "strategy-market-layer.md": "Strategy / Market Layer",
                    "oracle-risk-layer.md": "Oracle & Risk Layer"
                }
            },
            "modular-components": {
                "label": "Modular Components",
                "items": {
                    "vaults-markets.md": "Vaults / Markets",
                    "risk-engine.md": "Risk Engine",
                    "liquidation-engine.md": "Liquidation Engine",
                    "interest-rate-model.md": "Interest Rate Model"
                }
            },
            "capital-flow-model": {
                "label": "Capital Flow Model",
                "items": {
                    "supply-borrow-repay.md": "Supply → Borrow → Repay",
                    "leverage-lifecycle.md": "Leverage Lifecycle",
                    "liquidation-recovery-path.md": "Liquidation & Recovery Path"
                }
            }
        }
    },
    "core-flow": {
        "position": 4,
        "label": "Core Flow",
        "items": {
            "lender-flow": {
                "label": "Lender Flow",
                "items": {
                    "deposit-assets.md": "Deposit Assets",
                    "earn-yield.md": "Earn Yield",
                    "withdraw-liquidity.md": "Withdraw Liquidity"
                }
            },
            "borrower-flow": {
                "label": "Borrower Flow",
                "items": {
                    "deposit-collateral.md": "Deposit Collateral",
                    "open-credit-position.md": "Open Credit Position",
                    "adjust-leverage.md": "Adjust Leverage",
                    "repay-close-position.md": "Repay / Close Position"
                }
            },
            "liquidation-flow": {
                "label": "Liquidation Flow",
                "items": {
                    "trigger-conditions.md": "Trigger Conditions",
                    "execution.md": "Execution",
                    "loss-allocation.md": "Loss Allocation"
                }
            }
        }
    },
    "key-features": {
        "position": 5,
        "label": "Key Features",
        "items": {
            "modular-credit-markets.md": "Modular Credit Markets",
            "capital-efficient-borrowing.md": "Capital-Efficient Borrowing",
            "isolated-risk-vaults.md": "Isolated Risk Vaults",
            "flexible-liquidation-mechanism.md": "Flexible Liquidation Mechanism",
            "composable-credit-positions.md": "Composable Credit Positions"
        }
    },
    "technical-details": {
        "position": 6,
        "label": "Technical Details",
        "items": {
            "smart-contract-architecture": {
                "label": "Smart Contract Architecture",
                "items": {
                    "core-contracts.md": "Core Contracts",
                    "vault-market-contracts.md": "Vault / Market Contracts",
                    "risk-oracle-contracts.md": "Risk & Oracle Contracts"
                }
            },
            "permission-governance-model": {
                "label": "Permission & Governance Model",
                "items": {
                    "admin-roles.md": "Admin Roles",
                    "parameter-control.md": "Parameter Control",
                    "emergency-actions.md": "Emergency Actions"
                }
            },
            "security-considerations": {
                "label": "Security Considerations",
                "items": {
                    "risk-isolation.md": "Risk Isolation",
                    "oracle-dependency.md": "Oracle Dependency",
                    "known-attack-surfaces.md": "Known Attack Surfaces"
                }
            }
        }
    },
    "frontend-ux": {
        "position": 7,
        "label": "Frontend & UX",
        "items": {
            "user-flows.md": "User Flows",
            "risk-visualization.md": "Risk Visualization",
            "position-management-ux.md": "Position Management UX"
        }
    },
    "integration-guide": {
        "position": 8,
        "label": "Integration Guide",
        "items": {
            "read-only-integration.md": "Read-only Integration",
            "opening-positions-programmatically.md": "Opening Positions Programmatically",
            "risk-liquidation-monitoring.md": "Risk & Liquidation Monitoring"
        }
    },
    "conclusion": {
        "position": 9,
        "label": "Conclusion",
        "items": {
            "design-philosophy.md": "Design Philosophy",
            "long-term-vision.md": "Long-term Vision"
        }
    },
    "support": {
        "position": 10,
        "label": "Support",
        "items": {
            "documentation.md": "Documentation",
            "community.md": "Community",
            "security-contact.md": "Security Contact"
        }
    }
}

def create_items(parent_path, items, parent_position_base=0):
    for i, (key, value) in enumerate(items.items(), 1):
        path = os.path.join(parent_path, key)
        
        # If it's a dictionary, it's a folder/category
        if isinstance(value, dict):
            if not os.path.exists(path):
                os.makedirs(path)
            
            # Create _category_.json
            cat_label = value.get("label", key)
            cat_json = {
                "label": cat_label,
                "position": i, # Enforce order
                "link": {"type": "generated-index"}
            }
            with open(os.path.join(path, "_category_.json"), "w") as f:
                json.dump(cat_json, f, indent=2)
            
            # Recurse
            if "items" in value:
                create_items(path, value["items"])
        
        # If it's a string, it's a file title
        elif isinstance(value, str):
            # Check if file exists, if so skip (or overwrite if we want to reset)
            # user asked to "make it like this", so we will create if not exists
            if not os.path.exists(path):
                content = f"---\ntitle: {value}\nsidebar_position: {i}\n---\n\n# {value}\n\nContent coming soon...\n"
                with open(path, "w", encoding='utf-8') as f:
                    f.write(content)

# Process top level
for key, value in structure.items():
    path = os.path.join(base_dir, key)
    if not os.path.exists(path):
        os.makedirs(path)
    
    cat_label = value.get("label", key)
    cat_position = value.get("position", 1)
    
    cat_json = {
        "label": cat_label,
        "position": cat_position,
        "link": {"type": "generated-index"}
    }
    with open(os.path.join(path, "_category_.json"), "w") as f:
        json.dump(cat_json, f, indent=2)
    
    if "items" in value:
        create_items(path, value["items"])

print("Docs scaffolding complete.")
