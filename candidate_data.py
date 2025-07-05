# Sample candidate data for testing the ranking system

CANDIDATES = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "skills": ["Python", "Machine Learning", "Data Science", "SQL", "TensorFlow", "Pandas", "NumPy"],
        "experience_years": 5,
        "education": "MS Computer Science",
        "previous_roles": ["Data Scientist", "ML Engineer"],
        "certifications": ["AWS Certified Machine Learning", "Google Cloud Professional Data Engineer"],
        "summary": "Experienced data scientist with 5 years of experience in machine learning and data analysis. Skilled in Python, TensorFlow, and cloud platforms."
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@email.com",
        "skills": ["JavaScript", "React", "Node.js", "MongoDB", "HTML", "CSS", "Git"],
        "experience_years": 3,
        "education": "BS Computer Science",
        "previous_roles": ["Frontend Developer", "Full Stack Developer"],
        "certifications": ["React Developer Certification"],
        "summary": "Frontend developer with 3 years of experience in React and modern web technologies. Strong background in user interface design and responsive development."
    },
    {
        "id": 3,
        "name": "Carol Davis",
        "email": "carol.davis@email.com",
        "skills": ["Java", "Spring Boot", "Microservices", "Docker", "Kubernetes", "AWS", "PostgreSQL"],
        "experience_years": 7,
        "education": "BS Software Engineering",
        "previous_roles": ["Backend Developer", "System Architect", "DevOps Engineer"],
        "certifications": ["AWS Solutions Architect", "Kubernetes Administrator"],
        "summary": "Senior backend developer with 7 years of experience in enterprise applications. Expert in Java, Spring Boot, and cloud infrastructure."
    },
    {
        "id": 4,
        "name": "David Wilson",
        "email": "david.wilson@email.com",
        "skills": ["Python", "Django", "FastAPI", "REST APIs", "PostgreSQL", "Redis", "Docker"],
        "experience_years": 4,
        "education": "MS Software Engineering",
        "previous_roles": ["Python Developer", "API Developer"],
        "certifications": ["Django Developer Certification"],
        "summary": "Python backend developer with 4 years of experience in web development and API design. Skilled in Django and FastAPI frameworks."
    },
    {
        "id": 5,
        "name": "Emma Brown",
        "email": "emma.brown@email.com",
        "skills": ["Data Analysis", "R", "Python", "Statistics", "Machine Learning", "Tableau", "Power BI"],
        "experience_years": 6,
        "education": "PhD Statistics",
        "previous_roles": ["Data Analyst", "Business Intelligence Analyst"],
        "certifications": ["Tableau Desktop Specialist", "Microsoft Power BI Certification"],
        "summary": "Data analyst with 6 years of experience in statistical analysis and business intelligence. Strong background in R, Python, and data visualization."
    },
    {
        "id": 6,
        "name": "Frank Miller",
        "email": "frank.miller@email.com",
        "skills": ["C++", "System Programming", "Linux", "Performance Optimization", "Embedded Systems"],
        "experience_years": 8,
        "education": "MS Computer Engineering",
        "previous_roles": ["Systems Engineer", "Embedded Software Developer"],
        "certifications": ["Linux Professional Institute Certification"],
        "summary": "Systems engineer with 8 years of experience in low-level programming and embedded systems. Expert in C++ and Linux system development."
    },
    {
        "id": 7,
        "name": "Grace Lee",
        "email": "grace.lee@email.com",
        "skills": ["UI/UX Design", "Figma", "Adobe Creative Suite", "Prototyping", "User Research", "JavaScript", "React"],
        "experience_years": 4,
        "education": "BFA Graphic Design",
        "previous_roles": ["UI Designer", "UX Designer", "Product Designer"],
        "certifications": ["Google UX Design Certificate"],
        "summary": "UI/UX designer with 4 years of experience in user-centered design and prototyping. Strong skills in design tools and frontend development."
    },
    {
        "id": 8,
        "name": "Henry Chen",
        "email": "henry.chen@email.com",
        "skills": ["DevOps", "CI/CD", "Jenkins", "GitLab", "Terraform", "Ansible", "Monitoring"],
        "experience_years": 5,
        "education": "BS Information Technology",
        "previous_roles": ["DevOps Engineer", "Site Reliability Engineer"],
        "certifications": ["Jenkins Certified Engineer", "HashiCorp Terraform Associate"],
        "summary": "DevOps engineer with 5 years of experience in automation and infrastructure management. Expert in CI/CD pipelines and infrastructure as code."
    }
]

