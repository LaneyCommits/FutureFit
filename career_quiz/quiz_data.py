"""
Career quiz: major selection, interests, personality & teamwork (research-backed),
and career suggestions filtered by degree/major.
"""
# Categories used for scoring (interests + personality)
CAREER_CATEGORIES = [
    ('analytical', 'Analytical & Data-Driven', 'Data analysis, finance, accounting, strategy'),
    ('creative', 'Creative & Design', 'Design, writing, arts, marketing, media'),
    ('helping', 'Helping & People-Focused', 'Healthcare, teaching, counseling, social work'),
    ('leading', 'Leading & Influencing', 'Management, sales, entrepreneurship, law'),
    ('organizing', 'Organizing & Detail-Oriented', 'Operations, project management, administration'),
    ('technical', 'Technical & Building', 'Engineering, software, IT, construction'),
    ('outdoor', 'Hands-On & Outdoor', 'Agriculture, trades, environmental, sports'),
    ('research', 'Research & Discovery', 'Science, academia, R&D, journalism'),
]

# Majors/degree areas — careers are mapped to these for filtering
# Format: (key, label, short_description, search_keywords for search bar)
MAJORS = [
    ('business', 'Business & Management', 'Accounting, finance, marketing, management, HR', 'business management accounting finance marketing administration'),
    ('computer_science', 'Computer Science & IT', 'Software, data, cybersecurity, information systems', 'computer science IT tech software data cybersecurity information systems'),
    ('engineering', 'Engineering', 'Mechanical, civil, electrical, industrial, general engineering', 'engineering mechanical civil electrical industrial'),
    ('health_sciences', 'Health Sciences & Nursing', 'Nursing, pre-med, public health, allied health', 'health sciences nursing medical pre-med public health allied health'),
    ('humanities', 'Humanities', 'English, history, philosophy, languages, liberal arts', 'humanities english history philosophy languages liberal arts'),
    ('social_sciences', 'Social Sciences', 'Psychology, sociology, political science, economics', 'social sciences psychology sociology political science economics'),
    ('arts_design', 'Arts & Design', 'Graphic design, fine arts, media arts, UX design', 'arts design graphic fine arts media UX'),
    ('education', 'Education', 'Teaching, curriculum, educational leadership', 'education teaching curriculum'),
    ('environmental', 'Environmental & Sustainability', 'Environmental science, sustainability, conservation', 'environmental sustainability conservation science'),
    ('communications', 'Communications & Media', 'Journalism, PR, advertising, media production', 'communications media journalism PR advertising'),
    ('law', 'Law & Criminal Justice', 'Law, criminal justice, legal studies', 'law legal criminal justice'),
    ('agriculture', 'Agriculture & Natural Resources', 'Agriculture, forestry, natural resources', 'agriculture forestry natural resources'),
    ('hospitality', 'Hospitality & Tourism', 'Hotel, restaurant, tourism, event operations', 'hospitality tourism hotel restaurant events'),
    ('real_estate', 'Real Estate & Property', 'Real estate, property management, appraisal', 'real estate property appraisal'),
    ('sports_recreation', 'Sports & Recreation', 'Kinesiology, sports management, recreation', 'sports recreation kinesiology athletics'),
    ('trades_construction', 'Skilled Trades & Construction', 'Construction, trades, vocational, technical', 'trades construction vocational skilled trades'),
    ('cosmetology', 'Cosmetology & Beauty', 'Hair, nails, skincare, barbering, makeup', 'cosmetology beauty hair nails skincare barber esthetics'),
    ('allied_health', 'Allied Health & Clinical Support', 'Medical assistant, dental assisting, sonography, surgical tech', 'allied health medical assistant dental sonography radiologic phlebotomy'),
    ('culinary', 'Culinary & Baking', 'Culinary arts, baking, pastry, food service', 'culinary baking pastry chef cooking'),
    ('aviation_transportation', 'Aviation & Transportation', 'Aviation maintenance, truck driving, diesel, logistics', 'aviation transportation diesel truck driving'),
    ('fire_emergency', 'Fire & Emergency Services', 'Fire science, EMT, paramedic, emergency management', 'fire emergency EMT paramedic'),
]

