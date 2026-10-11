
import streamlit as st
from textwrap import dedent
import traceback
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.team import Team
from agno.tools.serpapi import SerpApiTools
from agno.models.openrouter import OpenRouter
from agno.models.google import Gemini


# --------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------

OPENROUTER_MODEL = "openai/gpt-oss-20b:free"
GEMINI_MODEL = "gemini-3.5-flash"


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.set_page_config(
    page_title="AI Movie Production Agent",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI Movie Production Agent")
st.write(
    "Transform your movie idea into a complete movie proposal "
    "using AI agents."
)


# --------------------------------------------------
# API KEYS
# --------------------------------------------------

google_api_key = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
)

openrouter_api_key = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
)

serp_api_key = st.sidebar.text_input(
    "SerpAPI Key",
    type="password",
)


# --------------------------------------------------
# MOVIE INPUTS — ORIGINAL TWO-COLUMN LAYOUT
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    movie_genre = st.selectbox(
        "Movie Genre",
        [
            "Action",
            "Comedy",
            "Drama",
            "Science Fiction",
            "Thriller",
            "Horror",
            "Romance",
            "Fantasy",
            "Adventure",
        ],
    )

with col2:
    target_audience = st.selectbox(
        "Target Audience",
        [
            "General Audience",
            "Children",
            "Teenagers",
            "Young Adults",
            "Adults",
            "Family",
        ],
    )

runtime = st.slider(
    "Movie Runtime (minutes)",
    min_value=30,
    max_value=180,
    value=120,
    step=15,
)

movie_idea = st.text_area(
    "Describe Your Movie Idea",
    placeholder="Enter your movie idea here...",
)

additional_requirements = st.text_area(
    "Additional Requirements (Optional)",
    placeholder="Any extra details for your movie...",
)


# --------------------------------------------------
# GENERATE MOVIE PROPOSAL
# --------------------------------------------------

if st.button("Generate Movie Proposal", use_container_width=True):

    if not google_api_key or not openrouter_api_key or not serp_api_key:
        st.warning(
            "Please enter your Google Gemini, OpenRouter, and SerpAPI keys."
        )

    elif not movie_idea.strip():
        st.warning("Please enter your movie idea.")

    else:
        try:

            # ------------------------------------------
            # SCRIPTWRITER — OPENROUTER
            # ------------------------------------------

            script_writer = Agent(
                name="ScriptWriter",
                model=OpenRouter(
                    id=OPENROUTER_MODEL,
                    api_key=openrouter_api_key,
                ),
                description=(
                    "An experienced screenwriter who develops "
                    "creative and engaging movie stories."
                ),
                instructions=[
                    "Develop an original movie story based on the user's idea.",
                    "Create a compelling title and logline.",
                    "Write a detailed synopsis.",
                    "Develop the main characters and their motivations.",
                    "Provide a clear three-act plot structure.",
                    "Follow the requested genre, audience, and runtime.",
                    "Use clear headings and readable Markdown.",
                ],
                markdown=True,
            )

            # ------------------------------------------
            # CASTING DIRECTOR — OPENROUTER + SERPAPI
            # ------------------------------------------

            casting_director = Agent(
                name="CastingDirector",
                model=OpenRouter(
                    id=OPENROUTER_MODEL,
                    api_key=openrouter_api_key,
                ),
                tools=[
                    SerpApiTools(api_key=serp_api_key)
                ],
                description=(
                    "A casting director who researches and recommends "
                    "suitable actors for movie characters."
                ),
                instructions=[
                    "Recommend actors suitable for the movie characters.",
                    "Use SerpAPI search tools to research actors when appropriate.",
                    "Explain why each actor fits the character.",
                    "Distinguish verified information from speculation.",
                    "Do not claim an actor has agreed to participate.",
                    "Provide alternative casting choices where possible.",
                    "Use clear headings and readable Markdown.",
                ],
                markdown=True,
            )

            # ------------------------------------------
            # MOVIE PRODUCER — GEMINI
            # ------------------------------------------

            movie_producer = Team(
                name="MovieProducer",
                model=Gemini(
                    id=GEMINI_MODEL,
                    api_key=google_api_key,
                ),
                members=[
                    script_writer,
                    casting_director,
                ],
                description=(
                    "A movie producer who coordinates the scriptwriting "
                    "and casting agents and prepares the final proposal."
                ),
                instructions=[
                    "Coordinate the ScriptWriter and CastingDirector.",
                    "Use the ScriptWriter to develop the story.",
                    "Use the CastingDirector to research suitable actors.",
                    "Combine the results into one coherent movie proposal.",
                    "Include the title, logline, synopsis, and three-act structure.",
                    "Include the main characters and casting recommendations.",
                    "Include the genre, audience, and runtime.",
                    "Keep the story and casting recommendations consistent.",
                    "Do not invent research findings or confirmed actor commitments.",
                    "Use clear headings and readable Markdown.",
                ],
                markdown=True,
            )

            # ------------------------------------------
            # MOVIE REQUEST
            # ------------------------------------------

            input_text = dedent(f"""
                Develop a complete movie proposal.

                Movie genre: {movie_genre}
                Target audience: {target_audience}
                Runtime: {runtime} minutes

                Original movie idea:
                {movie_idea}

                Additional requirements:
                {additional_requirements or "None provided."}

                The final proposal should include:
                1. Movie title
                2. Logline
                3. Story synopsis
                4. Main characters
                5. Three-act plot structure
                6. Important scenes and plot twists
                7. Casting recommendations and explanations
                8. Visual style and creative direction
                9. Final producer's summary

                Coordinate the available agents and combine their findings.
            """)

            # ------------------------------------------
            # RUN THE TEAM
            # ------------------------------------------

            with st.spinner("Developing your movie proposal..."):
                response = movie_producer.run(
                    input_text,
                    stream=False,
                )

            # ------------------------------------------
            # DISPLAY RESULTS
            # ------------------------------------------

            if response and response.content:
                st.subheader("Your Movie Proposal")
                st.markdown(response.content)

                st.download_button(
                    label="Download Movie Proposal",
                    data=str(response.content),
                    file_name="movie_proposal.md",
                    mime="text/markdown",
                )
            else:
                st.warning("No proposal was returned. Please try again.")

        except Exception as error:
            st.error("Something went wrong while generating the movie proposal.")

            with st.expander("View error details"):
                st.code(str(error))
                st.code(traceback.format_exc())


# --------------------------------------------------
# INITIAL MESSAGE
# --------------------------------------------------

else:
    st.info(
        "Enter your Google Gemini, OpenRouter, and SerpAPI keys "
        "to start developing your movie concept."
    )

  