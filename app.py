import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="StudyMast Arcade Diagnostic",
    page_icon="🦊",
    layout="centered"
)

# ---------------- DESIGN & STYLING ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(150deg,#dbeafe,#ede9fe,#fce7f3);
    color: #172554;
}
.block-container {
    max-width: 760px;
    padding-top: 2rem;
}
h1,h2,h3,p,label,li {
    color: #172554 !important;
}
[data-testid="stForm"] {
    background: white;
    padding: 22px;
    border-radius: 22px;
    border: 2px solid #bfdbfe;
}
.stButton > button,
.stFormSubmitButton > button {
    background: #4f46e5;
    color: white !important;
    border: 0;
    border-radius: 15px;
    min-height: 48px;
    font-weight: 700;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #3730a3;
    border: 0;
}
[data-testid="stProgressBar"] > div > div {
    background: #8b5cf6;
}
</style>
""", unsafe_allow_html=True)


# ---------------- AUTOMATIC RETRO ARCADE SOUND ENGINE ----------------

def play_auto_audio(sound_type="win"):
    patterns = {
        "intro": [(523, .08), (659, .08), (784, .08), (1047, .16), (880, .08), (1047, .25)],
        "win": [(440, .08), (554, .08), (659, .08), (880, .2)],
        "try": [(220, .12), (185, .18)],
        "finish": [(523, .1), (659, .1), (784, .1), (1047, .15), (1318, .3)]
    }
    notes = patterns.get(sound_type, patterns["win"])
    note_data = ",".join(f"{{f:{freq},d:{duration}}}" for freq, duration in notes)

    components.html(f"""
    <script>
    try {{
      const notes = [{note_data}];
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      let t = ctx.currentTime;
      notes.forEach(n => {{
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "square";
        osc.frequency.value = n.f;
        gain.gain.setValueAtTime(0.0001, t);
        gain.gain.linearRampToValueAtTime(0.08, t + 0.01);
        gain.gain.setValueAtTime(0.08, t + n.d * 0.7);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + n.d);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + n.d);
        t += n.d + 0.02;
      }});
      setTimeout(() => ctx.close(), 3000);
    }} catch(e) {{
      console.log("Autoplay restricted", e);
    }}
    </script>
    """, height=0)


# ---------------- TOPIC IMPORTANCE GUIDE FOR REPORTS ----------------

topic_importance = {
    "Addition": "Builds the foundational base for counting, scaling, and everyday financial calculation.",
    "Subtraction": "Teaches loss, differences, and inverse operations crucial for mental math.",
    "Number sense": "Develops deep intuition about number magnitude, sequencing, and place values.",
    "Shapes": "Enhances spatial awareness, geometry basics, and structural visualization.",
    "Patterns": "Trains the brain for logical forecasting, sequencing, and algebraic thinking.",
    "Place value": "The core skeleton of our decimal system; vital for handling large numbers and decimals.",
    "Multiplication": "Accelerates calculation speed and introduces scaling and area concepts.",
    "Division": "Teaches fair sharing, grouping, and fractions foundation.",
    "Time": "Essential life skill for scheduling, discipline, and understanding intervals.",
    "Fractions": "Critical for proportional reasoning, cooking, measurements, and advanced math.",
    "Perimeter": "Applies geometry to physical boundaries, fencing, and framing real-world objects.",
    "Measurement": "Bridges abstract math with physical units (length, weight, volume).",
    "Word problem": "Translates plain English text into mathematical equations; builds critical thinking.",
    "Estimation": "Trains quick mental approximations and error-checking in real life.",
    "Decimals": "Vital for currency, precise scientific measurements, and data representation.",
    "Area": "Measures surface coverage; essential for construction, design, and land calculation.",
    "Factors": "Unlocks divisibility rules, simplifying fractions, and finding common denominators.",
    "Volume": "Calculates 3D space capacity, packaging, and spatial storage.",
    "Integers": "Introduces negative numbers (temperatures, debts, elevations) essential for algebra.",
    "Algebra": "Unlocks abstract problem-solving, formula manipulation, and logical variables.",
    "Ratio": "Compares quantities proportionally; heavily used in recipes, scaling, and finance.",
    "Geometry": "Develops theorem proofs, spatial reasoning, and structural integrity principles.",
    "Percentages": "Crucial for financial literacy, taxes, discounts, and statistical data analysis.",
    "Arithmetic": "Core computation skill governing commercial math and interest calculations.",
    "Rational numbers": "Expands number systems to fractions and decimals with negative values.",
    "Exponents": "Handles extremely large or tiny numbers efficiently (scientific notation).",
    "Squares": "Foundational for quadratic equations and geometric Pythagorean relationships.",
    "Cubes": "Extends dimensional scaling into 3D volume calculations.",
    "Probability": "Teaches risk assessment, odds, statistics, and logical forecasting."
}


# ---------------- 10-QUESTION CLEAN DIAGNOSTIC BANK ----------------

quiz_bank = {
    "Class 1": [
        ("Addition", "8 + 7 = ?", ["13", "14", "15", "16"], "15"),
        ("Subtraction", "16 - 9 = ?", ["5", "6", "7", "8"], "7"),
        ("Number sense", "What comes after 39?", ["38", "40", "41", "49"], "40"),
        ("Shapes", "How many sides has a triangle?", ["2", "3", "4", "5"], "3"),
        ("Patterns", "2, 4, 6, __", ["7", "8", "9", "10"], "8"),
        ("Shapes", "What shape has 4 equal sides?", ["Triangle", "Square", "Circle", "Rectangle"], "Square"),
        ("Addition", "10 + 5 - 3 = ?", ["10", "11", "12", "13"], "12"),
        ("Comparison", "Which number is largest: 12, 19, 15?", ["12", "19", "15", "All equal"], "19"),
        ("Word problem", "If you have 3 apples and get 2 more, how many?", ["4", "5", "6", "7"], "5"),
        ("Time", "What day comes after Monday?", ["Sunday", "Tuesday", "Wednesday", "Friday"], "Tuesday")
    ],
    "Class 2": [
        ("Addition", "47 + 28 = ?", ["65", "75", "85", "74"], "75"),
        ("Subtraction", "83 - 46 = ?", ["37", "47", "43", "27"], "37"),
        ("Place value", "Value of 6 in 364?", ["6", "60", "600", "64"], "60"),
        ("Multiplication", "5 × 7 = ?", ["30", "35", "40", "25"], "35"),
        ("Time", "One hour after 3:30 is?", ["4:00", "4:30", "5:30", "2:30"], "4:30"),
        ("Multiplication", "Double of 15 is?", ["25", "30", "35", "40"], "30"),
        ("Time", "How many days in 2 weeks?", ["7", "10", "14", "21"], "14"),
        ("Subtraction", "100 - 45 = ?", ["45", "55", "65", "50"], "55"),
        ("Number sense", "Which is an even number?", ["13", "17", "22", "9"], "22"),
        ("Time", "A clock shows 12:00. Where is the minute hand pointing?", ["6", "9", "12", "3"], "12")
    ],
    "Class 3": [
        ("Multiplication", "24 × 3 = ?", ["62", "72", "82", "64"], "72"),
        ("Division", "56 ÷ 7 = ?", ["6", "7", "8", "9"], "8"),
        ("Fractions", "Half of 38 is?", ["18", "19", "20", "16"], "19"),
        ("Place value", "Value of 5 in 3,572?", ["5", "50", "500", "5000"], "500"),
        ("Word problem", "6 boxes have 8 pencils each. Total?", ["42", "46", "48", "56"], "48"),
        ("Division", "72 ÷ 8 = ?", ["7", "8", "9", "6"], "9"),
        ("Perimeter", "Perimeter of square with side 5 cm?", ["15 cm", "20 cm", "25 cm", "10 cm"], "20 cm"),
        ("Measurement", "3 meters = ? centimeters", ["30 cm", "300 cm", "3000 cm", "3 cm"], "300 cm"),
        ("Fractions", "What is 1/4 of 40?", ["5", "10", "15", "20"], "10"),
        ("Time", "If today is Wednesday, what day was yesterday?", ["Monday", "Tuesday", "Thursday", "Friday"], "Tuesday")
    ],
    "Class 4": [
        ("Multiplication", "126 × 4 = ?", ["484", "504", "514", "404"], "504"),
        ("Division", "936 ÷ 9 = ?", ["104", "114", "94", "106"], "104"),
        ("Fractions", "Which fraction equals 1/2?", ["2/3", "3/6", "2/5", "4/6"], "3/6"),
        ("Perimeter", "Square side = 7 cm. Perimeter?", ["14 cm", "21 cm", "28 cm", "49 cm"], "28 cm"),
        ("Word problem", "One book costs ₹135. Cost of 4?", ["₹440", "₹500", "₹540", "₹560"], "₹540"),
        ("Estimation", "Round 487 to the nearest 100", ["400", "500", "480", "490"], "500"),
        ("Multiplication", "7 × 9 = ?", ["56", "63", "72", "64"], "63"),
        ("Measurement", "Convert 3 kg to grams", ["30 g", "300 g", "3000 g", "30000 g"], "3000 g"),
        ("Percentages", "What is 50% of 180?", ["80", "90", "100", "60"], "90"),
        ("Area", "Area of a rectangle with length 6 and width 4?", ["20", "24", "10", "12"], "24")
    ],
    "Class 5": [
        ("Multiplication", "248 × 16 = ?", ["3,868", "3,968", "3,986", "3,768"], "3,968"),
        ("Fractions", "3/4 of 80 = ?", ["40", "50", "60", "70"], "60"),
        ("Decimals", "4.75 + 2.8 = ?", ["6.55", "7.55", "7.45", "6.75"], "7.55"),
        ("Area", "Rectangle: length 12 cm, width 7 cm. Area?", ["38 cm²", "72 cm²", "84 cm²", "96 cm²"], "84 cm²"),
        ("Word problem", "125 notebooks daily for 8 days. Total?", ["900", "1,000", "1,025", "875"], "1,000"),
        ("Factors", "Find LCM of 4 and 6", ["10", "12", "24", "18"], "12"),
        ("Fractions", "Simplify 15/25", ["3/5", "1/2", "2/5", "3/4"], "3/5"),
        ("Decimals", "10.5 - 3.25 = ?", ["7.25", "7.5", "6.25", "8.25"], "7.25"),
        ("Volume", "Volume of a cube with side 3 cm?", ["9 cm³", "18 cm³", "27 cm³", "36 cm³"], "27 cm³"),
        ("Number sense", "What is the next prime number after 7?", ["8", "9", "10", "11"], "11")
    ],
    "Class 6": [
        ("Integers", "-8 + 15 = ?", ["-23", "-7", "7", "23"], "7"),
        ("Fractions", "2/3 + 1/6 = ?", ["3/9", "1/2", "5/6", "1"], "5/6"),
        ("Algebra", "x + 17 = 42. Find x.", ["25", "35", "59", "24"], "25"),
        ("Ratio", "Simplify 18:24.", ["2:3", "3:4", "4:5", "6:8"], "3:4"),
        ("Geometry", "Triangle angles 50° and 60°. Third angle?", ["60°", "70°", "80°", "90°"], "70°"),
        ("Factors", "Find HCF of 24 and 36", ["6", "12", "8", "4"], "12"),
        ("Integers", "Absolute value of |-25| is", ["-25", "0", "25", "5"], "25"),
        ("Algebra", "If 3x = 36, then x = ?", ["10", "11", "12", "13"], "12"),
        ("Geometry", "Complement of a 35° angle?", ["55°", "145°", "65°", "90°"], "55°"),
        ("Statistics", "Average of 10, 20, 30, 40, 50?", ["25", "30", "35", "40"], "30")
    ],
    "Class 7": [
        ("Integers", "(-12) × (-5) = ?", ["-60", "-17", "17", "60"], "60"),
        ("Fractions", "3/4 ÷ 1/2 = ?", ["3/8", "2/3", "3/2", "1/4"], "3/2"),
        ("Algebra", "3x - 7 = 20. Find x.", ["7", "8", "9", "11"], "9"),
        ("Percentages", "15% of 240 = ?", ["24", "30", "36", "40"], "36"),
        ("Angles", "Supplementary angles are in ratio 2:3. Smaller angle?", ["36°", "72°", "90°", "108°"], "72°"),
        ("Algebra", "Solve: 2(x + 3) = 14", ["x = 3", "x = 4", "x = 5", "x = 6"], "x = 4"),
        ("Arithmetic", "Find simple interest on ₹1000 at 10% per annum for 1 year", ["₹100", "₹150", "₹200", "₹50"], "₹100"),
        ("Squares", "Square root of 529", ["21", "23", "27", "29"], "23"),
        ("Geometry", "Exterior angle of a triangle equals sum of two ?", ["Adjacent angles", "Interior opposite angles", "Hypotenuse", "Base angles"], "Interior opposite angles"),
        ("Percentages", "Express 7/8 as a percentage", ["75%", "82.5%", "87.5%", "90%"], "87.5%")
    ],
    "Class 8": [
        ("Rational numbers", "(-3/5) × (10/9) = ?", ["-2/3", "2/3", "-3/2", "1/3"], "-2/3"),
        ("Linear equations", "5x + 3 = 28. Find x.", ["4", "5", "6", "7"], "5"),
        ("Percentages", "₹800 item with 15% discount. Sale price?", ["₹680", "₹700", "₹720", "₹760"], "₹680"),
        ("Exponents", "2³ × 2⁴ = ?", ["2¹२", "2⁷", "4⁷", "2¹"], "2⁷"),
        ("Squares", "√2025 = ?", ["35", "40", "45", "55"], "45"),
        ("Cubes", "Cube root of 1728", ["11", "12", "13", "14"], "12"),
        ("Word problem", "If 8 workers take 6 days, how many days for 4 workers?", ["12 days", "8 days", "10 days", "15 days"], "12 days"),
        ("Algebra", "Factorise: x² - 9", ["(x-3)(x-3)", "(x+3)(x+3)", "(x-3)(x+3)", "Cannot factorise"], "(x-3)(x+3)"),
        ("Probability", "Probability of getting an even number on a standard die?", ["1/2", "1/3", "1/6", "1/4"], "1/2"),
        ("Compound interest", "Compound interest on ₹10,000 at 10% for 2 years?", ["₹2,000", "₹2,100", "₹2,200", "₹2,500"], "₹2,100")
    ]
}


# ---------------- SESSION STATE ----------------

if "started" not in st.session_state:
    st.session_state.started = False
if "grade" not in st.session_state:
    st.session_state.grade = "Class 5"
if "index" not in st.session_state:
    st.session_state.index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "answered" not in st.session_state:
    st.session_state.answered = False
if "current_questions" not in st.session_state:
    st.session_state.current_questions = []

st.markdown("<h1 style='text-align:center'>🎮 STUDYMAST ARCADE</h1>", unsafe_allow_html=True)

# ---------------- WELCOME SCREEN ----------------

if not st.session_state.started:
    play_auto_audio("intro")
    
    st.markdown("""
    <div style="
      text-align:center;background:rgba(255,255,255,.9);
      border:3px solid #c4b5fd;border-radius:28px;
      padding:28px 16px;margin:12px 0">
      <div style="font-size:78px">🦊🎮</div>
      <div style="font-size:26px;font-weight:900;color:#4338ca">
        Welcome to StudyMast Arcade!
      </div>
      <div style="font-size:17px;color:#334155;margin:12px">
        Interactive Retro Maths Assessment & Worksheets 🧠✨
      </div>
      <div style="font-size:14px;color:#475569">
        Level up through StudyMast's <b>Learn → Practise → Master</b> framework!
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.grade = st.selectbox(
        "🎒 Choose your class",
        list(quiz_bank.keys()),
        index=4
    )

    if st.button("🚀 START RETRO ADVENTURE", use_container_width=True):
        st.session_state.started = True
        st.session_state.index = 0
        st.session_state.answers = {}
        st.session_state.answered = False
        
        # Shuffle questions for fresh replay
        shuffled_qs = list(quiz_bank[st.session_state.grade])
        random.shuffle(shuffled_qs)
        st.session_state.current_questions = shuffled_qs
        st.rerun()

    st.caption("StudyMast · Learn a little. Grow a lot.")
    st.stop()


