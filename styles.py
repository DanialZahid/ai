"""Inline icon constants (Heroicons outline set, embedded as top-level
constants so their quote characters never collide with surrounding HTML
strings) and the app's CSS theme."""

ICON_CAMERA = """<svg style="width:22px;height:22px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z"/> <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z"/> </svg>"""

ICON_USER_PLUS = """<svg style="width:22px;height:22px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z"/> </svg>"""

ICON_CPU_CHIP = """<svg style="width:22px;height:22px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75a2.25 2.25 0 0 0-2.25-2.25H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Zm.75-12h9v9h-9v-9Z"/> </svg>"""

ICON_VIEWFINDER = """<svg style="width:22px;height:22px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/> </svg>"""

ICON_TABLE_CELLS = """<svg style="width:22px;height:22px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 0 1-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0 1 12 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 1.5v-1.5m0 0c0-.621.504-1.125 1.125-1.125m0 0h7.5"/> </svg>"""

ICON_LIGHT_BULB = """<svg style="width:18px;height:18px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18"/> </svg>"""

ICON_STATUS = """<svg style="width:18px;height:18px;vertical-align:-4px;margin-right:8px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon"> <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"/> </svg>"""


CSS = """
<style>
/* Main page */
.stApp {
    background-color: #f5f8fa;
}

/* Sidebar - Navy Blue Ombre */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #234f78 0%,
        #123b61 55%,
        #082b4d 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar heading */
.sidebar-title {
    text-align: left;
    font-size: 24px;
    font-weight: 800;
    padding: 18px 5px 5px 14px;
}

.sidebar-subtitle {
    text-align: left;
    font-size: 12px;
    opacity: 0.85;
    margin-bottom: 25px;
    padding-left: 14px;
}

/* Main title */
.page-title {
    color: #123b61;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 5px;
}

.page-subtitle {
    color: #777777;
    font-size: 15px;
    margin-bottom: 25px;
}

/* White content card */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(18, 59, 97, 0.12);
    margin-bottom: 20px;
}

/* Section heading */
.section-title {
    color: #123b61;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Buttons */
.stButton > button {
    background-color: #123b61;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 25px;
}

.stButton > button:hover {
    background-color: #082b4d;
    color: white;
}

section[data-testid="stSidebar"] > div:first-child {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.sidebar-bottom-anchor {
    margin-top: auto;
}

section[data-testid="stSidebar"] .stButton > button {
    border-radius: 8px;
    text-align: left;
    justify-content: flex-start;
    padding: 10px 14px;
    margin-bottom: 4px;
    font-weight: 500;
    background-color: transparent;
}

/* The icon+label inside a button live in their own inner flex wrapper,
   which centers content independently of the outer button — this rule
   targets that inner wrapper directly so left-alignment actually applies. */
section[data-testid="stSidebar"] .stButton > button > div {
    justify-content: flex-start !important;
    width: 100%;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255, 255, 255, 0.12);
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: rgba(255, 255, 255, 0.18);
    color: white;
}

/* Text input */
div[data-baseweb="input"] {
    border-radius: 10px;
}

/* Camera */
div[data-testid="stCameraInput"] {
    border-radius: 15px;
    overflow: hidden;
}

/* Success */
.success-card {
    background-color: #edf8f0;
    border-left: 5px solid #28a745;
    padding: 15px;
    border-radius: 10px;
    color: #236b38;
}

/* Info - Teal */
.info-card {
    background-color: #e0f4f3;
    border-left: 5px solid #159a9c;
    padding: 15px;
    border-radius: 10px;
    color: #087f81;
}

/* Footer */
.footer {
    text-align: center;
    color: #999999;
    font-size: 12px;
    padding: 30px 0 10px 0;
}
</style>
"""
