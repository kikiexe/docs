import os
import json

# Menggunakan relative path agar aman dijalankan di mana saja
# Asumsi: script ini ada di root project, sejajar dengan folder 'docs'
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

print(f"Targeting directory: {base_dir}")

structure = {
    "introduction": {
        "position": 1,
        "label": "Introduction",
        "items": {
            "context-positioning.md": "Context & Positioning",
            "overview.md": "Overview",
            "why-zk-yield-exists": {
                "label": "Why ZK-Yield Exists",
                "items": {
                    "problem-space.md": "Problem Space",
                    "solution-overview.md": "Solution Overview"
                }
            },
            "who-is-this-for": {
                "label": "Who is this for?",
                "items": {
                    "retail-investors.md": "Retail Investors",
                    "privacy-conscious-users.md": "Privacy-Conscious Users",
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
                    "yield-aggregation.md": "Yield Aggregation",
                    "zero-knowledge-proofs.md": "Zero-Knowledge Proofs",
                    "privacy-preserving-defi.md": "Privacy-Preserving DeFi",
                    "kyc-compliance.md": "KYC Compliance"
                }
            },
            "core-principles": {
                "label": "Core Principles",
                "items": {
                    "privacy-first.md": "Privacy First",
                    "yield-optimization.md": "Yield Optimization",
                    "compliance-friendly.md": "Compliance Friendly",
                    "modular-strategies.md": "Modular Strategies"
                }
            },
            "yield-model-overview": {
                "label": "Yield Model Overview",
                "items": {
                    "how-aggregation-works.md": "How Aggregation Works",
                    "how-yields-are-distributed.md": "How Yields are Distributed",
                    "strategy-allocation.md": "Strategy Allocation"
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
                    "core-vault-layer.md": "Core Vault Layer",
                    "strategy-layer.md": "Strategy Layer",
                    "zk-proof-layer.md": "ZK Proof Layer"
                }
            },
            "modular-components": {
                "label": "Modular Components",
                "items": {
                    "strategy-vault.md": "Strategy Vault",
                    "compliance-manager.md": "Compliance Manager",
                    "zk-verifier.md": "ZK Verifier",
                    "yield-distributor.md": "Yield Distributor"
                }
            },
            "capital-flow-model": {
                "label": "Capital Flow Model",
                "items": {
                    "deposit-allocation.md": "Deposit & Allocation",
                    "yield-harvest-cycle.md": "Yield Harvest Cycle",
                    "withdrawal-process.md": "Withdrawal Process"
                }
            }
        }
    },
    "zk-circuits": {
        "position": 4,
        "label": "ZK Circuits",
        "items": {
            "introduction.md": "Introduction to ZK Circuits",
            "circuit-design": {
                "label": "Circuit Design",
                "items": {
                    "kyc-verification.md": "KYC Verification Circuit",
                    "balance-proof.md": "Balance Proof Circuit"
                }
            },
            "implementation": {
                "label": "Implementation",
                "items": {
                    "circom-setup.md": "Circom Setup",
                    "proof-generation.md": "Proof Generation",
                    "proof-verification.md": "Proof Verification"
                }
            }
        }
    },
    "defi-strategies": {
        "position": 5,
        "label": "DeFi Strategies",
        "items": {
            "overview.md": "Strategies Overview",
            "supported-protocols": {
                "label": "Supported Protocols",
                "items": {
                    "aave-strategy.md": "Aave Strategy",
                    "lido-strategy.md": "Lido Strategy",
                    "uniswap-strategy.md": "Uniswap Strategy"
                }
            },
            "strategy-management": {
                "label": "Strategy Management",
                "items": {
                    "allocation-algorithm.md": "Allocation Algorithm",
                    "rebalancing.md": "Rebalancing",
                    "risk-assessment.md": "Risk Assessment"
                }
            }
        }
    },
    "core-flow": {
        "position": 6,
        "label": "Core Flow",
        "items": {
            "user-flow": {
                "label": "User Flow",
                "items": {
                    "wallet-connection.md": "Wallet Connection",
                    "kyc-verification.md": "KYC Verification",
                    "deposit-funds.md": "Deposit Funds",
                    "view-yields.md": "View Yields",
                    "withdraw-funds.md": "Withdraw Funds"
                }
            },
            "admin-flow": {
                "label": "Admin Flow",
                "items": {
                    "manage-strategies.md": "Manage Strategies",
                    "allocate-funds.md": "Allocate Funds",
                    "harvest-yields.md": "Harvest Yields",
                    "kyc-management.md": "KYC Management"
                }
            },
            "privacy-flow": {
                "label": "Privacy Flow",
                "items": {
                    "generate-zk-proofs.md": "Generate ZK Proofs",
                    "private-deposits.md": "Private Deposits",
                    "private-withdrawals.md": "Private Withdrawals"
                }
            }
        }
    },
    "key-features": {
        "position": 7,
        "label": "Key Features",
        "items": {
            "privacy-preserving-transactions.md": "Privacy-Preserving Transactions",
            "multi-strategy-aggregation.md": "Multi-Strategy Aggregation",
            "compliant-kyc-system.md": "Compliant KYC System",
            "automated-yield-optimization.md": "Automated Yield Optimization",
            "transparent-on-chain-verification.md": "Transparent On-Chain Verification"
        }
    },
    "smart-contracts": {
        "position": 8,
        "label": "Smart Contracts",
        "items": {
            "overview.md": "Smart Contracts Overview",
            "core-contracts": {
                "label": "Core Contracts",
                "items": {
                    "strategy-vault-v2.md": "StrategyVaultV2",
                    "compliance-manager-v2.md": "ComplianceManagerV2"
                }
            },
            "strategy-contracts": {
                "label": "Strategy Contracts",
                "items": {
                    "mock-aave-strategy.md": "Mock Aave Strategy",
                    "mock-lido-strategy.md": "Mock Lido Strategy",
                    "mock-uniswap-strategy.md": "Mock Uniswap Strategy"
                }
            },
            "deployment": {
                "label": "Deployment",
                "items": {
                    "mantle-sepolia.md": "Mantle Sepolia Testnet",
                    "contract-addresses.md": "Contract Addresses",
                    "verification.md": "Contract Verification"
                }
            }
        }
    },
    "frontend-ux": {
        "position": 9,
        "label": "Frontend & UX",
        "items": {
            "tech-stack.md": "Tech Stack",
            "pages": {
                "label": "Pages",
                "items": {
                    "landing-page.md": "Landing Page",
                    "login-kyc.md": "Login & KYC",
                    "dashboard.md": "Dashboard",
                    "admin-panel.md": "Admin Panel"
                }
            },
            "components": {
                "label": "Components",
                "items": {
                    "wallet-connector.md": "Wallet Connector",
                    "yield-display.md": "Yield Display",
                    "strategy-cards.md": "Strategy Cards"
                }
            }
        }
    },
    "developer-guide": {
        "position": 10,
        "label": "Developer Guide",
        "items": {
            "quick-start.md": "Quick Start",
            "setup": {
                "label": "Setup",
                "items": {
                    "prerequisites.md": "Prerequisites",
                    "installation.md": "Installation",
                    "environment-config.md": "Environment Configuration"
                }
            },
            "development": {
                "label": "Development",
                "items": {
                    "run-frontend.md": "Run Frontend",
                    "deploy-contracts.md": "Deploy Contracts",
                    "build-circuits.md": "Build ZK Circuits"
                }
            },
            "testing": {
                "label": "Testing",
                "items": {
                    "smart-contract-tests.md": "Smart Contract Tests",
                    "zk-circuit-tests.md": "ZK Circuit Tests",
                    "integration-tests.md": "Integration Tests"
                }
            }
        }
    },
    "integration-guide": {
        "position": 11,
        "label": "Integration Guide",
        "items": {
            "overview.md": "Integration Overview",
            "read-contract-data.md": "Read Contract Data",
            "interact-with-vault.md": "Interact with Vault",
            "zk-proof-generation.md": "ZK Proof Generation"
        }
    },
    "security": {
        "position": 12,
        "label": "Security",
        "items": {
            "overview.md": "Security Overview",
            "zk-proof-security.md": "ZK Proof Security",
            "smart-contract-audit.md": "Smart Contract Audit",
            "best-practices.md": "Best Practices",
            "known-risks.md": "Known Risks"
        }
    },
    "roadmap": {
        "position": 13,
        "label": "Roadmap",
        "items": {
            "current-status.md": "Current Status",
            "upcoming-features.md": "Upcoming Features",
            "long-term-vision.md": "Long-term Vision"
        }
    },
    "support": {
        "position": 14,
        "label": "Support",
        "items": {
            "faq.md": "FAQ",
            "troubleshooting.md": "Troubleshooting",
            "community.md": "Community",
            "contributing.md": "Contributing"
        }
    }
}

def create_items(parent_path, items):
    for i, (key, value) in enumerate(items.items(), 1):
        path = os.path.join(parent_path, key)
        
        # If dictionary -> create folder & category json
        if isinstance(value, dict):
            if not os.path.exists(path):
                print(f"Creating directory: {path}")
                os.makedirs(path)
            
            cat_label = value.get("label", key)
            cat_json = {
                "label": cat_label,
                "position": i, 
                "link": {"type": "generated-index"}
            }
            # Always update category json to ensure labels are correct
            with open(os.path.join(path, "_category_.json"), "w") as f:
                json.dump(cat_json, f, indent=2)
            
            if "items" in value:
                create_items(path, value["items"])
        
        # If string -> create markdown file
        elif isinstance(value, str):
            if not os.path.exists(path):
                print(f"Creating file: {path}")
                content = f"---\ntitle: {value}\nsidebar_position: {i}\n---\n\n# {value}\n\nContent coming soon...\n"
                with open(path, "w", encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"Exists (skipping): {path}")

# Process top level
if not os.path.exists(base_dir):
    print(f"Error: Docs directory not found at {base_dir}")
else:
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

    print("\n[SUCCESS] Docs scaffolding complete. Missing files created.")