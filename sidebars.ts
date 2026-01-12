import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Main sidebar for Veilfi documentation
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      collapsed: false,
      items: [
        'introduction/context-positioning',
        'introduction/overview',
        {
          type: 'category',
          label: 'Why Veilfi Exists',
          items: [
            'introduction/why-zk-yield-exists/problem-space',
            'introduction/why-zk-yield-exists/solution-overview',
          ],
        },
        {
          type: 'category',
          label: 'Who is this for?',
          items: [
            'introduction/who-is-this-for/retail-investors',
            'introduction/who-is-this-for/privacy-conscious-users',
            'introduction/who-is-this-for/integrators',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Core Concepts',
      items: [
        {
          type: 'category',
          label: 'Key Concepts & Definitions',
          items: [
            'core-concepts/key-concepts-definitions/yield-aggregation',
            'core-concepts/key-concepts-definitions/zero-knowledge-proofs',
            'core-concepts/key-concepts-definitions/privacy-preserving-defi',
            'core-concepts/key-concepts-definitions/kyc-compliance',
          ],
        },
        {
          type: 'category',
          label: 'Core Principles',
          items: [
            'core-concepts/core-principles/privacy-first',
            'core-concepts/core-principles/yield-optimization',
            'core-concepts/core-principles/compliance-friendly',
            'core-concepts/core-principles/modular-strategies',
          ],
        },
        {
          type: 'category',
          label: 'Yield Model Overview',
          items: [
            'core-concepts/yield-model-overview/how-aggregation-works',
            'core-concepts/yield-model-overview/how-yields-are-distributed',
            'core-concepts/yield-model-overview/strategy-allocation',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Protocol Design',
      items: [
        {
          type: 'category',
          label: 'Architecture Overview',
          items: [
            'protocol-design/architecture-overview/core-vault-layer',
            'protocol-design/architecture-overview/strategy-layer',
            'protocol-design/architecture-overview/zk-proof-layer',
          ],
        },
        {
          type: 'category',
          label: 'Modular Components',
          items: [
            'protocol-design/modular-components/strategy-vault',
            'protocol-design/modular-components/compliance-manager',
            'protocol-design/modular-components/zk-verifier',
            'protocol-design/modular-components/yield-distributor',
          ],
        },
        {
          type: 'category',
          label: 'Capital Flow Model',
          items: [
            'protocol-design/capital-flow-model/deposit-allocation',
            'protocol-design/capital-flow-model/yield-harvest-cycle',
            'protocol-design/capital-flow-model/withdrawal-process',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'ZK Circuits',
      items: [
        'zk-circuits/introduction',
        {
          type: 'category',
          label: 'Circuit Design',
          items: [
            'zk-circuits/circuit-design/kyc-verification',
            'zk-circuits/circuit-design/balance-proof',
          ],
        },
        {
          type: 'category',
          label: 'Implementation',
          items: [
            'zk-circuits/implementation/circom-setup',
            'zk-circuits/implementation/proof-generation',
            'zk-circuits/implementation/proof-verification',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'DeFi Strategies',
      items: [
        'defi-strategies/overview',
        {
          type: 'category',
          label: 'Supported Protocols',
          items: [
            'defi-strategies/supported-protocols/aave-strategy',
            'defi-strategies/supported-protocols/lido-strategy',
            'defi-strategies/supported-protocols/uniswap-strategy',
          ],
        },
        {
          type: 'category',
          label: 'Strategy Management',
          items: [
            'defi-strategies/strategy-management/allocation-algorithm',
            'defi-strategies/strategy-management/rebalancing',
            'defi-strategies/strategy-management/risk-assessment',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Core Flow',
      items: [
        {
          type: 'category',
          label: 'User Flow',
          items: [
            'core-flow/user-flow/wallet-connection',
            'core-flow/user-flow/kyc-verification',
            'core-flow/user-flow/deposit-funds',
            'core-flow/user-flow/view-yields',
            'core-flow/user-flow/withdraw-funds',
          ],
        },
        {
          type: 'category',
          label: 'Privacy Flow',
          items: [
            'core-flow/privacy-flow/private-deposits',
            'core-flow/privacy-flow/private-withdrawals',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Key Features',
      items: [
        'key-features/privacy-preserving-transactions',
        'key-features/multi-strategy-aggregation',
        'key-features/compliant-kyc-system',
        'key-features/automated-yield-optimization',
        'key-features/transparent-on-chain-verification',
      ],
    },
    {
      type: 'category',
      label: 'Technical Details',
      items: [
        {
          type: 'category',
          label: 'Smart Contract Architecture',
          items: [
            'smart-contracts/overview',
            'smart-contracts/core-contracts/strategy-vault-v2',
            'smart-contracts/core-contracts/compliance-manager-v2',
            'smart-contracts/strategy-contracts/mock-aave-strategy',
            'smart-contracts/strategy-contracts/mock-lido-strategy',
            'smart-contracts/strategy-contracts/mock-uniswap-strategy',
          ],
        },
        {
          type: 'category',
          label: 'Deployment & Verification',
          items: [
            'smart-contracts/deployment/mantle-sepolia',
            'smart-contracts/deployment/contract-addresses',
            'smart-contracts/deployment/verification',
          ],
        },
        {
          type: 'category',
          label: 'Security Considerations',
          items: [
            'security/overview',
            'security/zk-proof-security',
            'security/smart-contract-audit',
            'security/best-practices',
            'security/known-risks',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Frontend & UX',
      items: [
        'frontend-ux/tech-stack',
        {
          type: 'category',
          label: 'User Flows',
          items: [
            'frontend-ux/pages/landing-page',
            'frontend-ux/pages/login-kyc',
            'frontend-ux/pages/dashboard',
            'frontend-ux/pages/admin-panel',
          ],
        },
        {
          type: 'category',
          label: 'Components',
          items: [
            'frontend-ux/components/wallet-connector',
            'frontend-ux/components/yield-display',
            'frontend-ux/components/strategy-cards',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Integration Guide',
      items: [
        'integration-guide/overview',
        'integration-guide/read-contract-data',
        'integration-guide/interact-with-vault',
        'integration-guide/zk-proof-generation',
      ],
    },
    {
      type: 'category',
      label: 'Conclusion',
      items: [
        'conclusion/design-philosophy',
        'conclusion/long-term-vision',
      ],
    },
    {
      type: 'category',
      label: 'Support',
      items: [
        'support/documentation',
        'support/community',
        'support/security-contact',
      ],
    },
  ],
};

export default sidebars;