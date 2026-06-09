# Component BDD Generation Decision Tree

Start

├── Does the component have any mandatory dependent APIs?
│
├── NO
│   └── Generate README.md only
│
└── YES
    │
    ├── Number of mandatory dependent APIs = 1 ?
    │
    ├── YES
    │   └── Follow TMFC005 pattern
    │
    └── NO
        │
        ├── Do dependent APIs require chained resource creation?
        │
        ├── YES
        │   └── Follow TMFC028 pattern
        │
        └── NO
            └── Follow TMFC007 pattern