SAMPLE_JOB_DESCRIPTIONS = [
    {
        "id": 1,
        "title": "Senior Data Scientist",
        "company": "TechCorp",
        "description": "We are looking for a Senior Data Scientist to join our AI team. The ideal candidate will have experience in machine learning, deep learning, and statistical analysis.",
        "required_skills": ["Python", "Machine Learning", "Statistics", "TensorFlow", "Data Analysis"],
        "preferred_skills": ["Deep Learning", "NLP", "Computer Vision", "AWS", "MLOps"],
        "min_experience": 4,
        "education_requirements": "MS in Computer Science, Statistics, or related field",
        "responsibilities": [
            "Develop machine learning models for business applications",
            "Analyze large datasets to extract insights",
            "Collaborate with engineering teams to deploy models",
            "Present findings to stakeholders"
        ]
    },
    {
        "id": 2,
        "title": "Frontend Developer",
        "company": "WebTech Solutions",
        "description": "Join our frontend team to build modern, responsive web applications. We need someone with strong React skills and eye for design.",
        "required_skills": ["JavaScript", "React", "HTML", "CSS", "Git"],
        "preferred_skills": ["TypeScript", "Next.js", "Tailwind CSS", "Testing"],
        "min_experience": 2,
        "education_requirements": "BS in Computer Science or equivalent experience",
        "responsibilities": [
            "Develop user interfaces using React",
            "Ensure responsive design across devices",
            "Collaborate with designers and backend developers",
            "Write clean, maintainable code"
        ]
    },
    {
        "id": 3,
        "title": "Backend Software Engineer",
        "company": "Enterprise Systems Inc",
        "description": "We're seeking a Backend Software Engineer to work on scalable enterprise applications. Experience with Java and microservices architecture is essential.",
        "required_skills": ["Java", "Spring Boot", "REST APIs", "Database Design", "Git"],
        "preferred_skills": ["Microservices", "Docker", "Kubernetes", "Cloud Platforms"],
        "min_experience": 5,
        "education_requirements": "BS in Software Engineering or Computer Science",
        "responsibilities": [
            "Design and develop backend services",
            "Implement microservices architecture",
            "Optimize application performance",
            "Mentor junior developers"
        ]
    },
    {
        "id": 4,
        "title": "Python Developer",
        "company": "StartupTech",
        "description": "Looking for a Python developer to work on web applications and APIs. Experience with Django or FastAPI is highly preferred.",
        "required_skills": ["Python", "Web Development", "REST APIs", "Database"],
        "preferred_skills": ["Django", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "min_experience": 3,
        "education_requirements": "BS in Computer Science or related field",
        "responsibilities": [
            "Develop web applications using Python frameworks",
            "Design and implement REST APIs",
            "Work with databases and caching systems",
            "Collaborate with frontend developers"
        ]
    },
    {
        "id": 5,
        "title": "DevOps Engineer",
        "company": "CloudFirst",
        "description": "Join our DevOps team to manage CI/CD pipelines and infrastructure automation. Experience with containerization and orchestration is required.",
        "required_skills": ["DevOps", "CI/CD", "Docker", "Kubernetes", "Linux"],
        "preferred_skills": ["Terraform", "Ansible", "Jenkins", "Monitoring", "Cloud Platforms"],
        "min_experience": 4,
        "education_requirements": "BS in Computer Science, IT, or related field",
        "responsibilities": [
            "Design and maintain CI/CD pipelines",
            "Manage containerized applications",
            "Implement infrastructure as code",
            "Monitor system performance and reliability"
        ]
    }
]
