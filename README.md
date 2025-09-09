# Sankalpa - AI-Powered Personalization for SBI Life Insurance

## Problem Statement
**Enhancing Customer Experience and Retention through AI-Driven Personalization to Improve the Propensity to Purchase**

---

## 🧠 Overview
Developed an AI Driven Personalization Platform for SBI Life as part of a hackathon project. The goal was to enhance policy personalization, upselling, customer engagement, and trust through AI-powered solutions. The platform combines recommendation engines, AI chatbots, gamification, real-time analytics, and ethical AI practices to create an interactive and transparent customer experience.

---

## 🖼 Screenshots of Interface

<img width="1886" height="902" alt="image" src="https://github.com/user-attachments/assets/26b063fe-c8b8-4f0e-b859-ee2700c6f3d5" />
<img width="1917" height="902" alt="image" src="https://github.com/user-attachments/assets/c0c0365a-a782-43d8-aa32-6aaac74527a9" />
<img width="1917" height="900" alt="image" src="https://github.com/user-attachments/assets/0ae679ee-2c08-4501-9151-47ece6201592" />
<img width="1896" height="900" alt="image" src="https://github.com/user-attachments/assets/537660a0-af74-45cc-8882-cd31e0d452a9" />
<img width="1890" height="899" alt="image" src="https://github.com/user-attachments/assets/faa5ab50-79a3-4395-b037-f839674b7dbb" />
<img width="1896" height="906" alt="image" src="https://github.com/user-attachments/assets/3387d0db-67e7-48b8-8ef2-7015569239b6" />
<img width="1887" height="909" alt="image" src="https://github.com/user-attachments/assets/3df20903-5d03-499c-b9a6-8f8a366e9d1d" />
<img width="1892" height="947" alt="image" src="https://github.com/user-attachments/assets/618aa1bd-06f3-4963-a83e-e88d5cc5e3f3" />
<img width="1894" height="962" alt="image" src="https://github.com/user-attachments/assets/f53346e2-d205-4757-b3f2-0df23ac0322c" />
<img width="1882" height="900" alt="image" src="https://github.com/user-attachments/assets/00f79afb-f268-450f-889e-2f2b69ad3abb" />
<img width="1890" height="895" alt="image" src="https://github.com/user-attachments/assets/d437d396-10bf-4b1b-b529-e8db6ece1625" />
<img width="1914" height="901" alt="image" src="https://github.com/user-attachments/assets/5fcd20e1-371a-4f0a-8d6c-2770bd5ab066" />
<img width="1897" height="903" alt="image" src="https://github.com/user-attachments/assets/cbf33931-701c-49ba-9bc8-05d82dfc3f5c" />
<img width="1891" height="907" alt="image" src="https://github.com/user-attachments/assets/f9e87b28-f749-44e9-98c8-3165a8f22b0e" />

---

## ✨ Key Features

### 🔐 Authentication & Security
- **Dual Login System:** Separate portals for customers and agents  
- **Multi-Factor Authentication (MFA):** TOTP-based security using Google Authenticator  
- **Profile Management:** Comprehensive user profile setup for first-time users  

### 🎯 Smart Policy Recommender
- **RAG-based Policy Recommendations:** Personalized insurance policy suggestions using Retrieval-Augmented Generation  
- **Trust Policy Score:** Explainable AI that builds customer confidence through transparent recommendation reasoning  
- **Policy Upselling Engine:** AI-powered cross-selling and upgrade suggestions to maximize customer value  

### 🤖 TalkSmart Chatbot (TIA)
- **Multilingual Support:** Contextual customer support in multiple languages  
- **Intelligent Query Handling:** Advanced NLP for understanding complex customer queries  
- **24/7 Availability:** Round-the-clock customer assistance  

### 🎮 Interactive Financial Tools
- **Financial Simulator:** A gamified tool for financial planning and scenario modeling that helps users explore different financial strategies in an engaging way.  
- **Goal GPS:** An interactive goal-setting and tracking game that allows users to set, adjust, and achieve their financial objectives through a fun experience.  
- **AI Powered Nudges:** Intelligent, real-time suggestions during gameplay to help users adjust goals, amounts, and timelines for improved financial outcomes.  