# Each career: title, description, category (for scoring match), list of major keys
CAREERS_BY_MAJOR = [
    # Business
    ('Data Analyst', 'Interpret data to help organizations make decisions.', 'analytical', ['business', 'computer_science']),
    ('Financial Analyst', 'Analyze financial data and trends.', 'analytical', ['business']),
    ('Accountant', 'Manage and report financial information.', 'analytical', ['business']),
    ('Management Consultant', 'Advise organizations on strategy and operations.', 'analytical', ['business']),
    ('Marketing Specialist', 'Develop and run campaigns to reach audiences.', 'creative', ['business', 'communications']),
    ('Human Resources Specialist', 'Support employees and workplace culture.', 'helping', ['business', 'social_sciences']),
    ('Project Manager', 'Lead projects and teams to deliver results.', 'leading', ['business', 'engineering', 'computer_science']),
    ('Sales Representative', 'Connect products and services with customers.', 'leading', ['business']),
    ('Operations Manager', 'Keep day-to-day processes running smoothly.', 'organizing', ['business', 'engineering']),
    ('Supply Chain / Logistics', 'Manage the flow of goods and information.', 'organizing', ['business']),
    # Computer Science & IT
    ('Software Developer', 'Build applications and systems.', 'technical', ['computer_science', 'engineering']),
    ('IT Support / Systems Admin', 'Maintain technology and help users.', 'technical', ['computer_science']),
    ('Cybersecurity Analyst', 'Protect systems and data from threats.', 'technical', ['computer_science']),
    ('UX Designer', 'Design user experiences for apps and websites.', 'creative', ['computer_science', 'arts_design']),
    ('Data Scientist', 'Use data and models to solve business and research problems.', 'analytical', ['computer_science', 'business']),
    # Engineering
    ('Mechanical Engineer', 'Design and improve mechanical systems.', 'technical', ['engineering']),
    ('Civil Engineer', 'Plan and oversee infrastructure projects.', 'technical', ['engineering']),
    ('Industrial Engineer', 'Optimize processes and systems.', 'organizing', ['engineering', 'business']),
    # Health & Helping
    ('Nurse', 'Provide patient care and support in healthcare.', 'helping', ['health_sciences']),
    ('Healthcare Administrator', 'Manage healthcare facilities and operations.', 'organizing', ['health_sciences', 'business']),
    ('Counselor / Therapist', 'Help people with mental and emotional well-being.', 'helping', ['health_sciences', 'social_sciences', 'education']),
    ('Social Worker', 'Support individuals and families through challenges.', 'helping', ['social_sciences', 'health_sciences']),
    ('Teacher / Educator', 'Teach and support student learning.', 'helping', ['education']),
    ('University Professor', 'Teach and do research in academia.', 'research', ['education', 'humanities', 'social_sciences', 'engineering', 'computer_science']),
    # Creative & Communications
    ('Graphic Designer', 'Create visual content for brands and media.', 'creative', ['arts_design', 'communications']),
    ('Content Writer / Copywriter', 'Write for marketing, web, or publications.', 'creative', ['communications', 'humanities', 'arts_design']),
    ('Video Producer', 'Plan and produce video content.', 'creative', ['communications', 'arts_design']),
    ('Journalist / Reporter', 'Investigate and report on stories.', 'research', ['communications', 'humanities']),
    # Research & Policy
    ('Research Scientist', 'Conduct experiments and studies.', 'research', ['health_sciences', 'engineering', 'environmental', 'social_sciences']),
    ('Market Research Analyst', 'Study markets and consumer behavior.', 'analytical', ['business', 'social_sciences']),
    ('Policy Analyst', 'Research and advise on policy.', 'research', ['social_sciences', 'law']),
    ('Actuary', 'Assess risk using mathematics and statistics.', 'analytical', ['business']),
    # Law & Leadership
    ('Lawyer', 'Advise and represent clients in legal matters.', 'leading', ['law']),
    ('Paralegal', 'Support lawyers with research and documentation.', 'organizing', ['law']),
    ('Entrepreneur', 'Start and run your own business.', 'leading', ['business']),
    # Environmental & Outdoor
    ('Environmental Scientist', 'Study and protect the environment.', 'research', ['environmental', 'health_sciences']),
    ('Sustainability Consultant', 'Help organizations operate more sustainably.', 'analytical', ['environmental', 'business']),
    ('Park Ranger / Conservation', 'Manage and protect natural areas.', 'outdoor', ['environmental', 'agriculture']),
    ('Landscape Architect', 'Design outdoor spaces.', 'creative', ['environmental', 'arts_design']),
    ('Agriculture / Agribusiness', 'Grow food, manage land, or support farming.', 'outdoor', ['agriculture']),
    # Other
    ('Event Planner', 'Organize and run events.', 'organizing', ['business', 'communications']),
    ('Executive Assistant', 'Support leaders and manage schedules and tasks.', 'organizing', ['business']),
    ('Compliance Officer', 'Ensure rules and policies are followed.', 'organizing', ['business', 'law']),
    # Spotterful / Finance & Analytics
    ('Compensation Analyst', 'Evaluate and design pay and benefits packages.', 'analytical', ['business']),
    ('Cost Analyst', 'Analyze costs to improve efficiency and profitability.', 'analytical', ['business', 'engineering']),
    ('Real Estate Analyst', 'Analyze property markets and real estate investments.', 'analytical', ['business', 'real_estate']),
    ('Auditor', 'Review financial records and internal controls for accuracy.', 'analytical', ['business']),
    ('Recruiter', 'Source, screen, and hire candidates for organizations.', 'helping', ['business', 'humanities']),
    # Hospitality & Service
    ('Front of House Manager', 'Oversee customer-facing operations in restaurants, hotels, or venues.', 'leading', ['hospitality', 'business']),
    ('Hotel Manager', 'Manage hotel operations, staff, and guest experience.', 'organizing', ['hospitality', 'business']),
    ('Restaurant Manager', 'Run daily restaurant operations and team.', 'organizing', ['hospitality']),
    ('Tour Guide / Travel Coordinator', 'Lead tours or coordinate travel experiences.', 'helping', ['hospitality', 'communications']),
    # Warehouse & Logistics (Spotterful + standard)
    ('Warehouse Lead Hand', 'Oversee warehouse operations and workflow.', 'organizing', ['business', 'trades_construction']),
    ('Inventory Manager', 'Manage stock levels and inventory systems.', 'organizing', ['business']),
    ('Procurement Specialist', 'Source and purchase goods and services.', 'organizing', ['business']),
    # Real Estate
    ('Real Estate Agent / Broker', 'Help clients buy, sell, or rent properties.', 'leading', ['real_estate', 'business']),
    ('Property Manager', 'Manage day-to-day operations of rental properties.', 'organizing', ['real_estate', 'business']),
    ('Appraiser', 'Assess value of property or assets.', 'analytical', ['real_estate', 'business']),
    # Sports & Recreation
    ('Sports Manager / Athletic Director', 'Manage sports programs, facilities, or teams.', 'leading', ['sports_recreation', 'business']),
    ('Fitness Manager / Personal Trainer', 'Lead fitness programs and train clients.', 'helping', ['sports_recreation', 'health_sciences']),
    ('Recreation Coordinator', 'Plan and run recreation programs and activities.', 'helping', ['sports_recreation', 'education']),
    # Skilled Trades & Construction
    ('Construction Manager', 'Plan and oversee construction projects.', 'leading', ['trades_construction', 'engineering']),
    ('Electrical Engineer', 'Design and maintain electrical systems.', 'technical', ['engineering']),
    ('Quality Assurance Analyst', 'Test products and processes for quality.', 'organizing', ['engineering', 'computer_science']),
    ('Technical Writer', 'Write manuals, docs, and technical content.', 'creative', ['computer_science', 'communications', 'engineering']),
    # Cosmetology & Beauty
    ('Cosmetologist / Hairstylist', 'Provide hair, nail, and skincare services to clients.', 'creative', ['cosmetology']),
    ('Esthetician / Skincare Specialist', 'Offer facials, skincare treatments, and beauty services.', 'helping', ['cosmetology']),
    ('Barber', 'Cut and style hair, often specializing in men\'s grooming.', 'creative', ['cosmetology']),
    # Allied Health & Clinical Support
    ('Medical Assistant', 'Support clinicians with patient care and administrative tasks.', 'helping', ['allied_health', 'health_sciences']),
    ('Dental Hygienist', 'Clean teeth, take X-rays, and educate patients on oral health.', 'helping', ['allied_health', 'health_sciences']),
    ('Surgical Technologist', 'Prepare operating rooms and assist during surgery.', 'technical', ['allied_health', 'health_sciences']),
    ('Sonographer / Ultrasound Tech', 'Operate imaging equipment to capture diagnostic images.', 'technical', ['allied_health', 'health_sciences']),
    # Culinary & Baking
    ('Chef / Cook', 'Prepare and cook food in restaurants, hotels, or catering.', 'creative', ['culinary', 'hospitality']),
    ('Pastry Chef / Baker', 'Create baked goods, desserts, and pastries.', 'creative', ['culinary']),
    # Aviation & Transportation
    ('Aircraft Mechanic', 'Maintain and repair aircraft systems and structures.', 'technical', ['aviation_transportation', 'trades_construction']),
    ('Commercial Truck Driver', 'Transport goods long-distance by truck.', 'organizing', ['aviation_transportation']),
    ('Diesel Technician', 'Repair and maintain diesel engines in trucks and equipment.', 'technical', ['aviation_transportation', 'trades_construction']),
    # Fire & Emergency Services
    ('Firefighter', 'Respond to fires, emergencies, and rescue operations.', 'helping', ['fire_emergency']),
    ('EMT / Paramedic', 'Provide emergency medical care in the field.', 'helping', ['fire_emergency', 'health_sciences']),
]

