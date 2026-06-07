import os
import itertools
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# .env se comma separated keys read karega
API_KEYS = [
    key.strip()
    for key in os.getenv("GEMINI_API_KEYS", "").split(",")
    if key.strip()
]

if not API_KEYS:
    raise ValueError(
        "No Gemini API keys found. Add GEMINI_API_KEYS in .env"
    )

# Round Robin Cycle
KEY_CYCLE = itertools.cycle(API_KEYS)


def ask(prompt):

    last_error = None

    # Ek request me sabhi keys try kar sakta hai agar failure aaye
    for _ in range(len(API_KEYS)):

        api_key = next(KEY_CYCLE)

        try:

            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            response = model.generate_content(
                prompt
            )

            print(
                f"Success using key ending with ...{api_key[-6:]}"
            )

            return response.text

        except Exception as e:

            last_error = e

            print(
                f"Failed key ...{api_key[-6:]} | Error: {e}"
            )

            continue

    return f"All API keys failed. Last error: {last_error}"


def run_chain(prospect, competitor, mail):

    prompt1 = f"""
the {prospect} our prospect and they have a competitor {competitor}

research about both on web

Uploaded mail content:

{mail}

Compare:

- company overview
- services
- strengths
- weaknesses
- opportunities
- key differences
"""

    out1 = ask(prompt1)

    prompt2 = f"""
give me content for 10 page ppt to send to {prospect}

which says how bnxt.ai helped {competitor}

in ai integration and automation

Keep every slide separate

Slide1:

Slide2:

Slide3:

Slide4:

Slide5:

Slide6:

Slide7:

Slide8:

Slide9:

Slide10:
"""

    out2 = ask(prompt2)

    prompt3 = f"""
this is too generic

give detailed analysis

not surface level

keep it number oriented

Use this content:

{out2}
"""

    out3 = ask(prompt3)

    prompt4 = f"""
draft me a humanized msg without emdash

to send with this ppt

to come on meet

Prospect:

{prospect}

Context:

{out1}
"""

    out4 = ask(prompt4)

    return {
        "step1": out1,
        "step2": out2,
        "step3": out3,
        "step4": out4
    }