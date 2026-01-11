const fs = require('fs');
const path = require('path');

const baseDir = 'd:/documents/docs';

const structure = {
  "introduction": {
    position: 1,
    label: "Introduction",
    items: {
      "context-positioning.md": "Context & Positioning",
      "overview.md": "Overview",
      "why-veilfi-exists": {
        label: "Why Veilfi Exists",
        items: {
          "problem-space.md": "Problem Space",
          "solution-overview.md": "Solution Overview"
        }
      },
      "who-is-this-for": {
        label: "Who is this for?",
        items: {
          "borrowers.md": "Borrowers",
          "liquidity-providers.md": "Liquidity Providers",
          "integrators.md": "Integrators"
        }
      }
    }
  },
  "core-concepts": {
    position: 2,
    label: "Core Concepts",
    items: {
      "key-concepts-definitions": {
        label: "Key Concepts & Definitions",
        items: {
          "credit-position.md": "Credit Position",
          "collateral-efficiency.md": "Collateral Efficiency",
          "leverage-abstraction.md": "Leverage Abstraction",
          "risk-tranching.md": "Risk Tranching"
        }
      },
      "core-principles": {
        label: "Core Principles",
        items: {
          "capital-efficiency-first.md": "Capital Efficiency First",
          "risk-isolation.md": "Risk Isolation",
          "permissionless-credit.md": "Permissionless Credit",
          "modular-growth.md": "Modular Growth"
        }
      },
      "credit-model-overview": {
        label: "Credit Model Overview",
        items: {
          "how-borrowing-works.md": "How Borrowing Works in Veilfi",
          "how-risk-is-priced.md": "How Risk is Priced",
          "how-liquidation-differs.md": "How Liquidation Differs"
        }
      }
    }
  },
  "protocol-design": {
    position: 3,
    label: "Protocol Design",
    items: {
      "architecture-overview": {
        label: "Architecture Overview",
        items: {
          "core-protocol-layer.md": "Core Protocol Layer",
          "strategy-market-layer.md": "Strategy / Market Layer",
          "oracle-risk-layer.md": "Oracle & Risk Layer"
        }
      },
      "modular-components": {
        label: "Modular Components",
        items: {
          "vaults-markets.md": "Vaults / Markets",
          "risk-engine.md": "Risk Engine",
          "liquidation-engine.md": "Liquidation Engine",
          "interest-rate-model.md": "Interest Rate Model"
        }
      },
      "capital-flow-model": {
        label: "Capital Flow Model",
        items: {
          "supply-borrow-repay.md": "Supply → Borrow → Repay",
          "leverage-lifecycle.md": "Leverage Lifecycle",
          "liquidation-recovery-path.md": "Liquidation & Recovery Path"
        }
      }
    }
  },
  "core-flow": {
    position: 4,
    label: "Core Flow",
    items: {
      "lender-flow": {
        label: "Lender Flow",
        items: {
          "deposit-assets.md": "Deposit Assets",
          "earn-yield.md": "Earn Yield",
          "withdraw-liquidity.md": "Withdraw Liquidity"
        }
      },
      "borrower-flow": {
        label: "Borrower Flow",
        items: {
          "deposit-collateral.md": "Deposit Collateral",
          "open-credit-position.md": "Open Credit Position",
          "adjust-leverage.md": "Adjust Leverage",
          "repay-close-position.md": "Repay / Close Position"
        }
      },
      "liquidation-flow": {
        label: "Liquidation Flow",
        items: {
          "trigger-conditions.md": "Trigger Conditions",
          "execution.md": "Execution",
          "loss-allocation.md": "Loss Allocation"
        }
      }
    }
  },
  "key-features": {
    position: 5,
    label: "Key Features",
    items: {
      "modular-credit-markets.md": "Modular Credit Markets",
      "capital-efficient-borrowing.md": "Capital-Efficient Borrowing",
      "isolated-risk-vaults.md": "Isolated Risk Vaults",
      "flexible-liquidation-mechanism.md": "Flexible Liquidation Mechanism",
      "composable-credit-positions.md": "Composable Credit Positions"
    }
  },
  "technical-details": {
    position: 6,
    label: "Technical Details",
    items: {
      "smart-contract-architecture": {
        label: "Smart Contract Architecture",
        items: {
          "core-contracts.md": "Core Contracts",
          "vault-market-contracts.md": "Vault / Market Contracts",
          "risk-oracle-contracts.md": "Risk & Oracle Contracts"
        }
      },
      "permission-governance-model": {
        label: "Permission & Governance Model",
        items: {
          "admin-roles.md": "Admin Roles",
          "parameter-control.md": "Parameter Control",
          "emergency-actions.md": "Emergency Actions"
        }
      },
      "security-considerations": {
        label: "Security Considerations",
        items: {
          "risk-isolation.md": "Risk Isolation",
          "oracle-dependency.md": "Oracle Dependency",
          "known-attack-surfaces.md": "Known Attack Surfaces"
        }
      }
    }
  },
  "frontend-ux": {
    position: 7,
    label: "Frontend & UX",
    items: {
      "user-flows.md": "User Flows",
      "risk-visualization.md": "Risk Visualization",
      "position-management-ux.md": "Position Management UX"
    }
  },
  "integration-guide": {
    position: 8,
    label: "Integration Guide",
    items: {
      "read-only-integration.md": "Read-only Integration",
      "opening-positions-programmatically.md": "Opening Positions Programmatically",
      "risk-liquidation-monitoring.md": "Risk & Liquidation Monitoring"
    }
  },
  "conclusion": {
    position: 9,
    label: "Conclusion",
    items: {
      "design-philosophy.md": "Design Philosophy",
      "long-term-vision.md": "Long-term Vision"
    }
  },
  "support": {
    position: 10,
    label: "Support",
    items: {
      "documentation.md": "Documentation",
      "community.md": "Community",
      "security-contact.md": "Security Contact"
    }
  }
};

function createItems(parentPath, items) {
  let i = 0;
  for (const [key, value] of Object.entries(items)) {
    i++;
    const currentPath = path.join(parentPath, key);
    
    // Check if it's a directory (Category) or file
    if (typeof value === 'object' && value.items) {
      // It's a category
      if (!fs.existsSync(currentPath)) {
        fs.mkdirSync(currentPath, { recursive: true });
      }
      
      const categoryJson = {
        label: value.label || key,
        position: i,
        link: { type: 'generated-index' }
      };
      
      fs.writeFileSync(path.join(currentPath, '_category_.json'), JSON.stringify(categoryJson, null, 2));
      
      createItems(currentPath, value.items);
    } else {
      // It's a file (or just a title string if simpler map)
      let title = value;
      // Handle the case where value is just the title string
      if (typeof value === 'string') {
          title = value;
      }
      
      if (!fs.existsSync(currentPath)) {
        const content = `---
title: ${title}
sidebar_position: ${i}
---

# ${title}

Content coming soon...
`;
        fs.writeFileSync(currentPath, content);
      }
    }
  }
}

// Process top level
for (const [key, value] of Object.entries(structure)) {
  const currentPath = path.join(baseDir, key);
  if (!fs.existsSync(currentPath)) {
    fs.mkdirSync(currentPath, { recursive: true });
  }
  
  const categoryJson = {
    label: value.label || key,
    position: value.position,
    link: { type: 'generated-index' }
  };
  
  fs.writeFileSync(path.join(currentPath, '_category_.json'), JSON.stringify(categoryJson, null, 2));
  
  if (value.items) {
    createItems(currentPath, value.items);
  }
}

console.log("Docs generated successfully.");
