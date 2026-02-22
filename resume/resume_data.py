"""
Resume templates and tips data for every major.
Each template includes sections tailored to the major's typical career paths.
"""

RESUME_TEMPLATES = {
    'business': {
        'label': 'Business & Management',
        'icon': '📊',
        'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=280&fit=crop',
        'focus': 'Leadership, analytics, and business impact',
        'sections': ['Summary', 'Education', 'Professional Experience', 'Leadership & Activities', 'Skills', 'Certifications'],
        'tips': [
            'Lead with quantifiable achievements (e.g. "Increased sales 18% in Q3").',
            'Highlight leadership roles, even from student orgs or group projects.',
            'Include relevant coursework like accounting, finance, or marketing.',
            'List tools: Excel, Salesforce, QuickBooks, Tableau, etc.',
            'Add certifications like Six Sigma, Google Analytics, or Bloomberg.',
        ],
        'sample_bullets': [
            'Managed a team of 5 to deliver a marketing campaign that reached 12,000+ students.',
            'Analyzed quarterly sales data using Excel and presented findings to senior leadership.',
            'Led recruitment and onboarding for a student consulting organization with 40 members.',
        ],
    },
    'computer_science': {
        'label': 'Computer Science & IT',
        'icon': '💻',
        'image': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=280&fit=crop',
        'focus': 'Technical skills, projects, and problem-solving',
        'sections': ['Summary', 'Education', 'Technical Skills', 'Projects', 'Experience', 'Certifications'],
        'tips': [
            'Put a Technical Skills section near the top with languages, frameworks, and tools.',
            'Include personal or class projects with links to GitHub repos.',
            'Use action verbs like "developed," "deployed," "optimized," "automated."',
            'Quantify impact: "Reduced load time by 40%" or "Processed 10K+ records daily."',
            'List certifications: AWS, CompTIA, Google Cloud, etc.',
        ],
        'sample_bullets': [
            'Built a full-stack web application using React and Django, deployed on AWS.',
            'Developed a Python script to automate data cleaning, saving 5 hours/week.',
            'Contributed to an open-source project with 500+ GitHub stars.',
        ],
    },
    'engineering': {
        'label': 'Engineering',
        'icon': '⚙️',
        'image': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=280&fit=crop',
        'focus': 'Technical expertise, design projects, and certifications',
        'sections': ['Summary', 'Education', 'Technical Skills', 'Engineering Projects', 'Experience', 'Certifications & Licenses'],
        'tips': [
            'Highlight design projects, senior capstone, and lab work.',
            'Include CAD tools, simulation software, and programming languages.',
            'Mention EIT/FE exam status or PE licensure progress.',
            'Quantify results: tolerances, cost savings, efficiency improvements.',
            'List relevant coursework: thermodynamics, circuits, structural analysis, etc.',
        ],
        'sample_bullets': [
            'Designed a bridge model in AutoCAD that reduced material costs by 15% while meeting load requirements.',
            'Programmed a PLC system to automate a production line, increasing throughput by 20%.',
            'Passed the Fundamentals of Engineering (FE) exam on first attempt.',
        ],
    },
    'health_sciences': {
        'label': 'Health Sciences & Nursing',
        'icon': '🏥',
        'image': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=400&h=280&fit=crop',
        'focus': 'Clinical experience, patient care, and certifications',
        'sections': ['Summary', 'Education', 'Clinical Experience', 'Certifications & Licenses', 'Skills', 'Volunteer Experience'],
        'tips': [
            'List clinical rotations with hours, settings, and patient populations.',
            'Include all licenses and certifications: RN, BLS, CPR, ACLS, etc.',
            'Highlight patient care hours and any specializations.',
            'Use HIPAA-compliant language—no patient identifiers.',
            "Mention EMR systems you've used: Epic, Cerner, Meditech.",
        ],
        'sample_bullets': [
            'Completed 400+ clinical hours across medical-surgical, pediatric, and ICU settings.',
            'Administered medications and monitored vitals for 6–8 patients per shift.',
            'Educated patients and families on post-discharge care plans.',
        ],
    },
    'humanities': {
        'label': 'Humanities',
        'icon': '📚',
        'image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=280&fit=crop',
        'focus': 'Writing, research, and critical thinking',
        'sections': ['Summary', 'Education', 'Research & Writing', 'Experience', 'Skills', 'Activities & Honors'],
        'tips': [
            'Emphasize research, writing, and analytical skills.',
            'Include published papers, thesis work, or conference presentations.',
            'Highlight transferable skills: communication, editing, critical thinking.',
            'List languages spoken and proficiency levels.',
            'Tailor your summary to the specific role—humanities skills apply broadly.',
        ],
        'sample_bullets': [
            'Researched and wrote a 40-page honors thesis on 19th-century American literature.',
            'Edited and proofread 50+ articles for the university literary magazine.',
            'Presented original research at the Midwest Undergraduate Humanities Conference.',
        ],
    },
    'social_sciences': {
        'label': 'Social Sciences',
        'icon': '🧠',
        'image': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400&h=280&fit=crop',
        'focus': 'Research methods, data analysis, and people skills',
        'sections': ['Summary', 'Education', 'Research Experience', 'Professional Experience', 'Skills', 'Publications & Presentations'],
        'tips': [
            'Highlight research methods: surveys, interviews, statistical analysis.',
            'Include tools: SPSS, R, Qualtrics, NVivo.',
            'Mention IRB experience and any published or presented research.',
            'Emphasize interpersonal skills and community engagement.',
            'Quantify research scope: sample sizes, datasets, populations served.',
        ],
        'sample_bullets': [
            'Conducted a mixed-methods study on student mental health with a sample of 200 participants.',
            'Analyzed survey data using SPSS and presented findings to faculty and peers.',
            'Co-authored a paper accepted at the National Social Science Association conference.',
        ],
    },
    'arts_design': {
        'label': 'Arts & Design',
        'icon': '🎨',
        'image': 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=280&fit=crop',
        'focus': 'Portfolio, creative tools, and client work',
        'sections': ['Summary', 'Education', 'Portfolio & Projects', 'Experience', 'Tools & Software', 'Exhibitions & Awards'],
        'tips': [
            'Link to your online portfolio (Behance, Dribbble, personal site).',
            'List tools: Adobe Creative Suite, Figma, Sketch, Procreate, etc.',
            'Include freelance and client work with measurable outcomes.',
            'Mention exhibitions, shows, or competitions.',
            'Keep the resume itself clean and well-designed—it\'s a design sample.',
        ],
        'sample_bullets': [
            'Designed branding package for a local nonprofit, increasing social media engagement by 35%.',
            'Created wireframes and high-fidelity prototypes in Figma for a mobile app with 10K+ users.',
            'Selected for juried exhibition at the university gallery; work displayed for 3 months.',
        ],
    },
    'education': {
        'label': 'Education',
        'icon': '🍎',
        'image': 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400&h=280&fit=crop',
        'focus': 'Teaching experience, certifications, and classroom skills',
        'sections': ['Summary', 'Education', 'Teaching Experience', 'Certifications & Licenses', 'Skills', 'Professional Development'],
        'tips': [
            'Include student teaching placements with grade levels and subjects.',
            'List teaching certifications and endorsements.',
            'Highlight differentiated instruction, assessment, and classroom management.',
            'Mention technology tools: Google Classroom, Smartboard, Canvas.',
            'Add professional development workshops and trainings.',
        ],
        'sample_bullets': [
            'Student taught 4th grade for 16 weeks, planning and delivering daily lessons for 25 students.',
            'Developed and implemented a reading intervention program that improved scores by 12%.',
            'Earned Praxis II certification in Elementary Education.',
        ],
    },
    'environmental': {
        'label': 'Environmental & Sustainability',
        'icon': '🌱',
        'image': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400&h=280&fit=crop',
        'focus': 'Fieldwork, data collection, and sustainability projects',
        'sections': ['Summary', 'Education', 'Field & Research Experience', 'Professional Experience', 'Technical Skills', 'Certifications'],
        'tips': [
            'Highlight fieldwork, lab work, and data collection methods.',
            'Include GIS, remote sensing, and statistical tools.',
            'Mention regulatory knowledge: EPA, NEPA, OSHA.',
            'Quantify environmental impact: acres surveyed, species counted, waste reduced.',
            'Add relevant certifications: LEED, hazardous waste, first aid.',
        ],
        'sample_bullets': [
            'Conducted water quality sampling across 12 sites over a 6-month field season.',
            'Used ArcGIS to map habitat corridors for a state conservation agency.',
            'Developed a campus sustainability plan that reduced waste by 20% in one year.',
        ],
    },
    'communications': {
        'label': 'Communications & Media',
        'icon': '📡',
        'image': 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=400&h=280&fit=crop',
        'focus': 'Content creation, campaigns, and media skills',
        'sections': ['Summary', 'Education', 'Media & Content Experience', 'Professional Experience', 'Skills & Tools', 'Portfolio'],
        'tips': [
            'Link to published work, clips, or your portfolio site.',
            'Highlight social media management with metrics (followers, engagement).',
            'Include tools: Adobe Premiere, Final Cut, Canva, WordPress, Hootsuite.',
            'Mention campaigns, press releases, or content strategies you led.',
            'Quantify reach: views, impressions, audience size.',
        ],
        'sample_bullets': [
            'Managed social media accounts with 8,000+ followers, growing engagement 25% in 6 months.',
            'Produced and edited 15 video segments for the campus news station.',
            'Wrote press releases and media kits for 3 university events.',
        ],
    },
    'law': {
        'label': 'Law & Criminal Justice',
        'icon': '⚖️',
        'image': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=280&fit=crop',
        'focus': 'Research, writing, and legal experience',
        'sections': ['Summary', 'Education', 'Legal Experience', 'Research & Writing', 'Skills', 'Activities & Honors'],
        'tips': [
            'Highlight legal research, writing, and case analysis.',
            'Include moot court, mock trial, or law review experience.',
            'Mention Westlaw, LexisNexis, and other legal databases.',
            'List relevant coursework: constitutional law, criminal procedure, etc.',
            'Add internships at law firms, courts, or public defender offices.',
        ],
        'sample_bullets': [
            'Researched case law and drafted legal memoranda for a family law practice.',
            'Competed in regional moot court competition, advancing to quarterfinals.',
            'Completed 200-hour internship at the county public defender\'s office.',
        ],
    },
    'agriculture': {
        'label': 'Agriculture & Natural Resources',
        'icon': '🌾',
        'image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400&h=280&fit=crop',
        'focus': 'Hands-on experience, land management, and agribusiness',
        'sections': ['Summary', 'Education', 'Field Experience', 'Professional Experience', 'Technical Skills', 'Certifications'],
        'tips': [
            'Highlight farm, ranch, or field experience with specific tasks.',
            'Include equipment and technology: GPS, soil testing, precision ag tools.',
            'Mention FFA, 4-H, or ag club leadership.',
            'Quantify results: yield improvements, acreage managed, cost savings.',
            'Add certifications: pesticide applicator, CDL, first aid.',
        ],
        'sample_bullets': [
            'Managed daily operations on a 500-acre grain farm including planting and harvest.',
            'Implemented precision agriculture techniques that improved yield by 8%.',
            'Served as FFA chapter president, organizing community service for 60 members.',
        ],
    },
    'hospitality': {
        'label': 'Hospitality & Tourism',
        'icon': '🏨',
        'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=280&fit=crop',
        'focus': 'Guest experience, operations, and service leadership',
        'sections': ['Summary', 'Education', 'Hospitality Experience', 'Leadership & Activities', 'Skills', 'Certifications'],
        'tips': [
            'Emphasize customer service, guest satisfaction, and operations.',
            'Include POS systems, reservation software, and event planning tools.',
            'Highlight teamwork and leadership in fast-paced environments.',
            'Quantify: covers served, events managed, satisfaction scores.',
            'Add certifications: ServSafe, TIPS, CPR.',
        ],
        'sample_bullets': [
            'Supervised front-of-house operations for a 200-seat restaurant during peak hours.',
            'Coordinated 10+ events per semester for the university hospitality club.',
            'Achieved 95% guest satisfaction rating based on post-stay surveys.',
        ],
    },
    'real_estate': {
        'label': 'Real Estate & Property',
        'icon': '🏠',
        'image': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=280&fit=crop',
        'focus': 'Sales, analysis, and property management',
        'sections': ['Summary', 'Education', 'Real Estate Experience', 'Professional Experience', 'Skills', 'Licenses & Certifications'],
        'tips': [
            'Highlight sales volume, properties managed, or deals closed.',
            'Include market analysis and financial modeling experience.',
            'List tools: MLS, Argus, CoStar, Excel.',
            'Mention licenses: real estate salesperson, broker, appraiser.',
            'Add client relationship and negotiation achievements.',
        ],
        'sample_bullets': [
            'Assisted in managing a portfolio of 50 residential rental units.',
            'Conducted comparative market analyses for 20+ residential properties.',
            'Earned real estate salesperson license and completed 3 transactions in first quarter.',
        ],
    },
    'sports_recreation': {
        'label': 'Sports & Recreation',
        'icon': '🏃',
        'image': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&h=280&fit=crop',
        'focus': 'Coaching, program management, and fitness',
        'sections': ['Summary', 'Education', 'Coaching & Recreation Experience', 'Professional Experience', 'Certifications', 'Skills'],
        'tips': [
            'Highlight coaching, training, or program coordination.',
            'Include certifications: NASM, ACE, CPR/AED, lifeguard.',
            'Quantify: athletes trained, programs managed, participation rates.',
            'Mention sport-specific skills and event management.',
            'Add leadership in athletics or recreation clubs.',
        ],
        'sample_bullets': [
            'Coached a youth soccer team of 18 players, leading them to a league championship.',
            'Designed and led group fitness programs for 30+ participants per session.',
            'Coordinated intramural sports program serving 500+ students per semester.',
        ],
    },
    'trades_construction': {
        'label': 'Skilled Trades & Construction',
        'icon': '🔧',
        'image': 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=400&h=280&fit=crop',
        'focus': 'Hands-on skills, safety, and project experience',
        'sections': ['Summary', 'Education & Training', 'Project Experience', 'Work Experience', 'Certifications & Licenses', 'Skills & Equipment'],
        'tips': [
            'Lead with certifications: OSHA 10/30, CDL, welding, electrical license.',
            'List specific tools, equipment, and machinery you can operate.',
            'Highlight safety record and training.',
            'Include project details: scope, timeline, budget, team size.',
            'Quantify: square footage, units built, projects completed.',
        ],
        'sample_bullets': [
            'Completed OSHA 30-hour construction safety certification.',
            'Assisted in framing and finishing 12 residential units over a 6-month project.',
            'Operated heavy equipment including excavators, skid steers, and forklifts.',
        ],
    },
}