### 📊 InsureInsights Dashboard
- **Predictive Analytics:** Advanced insights for business intelligence  
- **Campaign AI Optimization:** Automated marketing campaign enhancement  
- **Real-time Engagement Metrics:** Live tracking of user interactions and performance  
- **Inspirational Stories:** Customer success stories to drive motivation  

### 💬 FinChat Assistant
- **General Financial Knowledge:** Comprehensive financial information chatbot  
- **Educational Content:** Answers to financial queries and learning resources  
- **Contextual Responses:** Tailored information based on user profile and history  

---

### 🏗 Model Architecture
<img width="1686" height="927" alt="image" src="https://github.com/user-attachments/assets/fa5c5a80-4686-4877-bb39-9831dc698c92" />
<img width="1809" height="898" alt="image" src="https://github.com/user-attachments/assets/91091a36-8c69-4f6a-a788-65ef940e6269" />

---

## 📁 Project Structure

<pre>
├── public/ # Static files
├── views/ # Frontend views
├── app.js # Main backend server
├── chatbot_server.py # Chatbot interaction logic
├── dashboard.py # Backend dashboard and visualizations
├── dbSetup.js # Database initialization
├── policy_classifier.py # ML model for policy prediction
├── policy_recommend.py # Core AI logic for recommending policies
├── start_chatbot.js # Starts the chatbot service
├── start_streamlit.js # Launches Streamlit frontend (optional)
├── goal_gps.js # Financial GPS module
├── totpUtils.js # MFA Support with TOTP
├── trust_policy.py # Ethics and fairness enforcement
├── upsell_predictor.py # Predicts upselling opportunities
├── sbilife.xlsx # Sample financial data
└── README.md
</pre>

---

## 🔄 User Flow
### Customer Journey:
1. Login/Registration → Profile Setup (first-time users)  
2. Dashboard Access → Feature Selection  
3. Smart Recommendations → Policy Exploration  
4. Interactive Tools → Financial Planning  
5. Chat Support → Query Resolution  
6. Insights & Analytics → Progress Tracking  

---

## 📈 Business Impact
- **Increased Customer Engagement:** Gamified tools drive user interaction  
- **Improved Conversion Rates:** AI-powered recommendations boost sales  
- **Enhanced Customer Satisfaction:** Multilingual support and personalization  
- **Data-Driven Decision Making:** Comprehensive analytics and insights  
- **Operational Efficiency:** Automated processes and intelligent routing  

---

## ⚙️ Tech Stack
- **Backend:** Node.js, Python, REST API  
- **Frontend:** HTML, CSS, JS, Streamlit  
- **AI/ML:** Scikit-learn, Sentiment Analysis, RAG  
- **Database & Security:** SQLite, TOTP (Time-based One-Time Password)  

---

## 🎯 Future Scope

### Phase 1: Enhanced AI Capabilities
- Advanced ML Models: Implementation of deep learning for better predictions  
- Voice Integration: Voice-enabled chatbot interactions  
- Computer Vision: Document analysis and claim processing automation  
- Blockchain Integration: Secure policy management and claim verification  

### Phase 2: Platform Expansion
- Mobile Application: Native iOS and Android apps  
- API Marketplace: Third-party integrations and partnerships  
- Microservices Architecture: Scalable system redesign  
- Cloud Migration: AWS/Azure deployment for better scalability  

### Phase 3: Advanced Features
- IoT Integration: Smart device data for personalized pricing  
- Augmented Reality: Virtual policy consultations  
- Predictive Analytics: Advanced risk assessment models  
- Social Features: Community-driven financial planning  

### Phase 4: Global Expansion
- Multi-Currency Support: International market expansion  
- Regulatory Compliance: Region-specific insurance regulations  
- Localization: Cultural adaptation for different markets  
- Partnership Ecosystem: Insurance provider network expansion  

### Phase 5: Innovation Lab
- Quantum Computing: Advanced risk calculations  
- AI Ethics Framework: Responsible AI implementation  
- Sustainability Metrics: Environmental impact tracking  
- Research & Development: Continuous innovation pipeline  

---

## 👥 Team
- Paranthagan S  
- Pranaav U  
- Padmapriya C  
- Nandana M  