# Extended "Learn more" copy for each career (shown in dropdown on results)
CAREER_LEARN_MORE = {
    'Data Analyst': 'Data analysts collect, clean, and analyze data to help organizations make decisions. You might build dashboards, run reports, or find trends. Strong Excel and SQL skills are common; many roles also use Python or R. Entry-level titles include Business Analyst or Reporting Analyst.',
    'Financial Analyst': 'Financial analysts evaluate investments, budgets, and financial performance. You could work in corporate finance, banking, or investment firms. The role often involves modeling, forecasting, and presenting to stakeholders. A CFA or MBA can help with advancement.',
    'Accountant': 'Accountants prepare and review financial records, ensure compliance with tax and reporting rules, and advise on efficiency. You can work in public accounting (audit/tax), industry, or government. CPA licensure is required for many senior and public accounting roles.',
    'Management Consultant': 'Consultants help organizations solve problems and improve performance. You might work on strategy, operations, or technology. The work is project-based and often involves research, interviews, and presenting recommendations. Travel and long hours are common; exit opportunities are strong.',
    'Marketing Specialist': 'Marketing specialists develop and run campaigns across digital, social, email, or traditional channels. You might focus on content, analytics, or brand. Roles often require creativity plus comfort with data and tools like Google Analytics or social platforms.',
    'Human Resources Specialist': 'HR specialists support recruiting, benefits, training, and employee relations. You might screen candidates, run onboarding, or handle policy questions. Strong communication and discretion are important. Many grow into HR business partner or specialist roles (e.g., compensation, L&D).',
    'Project Manager': 'Project managers plan, track, and deliver projects on time and on budget. You coordinate people and tasks, manage risks, and report to stakeholders. Certifications like PMP or CAPM are common. Used in tech, construction, healthcare, and many other industries.',
    'Sales Representative': 'Sales reps connect products or services with customers through outreach, demos, and relationship building. Roles range from inside sales (calls/emails) to field sales. Compensation often includes base plus commission. Strong communication and resilience are key.',
    'Operations Manager': 'Operations managers keep day-to-day processes running smoothly. You might oversee supply chain, production, or service delivery. The role focuses on efficiency, quality, and team coordination. Common in manufacturing, logistics, and retail.',
    'Supply Chain / Logistics': 'Supply chain and logistics professionals manage the flow of goods from suppliers to customers. You might handle procurement, inventory, or transportation. Roles can be analytical (planning) or hands-on (warehouse, distribution).',
    'Software Developer': 'Software developers design, build, and maintain applications and systems. You might work on web, mobile, backend, or full-stack. Coding skills in languages like Python, JavaScript, or Java are core; problem-solving and collaboration are equally important. Many roles are remote-friendly.',
    'IT Support / Systems Admin': 'IT support and sysadmins keep technology running: troubleshooting issues, managing servers and networks, and helping users. You might work at a help desk, in infrastructure, or in security. Certifications (e.g., CompTIA, Microsoft) can help with hiring.',
    'Cybersecurity Analyst': 'Cybersecurity analysts protect systems and data from threats. You might monitor for incidents, run vulnerability assessments, or implement controls. The field is in high demand; roles exist in every industry. Certifications like Security+ or CISSP are common.',
    'UX Designer': 'UX designers focus on how users experience products—researching needs, creating wireframes and prototypes, and testing with users. You work closely with developers and product managers. A portfolio is essential; many have design or psychology backgrounds.',
    'Data Scientist': 'Data scientists use statistics, programming, and domain knowledge to extract insights and build models from data. You might work on forecasting, recommendation systems, or A/B tests. Python/R and SQL are standard; ML and cloud tools are increasingly common.',
    'Mechanical Engineer': 'Mechanical engineers design and analyze mechanical systems—from machines and vehicles to HVAC and manufacturing equipment. You might work in R&D, production, or consulting. A PE license can be required for certain roles.',
    'Civil Engineer': 'Civil engineers plan and oversee infrastructure projects: roads, bridges, water systems, and buildings. You might work in design, construction, or government. Licensure (EIT then PE) is typical for advancement.',
    'Industrial Engineer': 'Industrial engineers optimize processes and systems for efficiency and quality. You might focus on production, supply chain, or ergonomics. The work blends analysis with hands-on improvement and is common in manufacturing and logistics.',
    'Nurse': 'Nurses provide direct patient care, educate families, and coordinate with doctors and other staff. You can work in hospitals, clinics, schools, or community settings. RN licensure is required; BSN is increasingly preferred. Specializations include ICU, pediatrics, and public health.',
    'Healthcare Administrator': 'Healthcare administrators manage operations, finances, and strategy in hospitals, clinics, or health systems. You might oversee a department or an entire facility. An MHA or MBA is common for leadership roles.',
    'Counselor / Therapist': 'Counselors and therapists help individuals and groups with mental health, behavior, and life challenges. You might work in schools, clinics, or private practice. Licensure (e.g., LPC, LCSW) is required; a master’s in counseling or social work is typical.',
    'Social Worker': 'Social workers support individuals and families through difficult situations—child welfare, housing, health, or crisis intervention. You might work for government, nonprofits, or healthcare. An MSW and state licensure are standard for clinical roles.',
    'Teacher / Educator': 'Teachers plan lessons, instruct students, and assess progress in K–12 or adult education. You might specialize by subject or grade level. State certification is required. Strong communication and patience are essential.',
    'University Professor': 'Professors teach courses and often conduct research in their field. You might work at a community college, four-year university, or research institution. A PhD is typical for tenure-track roles; master’s degrees can suffice for teaching-focused positions.',
    'Graphic Designer': 'Graphic designers create visual content for brands, marketing, and media. You might work on logos, layouts, or digital assets. Proficiency in tools like Adobe Creative Suite and a strong portfolio are key. Roles exist in agencies, in-house teams, and freelance.',
    'Content Writer / Copywriter': 'Content writers and copywriters produce text for websites, ads, emails, and other channels. You might focus on SEO, brand voice, or conversion. Strong writing and often some marketing or SEO knowledge are expected.',
    'Video Producer': 'Video producers plan and produce video content—from concept and scripting to shooting and editing. You might work in marketing, news, or entertainment. Skills in editing software and storytelling are central.',
    'Journalist / Reporter': 'Journalists research and report on news and stories for print, broadcast, or digital outlets. You might specialize in a beat (e.g., politics, science). Strong writing, ethics, and often multimedia skills are required.',
    'Research Scientist': 'Research scientists design and run experiments, analyze data, and publish findings. You might work in academia, industry, or government. A PhD is common; postdocs often lead to faculty or industry R&D roles.',
    'Market Research Analyst': 'Market research analysts study consumers and markets through surveys, data, and trends. You help companies understand demand and competition. Quantitative and qualitative skills are both useful.',
    'Policy Analyst': 'Policy analysts research and advise on public policy. You might work for government, think tanks, or advocacy groups. Strong research and writing are key; economics or law backgrounds are common.',
    'Actuary': 'Actuaries use math and statistics to assess risk in insurance, finance, and pensions. You need strong analytical skills and often pursue professional exams (e.g., SOA or CAS) for credentialing.',
    'Lawyer': 'Lawyers advise and represent clients in legal matters. You might specialize in litigation, corporate, criminal, or other areas. A JD and bar passage are required. Long hours are common in many settings.',
    'Paralegal': 'Paralegals support lawyers with research, drafting, and case management. You do not give legal advice but are essential to law practice. Certificates or associate degrees are common; some firms train on the job.',
    'Entrepreneur': 'Entrepreneurs start and run their own businesses. You might build a product, offer a service, or lead a small team. Risk tolerance, resilience, and versatility are important; many have prior industry experience.',
    'Environmental Scientist': 'Environmental scientists study and address environmental issues—pollution, conservation, climate, or compliance. You might work for government, consulting firms, or nonprofits. Fieldwork and data analysis are both common.',
    'Sustainability Consultant': 'Sustainability consultants help organizations reduce environmental impact and operate more sustainably. You might focus on energy, waste, supply chain, or reporting. Demand is growing in corporate and consulting roles.',
    'Park Ranger / Conservation': 'Park rangers and conservation workers manage and protect natural areas. You might lead programs, enforce rules, or support research. Roles exist with federal and state agencies, and nonprofits.',
    'Landscape Architect': 'Landscape architects design outdoor spaces—parks, campuses, and residential or commercial sites. You blend design with environmental and technical knowledge. Licensure is required in most states.',
    'Agriculture / Agribusiness': 'Professionals in agriculture and agribusiness work on farming, ranching, supply chain, or ag tech. You might focus on production, sales, or sustainability. Roles range from hands-on to business and research.',
    'Event Planner': 'Event planners organize and run events—conferences, weddings, or corporate gatherings. You handle logistics, vendors, and budgets. Strong organization and people skills are essential.',
    'Executive Assistant': 'Executive assistants support senior leaders with scheduling, communication, and projects. You might manage calendars, prepare materials, and coordinate across teams. Discretion and organization are key.',
    'Compliance Officer': 'Compliance officers ensure organizations follow laws and internal policies. You might work in finance, healthcare, or general corporate compliance. Attention to detail and integrity are critical.',
    'Compensation Analyst': 'Compensation analysts evaluate and design pay and benefits packages to attract and retain talent. You use market data and internal equity to set salary bands and bonus structures. Strong Excel and analytical skills are common; HR or finance backgrounds fit well.',
    'Cost Analyst': 'Cost analysts dig into a company’s costs to find savings and improve profitability. You might track spending by project, product, or department and recommend changes. Common in manufacturing, construction, and corporate finance.',
    'Real Estate Analyst': 'Real estate analysts support investment and development decisions with market research, financial models, and due diligence. You might work for investors, developers, or lenders. Excel and Argus (or similar) are standard tools.',
    'Auditor': 'Auditors review financial records and internal controls to ensure accuracy and compliance. You might work in public accounting (external audit) or inside a company (internal audit). CPA is typical for public accounting.',
    'Recruiter': 'Recruiters source and screen candidates, run interviews, and help hire for open roles. You might work in-house or at a staffing agency. Strong communication and organization are key; many specialize by function or industry.',
    'Front of House Manager': 'Front of house managers oversee customer-facing operations in restaurants, hotels, theaters, or event venues. You ensure guests have a positive experience and that service runs smoothly. Hospitality or management experience is typical.',
    'Hotel Manager': 'Hotel managers run daily operations: front desk, housekeeping, events, and often F&B. You might manage a single property or a region. Degree in hospitality or business is common; many work their way up from front-line roles.',
    'Restaurant Manager': 'Restaurant managers handle staffing, inventory, service standards, and often finances for a restaurant. You work closely with kitchen and front-of-house staff. Experience in food service is usually expected.',
    'Tour Guide / Travel Coordinator': 'Tour guides lead groups through destinations; travel coordinators plan trips and itineraries. You might work for tour operators, cruise lines, or destinations. People skills and organization are central.',
    'Warehouse Lead Hand': 'Warehouse lead hands supervise daily warehouse operations: receiving, picking, packing, and shipping. You coordinate the team and keep workflows efficient. Experience in logistics or warehousing is typical; some roles require forklift certification.',
    'Inventory Manager': 'Inventory managers maintain optimal stock levels and oversee inventory systems. You might work with purchasing, warehousing, and planning. Analytical skills and ERP experience are often required.',
    'Procurement Specialist': 'Procurement specialists source and purchase goods and services for their organization. You might negotiate with suppliers and manage contracts. Roles exist in almost every industry; certifications (e.g., CPSM) can help.',
    'Real Estate Agent / Broker': 'Real estate agents and brokers help clients buy, sell, or rent properties. You show listings, negotiate, and guide clients through closing. State licensure is required; commission-based pay is common.',
    'Property Manager': 'Property managers handle day-to-day operations of rental properties: leasing, maintenance, tenant relations, and often budgets. You might work for owners or management companies. Leasing or maintenance experience is helpful.',
    'Appraiser': 'Appraisers assess the value of real estate, equipment, or other assets. You might work for lenders, government, or appraisal firms. State licensure or certification is typically required for real estate appraisal.',
    'Sports Manager / Athletic Director': 'Sports managers and athletic directors run sports programs, facilities, or teams. You might work for a school, university, or sports organization. Background in athletics plus business or administration is common.',
    'Fitness Manager / Personal Trainer': 'Fitness managers run gym or studio operations; personal trainers design and deliver workouts for clients. Certification (e.g., NASM, ACE) is often required. Roles can be in gyms, corporate wellness, or freelance.',
    'Recreation Coordinator': 'Recreation coordinators plan and run recreation programs—youth sports, camps, community activities. You might work for parks and rec, nonprofits, or community centers. Organization and people skills are key.',
    'Construction Manager': 'Construction managers plan and oversee construction projects from bid through completion. You coordinate contractors, schedule, budget, and safety. Experience in construction and often a degree or certification (e.g., CM) are typical.',
    'Electrical Engineer': 'Electrical engineers design and maintain electrical systems—power, electronics, or control systems. You might work in utilities, manufacturing, or tech. A PE license can be required for certain roles.',
    'Quality Assurance Analyst': 'QA analysts test software or products to find defects and ensure quality. You might write test cases, run manual or automated tests, and work with developers. Common in tech and manufacturing.',
    'Technical Writer': 'Technical writers create manuals, docs, and other technical content so users can understand products or processes. You might work with engineers and product teams. Clear writing and ability to learn technical topics are essential.',
    'Cosmetologist / Hairstylist': 'Cosmetologists and hairstylists cut, color, and style hair for clients. You might work in a salon, spa, or as a freelancer. State licensure is required. Customer service and creativity are key.',
    'Esthetician / Skincare Specialist': 'Estheticians provide facials, skincare treatments, and sometimes makeup services. You might work in spas, salons, or medical offices. State licensure is required.',
    'Barber': 'Barbers cut and style hair, often specializing in men\'s cuts, shaves, and grooming. You might work in a barbershop or salon. State licensure is typically required.',
    'Medical Assistant': 'Medical assistants perform clinical and administrative tasks in healthcare settings. You might take vital signs, prepare patients, and handle records. Certification can help with hiring.',
    'Dental Hygienist': 'Dental hygienists clean teeth, take X-rays, and educate patients on oral health. You work in dental offices. State licensure is required; associate degree programs are common.',
    'Surgical Technologist': 'Surgical technologists prepare operating rooms, sterilize instruments, and assist surgeons during procedures. You work in hospitals and surgical centers. Certification is available.',
    'Sonographer / Ultrasound Tech': 'Sonographers operate ultrasound equipment to capture diagnostic images. You might specialize in abdominal, cardiac, or vascular imaging. Certification is typical.',
    'Chef / Cook': 'Chefs and cooks prepare food in restaurants, hotels, or catering. You might start on the line and work up to sous or head chef. Culinary school or apprenticeship is common.',
    'Pastry Chef / Baker': 'Pastry chefs and bakers create breads, pastries, desserts, and baked goods. You might work in bakeries, restaurants, or hotels. Formal training or apprenticeship is typical.',
    'Aircraft Mechanic': 'Aircraft mechanics maintain and repair aircraft systems, structures, and engines. FAA certification (A&P) is required. You might work for airlines, repair stations, or the military.',
    'Commercial Truck Driver': 'Commercial truck drivers transport goods across the country. A CDL (Commercial Driver\'s License) is required. Long hauls or regional routes are common.',
    'Diesel Technician': 'Diesel technicians repair and maintain diesel engines in trucks, buses, and heavy equipment. You might work for fleets, dealerships, or repair shops. Technical training or apprenticeship is typical.',
    'Firefighter': 'Firefighters respond to fires, emergencies, and rescue situations. You might work for municipal, wildland, or industrial fire departments. Physical fitness and certification are required.',
    'EMT / Paramedic': 'EMTs and paramedics provide emergency medical care in the field. You respond to 911 calls and transport patients. State certification is required; paramedics have advanced training.',
}