# ---------------- GAMEPLAY ----------------

grade = st.session_state.grade
questions = st.session_state.current_questions
index = st.session_state.index

if index < len(questions):
    topic, question, options, correct = questions[index]
    score = sum(a["correct"] for a in st.session_state.answers.values())

    st.markdown(
        f"### 🪙 {score * 100} POINTS"
        f" <span style='font-size:15px'> · {grade}</span>",
        unsafe_allow_html=True
    )
    st.progress((index + 1) / len(questions))
    
    stage_name = "Learn & Practise" if index < 5 else "Master"
    st.caption(f"LEVEL {index + 1} / {len(questions)} · TOPIC: {topic.upper()} · STAGE: {stage_name}")

    st.markdown(f"""
    <div style="
      background:white;border:2px solid #c4b5fd;
      padding:24px;border-radius:22px;margin:12px 0">
      <div style="font-size:18px;color:#7c3aed;font-weight:bold;margin-bottom:8px">
        🦊 MATH FOX QUEST — LEVEL {index + 1}
      </div>
      <div style="font-size:24px;color:#172554;font-weight:800;margin-top:10px">
        {question}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered:
        with st.form(key=f"answer_{grade}_{index}"):
            choice = st.radio("Pick your answer:", options, index=None)
            submit = st.form_submit_button("⚡ LOCK IN ANSWER", use_container_width=True)

        if submit:
            if choice is None:
                st.warning("Choose an answer first, champion! 😊")
            else:
                is_correct = choice == correct
                st.session_state.answers[index] = {
                    "topic": topic,
                    "correct": is_correct,
                    "chosen": choice,
                    "answer": correct
                }
                st.session_state.answered = True
                st.rerun()

    else:
        result = st.session_state.answers[index]

        if result["correct"]:
            play_auto_audio("win")
            st.success("🎉 LEVEL CLEARED! +100 POINTS!")
        else:
            play_auto_audio("try")
            st.warning(f"💡 Not quite! The correct answer is **{correct}**.")

        if index + 1 < len(questions):
            if st.button("NEXT LEVEL ➜", use_container_width=True):
                st.session_state.index += 1
                st.session_state.answered = False
                st.rerun()
        else:
            if st.button("🏆 VIEW MY REPORT CARD", use_container_width=True):
                st.session_state.index += 1
                st.rerun()

    st.stop()


# ---------------- RESULTS REPORT & TOPIC IMPORTANCE BREAKDOWN ----------------

answers = st.session_state.answers
score = sum(a["correct"] for a in answers.values())
total = len(questions)
percentage = round(score / total * 100)

play_auto_audio("finish")
st.balloons()

st.markdown("""
<div style="text-align:center;background:white;border-radius:24px;
padding:22px;border:3px solid #a78bfa">
<div style="font-size:56px">🏆</div>
<div style="font-size:30px;font-weight:900;color:#4338ca">
MISSION ACCOMPLISHED!
</div>
<div style="font-size:17px;color:#334155">
Great job completing your diagnostic arcade session.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.metric("⭐ Final Score", f"{score} / {total}", f"{percentage}%")

st.markdown("## 🗺️ Visited Topics & Why They Matter")
st.write("Here is a breakdown of the specific math topics attempted in this session and why mastering them is crucial for a child at this grade level:")

topic_results = {}
for item in answers.values():
    topic_results.setdefault(item["topic"], []).append(item["correct"])

for topic, results in topic_results.items():
    correct_count = sum(results)
    status_emoji = "✅" if (correct_count / len(results)) >= 0.5 else "📘"
    st.markdown(f"### {status_emoji} {topic} ({correct_count}/{len(results)} correct)")
    st.progress(correct_count / len(results))
    
    importance_text = topic_importance.get(topic, "Builds critical mathematical reasoning and problem-solving skills.")
    st.info(f"**Why practice this?** {importance_text}")

# ---------------- STUDYMAST BRANDING & VALUE PROPOSITION ----------------
st.markdown("---")
st.markdown("## 🌟 Why StudyMast Works")
st.write(
    "StudyMast isn't simply a worksheet website. Our methodology is designed to build true independence and conceptual clarity:"
)

st.markdown("""
- **Small-Group Attention:** Just **five students per teacher**, ensuring zero hiding in the back and 100% active engagement.
- **Structured Learning:** Guided progression through **Learn → Practise → Master**.
- **Interactive Worksheets:** Designed to make mathematics engaging, colorful, and fun rather than intimidating.
- **Visible Progress:** Clear insights into what your child understands and where they need targeted support.
""")

# WhatsApp Booking CTA Button for sameer's Uncle
whatsapp_number = "919876543210" # Replace with your uncle's actual WhatsApp number
msg = f"Hi StudyMast! My child just finished the {grade} Assessment with a score of {score}/{total}. I'd love to book a free demo class."
whatsapp_url = f"https://wa.me/{whatsapp_number}?text={msg.replace(' ', '%20')}"

st.link_button("📱 Book a Free Demo Class on WhatsApp", whatsapp_url)

st.markdown("")
if st.button("🔄 PLAY AGAIN ", use_container_width=True):
    st.session_state.started = False
    st.session_state.index = 0
    st.session_state.answers = {}
    st.session_state.answered = False
    st.rerun()

st.caption("StudyMast · Learn a little. Grow a lot.")