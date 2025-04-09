from libs.config import create_session
from libs.db_models import Source, NewsletterConfig, LLMConfig

system_prompt = """You do technical monitoring on Discord servers. Your role is to produce a newsletter on the latest messages received.

Write only the chapters of the newsletter, with a title and content for each chapter. Each chapter should not exceed 50 words.
Keep it short and concise. Include in your newsletter only information that is technically advanced for a very experienced user.
Their are at most 5 chapters in the newsletter.

You'll focus on information that comes up often, and on those that get the most upvotes or reactions.

Don't include the source of the information in the newsletter. The source will be added later.

For each paragraph, if available, give the links from the source that are relevant to the content of the paragraph.
Do not include any other information or context about the links.

Don't give the newsletter an intro or outro.

You're talking to a very experienced audience.

Include only serious and relevant information. Do not include any jokes, light-hearted content or other non-technical information.

The output will follow this structure:

## {Paragraph title}

{content}

Links:

- https://www.example.com
- https://www.example.com

## {Paragraph title}

{content}

To generate the newsletter, you will get the raw data as :

# {Source name}

{content}

---

# {Source name}
    
{content}
"""

# Init LLM Configs
llm_configs = [
    LLMConfig(
        name="OpenAI 4o (Tech)",
        base_url="https://api.openai.com/v1",
        api_key_name="OPENAI_API_KEY",
        model_name="gpt-4o",
        system_prompt=system_prompt,
        params={
            "temperature": 1,
            "top_p": 1,
        },
    ),
    LLMConfig(
        name="Gemini 2.5 Pro (Tech)",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key_name="GEMINI_API_KEY",
        model_name="gemini-2.5-pro-exp-03-25",
        system_prompt=system_prompt,
        params={
            "temperature": 1,
            "top_p": 1,
        },
    )
]

# Init sources
sources_data = [
    # AI Music
    Source(
        name="Discord server Harmonai, channel #general",
        type="discord",
        config={"channel": "1001555639228702822"},
    ),
    Source(
        name="Discord server Harmonai, channel #stable-audio-open",
        type="discord",
        config={"channel": "1154633787838308372"},
    ),

    # LLMs
    Source(
        name="Discord server Nous Research, channel #general",
        type="discord",
        config={"channel": "1149866623109439599"},
    ),
    Source(
        name="Discord server Nous Research, channel #ask-about-llm",
        type="discord",
        config={"channel": "1154120232051408927"},
    ),
    Source(
        name="Discord server LlamaIndex, channel #general",
        type="discord",
        config={"channel": "1059201661417037995"},
    ),
    Source(
        name="Discord server Learn Prompting, channel #news",
        type="discord",
        config={"channel": "1177304954059374744"},
    ),

    # Reddit LLM
    Source(
        name="Reddit r/LocalLLaMA",
        type="reddit",
        config={
            "subreddit": "LocalLLaMA",
        },
    ),
]

# Init newsletter configs
newsletter_configs = [
    {
        "name": "LLM News",
        "slug": "llm-news",
        "sources": [
            "Discord server Nous Research, channel #general",
            "Discord server Nous Research, channel #ask-about-llm",
            "Discord server LlamaIndex, channel #general",
            "Discord server Learn Prompting, channel #news",
            "Reddit r/LocalLLaMA",
        ],
        "llm_config": "Gemini 2.5 Pro (Tech)",
    },
    # {
    #     "name": "AI Music",
    #     "sources": [
    #         "Discord server Harmonai, channel #general",
    #         "Discord server Harmonai, channel #stable-audio-open",
    #     ],
    #     "llm_config": "Gemini 2.5 Pro (Tech)",
    # },
]



with create_session() as session:
    # Ensure LLM configs exist
    existing_llms = {llm.name for llm in session.query(LLMConfig).all()}
    llms_to_add = []
    for llm_data in llm_configs:
        if llm_data.name not in existing_llms:
            llms_to_add.append(llm_data)
            existing_llms.add(llm_data.name)
    if llms_to_add:
        session.add_all(llms_to_add)
        session.commit() # Commit LLM configs first to get IDs if needed, or just flush
        print(f"{len(llms_to_add)} LLM configs added: {[llm.name for llm in llms_to_add]}")
    else:
        print("No new LLM configs to add.")

    # Ensure sources exist
    existing_sources = {s.name for s in session.query(Source).all()}
    sources_to_add = []
    for source_data in sources_data:
        if source_data.name not in existing_sources:
            sources_to_add.append(source_data)
            existing_sources.add(source_data.name)

    if sources_to_add:
        session.add_all(sources_to_add)
        session.commit() # Commit sources first to get IDs if needed, or just flush
        print(f"{len(sources_to_add)} Sources added: {[s.name for s in sources_to_add]}")
    else:
        print("No new sources to add.")

    # Add newsletter configs
    existing_newsletters = {nc.name for nc in session.query(NewsletterConfig).all()}
    newsletters_to_add = []
    for newsletter_data in newsletter_configs:
        if newsletter_data["name"] not in existing_newsletters:
            # Fetch the sources from the DB
            sources = session.query(Source).filter(Source.name.in_(newsletter_data["sources"])).all()
            # Get the corresponding LLM config from the DB
            llm_config = session.query(LLMConfig).filter_by(name=newsletter_data["llm_config"]).first()

            # Create the NewsletterConfig instance
            new_newsletter_config = NewsletterConfig(
                name=newsletter_data["name"],
                sources=sources,
                llm_config_id=llm_config.id,
                slug=newsletter_data["slug"],
            )
            newsletters_to_add.append(new_newsletter_config)
            existing_newsletters.add(newsletter_data["name"])

    if newsletters_to_add:
        session.add_all(newsletters_to_add)
        session.commit()
        print(f"{len(newsletters_to_add)} Newsletter configs added: {[nc.name for nc in newsletters_to_add]}")

    else:
        print("No new newsletter configs to add.")