# Default when no extended copy exists
CAREER_LEARN_MORE_DEFAULT = 'This role aligns with your interests and major. Typical duties vary by employer; researching job postings and talking to people in the field can give you a clearer picture of day-to-day work and requirements.'

# --- Interest & preference questions ---
INTEREST_QUESTIONS = [
    {
        'id': 1,
        'text': 'How do you prefer to spend your free time?',
        'options': [
            ('building', 'Building or fixing things', ['technical', 'organizing']),
            ('reading', 'Reading or learning something new', ['research', 'analytical']),
            ('people', 'Spending time with friends or helping others', ['helping', 'leading']),
            ('creative', 'Creating art, music, or writing', ['creative']),
            ('outdoors', 'Being outdoors or doing physical activity', ['outdoor', 'technical']),
        ],
    },
    {
        'id': 2,
        'text': 'What type of problems do you enjoy solving?',
        'options': [
            ('numbers', 'Numbers, patterns, and logic', ['analytical', 'technical']),
            ('people_problems', 'Helping people overcome challenges', ['helping', 'leading']),
            ('design', 'Design and making things look or work better', ['creative', 'technical']),
            ('systems', 'How things fit together and run smoothly', ['organizing', 'analytical']),
            ('discovery', 'Unknown questions and finding new answers', ['research', 'analytical']),
        ],
    },
    {
        'id': 3,
        'text': 'Which subject in school did you enjoy most (or would you)?',
        'options': [
            ('math_science', 'Math or science', ['analytical', 'technical', 'research']),
            ('english_arts', 'English, art, or music', ['creative', 'helping']),
            ('history_social', 'History or social studies', ['research', 'leading', 'helping']),
            ('shop_pe', 'Shop class, PE, or hands-on activities', ['technical', 'outdoor', 'organizing']),
            ('business', 'Business or economics', ['leading', 'analytical', 'organizing']),
        ],
    },
    {
        'id': 4,
        'text': 'What would you rather avoid in a job?',
        'options': [
            ('no_people', 'Working mostly alone with little contact', ['helping', 'leading']),
            ('no_creativity', 'Repetitive work with no room for new ideas', ['creative', 'research']),
            ('no_structure', 'Unclear goals and disorganization', ['organizing', 'analytical']),
            ('no_impact', 'Work that doesn’t help people or society', ['helping', 'leading']),
            ('no_technical', 'Work that doesn’t use technology or tools', ['technical', 'analytical']),
        ],
    },
    {
        'id': 5,
        'text': 'What matters most to you in a career?',
        'options': [
            ('security', 'Stability and clear structure', ['organizing', 'analytical']),
            ('impact', 'Making a difference for others', ['helping', 'leading']),
            ('innovation', 'Creating something new or cutting-edge', ['creative', 'research', 'technical']),
            ('success', 'Recognition and advancement', ['leading', 'analytical']),
            ('balance', 'Work-life balance and variety', ['outdoor', 'helping', 'creative']),
        ],
    },
]

