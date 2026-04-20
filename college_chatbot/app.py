import streamlit as st
import json
import re

# -------------------------------
# Load Data
# -------------------------------
with open("data/college_data.json") as f:
    data = json.load(f)

# -------------------------------
# Email Validation
# -------------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# -------------------------------
# Retrieve Relevant Info
# -------------------------------
def get_relevant_info(query):
    query = query.lower()

    if "fee" in query:
        return data["courses"]
    elif "course" in query:
        return data["courses"]
    elif "admission" in query:
        return data["admission_process"]
    elif "contact" in query:
        return data["contact"]
    elif any(word in query for word in ["facility","facilities", "gym", "playground", "sports", "wifi"]):
        return data["facilities"]
    elif "placement" in query:
        return data["placements"]
    elif "internship" in query:
        return data["internships"]
    elif "scholarship" in query:
        return data["scholarships"]
    elif "hostel" in query:
        return data["hostel_fees"]
    elif "campus" in query or "vibe" in query:
        return data["campus_vibe"]
    else:
        return "general"

# -------------------------------
# Generate Response (No API)
# -------------------------------
def generate_response(query, context):
    query = query.lower()

    if "fee" in query:
        response = "💰 Course Fee Structure:\n"
        for course in data["courses"]:
            response += f"- {course['name']}: {course['fees']}\n"
        return response

    elif "hostel" in query:
        return f"🏨 Hostel Fees:\n{data['hostel_fees']}"

    elif "course" in query:
        response = "📚 Courses Offered:\n"
        for course in data["courses"]:
            response += f"- {course['name']} ({course['duration']})\n"
        return response

    elif "eligibility" in query:
        response = "🎓 Eligibility Criteria:\n"
        for course in data["courses"]:
            response += f"- {course['name']}: {course['eligibility']}\n"
        return response

    elif "admission" in query:
        return f"📝 Admission Process:\n{data['admission_process']}"

    elif "contact" in query:
        c = data["contact"]
        return f"📞 Contact Details:\nPhone: {c['phone']}\nEmail: {c['email']}\nAddress: {c['address']}"

    # ✅ FIXED FACILITIES LOGIC
    elif any(word in query for word in ["facility", "gym", "playground", "sports", "wifi"]):
        return "🏫 Facilities:\n" + ", ".join(data["facilities"])

    elif "placement" in query:
        p = data["placements"]
        return f"""💼 Placement Details:
Average Package: {p['average_package']}
Highest Package: {p['highest_package']}
Top Companies: {", ".join(p['top_companies'])}"""

    elif "internship" in query:
        i = data["internships"]
        return f"""💻 Internship Opportunities:
{i['details']}
Companies: {", ".join(i['companies'])}"""

    elif "scholarship" in query:
        s = data["scholarships"]
        return f"""🎓 Scholarships:
Merit-Based: {s['merit']}
Sports: {s['sports']}
Financial Aid: {s['financial']}"""

    elif "campus" in query or "vibe" in query:
        return f"🌿 Campus Life:\n{data['campus_vibe']}"

    else:
        return "❓ Ask about courses, fees, hostel, admission, facilities, placements, internships, scholarships, or campus life."

# -------------------------------
# UI STARTS HERE
# -------------------------------

st.title(f"🎓 {data['college_name']} Enquiry Chatbot")

# -------------------------------
# Email Section
# -------------------------------
if "email" not in st.session_state:
    st.session_state.email = None

if st.session_state.email is None:
    email_input = st.text_input("📧 Enter your email to continue:")

    if st.button("Submit Email"):
        if is_valid_email(email_input):
            st.session_state.email = email_input
            st.success("✅ Email saved! Continue below.")
        else:
            st.error("❌ Enter a valid email")

# -------------------------------
# Main App After Email
# -------------------------------
else:
    st.write(f"Logged in as: {st.session_state.email}")

    # Course Selection
    course_names = [course["name"] for course in data["courses"]]
    selected_course = st.selectbox("🎯 Select a course:", course_names)

    # Enquiry Form
    st.subheader("📋 Enquiry Form")

    name = st.text_input("Enter your name")
    phone = st.text_input("Enter your phone number")

    if st.button("Submit Enquiry"):
        if name and phone:
            with open("enquiries.txt", "a") as f:
                f.write(f"{name}, {st.session_state.email}, {phone}, {selected_course}\n")

            st.success("✅ Enquiry submitted successfully!")
        else:
            st.error("❌ Please fill all fields")

    # Chat Section
    st.subheader("💬 Chat with us")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask your question:")

    if st.button("Send"):
        if user_input:
            context = get_relevant_info(user_input)
            reply = generate_response(user_input, context)

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))

    # Display Chat
    for sender, message in st.session_state.chat_history:
        st.write(f"**{sender}:** {message}")