# Sample cover letters by major — editable templates for the cover letters section
COVER_LETTER_TEMPLATES = {
    'business': {
        'label': 'Business & Management',
        'icon': '📊',
        'focus': 'Leadership, analytics, and business impact',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Hiring Manager<br>Company Name<br>123 Business Ave<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am writing to express my interest in the [Position Title] opportunity at [Company Name]. '
            'As a Business &amp; Management student at [Your University] with a focus on leadership and analytics, '
            'I am eager to contribute to your team and grow as a professional.</p>'
            '<p>Through my coursework in finance, marketing, and operations, I have developed strong analytical '
            'and problem-solving skills. In my role with [Student Organization/Internship], I managed a team of five '
            'and delivered a marketing campaign that reached 12,000+ students. I am confident that my ability to '
            'analyze data, communicate findings, and work collaboratively would add value to [Company Name].</p>'
            '<p>I would welcome the opportunity to discuss how my background aligns with your needs. Thank you for '
            'considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
    'computer_science': {
        'label': 'Computer Science & IT',
        'icon': '💻',
        'focus': 'Technical skills, projects, and problem-solving',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · github.com/yourname · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Hiring Manager<br>Company Name<br>456 Tech Blvd<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am excited to apply for the [Software Engineer/Developer] position at [Company Name]. '
            'As a Computer Science student at [Your University], I have built a strong foundation in full-stack '
            'development, algorithms, and system design, and I am eager to contribute to your engineering team.</p>'
            '<p>I recently developed a full-stack web application using React and Django, deployed on AWS, and '
            'contributed to an open-source project with 500+ GitHub stars. These experiences have strengthened my '
            'ability to write clean code, collaborate with others, and ship features iteratively. I am particularly '
            'drawn to [Company Name] because of [specific reason—product, mission, or tech stack].</p>'
            '<p>I would welcome the chance to discuss how my skills and passion for technology can benefit your team. '
            'Thank you for considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
    'engineering': {
        'label': 'Engineering',
        'icon': '⚙️',
        'focus': 'Technical expertise, design projects, and certifications',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Hiring Manager<br>Company Name<br>789 Innovation Dr<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am writing to apply for the [Mechanical/Civil/Electrical] Engineer position at [Company Name]. '
            'As an Engineering student at [Your University] with hands-on experience in design and analysis, '
            'I am eager to bring my technical skills and problem-solving mindset to your organization.</p>'
            '<p>My coursework in [relevant area] and my capstone project—designing a [type of system] that reduced '
            'material costs by 15% while meeting load requirements—have prepared me for real-world engineering '
            'challenges. I have also passed the Fundamentals of Engineering (FE) exam and am familiar with AutoCAD, '
            'MATLAB, and industry standards. I am excited about [Company Name]\'s work in [specific area].</p>'
            '<p>I would appreciate the opportunity to discuss how I can contribute to your team. Thank you for '
            'considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
    'health_sciences': {
        'label': 'Health Sciences & Nursing',
        'icon': '🏥',
        'focus': 'Clinical experience, patient care, and certifications',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Hiring Manager<br>[Hospital/Clinic Name]<br>100 Care Lane<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am writing to express my interest in the [RN/Nurse/Clinical] position at [Organization Name]. '
            'As a Health Sciences student at [Your University] with over 400 clinical hours across medical-surgical, '
            'pediatric, and ICU settings, I am eager to provide high-quality patient care as part of your team.</p>'
            '<p>My clinical experience has reinforced my commitment to patient safety, evidence-based practice, '
            'and compassionate care. I am BLS and CPR certified and proficient with EMR systems including Epic. '
            'I am particularly drawn to [Organization Name] because of your focus on [specific program or value].</p>'
            '<p>I would welcome the opportunity to discuss how my clinical skills and dedication can contribute to '
            'your mission. Thank you for considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
    'humanities': {
        'label': 'Humanities',
        'icon': '📚',
        'focus': 'Writing, research, and critical thinking',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Hiring Manager<br>Company Name<br>200 Research Way<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am writing to apply for the [Editor/Research/Communications] position at [Company Name]. '
            'As a Humanities student at [Your University] with a strong background in research, writing, and '
            'critical analysis, I am eager to bring my communication and analytical skills to your organization.</p>'
            '<p>My experience includes researching and writing a 40-page honors thesis, editing 50+ articles for '
            'the university literary magazine, and presenting original research at a regional conference. These '
            'experiences have sharpened my ability to synthesize complex ideas, write clearly for diverse audiences, '
            'and meet deadlines. I am excited about [Company Name]\'s work in [specific area].</p>'
            '<p>I would welcome the opportunity to discuss how my skills align with your needs. Thank you for '
            'considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
    'education': {
        'label': 'Education',
        'icon': '📖',
        'focus': 'Teaching, curriculum, and student development',
        'sample_letter': (
            '<p>Your Name<br>email@example.com · (555) 123-4567 · linkedin.com/in/yourname</p>'
            '<p>February 18, 2026</p>'
            '<p>Principal / Hiring Manager<br>[School/District Name]<br>300 Education Dr<br>City, State 12345</p>'
            '<p>Dear Hiring Manager,</p>'
            '<p>I am writing to express my interest in the [Teacher/Educator] position at [School Name]. '
            'As an Education student at [Your University] with fieldwork and student-teaching experience, '
            'I am eager to create an inclusive, engaging learning environment for your students.</p>'
            '<p>My coursework in curriculum development and differentiated instruction, combined with my '
            'student-teaching at [School], has prepared me to plan lessons, manage a classroom, and support '
            'diverse learners. I am committed to fostering a growth mindset and building positive relationships '
            'with students and families. I am drawn to [School Name] because of [specific program or mission].</p>'
            '<p>I would welcome the opportunity to discuss how I can contribute to your team. Thank you for '
            'considering my application.</p>'
            '<p>Sincerely,<br>Your Name</p>'
        ),
    },
}

RESUME_TIPS = [
    {
        'title': 'Keep it to one page',
        'desc': 'As a student or recent grad, one page is the standard. Recruiters spend 6–7 seconds on an initial scan—make every line count.',
    },
    {
        'title': 'Use a clean, readable format',
        'desc': 'Stick to a professional font (like the ones in our templates), clear section headers, and consistent spacing. Avoid graphics, photos, or columns that confuse ATS systems.',
    },
    {
        'title': 'Tailor it for every application',
        'desc': 'Adjust your summary, skills, and bullet points to match the job description. Use keywords from the posting—many companies use ATS to filter resumes.',
    },
    {
        'title': 'Lead with action verbs',
        'desc': 'Start each bullet point with a strong verb: managed, developed, analyzed, designed, led, coordinated, implemented, created.',
    },
    {
        'title': 'Quantify your achievements',
        'desc': 'Use numbers wherever possible: "Increased engagement by 25%," "Managed a budget of $5,000," "Trained 15 new hires." Numbers make your impact concrete.',
    },
    {
        'title': 'Include relevant coursework',
        'desc': 'If you lack work experience, list 4–6 relevant courses. This shows employers you have foundational knowledge for the role.',
    },
    {
        'title': 'Add a skills section',
        'desc': 'List technical and soft skills relevant to your target role. Include tools, software, languages, and certifications.',
    },
    {
        'title': 'Don\'t include references',
        'desc': '"References available upon request" is outdated. Use that space for something more valuable. Employers will ask for references when they need them.',
    },
    {
        'title': 'Proofread everything',
        'desc': 'Typos and grammar mistakes are the fastest way to get rejected. Read it out loud, use spell check, and have someone else review it.',
    },
    {
        'title': 'Use a professional email',
        'desc': 'firstname.lastname@email.com looks much better than coolgamer99@email.com. Create a professional email if you don\'t have one.',
    },
    {
        'title': 'Save and send as PDF',
        'desc': 'Always submit your resume as a PDF unless the employer asks for another format. PDFs preserve formatting across all devices.',
    },
    {
        'title': 'Include links when relevant',
        'desc': 'Add your LinkedIn, portfolio, GitHub, or personal website. Make sure the links work and the profiles are up to date.',
    },
]