# --- Big Five (OCEAN) questions - Scontrino-Powell / personality–job performance research ---
# Conscientiousness predicts performance across all job types; extraversion/agreeableness/openness matter more for sales, customer service, leadership
BIG_FIVE_QUESTIONS = [
    {
        'id': 6,
        'text': 'When you have a big task, you usually:',
        'options': [
            ('bf_plan_first', 'Make a plan and stick to it', ['organizing', 'analytical']),
            ('bf_deadline_drive', 'Work in bursts and meet the deadline', ['leading', 'technical']),
            ('bf_explore_approach', 'Try different approaches and see what works', ['creative', 'research']),
            ('bf_team_check', 'Check in with others and divide the work', ['helping', 'organizing']),
            ('bf_steady_pace', 'Keep a steady pace and avoid last-minute rushes', ['organizing', 'analytical']),
        ],
    },
    {
        'id': 7,
        'text': 'At a party or networking event, you tend to:',
        'options': [
            ('bf_energized_mingle', 'Feel energized and enjoy meeting new people', ['leading', 'helping']),
            ('bf_deep_convo', 'Have a few deeper conversations rather than many quick ones', ['helping', 'research']),
            ('bf_observe_engage', 'Observe at first, then engage when it feels right', ['analytical', 'leading']),
            ('bf_ideas_share', 'Get excited sharing ideas and hearing others’ perspectives', ['creative', 'research']),
            ('bf_leave_early', 'Stay a bit then leave when you’ve had enough', ['organizing', 'technical']),
        ],
    },
    {
        'id': 8,
        'text': 'How do you feel about trying something completely new (e.g. a new hobby or way of working)?',
        'options': [
            ('bf_love_new', 'I love it—variety and new experiences are important to me', ['creative', 'research']),
            ('bf_curious_selective', 'I’m curious and will try it if it fits my goals', ['research', 'analytical']),
            ('bf_comfort_familiar', 'I prefer to get really good at a few things I know', ['technical', 'organizing']),
            ('bf_new_with_others', 'I like trying new things when I can do it with others', ['helping', 'creative']),
            ('bf_practical_new', 'I’m open if it’s practical and has a clear benefit', ['organizing', 'analytical']),
        ],
    },
    {
        'id': 9,
        'text': 'When a teammate is struggling or disagrees with you, you usually:',
        'options': [
            ('bf_support_listen', 'Listen and try to support or find common ground', ['helping', 'leading']),
            ('bf_fair_solution', 'Focus on what’s fair and how to fix the situation', ['analytical', 'organizing']),
            ('bf_stand_conviction', 'Stand by my view but stay respectful', ['leading', 'analytical']),
            ('bf_collaborate_idea', 'Suggest a different approach we could both try', ['creative', 'helping']),
            ('bf_step_back', 'Step back and let things cool down before re-engaging', ['organizing', 'research']),
        ],
    },
    {
        'id': 10,
        'text': 'When something goes wrong or you get critical feedback, you typically:',
        'options': [
            ('bf_calm_assess', 'Stay calm and figure out what to do next', ['organizing', 'analytical']),
            ('bf_talk_through', 'Talk it through with someone you trust', ['helping', 'leading']),
            ('bf_focus_fix', 'Focus on fixing the problem rather than dwelling on it', ['technical', 'organizing']),
            ('bf_reflect_learn', 'Reflect on it and look for what you can learn', ['research', 'analytical']),
            ('bf_upset_briefly', 'Feel upset or stressed briefly, then move on', ['helping', 'creative']),
        ],
    },
]

