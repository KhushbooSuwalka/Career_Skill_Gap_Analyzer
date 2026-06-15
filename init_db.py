import sqlite3
import os

DATABASE_FILE = 'careers.db'

def init_database():
    print("Initializing SQLite database...")
    
    # Remove existing database if it exists to start fresh
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Removed existing database '{DATABASE_FILE}'.")
        
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create careers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS careers (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Create roadmap_steps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roadmap_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_id TEXT NOT NULL,
            skill TEXT NOT NULL,
            phase TEXT NOT NULL,
            topic TEXT NOT NULL,
            sort_order INTEGER NOT NULL,
            FOREIGN KEY (career_id) REFERENCES careers (id)
        )
    ''')
    
    # Create skill_checks table for history archiving
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_id TEXT NOT NULL,
            career_title TEXT NOT NULL,
            readiness_score INTEGER NOT NULL,
            user_skills TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (career_id) REFERENCES careers (id)
        )
    ''')
    
    # Seed 16 careers data
    careers_data = [
        ("frontend-dev", "Frontend Developer", "Builds user interfaces and dynamic web applications."),
        ("data-scientist", "Data Scientist", "Analyzes datasets to build machine learning models and extract insights."),
        ("product-manager", "Product Manager", "Leads the design, execution, and release of new software products."),
        ("cybersecurity-analyst", "Cyber Security", "Monitors and secures computer networks, systems, and sensitive data."),
        ("backend-dev", "Backend Developer", "Designs and implements server-side logic, databases, APIs, and business logic."),
        ("fullstack-dev", "Full Stack Developer", "Handles both frontend visual interfaces and backend infrastructure/databases."),
        ("mobile-dev", "Mobile App Developer", "Builds native and cross-platform mobile apps for iOS and Android platforms."),
        ("devops-engineer", "DevOps Engineer", "Automates software delivery, deployment pipelines, infrastructure, and monitoring."),
        ("cloud-architect", "Cloud Architect", "Designs and manages scalable, secure cloud-based infrastructures and network layouts."),
        ("ui-ux-designer", "UI/UX Designer", "Creates engaging digital interfaces, visual wireframes, user flows, and custom style systems."),
        ("qa-engineer", "QA Automation Engineer", "Scripts automated testing workflows for web apps, services, and REST APIs."),
        ("machine-learning-eng", "AI / ML Engineer", "Designs algorithms, builds mathematical pipelines, and deploys predictive neural networks."),
        ("data-engineer", "Data Engineer", "Establishes data integration schedules, pipelines, warehouses, and stream processors."),
        ("game-developer", "Game Developer", "Programs game loops, coordinates 3D/2D physics, HUD layouts, and optimizations."),
        ("system-admin", "System Administrator", "Maintains corporate operating systems, virtualization, networking configurations, and backup sets."),
        ("blockchain-developer", "Blockchain Developer", "Writes secure smart contracts, implements crypto protocols, and builds decentralized apps (DApps).")
    ]
    
    cursor.executemany('INSERT INTO careers (id, title, description) VALUES (?, ?, ?)', careers_data)
    
    # Seed roadmap steps (6 steps per career, total 96 steps)
    roadmap_steps_data = [
        # Frontend Developer
        ("frontend-dev", "HTML", "Phase 1: Structure", "Master semantic markup, SEO basics, and modern web accessibility (A11y).", 1),
        ("frontend-dev", "CSS", "Phase 1: Styling", "Learn Flexbox, CSS Grid, custom variables, responsive design, and CSS transitions.", 2),
        ("frontend-dev", "JavaScript", "Phase 2: Interactivity", "Understand ES6+ features, asynchronous programming (APIs/Fetch), and DOM manipulation.", 3),
        ("frontend-dev", "Git", "Phase 2: Version Control", "Learn Git branching, merging, pull requests, and collaborative workflows on GitHub.", 4),
        ("frontend-dev", "React", "Phase 3: Frontend Framework", "Learn React component lifecycle, Hooks (useState, useEffect), state management, and routing.", 5),
        ("frontend-dev", "Webpack", "Phase 4: Tooling & Deploy", "Learn build tools (Vite/Webpack), package managers (npm), and hosting platforms (Netlify/Vercel).", 6),
        
        # Data Scientist
        ("data-scientist", "Python", "Phase 1: Programming Basics", "Learn core Python programming, data structures, loops, and custom functions.", 1),
        ("data-scientist", "SQL", "Phase 1: Database Querying", "Master relational database structures, complex Joins, Subqueries, and data grouping.", 2),
        ("data-scientist", "Pandas", "Phase 2: Data Manipulation", "Master Pandas and NumPy for cleaning, filtering, and preparing messy tabular datasets.", 3),
        ("data-scientist", "Data Visualization", "Phase 2: Storytelling", "Learn data communication using Matplotlib, Seaborn, or interactive BI dashboards.", 4),
        ("data-scientist", "Statistics", "Phase 3: Mathematical Core", "Learn hypothesis testing, regression analysis, probability models, and sampling distributions.", 5),
        ("data-scientist", "Machine Learning", "Phase 4: Predictive Models", "Build models using Scikit-Learn (regression, trees, clustering) and evaluate performance.", 6),

        # Product Manager
        ("product-manager", "Agile/Scrum", "Phase 1: Project Methodologies", "Understand sprints, daily standups, backlog grooming, and issue tracking in Jira.", 1),
        ("product-manager", "User Research", "Phase 1: Empathy & Needs", "Conduct user interviews, design feedback surveys, and build target user personas.", 2),
        ("product-manager", "Wireframing", "Phase 2: UX Prototyping", "Learn basic layout prototyping and visual mockup creation using Figma or Balsamiq.", 3),
        ("product-manager", "Data Analytics", "Phase 2: Product Metrics", "Understand key metrics (AARRR funnel, retention), funnel conversions, and tracking platforms.", 4),
        ("product-manager", "Roadmapping", "Phase 3: Prioritization", "Learn feature estimation, MoSCoW prioritization, and building timelines with product planning software.", 5),
        ("product-manager", "Product Strategy", "Phase 4: Market Validation", "Define product positioning, analyze competitors, write PRDs, and coordinate launch plans.", 6),

        # Cyber Security Analyst
        ("cybersecurity-analyst", "Networking", "Phase 1: Core Networking", "Learn TCP/IP layers, routing protocols, subnets, ports, DNS, and local host configurations.", 1),
        ("cybersecurity-analyst", "Linux", "Phase 1: Admin Basics", "Master command-line operations, shell scripts, user permissions, and directory trees.", 2),
        ("cybersecurity-analyst", "Wireshark", "Phase 2: Traffic Inspection", "Learn to capture and analyze network packets to identify security anomalies.", 3),
        ("cybersecurity-analyst", "Cryptography", "Phase 2: Safe Encryption", "Understand symmetric/asymmetric encryption, hashing algorithms, and SSL/TLS standards.", 4),
        ("cybersecurity-analyst", "Ethical Hacking", "Phase 3: Vulnerabilities", "Perform network vulnerability scanning with Nmap and understand OWASP Top 10 vulnerabilities.", 5),
        ("cybersecurity-analyst", "Security Auditing", "Phase 4: Governance & SIEM", "Learn standard security frameworks (NIST, ISO), log auditing, and SIEM monitoring dashboards.", 6),

        # Backend Developer
        ("backend-dev", "Python", "Phase 1: Language Basics", "Learn backend scripting with Python data structures, loops, and OOP concepts.", 1),
        ("backend-dev", "SQL", "Phase 1: Databases", "Learn relational databases, queries, indexes, and normalization.", 2),
        ("backend-dev", "Django", "Phase 2: Frameworks", "Master MVC architectural pattern, routing, Django ORM, and template rendering.", 3),
        ("backend-dev", "REST APIs", "Phase 2: Integration", "Build RESTful endpoints, handle HTTP requests/responses, and JSON payloads.", 4),
        ("backend-dev", "Docker", "Phase 3: Containerization", "Containerize your web backend, write Dockerfiles, and use docker-compose.", 5),
        ("backend-dev", "Redis", "Phase 4: Caching & Performance", "Implement Redis caching, rate limiting, and manage background tasks.", 6),

        # Full Stack Developer
        ("fullstack-dev", "JavaScript", "Phase 1: Programming Core", "Learn dynamic scripting, ES6 features, async-await, and DOM manipulation.", 1),
        ("fullstack-dev", "Node.js", "Phase 1: Backend Runtime", "Learn asynchronous runtime event loop, file system, and Express server creation.", 2),
        ("fullstack-dev", "React", "Phase 2: Frontend Library", "Build user interfaces with JSX, component state, custom hooks, and context.", 3),
        ("fullstack-dev", "MongoDB", "Phase 2: Database", "Learn NoSQL document databases, indexing, aggregation, and Mongoose schema design.", 4),
        ("fullstack-dev", "GraphQL", "Phase 3: Modern API", "Design schemas, write queries, mutations, and set up Apollo server.", 5),
        ("fullstack-dev", "CI/CD", "Phase 4: Deployment", "Set up automated test runners and deployment pipelines using GitHub Actions.", 6),

        # Mobile Developer
        ("mobile-dev", "Swift", "Phase 1: iOS Core", "Learn Apple Swift programming syntax, optionals, structs, and protocol-oriented programming.", 1),
        ("mobile-dev", "Flutter", "Phase 1: Cross-Platform", "Master Dart programming, stateless/stateful widgets, and cross-platform layouts.", 2),
        ("mobile-dev", "UIKit", "Phase 2: iOS UI Layout", "Build native screens, navigation, tables, constraint-based Auto Layouts, and storyboards.", 3),
        ("mobile-dev", "Firebase", "Phase 2: Mobile Backend", "Integrate authentication, Firestore databases, and analytics into mobile projects.", 4),
        ("mobile-dev", "CoreData", "Phase 3: Local Database", "Persist structured data locally on Apple devices using SQLite-backed CoreData.", 5),
        ("mobile-dev", "App Store Deploy", "Phase 4: Release", "Configure certificates, provisioning profiles, TestFlight builds, and submit to App Store.", 6),

        # DevOps Engineer
        ("devops-engineer", "Linux Admin", "Phase 1: Systems Management", "Learn shell scripting, cron jobs, file systems, permissions, and process management.", 1),
        ("devops-engineer", "Git", "Phase 1: Version Control", "Learn git branching strategy, merge conflict resolution, and SSH keys configuration.", 2),
        ("devops-engineer", "Docker", "Phase 2: Containerization", "Build lightweight container images, manage container ports, volumes, and network bridge configurations.", 3),
        ("devops-engineer", "Kubernetes", "Phase 2: Orchestration", "Manage multi-container deployments, service routing, configurations, and horizontal pod scaling.", 4),
        ("devops-engineer", "Terraform", "Phase 3: IaC (Infrastructure as Code)", "Define cloud infrastructure as code using declarative provider configs.", 5),
        ("devops-engineer", "Prometheus", "Phase 4: Observability", "Set up system metrics collectors, log aggregators, and target alerting rules.", 6),

        # Cloud Architect
        ("cloud-architect", "Networking", "Phase 1: Infrastructure Foundations", "Understand TCP/IP, subnets, routers, firewalls, DNS, and load balancing.", 1),
        ("cloud-architect", "AWS Core", "Phase 1: Cloud Provider", "Configure EC2 instances, IAM roles, S3 buckets, and basic security groups.", 2),
        ("cloud-architect", "VPC", "Phase 2: Network Isolation", "Design secure private subnets, NAT gateways, VPC peering, and routing tables.", 3),
        ("cloud-architect", "Serverless", "Phase 2: Code Execution", "Build lightweight serverless APIs using AWS Lambda, API Gateway, and DynamoDB.", 4),
        ("cloud-architect", "CloudFormation", "Phase 3: Automated IaC", "Write template files to provision complex cloud infrastructures automatically.", 5),
        ("cloud-architect", "Cloud Security", "Phase 4: Compliance Audits", "Implement cloud auditing, key management KMS, identity policies, and log trail tracking.", 6),

        # UI/UX Designer
        ("ui-ux-designer", "Figma", "Phase 1: Vector Tool", "Master vector components, layout grids, auto-layouts, and design system creation.", 1),
        ("ui-ux-designer", "Wireframing", "Phase 1: Conceptual Mockups", "Design low-fidelity user flow wireframes and interactive mockups.", 2),
        ("ui-ux-designer", "User Research", "Phase 2: Empathy", "Conduct user interviews, analyze feedback surveys, and construct target user personas.", 3),
        ("ui-ux-designer", "Typography", "Phase 2: UI Visuals", "Learn font pairings, contrast ratios, spacing grids, and style guide design.", 4),
        ("ui-ux-designer", "Prototyping", "Phase 3: Interactive Visuals", "Build high-fidelity click-through prototypes, micro-interactions, and smart transitions.", 5),
        ("ui-ux-designer", "Usability Testing", "Phase 4: Validation", "Observe users navigating prototypes, record friction points, and iterate design.", 6),

        # QA Automation Engineer
        ("qa-engineer", "Python", "Phase 1: Scripting Basics", "Learn basic syntax, loops, libraries, and scripting automated steps.", 1),
        ("qa-engineer", "Manual Testing", "Phase 1: Testing Methodologies", "Write test cases, perform exploratory testing, and file clear bug reports.", 2),
        ("qa-engineer", "Selenium", "Phase 2: Web Testing", "Locate web elements and automate browser test flows using WebDriver API.", 3),
        ("qa-engineer", "PyTest", "Phase 2: Test Frameworks", "Organize unit and integration tests, use test fixtures, and generate HTML reports.", 4),
        ("qa-engineer", "Postman", "Phase 3: API testing", "Automate REST endpoint assertions, pass variables, and run collections.", 5),
        ("qa-engineer", "CI/CD Integration", "Phase 4: Automation", "Trigger test runs automatically on code push inside GitHub Actions.", 6),

        # AI/ML Engineer
        ("machine-learning-eng", "Python", "Phase 1: Programming Core", "Learn OOP, data structures, list comprehensions, and basic scientific packages.", 1),
        ("machine-learning-eng", "Math/Linear Algebra", "Phase 1: Mathematical Foundations", "Master matrices, eigenvectors, calculus derivatives, and statistical distributions.", 2),
        ("machine-learning-eng", "NumPy/Pandas", "Phase 2: Data Cleaning", "Clean datasets, slice arrays, manipulate tables, and handle missing values.", 3),
        ("machine-learning-eng", "Scikit-Learn", "Phase 2: Core ML Models", "Build regression, decision trees, random forests, and evaluate precision/recall.", 4),
        ("machine-learning-eng", "PyTorch", "Phase 3: Deep Learning", "Build neural networks, configure layer dimensions, design custom loss, and optimize weights.", 5),
        ("machine-learning-eng", "MLOps", "Phase 4: Production Deployment", "Deploy ML models as REST APIs using Flask/FastAPI, containerize with Docker, and track models.", 6),

        # Data Engineer
        ("data-engineer", "Python", "Phase 1: ETL Programming", "Learn file handling, JSON parsing, API interactions, and scripting schedules.", 1),
        ("data-engineer", "SQL", "Phase 1: Core Querying", "Master window functions, CTEs, custom joins, and indexing structures.", 2),
        ("data-engineer", "Apache Spark", "Phase 2: Distributed Processing", "Perform distributed computations on large datasets using Spark DataFrames.", 3),
        ("data-engineer", "Airflow", "Phase 2: Pipeline Orchestration", "Write data pipeline workflows (DAGs) and schedule recurring ETL scripts.", 4),
        ("data-engineer", "Data Warehousing", "Phase 3: Warehouses", "Design schema models (Star/Snowflake), configure index clustering, and use Snowflake/Redshift.", 5),
        ("data-engineer", "Kafka", "Phase 4: Event Streaming", "Establish message topics, build producers, consumers, and handle stream events.", 6),

        # Game Developer
        ("game-developer", "C#", "Phase 1: Game Language", "Understand strict types, classes, interfaces, generic collections, and memory management.", 1),
        ("game-developer", "Unity", "Phase 1: Engine Basics", "Navigate the Unity editor, handle transforms, components, inputs, and scenes.", 2),
        ("game-developer", "Physics 2D/3D", "Phase 2: Mechanics", "Configure rigidbodies, colliders, raycasting, forces, and trigger events.", 3),
        ("game-developer", "Blender", "Phase 2: 3D Art Asset Creation", "Model basic 3D shapes, map textures, bake lighting, and export assets.", 4),
        ("game-developer", "UI Canvas", "Phase 3: Game HUD & Canvas", "Design main menus, layout HUD indicators, and coordinate inventory screens.", 5),
        ("game-developer", "Game Optimization", "Phase 4: Execution Profiling", "Optimize draw calls, handle sprite packing, run performance profilers, and build game executables.", 6),

        # System Administrator
        ("system-admin", "Linux Admin", "Phase 1: Server Setup", "Perform standard system setup, command-line operations, shell scripts, and package management.", 1),
        ("system-admin", "Active Directory", "Phase 1: Access Control", "Manage domain user accounts, set up groups, define OUs, and apply group policies.", 2),
        ("system-admin", "Networking", "Phase 2: Routing Protocols", "Configure DHCP scopes, static IP ranges, routing tables, and firewall rules.", 3),
        ("system-admin", "Virtualization", "Phase 2: Hypervisors", "Create, clone, and configure virtual machines using VMware ESXi or Hyper-V.", 4),
        ("system-admin", "PowerShell", "Phase 3: WinAdmin Automation", "Script administrative routines, audit Active Directory user logs, and patch servers.", 5),
        ("system-admin", "Backup & Recovery", "Phase 4: Continuity", "Maintain server image backups, establish disaster recovery sites, and monitor system health.", 6),

        # Blockchain Developer
        ("blockchain-developer", "Cryptography", "Phase 1: Public Key Ledger", "Master public/private key pairs, hash functions, and digital signatures.", 1),
        ("blockchain-developer", "JavaScript", "Phase 1: Asynchronous Core", "Learn async scripting, Node.js packages, and JSON-RPC integrations.", 2),
        ("blockchain-developer", "Solidity", "Phase 2: Ethereum Contracts", "Write Ethereum contracts, structure data, manage states, and declare modifier checks.", 3),
        ("blockchain-developer", "Web3.js / Ethers", "Phase 2: Client DApp Integration", "Connect browser wallets (MetaMask) to smart contracts and listen to blockchain events.", 4),
        ("blockchain-developer", "Hardhat / Truffle", "Phase 3: Compile Frameworks", "Set up local test nodes, compile contracts, write unit tests, and deploy scripts.", 5),
        ("blockchain-developer", "DeFi Security", "Phase 4: Vulnerability Audits", "Prevent reentrancy attacks, handle gas optimizations, and audit contracts.", 6)
    ]
    
    cursor.executemany('''
        INSERT INTO roadmap_steps (career_id, skill, phase, topic, sort_order)
        VALUES (?, ?, ?, ?, ?)
    ''', roadmap_steps_data)
    
    conn.commit()
    conn.close()
    print("Database successfully initialized and seeded with 16 careers!")

if __name__ == '__main__':
    init_database()
