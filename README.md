
# **Askly App**  

A full-stack application that allows users to upload PDF files and interact with them through a chat interface. Built with **React (frontend) and Django (backend)**, deployed on **AWS**, and using a domain from **Hostinger**.

---

## **Features**  
✔ **Google/JWT Authentication** – Secure user login  
✔ **PDF Upload** – Users can upload PDFs for processing  
✔ **Chat with PDF** – Extract answers by querying the document  
✔ **Real-time Interaction** – Seamless user experience  
✔ **Deployed on AWS** – Scalable cloud infrastructure  

---

## **Tech Stack**  
- **Frontend:** React, Next.js  
- **Backend:** Django, Django Rest Framework  
- **Authentication:** Google OAuth, JWT  
- **Storage & Deployment:** AWS S3, EC2, Hostinger (Domain)  
- **WebSocket Support:** For real-time communication  

---

## **Installation & Setup**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/chiraagb/askly.git
cd askly
```

### **2. Backend Setup (Django)**
```bash
add .env secrets
docker compose up --build
```

### **3. Frontend Setup (React)**
```bash
cd frontend
npm install
npm run dev
```

---

## **Deployment**  
- **Backend** is deployed on **AWS EC2**  
- **Frontend** is hosted on **AWS S3/CloudFront**  
- **Domain** from **Hostinger** with SSL setup  

---

## **Usage**  
1. **Sign in with Google/JWT**  
2. **Upload a PDF file**  
3. **Start chatting** – Ask questions, get answers from the document  

---

## **Contributing**  
Contributions are welcome! Open a PR or submit an issue.

---

## **License**  
MIT License  

---

Let me know if you need any modifications!