# --- Research-backed personality & teamwork questions ---
# Based on team role (Belbin), conflict style, and work preference research
PERSONALITY_QUESTIONS = [
    {
        'id': 11,
        'text': 'In a team project, you usually:',
        'options': [
            ('role_coordinator', 'Coordinate people and keep the group on track', ['leading', 'organizing']),
            ('role_ideas', 'Generate ideas and suggest new approaches', ['creative', 'research']),
            ('role_analyzer', 'Analyze options and spot potential problems', ['analytical', 'research']),
            ('role_supporter', 'Support others and make sure everyone is heard', ['helping', 'organizing']),
            ('role_doer', 'Focus on getting concrete tasks done on time', ['technical', 'organizing']),
        ],
    },
    {
        'id': 12,
        'text': 'When there’s disagreement on the team, you tend to:',
        'options': [
            ('conflict_mediate', 'Listen to both sides and help find a middle ground', ['helping', 'leading']),
            ('conflict_advocate', 'Stand firm on what you think is right', ['leading', 'analytical']),
            ('conflict_research', 'Look for data or evidence to decide', ['analytical', 'research']),
            ('conflict_defer', 'Go along with the group to keep things moving', ['organizing', 'helping']),
            ('conflict_innovate', 'Suggest a new option that might satisfy everyone', ['creative', 'research']),
        ],
    },
    {
        'id': 13,
        'text': 'You work best when:',
        'options': [
            ('work_structured', 'Goals and deadlines are clear', ['organizing', 'analytical']),
            ('work_collab', 'You can bounce ideas off others regularly', ['helping', 'creative']),
            ('work_autonomous', 'You have ownership and can decide how to do it', ['leading', 'technical']),
            ('work_learning', 'You’re learning something new', ['research', 'technical']),
            ('work_varied', 'Tasks and people change so it doesn’t get stale', ['creative', 'helping']),
        ],
    },
    {
        'id': 14,
        'text': 'Under pressure, you’re more likely to:',
        'options': [
            ('stress_plan', 'Make a plan and work through it step by step', ['organizing', 'analytical']),
            ('stress_talk', 'Talk it through with someone', ['helping', 'leading']),
            ('stress_focus', 'Block out distractions and focus on one thing', ['technical', 'research']),
            ('stress_adapt', 'Stay flexible and adjust as things change', ['creative', 'leading']),
            ('stress_action', 'Take action quickly to fix the problem', ['technical', 'leading']),
        ],
    },
    {
        'id': 15,
        'text': 'What motivates you most at work?',
        'options': [
            ('motivate_mastery', 'Getting really good at something', ['technical', 'research', 'analytical']),
            ('motivate_impact', 'Seeing that your work helps people', ['helping', 'leading']),
            ('motivate_creativity', 'Creating something new or original', ['creative', 'research']),
            ('motivate_team', 'Being part of a strong team', ['helping', 'organizing']),
            ('motivate_challenge', 'Solving hard problems or winning', ['leading', 'analytical', 'technical']),
        ],
    },
]

