# Component BDD Generation Decision Tree

Start

├── Resolve Component Specification
│
├── Any mandatory dependent APIs?
│
├── NO
│   └── Generate README.md only
│
└── YES
    │
    ├── Resolve OpenAPI specifications
    │
    ├── Fully resolve POST request schemas and all nested $ref definitions
    │
    ├── Can schemas be fully resolved?
    │
    ├── NO
    │   └── Report unresolved schema and request human review
    │
    └── YES
        │
        ├── Do dependent APIs require chained resource creation?
        │
        ├── YES
        │   └── Follow TMFC028 pattern
        │
        └── NO
            │
            ├── Number of mandatory dependent APIs = 1 ?
            │
            ├── YES
            │   └── Follow TMFC005 pattern
            │
            └── NO
                │
                └── Follow TMFC007 pattern
                    │
                    ├── Can valid base payloads be generated?
                    │
                    ├── NO
                    │   └── Report validation issue in README.md
                    │
                    └── YES
                        │
                        ├── Can dependency references be located in exposed API schema?
                        │
                        ├── NO
                        │   └── Report unresolved dependency mapping in README.md
                        │
                        └── YES
                            └── Generate BDD artefacts