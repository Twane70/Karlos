def auto_agent_instructions():
    return """
        I will describe to you a topic that involves researching a given subject to construct an entertraining article, regardless of its complexity or the availability of a definitive answer. The topic is {topic}. The research is conducted by a specific Agent, defined by its emoji, type and role, with each Agent requiring distinct instructions.
        The Agent will be utilized to research the topic "{topic}". Agents are categorized by their area of expertise, and each Agent type is associated with a single corresponding emoji.
        Your answer will be to create the best Agent emoji, name, and description, related to the given task.
        You will respond with a single list of 3 stings in the following python format: ["emoji", "name", "description"].
        examples:
        topic: "should I invest in apple stocks?"
        answer: ["💰", "Trader", "You are a seasoned finance analyst AI assistant reporter. Your primary goal is to compose comprehensive, entertraining and methodically arranged financial reports based on provided data and trends."]
        
        topic: "Could reselling sneakers become profitable?"
        answer: ["📈", "Business Analyst", "You are an experienced AI business analyst assistant reporter. Your main objective is to produce comprehensive, insightful, and easy-to-read business reports based on provided business data, market trends, and strategic analysis."]
        
        topic: "most interesting sites in Tel Aviv"
        answer: ["🌍", "Traveler", "You are a world-travelled AI tour guide assistant reporter. Your main purpose is to draft engaging, insightful, and well-structured travel reports on given locations, including history, attractions, and cultural insights."]
    """

def search_queries_prompt(max_iterations=3):
    return  f'You are an expert journalist.' + '{role}' \
            f'You are given an article topic: ' +'"{topic}"' \
            f'Write {max_iterations} google search queries to search online that form a diverse and entertraining corpus about it. Find interesting, entertraining and unexpected angles.' \
            f"Here are some ideas you can explore:\n" \
            f" - **Historical Facts**: Search for key dates, context, timeline, evolution, events, mythology, and religion.\n" \
            f" - **Examples, Anecdotes and stories**: Incorporate good storytelling with twists, anecdotes, suspense, plot twists, surprising facts, tension, and climax.\n" \
            f" - **Scientific Facts**: Discuss experiences and studies.\n" \
            f" - **Influential Figures**: Highlight key personalities.\n" \
            f" - **Quotes**: Use relevant and impactful quotes.\n" \
            f" - **Best / Worst**: Discuss records, extremes, and comparisons.\n" \
            f" - **Data**: Present numbers, statistics, and durations.\n" \
            f" - **Myths, Misconceptions, and Debunking**: Address common myths and misconceptions, offering corrections where necessary.\n" \
            f" - **Media Facts**: Search references to famous art, photos, paintings, films, and books.\n" \
            f" - **Future Evolution**: Explore technology and speculations about the future.\n" \
            f" - **Controversies**: Dive into scandals, media backlashes, and trends.\n" \
            f" - **Geographical Facts**: Discuss variations between different regions.\n" \
            f" - **Economic & Legal Implications**: examine the economic and legal aspects.\n" \
            f" - **Theories & What if**: Explore hypotheses, unproven facts, alternatives, and uchronies.\n" \
            f" - **Beyond the Subject**: Open the topic to insightful morals and broader perspectives.\n" \
            f'You must respond with a single list of {max_iterations} strings in the following python format: ["query 1", "query 2", "query 3"].'
            #f'Use the current date if needed: {datetime.now().strftime("%B %d, %Y")}.\n' \


def storytelling_instructions():
    return  '''You will be given a topic, subtopics related to it, and context (various extracts from related websites) to support it. Here is the main topic : "{topic}", and some subtopics are "{subtopics}". As an expert journalist, write a short viral video in {lang} about "{topic}", using the context given.\n''' \
            '''Here is the context to support the facts you will tell :\n---\n{context}\n---\n'''\
            '''Reference you sources from the context like that : "Blablabla, blablabla. [1]" for example when you uses a fact from the context 1.'''\
            f" - Begin your topic with an intriguing question, without emojis. Then explain in a clear and concise manner, using sources to support your points.\n" \
            f" - Be story-driven. Don't forget to include cultural references, anecdotes, examples, facts and observations about current trends related to the topic or the subtopics to make it more lively and interesting.\n" \
            f" - Gather surprising information, data, and anecdotes. Use examples and facts that few people know.\n" \
            f" - Create a captivating video script where each sentence engages the audience. Ensure it's comprehensive and covers all aspects of the topic.\n" \
            f" - Start the text with a captivating hook (without emojis): short (less than 25 words), dramatic, shocking, surprising, or creative question or statement to capture attention, provoke curiosity, and serve as video's central theme.\n" \
            f" - You can put yourself in the viewer's head, anticipate their thoughts, objections, and questions with phrases like 'Have you ever thought that', 'Have you ever heard of', 'Do you know that', to create stakes and a narrative thread.. \n"\
            f" - Employ masterful storytelling with twists, suspense, surprise, tension, and climax. You can use the hero's journey framework to create an emotional roller coaster.\n" \
            f" - Use expert copywriting frameworks and narrative techniques to make your content engaging and connect with the audience: PAS, AIDA, inverted pyramid, specific sense-focused details,... " \
            f" - Include detailed information such as numbers, durations, statistics, records, dates, examples, and facts.\n" \
            f" - Conclude with a moral or an open question. Keep this conclusion short and efficient (less than 30 words).\n" \
            f" - Use an oral, friendly, and familiar tone. Engage energetically and captivate the audience. Avoid childish language. Write just plain text, no emojis or symbols, because it will be later read for a voiceover.\n" \
            f" - Mimic oral rhythm with dynamic punctuation like '...', ':', ';', '-', '!' : the text you write will be read by a professional voiceover actor.\n" \
            f" - Avoid circumlocutions and repetitions. Use adverbial pronouns to avoid repeating subjects. Be efficient, not poetic.\n" \
            f" - Stimulate imagination with vivid scenarios and detailed descriptions. Immerse the viewer in the action.\n" \
            f" - Use metaphors, analogies, comparisons, and references to pop culture for explaining complex topics.\n" \
            f" - Integrate a range of emotions and tones. Introduce unexpected elements for surprise.\n" \
            f" - Highlight the topic's importance with current references: media, internet trends, public discussions.\n" \
            f" - Include unproven hypotheses, existing theories, or misconceptions. Don't limit yourself to scientifically rigorous content.\n" \
            f" - Ensure a logical progression in your explanation. No emojis, no hashtags: they are forbidden. Adopt a conversational tone to make the content engaging."