# --- Statistical job-match questions (O*NET work styles/values, Holland RIASEC) ---
# O*NET: work activities and work context predict occupational fit; Holland: interest–occupation congruence predicts satisfaction
JOB_MATCH_QUESTIONS = [
    {
        'id': 16,
        'text': 'How important is it to you that your job has clear rules and predictable structure?',
        'options': [
            ('value_structure_high', 'Very important—I like knowing what to expect', ['organizing', 'analytical']),
            ('value_structure_some', 'Somewhat—I like a mix of structure and flexibility', ['leading', 'creative']),
            ('value_structure_low', 'Not very—I prefer roles that change and adapt', ['creative', 'research']),
            ('value_structure_team', 'It depends on the team—I adapt to how others work', ['helping', 'organizing']),
            ('value_structure_tools', 'I care more about having the right tools than rules', ['technical', 'outdoor']),
        ],
    },
    {
        'id': 17,
        'text': 'Would you rather work mainly with things and tools, with ideas and data, or with people?',
        'options': [
            ('holland_things', 'Things and tools—building, fixing, or operating', ['technical', 'outdoor']),
            ('holland_ideas', 'Ideas and data—analyzing, creating, or researching', ['research', 'analytical', 'creative']),
            ('holland_people', 'People—teaching, helping, or persuading', ['helping', 'leading']),
            ('holland_mix_pt', 'A mix of things and people', ['outdoor', 'helping']),
            ('holland_mix_id', 'A mix of ideas and people', ['leading', 'research']),
        ],
    },
    {
        'id': 18,
        'text': 'How do you feel about jobs where you are responsible for other people’s work or decisions?',
        'options': [
            ('responsibility_seek', 'I want that responsibility—I like leading and deciding', ['leading']),
            ('responsibility_ok', 'I’m fine with it when it’s part of the role', ['leading', 'organizing']),
            ('responsibility_avoid', 'I prefer to be responsible only for my own work', ['technical', 'research']),
            ('responsibility_share', 'I like shared responsibility with a team', ['helping', 'organizing']),
            ('responsibility_mentor', 'I like guiding others but not being the final decider', ['helping', 'leading']),
        ],
    },
    {
        'id': 19,
        'text': 'Which best describes your preference for how work is evaluated?',
        'options': [
            ('eval_achievement', 'I want to be judged on clear results and achievement', ['analytical', 'leading']),
            ('eval_quality', 'I want to be judged on quality and accuracy of work', ['organizing', 'technical']),
            ('eval_impact', 'I want to be judged on impact on people or society', ['helping', 'leading']),
            ('eval_innovation', 'I want to be judged on new ideas and creativity', ['creative', 'research']),
            ('eval_team', 'I want to be judged on how well the team does', ['helping', 'organizing']),
        ],
    },
    {
        'id': 20,
        'text': 'How much do you want your job to involve face-to-face or direct contact with others?',
        'options': [
            ('contact_high', 'A lot—I want to work with people most of the day', ['helping', 'leading']),
            ('contact_medium', 'A moderate amount—some meetings and collaboration', ['organizing', 'creative']),
            ('contact_low', 'A little—I prefer focused solo work with some contact', ['technical', 'research']),
            ('contact_varied', 'It varies—I like roles where it changes by project', ['creative', 'research']),
            ('contact_lead', 'I’m fine with contact when I’m in a leadership role', ['leading']),
        ],
    },
    {
        'id': 21,
        'text': 'What kind of pressure do you handle best?',
        'options': [
            ('pressure_deadlines', 'Time pressure and deadlines', ['organizing', 'analytical']),
            ('pressure_people', 'Dealing with difficult people or conflict', ['helping', 'leading']),
            ('pressure_accuracy', 'Getting details right with no errors', ['technical', 'organizing']),
            ('pressure_unknown', 'Uncertainty and the need to figure things out', ['research', 'creative']),
            ('pressure_physical', 'Physical demands or working in tough conditions', ['outdoor', 'technical']),
        ],
    },
    {
        'id': 22,
        'text': 'How important is it that your work has a direct, visible impact?',
        'options': [
            ('impact_very', 'Very—I need to see the results of my work', ['helping', 'outdoor', 'technical']),
            ('impact_longterm', 'I’m okay with impact that takes time to show', ['research', 'analytical']),
            ('impact_team', 'I care that the team or organization succeeds', ['leading', 'organizing']),
            ('impact_creative', 'I care that something new or better exists because of me', ['creative', 'research']),
            ('impact_financial', 'I care about measurable outcomes (e.g. revenue, efficiency)', ['analytical', 'leading']),
        ],
    },
    {
        'id': 23,
        'text': 'Do you prefer to follow established methods or develop new ones?',
        'options': [
            ('method_follow', 'Follow established methods—they exist for a reason', ['organizing', 'technical']),
            ('method_improve', 'Improve existing methods when I see a better way', ['analytical', 'research']),
            ('method_new', 'Develop new methods—I like to innovate', ['creative', 'research']),
            ('method_hybrid', 'It depends—some tasks need structure, others need creativity', ['leading', 'creative']),
            ('method_learn', 'I like learning both and choosing per situation', ['research', 'technical']),
        ],
    },
    {
        'id': 24,
        'text': 'Which work environment do you prefer?',
        'options': [
            ('env_office', 'Traditional office with a set desk and schedule', ['organizing', 'analytical']),
            ('env_flex', 'Flexible—remote, hybrid, or variable hours', ['creative', 'technical']),
            ('env_field', 'Field or on-site—different locations, not at a desk', ['outdoor', 'helping']),
            ('env_lab_studio', 'Lab, studio, or workshop', ['research', 'creative', 'technical']),
            ('env_people', 'Highly social—customer-facing or team-heavy', ['helping', 'leading']),
        ],
    },
    {
        'id': 25,
        'text': 'What would make you feel most satisfied at the end of a workday?',
        'options': [
            ('satisfy_done', 'Knowing I completed my list and met my goals', ['organizing', 'analytical']),
            ('satisfy_helped', 'Knowing I helped someone or made a difference', ['helping', 'leading']),
            ('satisfy_created', 'Knowing I made or improved something', ['creative', 'technical']),
            ('satisfy_learned', 'Knowing I learned something or solved a problem', ['research', 'analytical']),
            ('satisfy_team', 'Knowing the team did well and we collaborated', ['helping', 'organizing']),
        ],
    },
]

# Combined list for the quiz (interest + Big Five + team/personality + job-match) — 25 questions
QUESTIONS = INTEREST_QUESTIONS + BIG_FIVE_QUESTIONS + PERSONALITY_QUESTIONS + JOB_MATCH_QUESTIONS

# Short quiz: 10 questions (interest + Big Five). Less accurate but faster (~3 min).
SHORT_QUESTIONS = INTEREST_QUESTIONS + BIG_FIVE_QUESTIONS


def get_majors():
    return MAJORS


def get_major_by_key(key):
    for row in MAJORS:
        k, label, desc = row[0], row[1], row[2]
        if k == key:
            return {'key': k, 'label': label, 'description': desc}
    return None


def get_questions(short=False):
    """Return question list. short=True gives 10 questions; short=False gives full 25."""
    if short:
        return SHORT_QUESTIONS
    return QUESTIONS


def get_career_categories():
    return CAREER_CATEGORIES


def score_quiz(selected_options):
    """
    selected_options: list of option keys chosen.
    Returns: list of (category_key, score) sorted by score descending.
    """
    scores = {}
    for q in QUESTIONS:
        for opt_key, _label, categories in q['options']:
            if opt_key in selected_options:
                for cat in categories:
                    scores[cat] = scores.get(cat, 0) + 1
    return sorted(scores.items(), key=lambda x: -x[1])


def get_careers_for_major(major_key):
    """Return list of (title, description, category) for careers in this major."""
    result = []
    seen = set()
    for title, desc, category, majors in CAREERS_BY_MAJOR:
        if major_key in majors and title not in seen:
            seen.add(title)
            result.append({'title': title, 'description': desc, 'category': category})
    return result


def get_top_careers(score_tuples, major_key=None, top_n=4, max_careers=12):
    """
    Return career suggestions. If major_key is set, only include careers for that major.
    Rank by how well each career's category matches the user's top categories.
    """
    if major_key:
        pool = get_careers_for_major(major_key)
    else:
        pool = [{'title': t, 'description': d, 'category': c} for t, d, c, _ in CAREERS_BY_MAJOR]
        seen = set()
        unique = []
        for c in pool:
            if c['title'] not in seen:
                seen.add(c['title'])
                unique.append(c)
        pool = unique

    # Score each career by user's category scores (prefer careers in top categories)
    category_scores = dict(score_tuples)
    def career_score(career):
        return category_scores.get(career['category'], 0)

    # Sort by match to user profile: most to least compatible (higher category score = better match)
    sorted_pool = sorted(pool, key=career_score, reverse=True)
    result = []
    for rank, c in enumerate(sorted_pool[:max_careers], start=1):
        entry = dict(c)
        entry['learn_more'] = CAREER_LEARN_MORE.get(c['title'], CAREER_LEARN_MORE_DEFAULT)
        entry['compatibility_rank'] = rank
        entry['match_score'] = career_score(c)
        result.append(entry)
    return result


def get_results_summary_paragraph(scores_with_names, suggestions, major_label=None):
    """
    Build a brief paragraph explaining why the suggested jobs match the user's personality.
    scores_with_names: list of (cat_key, score, category_name, category_desc)
    suggestions: list of career dicts with title, category, compatibility_rank
    """
    if not scores_with_names or not suggestions:
        return None
    top_cats = [name for _k, _s, name, _d in scores_with_names[:3]]
    top_cat_str = ', '.join(top_cats[:-1])
    if len(top_cats) > 1:
        top_cat_str += ' and ' + top_cats[-1]
    else:
        top_cat_str = top_cats[0]
    first_jobs = [s['title'] for s in suggestions[:3]]
    first_jobs_str = ', '.join(first_jobs[:-1])
    if len(first_jobs) > 1:
        first_jobs_str += ', and ' + first_jobs[-1]
    else:
        first_jobs_str = first_jobs[0]
    intro = 'Your quiz results show strong alignment with ' + top_cat_str + '. '
    jobs_sentence = 'Roles like ' + first_jobs_str + ' appear at the top because they match these strengths most closely. '
    order_sentence = 'Suggestions are ordered from most to least compatible with your personality and interests. '
    if major_label:
        order_sentence = 'All suggestions fit your ' + major_label + ' background and are ordered from most to least compatible with your personality. '
    return intro + jobs_sentence + order_sentence


def get_suggested_majors(score_tuples, top_n=6):
    """
    Suggest majors based on category scores: score each major by how well its careers'
    categories match the user's top categories. Returns list of (major_key, major_label, major_desc, score).
    """
    category_scores = dict(score_tuples)
    major_totals = {}  # major_key -> total score
    for title, desc, category, majors in CAREERS_BY_MAJOR:
        cat_score = category_scores.get(category, 0)
        for m in majors:
            major_totals[m] = major_totals.get(m, 0) + cat_score
    # Sort by score descending and build list with labels
    major_keys_sorted = sorted(major_totals.keys(), key=lambda m: -major_totals[m])
    result = []
    for key in major_keys_sorted[:top_n]:
        info = get_major_by_key(key)
        if info:
            result.append((key, info['label'], info['description'], major_totals[key]))
    return result


def get_explore_summary_paragraph(scores_with_names, suggested_majors):
    """Brief paragraph for explore results: why these majors and categories fit."""
    if not scores_with_names or not suggested_majors:
        return None
    top_cats = [name for _k, _s, name, _d in scores_with_names[:3]]
    top_cat_str = ', '.join(top_cats[:-1])
    if len(top_cats) > 1:
        top_cat_str += ' and ' + top_cats[-1]
    else:
        top_cat_str = top_cats[0]
    major_names = [m[1] for m in suggested_majors[:3]]
    major_str = ', '.join(major_names[:-1])
    if len(major_names) > 1:
        major_str += ', and ' + major_names[-1]
    else:
        major_str = major_names[0]
    return (
        'Your answers show strong alignment with ' + top_cat_str + '. '
        'That’s why we’re suggesting majors like ' + major_str + '—they lead to careers that often match these strengths. '
        'You can explore jobs in any suggested major, or take the full quiz again after picking one to see roles tailored to that degree.'
    )
